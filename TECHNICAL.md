# Technical notes

This is the technical companion to the [README](README.md). It covers the data, the method, every test statistic
and how to reproduce the results. All tables are in [results/FINDINGS.md](results/FINDINGS.md), and a structured
review of the original paper is in [METHODS_REVIEW.md](METHODS_REVIEW.md).

## The original study

Jeremy I. Bulow, "Durable-Goods Monopolists," *Journal of Political Economy* 90(2), April 1982, pp. 314–332. The
paper is theory. In a two-period model of a perfectly durable good, a monopolist that sells earns less than one that
rents, because it cannot commit not to expand output later and buyers anticipate the lower second-period price.
The abstract adds that a seller unable to rent will make goods less durable than competitive firms or renters, will
invest less in fixed costs including research than a renter (a reverse Averch-Johnson result), and may cause a
larger deadweight loss despite having less market power.

The headline number comes from the textbook linear version of the model (rental demand $`p = 1 - Q`$, zero cost,
discount factor $`\delta`$), in which

```math
\Pi^R = \frac{1+\delta}{4}, \qquad \Pi^S = \frac{(2+\delta)^2}{4(4+\delta)}, \qquad \frac{\Pi^S}{\Pi^R}\bigg|_{\delta = 1} = \frac{0.45}{0.50} = 0.90
```

These are recomputed in `results/bulow_model.csv` for $`\delta`$ = 0.5, 0.8, 0.9 and 1.0 (ratios 0.926, 0.907, 0.903,
0.900).

## Headline results

| Test | Estimate | SE | p | N |
|---|---|---|---|---|
| Durable final goods vs. nondurables, rent share level (points) | +0.233 | 0.101 | 0.021 | 350 |
| CR4 slope for durable final goods, full model ($`\beta + \theta_{\text{final}}`$) | +0.0030 | 0.0050 | 0.55 | 350 |
| CR4 slope, durable final goods only | −0.0067 | 0.0084 | 0.42 | 121 |
| CR4 slope, durable final goods, receipt-weighted (added check) | −0.0316 | 0.0123 | 0.010 | 121 |
| CR4 slope, nondurables only (placebo) | +0.0039 | 0.0015 | 0.008 | 149 |
| Giants minus rest, mean gap in durable final goods ($2.5B+) | +1.054 | 0.525 | 0.045 | 130 |
| Same, difference from nondurables | +0.931 | 0.538 | 0.083 | 130 |
| Giants minus rest, mean gap in durable final goods ($500M+) | +0.988 | 0.463 | 0.033 | 138 |

Bulow's durability prediction holds. His market-power prediction fails across industries when market power is
measured by concentration, and holds within industries when it is measured by firm size.

## Data

- **IRS Statistics of Income, Table 5.1, Returns of Active Corporations** (balance sheet, income statement and tax
  items by minor industry), tax years 2018 to 2023. Files `data/raw/irs_soi/18co51ccr.xlsx` to `23co51ccr.xlsx`,
  from `https://www.irs.gov/pub/irs-soi/`. Money amounts in thousands of dollars. Items used are number of returns,
  total assets, business receipts, gross rents, net income, interest paid and depreciable assets.
- **IRS Corporation Source Book flat files**, tax years 2007, 2012 and 2013 (the last edition), files
  `data/raw/irs_sourcebook/07sbflatfile.zip`, `12sbfltfile.zip`, `13sbfltfile.zip`, from the same IRS directory.
  Table 1 (all returns) by industry and 13 asset classes. Variables `GRS_RCPTS` (business receipts),
  `COMP_GRS_RNTS` (rents), `WT_CT` (returns), `TOT_ASSTS`, and the disclosure flags `*_IND`.
- **US Census Bureau, Economic Census concentration tables** `EC1700SIZECONCEN` and `EC2200SIZECONCEN`
  (`data/raw/census/`), from `https://www2.census.gov/programs-surveys/economic-census/data/2017/sector00/` and
  `.../2022/sector00/`. CR4 (`CONCENFI` 604), shipments (`CONCENFI` 001) and HHI for the 50 largest firms
  (`CONCENFI` 650; values flagged D are withheld and treated as missing).

All files were downloaded on November 1, 2026. Every input is committed, about 6 MB in total.

## Method

These rules were fixed before the rent shares were examined.

- **Unit and outcome.** IRS manufacturing minor industry by tax year. Rent share
  $`s = H/(B + H)`$ with $`H`$ gross rents and $`B`$ business receipts, in percent.
- **Concentration.** Each IRS industry is mapped to NAICS prefixes from the IRS principal business activity codes,
  and its CR4 is the shipment-weighted mean over the 6-digit Census industries under those prefixes. Tax years
  2018 to 2020 use the 2017 Census, 2021 to 2023 the 2022 Census.
- **Groups.** Durable final goods are NAICS 333–337, 3391 and 3399, excluding 3344. Durable materials and parts are
  321, 327, 331, 332 and 3344. Nondurables are 311–326 except 321. The Census definition of durables (321, 327,
  331–339) is a robustness check.
- **Sample.** Industry-years with gross rents or receipts withheld by the IRS are dropped (40 of 390), leaving 350
  industry-years in 63 industries. Tobacco and leather are withheld in every year.
- **Main equation.** Standard errors are clustered by industry.

