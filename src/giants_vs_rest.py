"""Extension: inside each industry, do the giants rent and the small firms sell?

Bulow's prediction is about firms, not industries. A firm with market power over a durable good has a
reason to rent it out; a small price-taking rival does not. Comparing industries mixes that with
everything else that differs between, say, tractors and soft drinks. This script holds the industry
fixed. For each manufacturing minor industry it splits the IRS Corporation Source Book (the last
editions with asset-size detail, tax years 2007, 2012 and 2013) into the largest corporations, those
with $2.5 billion or more in assets, and everyone else, and compares their rent shares:

    gap_j = rents / (business receipts + rents) for giants  -  the same ratio for the rest

Bulow predicts a positive gap for durable final goods and none for nondurables. A second cut at
$500 million is a check.

Run from the repository root:
    python src/giants_vs_rest.py
Inputs: data/raw/irs_sourcebook/*.zip (committed). Outputs: results/giants_*.csv and one figure.
"""

import sys
import zipfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from bulow_leasing import GROUP_LABEL  # noqa: E402

RAW = ROOT / "data" / "raw" / "irs_sourcebook"
OUT = ROOT / "results"

FILES = {2007: ("07sbflatfile.zip", "07sb1.csv"), 2012: ("12sbfltfile.zip", "2012sb1.csv"),
         2013: ("13sbfltfile.zip", "2013sb1.csv")}
PRIMARY_YEAR = 2013  # the last Source Book with asset-size detail
GIANT_AC = 13        # asset class 13 = $2,500,000 thousand or more (Source Book documentation)
LARGE_AC = 12        # check: asset classes 12-13 = $500 million or more
# AC 1 is the industry total and AC 2 the returns reporting zero assets; both are left out of "the rest".
REST_MIN_AC = 3

# Source Book industry code -> (label, Bulow group), same groups as src/bulow_leasing.py
SB_INDUSTRIES = {
    311115: ("Animal food and grain milling", "nondur"), 311300: ("Sugar and confectionery", "nondur"),
    311400: ("Fruit and vegetable preserving", "nondur"), 311500: ("Dairy products", "nondur"),
    311615: ("Meat and seafood", "nondur"), 311800: ("Bakeries and tortillas", "nondur"),
    311900: ("Other food", "nondur"), 312110: ("Soft drinks and ice", "nondur"), 312120: ("Breweries", "nondur"),
    312135: ("Wineries and distilleries", "nondur"), 312200: ("Tobacco", "nondur"),
    313000: ("Textile mills", "nondur"), 314000: ("Textile products", "nondur"),
    315100: ("Apparel knitting", "nondur"), 315215: ("Cut and sew apparel", "nondur"),
    315990: ("Apparel accessories", "nondur"), 316: ("Leather", "nondur"), 321: ("Wood products", "parts"),
    322100: ("Pulp and paper mills", "nondur"), 322200: ("Converted paper", "nondur"),
    323100: ("Printing", "nondur"), 324110: ("Petroleum refineries", "nondur"),
    324125: ("Asphalt and other petroleum", "nondur"), 325100: ("Basic chemicals", "nondur"),
    325200: ("Resins and synthetic fibers", "nondur"), 325410: ("Pharmaceuticals", "nondur"),
    325500: ("Paint and adhesives", "nondur"), 325600: ("Soap and toiletries", "nondur"),
    325905: ("Other chemicals", "nondur"), 326100: ("Plastics products", "nondur"),
    326200: ("Rubber products", "nondur"), 327105: ("Clay and other mineral products", "parts"),
    327210: ("Glass", "parts"), 327305: ("Cement and concrete", "parts"), 331115: ("Iron and steel", "parts"),
    331315: ("Nonferrous metals", "parts"), 331500: ("Foundries", "parts"),
    332110: ("Forging and stamping", "parts"), 332215: ("Hardware, springs, machine shops", "parts"),
    332300: ("Structural metals", "parts"), 332400: ("Boilers and tanks", "parts"),
    332810: ("Metal coating", "parts"), 332900: ("Other fabricated metal", "parts"),
    333100: ("Farm, construction and mining machinery", "final"), 333200: ("Industrial machinery", "final"),
    333310: ("Commercial and service machinery", "final"), 333410: ("Heating and air conditioning", "final"),
    333510: ("Metalworking machinery", "final"), 333610: ("Engines and turbines", "final"),
    333900: ("Other general machinery", "final"), 334110: ("Computers and peripherals", "final"),
    334200: ("Communications equipment", "final"), 334315: ("Audio and video equipment", "final"),
    334410: ("Semiconductors and components", "parts"), 334500: ("Instruments and electromedical", "final"),
    335105: ("Lighting and household appliances", "final"), 335310: ("Electrical equipment", "final"),
    335900: ("Other electrical equipment", "final"), 336105: ("Motor vehicles and parts", "final"),
    336410: ("Aerospace", "final"), 336610: ("Ships and boats", "final"),
    336995: ("Railcars and other transport equipment", "final"), 337: ("Furniture", "final"),
    339110: ("Medical equipment and supplies", "final"), 339900: ("Other miscellaneous manufacturing", "final"),
}


