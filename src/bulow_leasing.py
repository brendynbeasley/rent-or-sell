"""Bulow (1982) on modern data: do manufacturers with market power over durable goods rent them out?

Bulow's two-period model says a monopolist that sells a durable good earns less than one that rents
it, because buyers anticipate that the seller will flood the market later. A firm with market power
over a durable good therefore has a reason to lease; a competitive firm, or a firm selling something
that is used up, does not. This script turns that into a test on every US manufacturing corporation:

    rent share of industry j in year t = gross rents / (business receipts + gross rents)

from IRS Statistics of Income Table 5.1 (tax years 2018-2023, 65 manufacturing minor industries),
against the industry's four-firm concentration ratio (CR4) from the 2017 and 2022 Economic Census.
The prediction is a positive CR4 slope for durable final goods and none for nondurables.

It also tabulates the model's own numbers (renting vs. selling profit by discount factor).

Run from the repository root:
    python src/bulow_leasing.py
Inputs are committed in data/raw/. Outputs go to results/.
"""

import zipfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "results"

TAX_YEARS = [2018, 2019, 2020, 2021, 2022, 2023]
# Census year paired with each tax year: the nearest Economic Census at or before it
CENSUS_FOR_YEAR = {2018: 2017, 2019: 2017, 2020: 2017, 2021: 2022, 2022: 2022, 2023: 2022}
IRS_ITEMS = {
    "Number of returns": "returns",
    "Total assets": "assets",
    "Business receipts": "receipts",
    "Gross rents": "rents",
    "Net income (less deficit)": "net_income",
    "Depreciable assets": "depreciable",
    "Interest paid": "interest_paid",
}