```math
\begin{aligned}
s_{jt} &= \alpha_t + \gamma_g + \beta\,\text{CR4}_{jt} + \theta_g\,(\text{CR4}_{jt} \times G_{gj}) \\
&\quad + \lambda \ln(B_{jt}/N_{jt}) + \varepsilon_{jt}, \qquad H_0\!: \beta + \theta_{\text{final}} = 0
\end{aligned}
```

- **Checks.** The same equation in logs; CR4 replaced by HHI/100; durable final goods alone; durable final goods
  without motor vehicles; the Census durable split; nondurables alone; a level regression on group dummies alone;
  Spearman rank correlations of industry averages by group; and, added after the others, receipt-weighted least
  squares for durable final goods.
- **Extension.** For each Source Book industry and year, the rent share of corporations in asset class 13 ($2.5
  billion or more) minus that of classes 3 to 12. Class 1 is the industry total and class 2 the zero-asset returns,
  both excluded. Industry-years whose top class is folded into a lower one (flag 2) or deleted (flag 3) are dropped.
  A smaller size class the IRS deletes is left out of the rest, so the rest's totals can fall slightly short of
  the industry total. The gap is regressed on group dummies with year effects coded as deviations from their
  average, so the intercept plus the durable final goods coefficient is that group's gap averaged over the three
  years. Standard errors are clustered by industry, and a Wilcoxon signed-rank test
  compares giants with the rest across 2013 industries within each group. A cut at asset class 12 ($500 million) is
  the check.

```math
\begin{aligned}
d_{jt} &= s^{\text{giants}}_{jt} - s^{\text{rest}}_{jt} \\
&= \alpha_t + \phi_{\text{final}} D^{\text{final}}_j + \phi_{\text{parts}} D^{\text{parts}}_j + u_{jt}, \qquad H_0\!: \bar{\alpha} + \phi_{\text{final}} = 0
\end{aligned}
```

## Full test statistics

Main panel, `results/regressions.csv`. Coefficients are in percentage points of rent share per point of CR4 unless
stated.

| Specification | Term | Coefficient | SE | p |
|---|---|---|---|---|
| Levels, full model | CR4 (nondurables) | 0.0015 | 0.0027 | 0.57 |
| Levels, full model | CR4 × durable final | 0.0015 | 0.0053 | 0.78 |
| Levels, full model | CR4 × materials and parts | −0.0028 | 0.0018 | 0.11 |
| Logs, full model | CR4 × durable final | −0.0214 | 0.0229 | 0.35 |
| Census durable split | CR4 × durable | 0.0023 | 0.0044 | 0.61 |
| Durable final goods, HHI/100 | HHI | −0.0159 | 0.0125 | 0.21 |
| Durable final goods, no motor vehicles | CR4 | −0.0011 | 0.0073 | 0.88 |
| Group dummies only | Durable final | 0.233 | 0.101 | 0.021 |
| Group dummies only | Materials and parts | −0.001 | 0.027 | 0.97 |

Spearman correlations of industry-average CR4 and rent share are 0.158 (p = 0.49, 21 industries) for durable final
goods, −0.310 (p = 0.28, 14) for materials and parts, and 0.490 (p = 0.008, 28) for nondurables.

Extension, `results/giants_regressions.csv` and `results/giants_summary.csv`. Pooled rent shares of giants versus the
rest in durable final goods are 2.235% vs. 0.093% (2007), 1.589% vs. 0.091% (2012) and 1.510% vs. 0.083% (2013).
In nondurables they are 0.147% vs. 0.049%, 0.071% vs. 0.045% and 0.069% vs. 0.042%. The 2013 Wilcoxon tests give
p = 0.16 for durable final goods at the $2.5 billion cut (10 of 17 gaps positive) and p = 0.007 at the $500 million
cut (11 of 17), against p = 0.67 and 0.34 for nondurables.

## Reproducing the results

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python src/bulow_leasing.py
python src/giants_vs_rest.py
```

Both scripts read only committed files and write to `results/`. They print the rows loaded, kept and dropped.

## Repository layout

| Path | What it is |
|---|---|
| `src/bulow_leasing.py` | Main test (IRS Table 5.1 with Census CR4), model table, first figure |
| `src/giants_vs_rest.py` | Extension (Source Book size classes), second figure |
| `results/industry_panel.csv` | The 350 industry-years used in the main test |
| `results/industries.csv` | One row per industry, averages over 2018–2023 |
| `results/naics6_concentration.csv` | The 6-digit Census industries behind each CR4 |
| `results/giants_industries.csv` | Giants and the rest by industry and year |

## References

- Bulow, J. I. (1982). Durable-goods monopolists. *Journal of Political Economy* 90(2), 314–332.
- Bulow, J. I. (1986). An economic theory of planned obsolescence. *Quarterly Journal of Economics* 101(4).
- Coase, R. H. (1972). Durability and monopoly. *Journal of Law and Economics* 15(1), 143–149.
- Waldman, M. (2003). Durable goods theory for real world markets. *Journal of Economic Perspectives* 17(1),
  131–154.
- US Census Bureau (2020, 2025). Economic Census concentration tables, 2017 and 2022.
- Internal Revenue Service, Statistics of Income. Corporation Source Book (2007–2013) and Table 5.1 (2018–2023).