def load_year(year):
    zname, member = FILES[year]
    with zipfile.ZipFile(RAW / zname) as z:
        x = pd.read_csv(z.open(member), low_memory=False)
    x.columns = [c.strip().upper() for c in x.columns]
    x = x[(x.TAB_NUM == 1) & x.INDY_CD.isin(list(SB_INDUSTRIES))].copy()
    for c in ["WT_CT", "TOT_ASSTS", "GRS_RCPTS", "COMP_GRS_RNTS"]:
        x[c] = pd.to_numeric(x[c], errors="coerce")
    print(f"Source Book TY{year}: {x.INDY_CD.nunique()} manufacturing industries, {len(x)} industry-by-size cells")
    return x


def split(x, year, top_ac):
    """Rent share of corporations in asset classes >= top_ac vs. classes REST_MIN_AC..top_ac-1."""
    rows, dropped = [], {}
    for code, g in x.groupby("INDY_CD"):
        label, group = SB_INDUSTRIES[code]
        top = g[g.AC >= top_ac]
        rest = g[(g.AC >= REST_MIN_AC) & (g.AC < top_ac)]
        # The IRS folds a size class into the one below it (flag 2) or deletes it (flag 3) to protect
        # identities. Either way the giants cannot be separated, so the industry-year is dropped.
        flags = pd.to_numeric(g[g.AC >= top_ac].COMP_GRS_RNTS_IND, errors="coerce").fillna(0)
        if top.empty or top.WT_CT.fillna(0).sum() == 0 or (flags >= 2).any() or top.COMP_GRS_RNTS.isna().any():
            dropped[label] = "largest class combined or withheld"
            continue
        if rest.GRS_RCPTS.sum() <= 0:
            dropped[label] = "no smaller corporations"
            continue
        sh = lambda d: 100 * d.COMP_GRS_RNTS.sum() / (d.GRS_RCPTS.sum() + d.COMP_GRS_RNTS.sum())
        rows.append({"year": year, "industry": label, "group": group, "sb_code": code,
                     "giants": top.WT_CT.sum(), "rest": rest.WT_CT.sum(),
                     "giants_assets_bn": top.TOT_ASSTS.sum() / 1e6, "rest_assets_bn": rest.TOT_ASSTS.sum() / 1e6,
                     "giants_receipts_bn": top.GRS_RCPTS.sum() / 1e6, "rest_receipts_bn": rest.GRS_RCPTS.sum() / 1e6,
                     "giants_rents_mn": top.COMP_GRS_RNTS.sum() / 1e3, "rest_rents_mn": rest.COMP_GRS_RNTS.sum() / 1e3,
                     "giants_share": sh(top), "rest_share": sh(rest)})
    out = pd.DataFrame(rows)
    out["gap"] = out.giants_share - out.rest_share
    out["giants_receipt_share"] = 100 * out.giants_receipts_bn / (out.giants_receipts_bn + out.rest_receipts_bn)
    print(f"  cut at asset class {top_ac}: kept {len(out)} industries, dropped {len(dropped)} "
          f"({', '.join(sorted(dropped))})")
    return out


def summarize(d, cut_label):
    rows = []
    for year, y in d.groupby("year"):
        for g in ["final", "parts", "nondur"]:
            s = y[y.group == g]
            pooled = lambda r, rec: 100 * s[r].sum() / (s[rec].sum() * 1e3 + s[r].sum())
            rows.append({"cut": cut_label, "year": year, "group": GROUP_LABEL[g], "industries": len(s),
                         "giants": int(s.giants.sum()),
                         "giants_share_pooled": pooled("giants_rents_mn", "giants_receipts_bn"),
                         "rest_share_pooled": pooled("rest_rents_mn", "rest_receipts_bn"),
                         "median_gap": s.gap.median(), "mean_gap": s.gap.mean(),
                         "industries_gap_positive": int((s.gap > 0).sum())})
    return pd.DataFrame(rows)