# IRS minor industry (as titled in Table 5.1) -> 2017/2022 NAICS prefixes it covers, and Bulow group.
# Prefixes follow the IRS principal business activity codes in the Form 1120 instructions.
# Groups were fixed before looking at rent shares:
#   final  = durable final goods a buyer keeps for years (NAICS 333-337, 3391, 3399)
#   parts  = durable materials and components that disappear into other products (321, 327, 331, 332, 3344)
#   nondur = nondurable goods (311-326 except 321)
INDUSTRIES = [
    ("Animal food manufacturing", ["3111", "3112"], "nondur", "Animal food and grain milling"),
    ("Sugar and confectionery", ["3113"], "nondur", "Sugar and confectionery"),
    ("Fruit and vegetable preserving", ["3114"], "nondur", "Fruit and vegetable preserving"),
    ("Dairy product", ["3115"], "nondur", "Dairy products"),
    ("Meat and seafood processing", ["3116", "3117"], "nondur", "Meat and seafood"),
    ("Bakeries and tortilla", ["3118"], "nondur", "Bakeries and tortillas"),
    ("Other food", ["3119"], "nondur", "Other food"),
    ("Soft drink and ice", ["31211"], "nondur", "Soft drinks and ice"),
    ("Breweries", ["31212"], "nondur", "Breweries"),
    ("Wineries and distilleries", ["31213", "31214"], "nondur", "Wineries and distilleries"),
    ("Tobacco manufacturing", ["3122"], "nondur", "Tobacco"),
    ("Textile mills", ["313"], "nondur", "Textile mills"),
    ("Textile product mills", ["314"], "nondur", "Textile products"),
    ("Apparel knitting mills", ["3151"], "nondur", "Apparel knitting"),
    ("Cut and sew apparel", ["3152"], "nondur", "Cut and sew apparel"),
    ("Apparel accessories", ["3159"], "nondur", "Apparel accessories"),
    ("Leather and allied", ["316"], "nondur", "Leather"),
    ("Wood product", ["321"], "parts", "Wood products"),
    ("Pulp, paper, and paperboard", ["3221"], "nondur", "Pulp and paper mills"),
    ("Converted paper", ["3222"], "nondur", "Converted paper"),
    ("Printing and related", ["323"], "nondur", "Printing"),
    ("Petroleum refineries", ["32411"], "nondur", "Petroleum refineries"),
    ("Asphalt paving", ["32412", "32419"], "nondur", "Asphalt and other petroleum"),
    ("Basic chemical", ["3251"], "nondur", "Basic chemicals"),
    ("Resin, synthetic rubber", ["3252"], "nondur", "Resins and synthetic fibers"),
    ("Pharmaceutical and medicine", ["3254"], "nondur", "Pharmaceuticals"),
    ("Paint, coating", ["3255"], "nondur", "Paint and adhesives"),
    ("Soap, cleaning compound", ["3256"], "nondur", "Soap and toiletries"),
    ("Other chemical product", ["3253", "3259"], "nondur", "Other chemicals"),
    ("Plastics product", ["3261"], "nondur", "Plastics products"),
    ("Rubber product", ["3262"], "nondur", "Rubber products"),
    ("Clay, refractory", ["3271", "3279"], "parts", "Clay and other mineral products"),
    ("Glass and glass product", ["3272"], "parts", "Glass"),
    ("Cement, concrete", ["3273", "3274"], "parts", "Cement and concrete"),
    ("Iron, steel mills", ["3311", "3312"], "parts", "Iron and steel"),
    ("Nonferrous metal", ["3313", "3314"], "parts", "Nonferrous metals"),
    ("Foundries", ["3315"], "parts", "Foundries"),
    ("Forging and stamping", ["3321"], "parts", "Forging and stamping"),
    ("Cutlery, hardware", ["3322", "3326", "3327"], "parts", "Hardware, springs, machine shops"),
    ("Architectural and structural metals", ["3323"], "parts", "Structural metals"),
    ("Boiler, tank", ["3324"], "parts", "Boilers and tanks"),
    ("Coating, engraving", ["3328"], "parts", "Metal coating"),
    ("Other fabricated metal", ["3325", "3329"], "parts", "Other fabricated metal"),
    ("Agriculture, construction, and mining machinery", ["3331"], "final", "Farm, construction and mining machinery"),
    ("Industrial machinery", ["3332"], "final", "Industrial machinery"),
    ("Commercial and service industry machinery", ["3333"], "final", "Commercial and service machinery"),
    ("Ventilation, heating", ["3334"], "final", "Heating and air conditioning"),
    ("Metalworking machinery", ["3335"], "final", "Metalworking machinery"),
    ("Engine, turbine", ["3336"], "final", "Engines and turbines"),
    ("Other general purpose machinery", ["3339"], "final", "Other general machinery"),
    ("Computer and peripheral", ["3341"], "final", "Computers and peripherals"),
    ("Communications equipment", ["3342"], "final", "Communications equipment"),
    ("Audio and video equipment", ["3343", "3346"], "final", "Audio and video equipment"),
    ("Semiconductor and other electronic", ["3344"], "parts", "Semiconductors and components"),
    ("Navigational, measuring", ["3345"], "final", "Instruments and electromedical"),
    ("Electrical lighting equipment and household appliance", ["3351", "3352"], "final", "Lighting and household appliances"),
    ("Electrical equipment", ["3353"], "final", "Electrical equipment"),
    ("Other electrical equipment", ["3359"], "final", "Other electrical equipment"),
    ("Motor vehicles and parts", ["3361", "3362", "3363"], "final", "Motor vehicles and parts"),
    ("Aerospace product", ["3364"], "final", "Aerospace"),
    ("Ship and boat building", ["3366"], "final", "Ships and boats"),
    ("Other transportation equipment", ["3365", "3369"], "final", "Railcars and other transport equipment"),
    ("Furniture and related", ["337"], "final", "Furniture"),
    ("Medical equipment and supplies", ["3391"], "final", "Medical equipment and supplies"),
    ("Other miscellaneous manufacturing", ["3399"], "final", "Other miscellaneous manufacturing"),
]
GROUP_LABEL = {"final": "Durable final goods", "parts": "Durable materials and parts", "nondur": "Nondurable goods"}
CENSUS_DURABLE = ("321", "327", "331", "332", "333", "334", "335", "336", "337", "339")  # Census M3 definition
DELTAS = [0.5, 0.8, 0.9, 1.0]  # discount factors for the model table


def norm(s):
    return " ".join(str(s).replace("\n", " ").split()).lower()


def load_irs(year):
    """One row per manufacturing minor industry, IRS SOI Table 5.1, money in $ thousands."""
    path = RAW / "irs_soi" / f"{year % 100}co51ccr.xlsx"
    d = pd.read_excel(path, header=None, dtype=str, engine="openpyxl")
    items = d.iloc[:, 0].map(norm)
    item_row = {}
    for label, short in IRS_ITEMS.items():
        hits = items[items == norm(label)].index
        item_row[short] = hits[0]
    titles = {c: norm(d.iloc[5, c] if pd.notna(d.iloc[5, c]) else d.iloc[4, c]) for c in range(1, d.shape[1])}
    rows, suppressed = [], 0
    for stem, prefixes, group, label in INDUSTRIES:
        cols = [c for c, t in titles.items() if t.startswith(norm(stem))]
        # Table 5.1 also has wholesale industries with similar titles; manufacturing columns come first
        c = cols[0]
        rec = {"industry": label, "irs_title": titles[c], "group": group, "naics": "+".join(prefixes), "year": year}
        for short, r in item_row.items():
            raw = str(d.iloc[r, c]).replace(",", "").strip()
            if raw.lower() == "d":
                suppressed += 1
            rec[short] = pd.to_numeric(raw, errors="coerce")
        rows.append(rec)
    out = pd.DataFrame(rows)
    print(f"IRS TY{year}: {len(out)} manufacturing minor industries loaded from {path.name}; "
          f"{suppressed} cells suppressed ('d') by the IRS")
    return out


def load_census(year):
    """6-digit NAICS manufacturing industries with shipments and CR4 from the Economic Census."""
    path = RAW / "census" / f"EC{year % 100}00SIZECONCEN.zip"
    with zipfile.ZipFile(path) as z:
        name = [n for n in z.namelist() if n.endswith(".dat")][0]
        d = pd.read_csv(z.open(name), sep="|", dtype=str)
    d.columns = [c.lstrip("#") for c in d.columns]
    code = f"NAICS{year}"
    d = d[d.SECTOR.isin(["31", "32", "33"]) & (d[code].str.len() == 6)]
    tot = d[d.CONCENFI == "001"].set_index(code).RCPTOT.astype(float).rename("ship")
    cr4 = d[d.CONCENFI == "604"].set_index(code).VAL_PCT.astype(float).rename("cr4")
    h = d[d.CONCENFI == "650"]
    h = h[h.HHI_F.isna() | (h.HHI_F.str.strip() == "")]  # flag D = withheld, published as 0
    hhi = h.set_index(code).HHI.astype(float).rename("hhi")
    out = pd.concat([tot, cr4, hhi], axis=1).dropna(subset=["ship", "cr4"])
    print(f"Census {year}: {len(out)} six-digit manufacturing industries with CR4 from {path.name}")
    return out


def industry_concentration(census, year, detail):
    """Shipment-weighted CR4 and HHI over the 6-digit industries inside each IRS minor industry."""
    rows = []
    for stem, prefixes, group, label in INDUSTRIES:
        sub = census[census.index.map(lambda c: c.startswith(tuple(prefixes)))]
        detail.append(sub.assign(census_year=year, industry=label).reset_index(names="naics6"))
        w = sub.ship
        h = sub.dropna(subset=["hhi"])
        rows.append({"industry": label, "cr4": np.average(sub.cr4, weights=w), "n_naics6": len(sub),
                     "hhi": np.average(h.hhi, weights=h.ship) if len(h) else np.nan, "census_ship": w.sum()})
    return pd.DataFrame(rows).set_index("industry")


def build_panel():
    detail = []
    census = {y: industry_concentration(load_census(y), y, detail) for y in (2017, 2022)}
    pd.concat(detail).to_csv(OUT / "naics6_concentration.csv", index=False, float_format="%.6g")
    frames = []
    for y in TAX_YEARS:
        f = load_irs(y).set_index("industry")
        f = f.join(census[CENSUS_FOR_YEAR[y]])
        frames.append(f.reset_index())
    p = pd.concat(frames, ignore_index=True)
    p["rent_share"] = 100 * p.rents / (p.receipts + p.rents)
    p["receipts_per_return"] = p.receipts / p.returns / 1000  # $ millions per corporation
    p["roa"] = 100 * (p.net_income + p.interest_paid) / p.assets
    p["durable_census"] = p.naics.str[:3].isin(CENSUS_DURABLE)
    n0 = len(p)
    keep = p.rent_share.notna() & p.receipts_per_return.notna()
    print(f"Panel: {n0} industry-years; dropped {int((~keep).sum())} with gross rents or receipts "
          f"suppressed by the IRS; kept {int(keep.sum())}")
    return p[keep].copy()


def group_table(p):
    """Bulow's comparison: rent share by group and by concentration (above / below the median CR4)."""
    med = p.drop_duplicates("industry").cr4.median()
    p = p.assign(conc=np.where(p.cr4 >= med, "high", "low"))
    rows = []
    for g in ["final", "parts", "nondur"]:
        s = p[p.group == g]
        agg = lambda x: 100 * x.rents.sum() / (x.receipts.sum() + x.rents.sum())
        hi, lo = s[s.conc == "high"], s[s.conc == "low"]
        ind = s.groupby("industry").rent_share.mean()
        rows.append({"group": GROUP_LABEL[g], "industries": s.industry.nunique(),
                     "rents_bn_per_year": s.rents.sum() / 1e6 / len(TAX_YEARS),
                     "rent_share_pooled": agg(s), "rent_share_high_cr4": agg(hi), "rent_share_low_cr4": agg(lo),
                     "industries_high_cr4": hi.industry.nunique(), "industries_low_cr4": lo.industry.nunique(),
                     "median_industry_rent_share": ind.median()})
    t = pd.DataFrame(rows)
    t["receipts_bn_per_year"] = [p[p.group == g].receipts.sum() / 1e6 / len(TAX_YEARS) for g in ["final", "parts", "nondur"]]
    t["pct_of_manufacturing_rents"] = 100 * t.rents_bn_per_year / (p.rents.sum() / 1e6 / len(TAX_YEARS))
    t["pct_of_manufacturing_receipts"] = 100 * t.receipts_bn_per_year / (p.receipts.sum() / 1e6 / len(TAX_YEARS))
    t.attrs["median_cr4"] = med
    return t