def gap_regressions(d, cut_label):
    """gap_jt on group dummies with year effects; SEs clustered by industry. Also a Wilcoxon test.

    Year effects use sum (deviation) coding, so the intercept is the nondurable gap averaged over the
    three years and intercept + final coefficient is the durable-final-goods gap averaged over the years.
    """
    rows = []
    m = smf.ols("gap ~ C(group, Treatment('nondur')) + C(year, Sum)", data=d).fit(
        cov_type="cluster", cov_kwds={"groups": d.sb_code.astype("category").cat.codes})
    for term in m.params.index:
        if term.startswith("C(year"):
            continue
        rows.append({"cut": cut_label, "spec": "gap on group, year effects", "term": term, "coef": m.params[term],
                     "se": m.bse[term], "p": m.pvalues[term], "ci_low": m.conf_int().loc[term, 0],
                     "ci_high": m.conf_int().loc[term, 1], "n_obs": int(m.nobs), "n_industries": d.sb_code.nunique()})
    t = m.t_test("Intercept + C(group, Treatment('nondur'))[T.final] = 0")
    ci = t.conf_int()[0]
    rows.append({"cut": cut_label, "spec": "gap on group, year effects", "term": "mean gap, durable final goods",
                 "coef": float(t.effect[0]), "se": float(t.sd[0, 0]), "p": float(t.pvalue), "ci_low": ci[0],
                 "ci_high": ci[1], "n_obs": int(m.nobs), "n_industries": d.sb_code.nunique()})
    # Wilcoxon signed-rank on the primary year: giants vs rest within each industry, by group
    from scipy import stats
    for g in ["final", "nondur", "parts"]:
        s = d[(d.year == PRIMARY_YEAR) & (d.group == g)]
        w = stats.wilcoxon(s.giants_share, s.rest_share, zero_method="zsplit")
        rows.append({"cut": cut_label, "spec": f"Wilcoxon signed-rank, TY{PRIMARY_YEAR}", "term": GROUP_LABEL[g],
                     "coef": float(np.median(s.gap)), "se": np.nan, "p": float(w.pvalue), "ci_low": np.nan,
                     "ci_high": np.nan, "n_obs": len(s), "n_industries": len(s)})
    return pd.DataFrame(rows)


def plot(d, path):
    s = d[d.year == PRIMARY_YEAR].sort_values("gap")
    colors = {"final": "#1f5fa8", "parts": "#9a9a9a", "nondur": "#d9822b"}
    s = s[(s.giants_share > 0.25) | (s.rest_share > 0.25) | (s.group == "final")]
    fig, ax = plt.subplots(figsize=(8, 0.28 * len(s) + 1.4))
    y = np.arange(len(s))
    ax.hlines(y, s.rest_share, s.giants_share, color="#cccccc", linewidth=2)
    ax.scatter(s.rest_share, y, color="white", edgecolor="#555555", s=30, zorder=3, label="Corporations under $2.5 billion")
    ax.scatter(s.giants_share, y, color=[colors[g] for g in s.group], s=36, zorder=4,
               label="Corporations with $2.5 billion or more")
    ax.set_yticks(y)
    ax.set_yticklabels(s.industry, fontsize=8)
    ax.set_xscale("symlog", linthresh=0.01)
    ax.set_xlim(0, 10)
    ax.set_xticks([0, 0.01, 0.1, 1, 10])
    ax.set_xticklabels(["0", "0.01%", "0.1%", "1%", "10%"])
    ax.set_xlabel("Gross rents as % of receipts, tax year 2013 (log scale)")
    ax.set_title("Inside each industry, the giants do the renting")
    ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.4, -0.09), ncol=2, fontsize=8)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def main():
    OUT.mkdir(exist_ok=True)
    frames = {"$2.5 billion+": [], "$500 million+": []}
    for year in FILES:
        x = load_year(year)
        frames["$2.5 billion+"].append(split(x, year, GIANT_AC))
        frames["$500 million+"].append(split(x, year, LARGE_AC))
    main_d = pd.concat(frames["$2.5 billion+"], ignore_index=True)
    check_d = pd.concat(frames["$500 million+"], ignore_index=True)
    main_d.to_csv(OUT / "giants_industries.csv", index=False, float_format="%.5g")

    summ = pd.concat([summarize(main_d, "$2.5 billion+"), summarize(check_d, "$500 million+")])
    summ.to_csv(OUT / "giants_summary.csv", index=False, float_format="%.4f")
    print(summ.round(3).to_string(index=False))

    reg = pd.concat([gap_regressions(main_d, "$2.5 billion+"), gap_regressions(check_d, "$500 million+")])
    reg.to_csv(OUT / "giants_regressions.csv", index=False, float_format="%.5g")
    print(reg[["cut", "spec", "term", "coef", "se", "p", "n_obs"]].round(4).to_string(index=False))

    top = main_d[main_d.year == PRIMARY_YEAR].sort_values("gap", ascending=False)
    print(f"Largest gaps, TY{PRIMARY_YEAR}:")
    print(top.head(10)[["industry", "group", "giants", "giants_share", "rest_share", "giants_rents_mn"]]
          .round(3).to_string(index=False))
    plot(main_d, OUT / "giants_vs_rest_2013.png")
    print("Wrote results/giants_industries.csv, giants_summary.csv, giants_regressions.csv, giants_vs_rest_2013.png")


if __name__ == "__main__":
    main()