def regressions(p):
    """Pooled industry-year regressions with year effects; standard errors clustered by industry."""
    specs = {
        "main_levels": ("rent_share ~ cr4 + cr4:C(group, Treatment('nondur')) + C(group, Treatment('nondur'))"
                        " + np.log(receipts_per_return) + C(year)", p),
        "main_logs": ("np.log(rent_share) ~ cr4 + cr4:C(group, Treatment('nondur')) + C(group, Treatment('nondur'))"
                      " + np.log(receipts_per_return) + C(year)", p[p.rent_share > 0]),
        "census_durable_split": ("rent_share ~ cr4 * durable_census + np.log(receipts_per_return) + C(year)", p),
        "final_goods_only": ("rent_share ~ cr4 + np.log(receipts_per_return) + C(year)", p[p.group == "final"]),
        "final_goods_hhi": ("rent_share ~ I(hhi / 100) + np.log(receipts_per_return) + C(year)",
                            p[(p.group == "final") & p.hhi.notna()]),
        "final_goods_no_vehicles": ("rent_share ~ cr4 + np.log(receipts_per_return) + C(year)",
                                    p[(p.group == "final") & (p.industry != "Motor vehicles and parts")]),
        "nondurables_only": ("rent_share ~ cr4 + np.log(receipts_per_return) + C(year)", p[p.group == "nondur"]),
        "durable_vs_nondurable_level": ("rent_share ~ C(group, Treatment('nondur')) + np.log(receipts_per_return)"
                                        " + C(year)", p),
    }
    rows = []
    for name, (f, data) in specs.items():
        m = smf.ols(f, data=data).fit(cov_type="cluster", cov_kwds={"groups": data.industry.astype("category").cat.codes})
        for term in m.params.index:
            if term.startswith("C(year)") or term == "Intercept":
                continue
            rows.append({"spec": name, "term": term, "coef": m.params[term], "se": m.bse[term],
                         "p": m.pvalues[term], "ci_low": m.conf_int().loc[term, 0], "ci_high": m.conf_int().loc[term, 1],
                         "n_obs": int(m.nobs), "n_industries": data.industry.nunique(), "r2": m.rsquared})
        if name == "main_levels":
            # slope of CR4 for durable final goods = cr4 + interaction, with its own clustered SE
            t = m.t_test("cr4 + cr4:C(group, Treatment('nondur'))[T.final] = 0")
            ci = t.conf_int()[0]
            rows.append({"spec": name, "term": "cr4 slope, durable final goods (sum)", "coef": float(t.effect[0]),
                         "se": float(t.sd[0, 0]), "p": float(t.pvalue), "ci_low": ci[0], "ci_high": ci[1],
                         "n_obs": int(m.nobs), "n_industries": data.industry.nunique(), "r2": m.rsquared})
    # Added check, not in the pre-set list: weight each industry by its receipts, as the pooled shares do
    fg = p[p.group == "final"]
    m = smf.wls("rent_share ~ cr4 + np.log(receipts_per_return) + C(year)", data=fg, weights=fg.receipts).fit(
        cov_type="cluster", cov_kwds={"groups": fg.industry.astype("category").cat.codes})
    rows.append({"spec": "final_goods_receipt_weighted", "term": "cr4", "coef": m.params["cr4"], "se": m.bse["cr4"],
                 "p": m.pvalues["cr4"], "ci_low": m.conf_int().loc["cr4", 0], "ci_high": m.conf_int().loc["cr4", 1],
                 "n_obs": int(m.nobs), "n_industries": fg.industry.nunique(), "r2": m.rsquared})
    r = pd.DataFrame(rows)
    print(f"Regressions: {r.spec.nunique()} specifications, clustered by industry")
    return r


def spearman_table(p):
    ind = p.groupby(["industry", "group"]).agg(cr4=("cr4", "mean"), rent_share=("rent_share", "mean")).reset_index()
    rows = []
    for g in ["final", "parts", "nondur"]:
        s = ind[ind.group == g]
        rho, pv = stats.spearmanr(s.cr4, s.rent_share)
        rows.append({"group": GROUP_LABEL[g], "industries": len(s), "spearman_rho": rho, "p": pv})
    return pd.DataFrame(rows), ind


def model_table():
    """Bulow's two-period model with linear rental demand p = 1 - q, zero cost, no depreciation."""
    rows = []
    for d in DELTAS:
        rent_profit = (1 + d) / 4
        q1 = 2 / (4 + d)
        q2 = (1 - q1) / 2
        p2 = q2
        p1 = (1 + d / 2) * (1 - q1)
        sell_profit = q1 * p1 + d * q2 * p2
        rows.append({"delta": d, "renter_output": 0.5, "renter_profit": rent_profit, "seller_q1": q1,
                     "seller_q2": q2, "seller_p1": p1, "seller_p2": p2, "seller_profit": sell_profit,
                     "seller_closed_form": (2 + d) ** 2 / (4 * (4 + d)), "seller_over_renter": sell_profit / rent_profit})
    return pd.DataFrame(rows)


def plot(ind, path):
    colors = {"final": "#1f5fa8", "parts": "#9a9a9a", "nondur": "#d9822b"}
    fig, ax = plt.subplots(figsize=(8, 5.2))
    for g in ["nondur", "parts", "final"]:
        s = ind[ind.group == g]
        ax.scatter(s.cr4, s.rent_share, s=36, color=colors[g], label=GROUP_LABEL[g], alpha=0.85,
                   edgecolor="white", linewidth=0.5)
    for _, r in ind.nlargest(6, "rent_share").iterrows():
        ax.annotate(r.industry, (r.cr4, r.rent_share), xytext=(5, 3), textcoords="offset points", fontsize=8)
    ax.set_xlabel("Four-firm concentration ratio (%), shipment-weighted, average of 2017 and 2022 Census pairings")
    ax.set_ylabel("Gross rents as % of receipts, 2018-2023 average")
    ax.set_title("Who rents out what they make: US manufacturing corporations")
    ax.legend(frameon=False, loc="upper left")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def main():
    OUT.mkdir(exist_ok=True)
    p = build_panel()
    p.to_csv(OUT / "industry_panel.csv", index=False, float_format="%.6g")

    g = group_table(p)
    g.to_csv(OUT / "group_rent_shares.csv", index=False, float_format="%.4f")
    print(f"Median industry CR4 (split point): {g.attrs['median_cr4']:.1f}%")
    print(g.round(3).to_string(index=False))

    r = regressions(p)
    r.to_csv(OUT / "regressions.csv", index=False, float_format="%.5g")
    show = r[r.term.str.contains("cr4|hhi") | r.term.str.contains("group")]
    print(show[["spec", "term", "coef", "se", "p", "n_obs"]].round(4).to_string(index=False))

    sp, ind = spearman_table(p)
    sp.to_csv(OUT / "spearman_by_group.csv", index=False, float_format="%.4f")
    print(sp.round(3).to_string(index=False))

    ind_full = p.groupby(["industry", "group", "naics"]).agg(
        cr4_2017=("cr4", lambda s: s[p.loc[s.index, "year"] <= 2020].mean()),
        cr4_2022=("cr4", lambda s: s[p.loc[s.index, "year"] >= 2021].mean()),
        rent_share=("rent_share", "mean"), rents_mn_per_year=("rents", lambda s: s.mean() / 1e3),
        receipts_bn_per_year=("receipts", lambda s: s.mean() / 1e6), corporations=("returns", "mean"),
        roa=("roa", "mean"), years=("year", "nunique")).reset_index().sort_values("rent_share", ascending=False)
    ind_full["group"] = ind_full.group.map(GROUP_LABEL)
    ind_full.to_csv(OUT / "industries.csv", index=False, float_format="%.4f")
    print("Top ten industries by rent share:")
    print(ind_full.head(10)[["industry", "group", "cr4_2022", "rent_share", "rents_mn_per_year"]].round(2).to_string(index=False))

    m = model_table()
    m.to_csv(OUT / "bulow_model.csv", index=False, float_format="%.4f")
    print(m.round(4).to_string(index=False))

    plot(ind, OUT / "rent_share_vs_cr4.png")
    print("Wrote results/industry_panel.csv, group_rent_shares.csv, regressions.csv, spearman_by_group.csv, "
          "industries.csv, bulow_model.csv, rent_share_vs_cr4.png")


if __name__ == "__main__":
    main()
