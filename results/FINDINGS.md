# Bulow (1982) on modern data: findings

## In plain English

Jeremy Bulow showed in 1982 that a company with market power over something durable earns more by renting it out
than by selling it. If that is how companies behave, renting should show up where durability and market power meet.

- **Renting happens almost only in durable final goods.** The industries that make cars, farm and construction
  machinery, copiers and appliances (home to General Motors, Ford, Deere, Caterpillar, Xerox and Whirlpool) belong
  to a group that accounts for 86.8% of all the rent American manufacturers report, while making 37.3% of what they
  sell. Drug makers, brewers and steel mills
  barely rent at all.
- **Industry concentration does not predict renting.** Highly concentrated durable industries such as aerospace
  (Boeing, Lockheed Martin) and computers (Dell, HP, Apple) rent out less than a tenth as much of their receipts as
  motor vehicles, and copier and postage-meter makers
  (Xerox, Pitney Bowes) rent a lot in an industry the Census counts as unconcentrated.
- **Inside an industry, the giants do the renting.** In durable final goods, corporations with $2.5 billion or
  more in assets got 1.51% of their 2013 receipts from rents, 18 times the 0.083% of smaller corporations in the same
  industries. In nondurables the giants and everyone else were nearly the same.

The [README](../README.md) tells the story. The rest of this page is every table the two scripts produce.

**Key to the labels.** *Rent share* = gross rents ÷ (business receipts + gross rents), in percent. *CR4* = share of
shipments made by an industry's four largest companies, shipment-weighted over its 6-digit Census industries.
*Durable final goods* = NAICS 333–337, 3391, 3399 (not 3344). *Durable materials and parts* = 321, 327, 331, 332,
3344. *Nondurable goods* = 311–326 except 321. *Giants* = corporations with $2.5 billion or more in assets (Source
Book asset class 13); *rest* = asset classes 3–12. *Gap* = giants' rent share minus the rest's, in points. Standard
errors are clustered by industry.

## 1. Rent shares by group, tax years 2018–2023

Source: `results/group_rent_shares.csv`. Pooled shares sum rents and receipts over all industry-years in the group.
The CR4 split is at 39%, the median across industries; an industry can fall on different sides in the 2017 and 2022
Census, so the counts of industries above and below can exceed the group total.

| Group | Industries | Rents, $bn/yr | Receipts, $bn/yr | % of rents | % of receipts | Rent share, pooled | CR4 ≥ 39% | CR4 < 39% | Median industry |
|---|---|---|---|---|---|---|---|---|---|
| Durable final goods | 21 | 19.93 | 2942 | 86.8 | 37.3 | 0.673 | 0.864 | 0.167 | 0.106 |
| Durable materials and parts | 14 | 0.38 | 1196 | 1.6 | 15.2 | 0.032 | 0.025 | 0.036 | 0.026 |
| Nondurable goods | 28 | 2.65 | 3750 | 11.5 | 47.5 | 0.071 | 0.080 | 0.037 | 0.034 |

## 2. Regressions, tax years 2018–2023

Source: `results/regressions.csv`. Outcome is the rent share in points (in logs for `main_logs`). All specifications
include year effects. `final_goods_receipt_weighted` was added after the pre-set checks.

| Specification | Term | Coef. | SE | p | 95% CI | N | Industries |
|---|---|---|---|---|---|---|---|
| main_levels | group[T.final] | 0.1662 | 0.1923 | 0.387 | [-0.2106, 0.5430] | 350 | 63 |
| main_levels | group[T.parts] | 0.1016 | 0.0628 | 0.105 | [-0.0214, 0.2246] | 350 | 63 |
| main_levels | cr4 | 0.0015 | 0.0027 | 0.574 | [-0.0038, 0.0069] | 350 | 63 |
| main_levels | cr4:group[T.final] | 0.0015 | 0.0053 | 0.782 | [-0.0090, 0.0120] | 350 | 63 |
| main_levels | cr4:group[T.parts] | -0.0028 | 0.0018 | 0.112 | [-0.0064, 0.0007] | 350 | 63 |
| main_levels | log receipts per corporation | 0.0238 | 0.0273 | 0.383 | [-0.0297, 0.0774] | 350 | 63 |
| main_levels | cr4 slope, durable final goods (sum) | 0.0030 | 0.0050 | 0.547 | [-0.0068, 0.0128] | 350 | 63 |
| main_logs | group[T.final] | 1.5726 | 0.9608 | 0.102 | [-0.3106, 3.4558] | 344 | 62 |
| main_logs | group[T.parts] | 1.1117 | 0.5780 | 0.054 | [-0.0212, 2.2446] | 344 | 62 |
| main_logs | cr4 | 0.0221 | 0.0154 | 0.153 | [-0.0082, 0.0523] | 344 | 62 |
| main_logs | cr4:group[T.final] | -0.0214 | 0.0229 | 0.351 | [-0.0663, 0.0235] | 344 | 62 |
| main_logs | cr4:group[T.parts] | -0.0329 | 0.0155 | 0.033 | [-0.0632, -0.0026] | 344 | 62 |
| main_logs | log receipts per corporation | 0.0888 | 0.0962 | 0.356 | [-0.0998, 0.2774] | 344 | 62 |
| census_durable_split | durable_census[T.True] | 0.0509 | 0.1378 | 0.712 | [-0.2192, 0.3210] | 350 | 63 |
| census_durable_split | cr4 | 0.0013 | 0.0029 | 0.656 | [-0.0044, 0.0069] | 350 | 63 |
| census_durable_split | cr4:durable_census[T.True] | 0.0023 | 0.0044 | 0.605 | [-0.0063, 0.0108] | 350 | 63 |
| census_durable_split | log receipts per corporation | 0.0274 | 0.0295 | 0.352 | [-0.0304, 0.0852] | 350 | 63 |
| final_goods_only | cr4 | -0.0067 | 0.0084 | 0.423 | [-0.0232, 0.0097] | 121 | 21 |
| final_goods_only | log receipts per corporation | 0.2065 | 0.1426 | 0.147 | [-0.0729, 0.4859] | 121 | 21 |
| final_goods_hhi | I(hhi / 100) | -0.0159 | 0.0125 | 0.206 | [-0.0404, 0.0087] | 118 | 21 |
| final_goods_hhi | log receipts per corporation | 0.1889 | 0.1043 | 0.070 | [-0.0155, 0.3933] | 118 | 21 |
| final_goods_no_vehicles | cr4 | -0.0011 | 0.0073 | 0.880 | [-0.0154, 0.0132] | 115 | 20 |
| final_goods_no_vehicles | log receipts per corporation | 0.0624 | 0.0815 | 0.444 | [-0.0974, 0.2221] | 115 | 20 |
| nondurables_only | cr4 | 0.0039 | 0.0015 | 0.008 | [0.0010, 0.0068] | 149 | 28 |
| nondurables_only | log receipts per corporation | -0.0094 | 0.0071 | 0.186 | [-0.0234, 0.0045] | 149 | 28 |
| durable_vs_nondurable_level | group[T.final] | 0.2331 | 0.1008 | 0.021 | [0.0355, 0.4306] | 350 | 63 |
| durable_vs_nondurable_level | group[T.parts] | -0.0011 | 0.0268 | 0.968 | [-0.0536, 0.0514] | 350 | 63 |
| durable_vs_nondurable_level | log receipts per corporation | 0.0328 | 0.0232 | 0.157 | [-0.0127, 0.0782] | 350 | 63 |
| final_goods_receipt_weighted | cr4 | -0.0316 | 0.0123 | 0.010 | [-0.0558, -0.0074] | 121 | 21 |

## 3. Rank correlations of industry averages

Source: `results/spearman_by_group.csv`.

| Group | Industries | Spearman rho | p |
|---|---|---|---|
| Durable final goods | 21 | 0.158 | 0.493 |
| Durable materials and parts | 14 | -0.310 | 0.281 |
| Nondurable goods | 28 | 0.490 | 0.008 |

## 4. Every industry, 2018–2023 averages

Source: `results/industries.csv`. Rent share is the mean of yearly shares. Years counts the tax years in which the
IRS published the industry's rents. Tobacco and leather are withheld in every year. The 6-digit detail behind each
CR4 is in `results/naics6_concentration.csv`, and the industry-year panel in `results/industry_panel.csv`.

| Industry | Group | NAICS | CR4 2017 | CR4 2022 | Rent share % | Rents $mn/yr | Receipts $bn/yr | Corporations | Years |
|---|---|---|---|---|---|---|---|---|---|
| Motor vehicles and parts | Durable final goods | 3361+3362+3363 | 53.4 | 47.9 | 1.545 | 14900.4 | 954.0 | 4746 | 6 |
| Farm, construction and mining machinery | Durable final goods | 3331 | 51.1 | 53.3 | 1.449 | 1961.2 | 138.0 | 3376 | 6 |
| Commercial and service machinery | Durable final goods | 3333 | 22.1 | 15.5 | 0.672 | 230.5 | 34.7 | 1649 | 6 |
| Lighting and household appliances | Durable final goods | 3351+3352 | 57.3 | 58.7 | 0.634 | 759.1 | 123.7 | 1052 | 6 |
| Breweries | Nondurable goods | 31212 | 68.6 | 63.6 | 0.355 | 121.4 | 33.7 | 1617 | 4 |
| Electrical equipment | Durable final goods | 3353 | 38.5 | 38.7 | 0.352 | 323.0 | 88.0 | 1731 | 6 |
| Other food | Nondurable goods | 3119 | 39.0 | 43.8 | 0.305 | 601.4 | 184.3 | 4811 | 6 |
| Medical equipment and supplies | Durable final goods | 3391 | 32.8 | 32.9 | 0.295 | 576.9 | 196.0 | 10833 | 6 |
| Sugar and confectionery | Nondurable goods | 3113 | 56.9 | 52.8 | 0.178 | 58.7 | 34.0 | 1658 | 6 |
| Industrial machinery | Durable final goods | 3332 | 25.5 | 31.8 | 0.146 | 72.1 | 50.3 | 4100 | 6 |
| Animal food and grain milling | Nondurable goods | 3111+3112 | 57.5 | 57.0 | 0.140 | 227.1 | 162.5 | 1626 | 6 |
| Engines and turbines | Durable final goods | 3336 | 55.5 | 55.4 | 0.138 | 67.9 | 44.3 | 313 | 6 |
| Aerospace | Durable final goods | 3364 | 82.5 | 77.6 | 0.136 | 458.6 | 340.4 | 1454 | 5 |
| Computers and peripherals | Durable final goods | 3341 | 57.2 | 61.7 | 0.120 | 441.8 | 306.8 | 2065 | 5 |
| Clay and other mineral products | Durable materials and parts | 3271+3279 | 43.1 | 38.1 | 0.108 | 33.6 | 32.5 | 1860 | 6 |
| Railcars and other transport equipment | Durable final goods | 3365+3369 | 62.8 | 64.6 | 0.106 | 43.7 | 42.5 | 1606 | 6 |
| Audio and video equipment | Durable final goods | 3343+3346 | 35.3 | 46.2 | 0.102 | 46.4 | 40.0 | 750 | 5 |
| Soft drinks and ice | Nondurable goods | 31211 | 55.8 |  | 0.098 | 52.9 | 55.1 | 533 | 2 |
| Cement and concrete | Durable materials and parts | 3273+3274 | 26.0 | 30.7 | 0.094 | 86.6 | 94.2 | 3290 | 6 |
| Pulp and paper mills | Nondurable goods | 3221 | 61.8 | 59.0 | 0.084 | 60.1 | 66.1 | 442 | 5 |
| Petroleum refineries | Nondurable goods | 32411 | 44.9 | 52.2 | 0.076 | 947.2 | 1367.3 | 136 | 6 |
| Boilers and tanks | Durable materials and parts | 3324 | 45.5 | 45.4 | 0.068 | 23.3 | 32.6 | 437 | 5 |
| Metalworking machinery | Durable final goods | 3335 | 17.8 | 18.9 | 0.064 | 17.3 | 26.9 | 4426 | 6 |
| Wineries and distilleries | Nondurable goods | 31213+31214 | 47.0 | 41.1 | 0.055 | 20.2 | 35.7 | 3156 | 6 |
| Basic chemicals | Nondurable goods | 3251 | 45.6 | 42.8 | 0.055 | 126.1 | 229.9 | 1170 | 6 |
| Converted paper | Nondurable goods | 3222 | 43.0 | 42.8 | 0.048 | 48.5 | 98.9 | 1216 | 6 |
| Pharmaceuticals | Nondurable goods | 3254 | 43.0 | 38.0 | 0.047 | 232.0 | 487.7 | 1610 | 6 |
| Other general machinery | Durable final goods | 3339 | 33.3 | 32.1 | 0.043 | 52.5 | 107.5 | 5308 | 6 |
| Communications equipment | Durable final goods | 3342 | 43.8 | 49.8 | 0.040 | 26.6 | 65.1 | 1080 | 6 |
| Fruit and vegetable preserving | Nondurable goods | 3114 | 35.2 | 38.6 | 0.038 | 32.5 | 84.5 | 1115 | 6 |
| Metal coating | Durable materials and parts | 3328 | 19.7 | 29.0 | 0.038 | 6.2 | 16.8 | 3314 | 5 |
| Bakeries and tortillas | Nondurable goods | 3118 | 36.7 | 34.4 | 0.038 | 19.5 | 50.3 | 5419 | 6 |
| Apparel knitting | Nondurable goods | 3151 | 38.5 |  | 0.037 | 1.4 | 3.9 | 137 | 1 |
| Resins and synthetic fibers | Nondurable goods | 3252 | 30.6 | 35.4 | 0.032 | 18.7 | 59.9 | 552 | 6 |
| Furniture | Durable final goods | 337 | 35.1 | 32.7 | 0.032 | 25.7 | 82.0 | 10382 | 5 |
| Plastics products | Nondurable goods | 3261 | 21.2 | 22.0 | 0.032 | 47.8 | 153.5 | 8507 | 5 |
| Textile products | Nondurable goods | 314 | 36.1 | 35.5 | 0.029 | 8.0 | 26.9 | 3901 | 5 |
| Other chemicals | Nondurable goods | 3253+3259 | 42.0 | 45.3 | 0.029 | 27.2 | 88.9 | 3142 | 6 |
| Textile mills | Nondurable goods | 313 | 34.9 | 35.3 | 0.028 | 4.6 | 15.4 | 1237 | 6 |
| Other miscellaneous manufacturing | Durable final goods | 3399 | 27.2 | 26.0 | 0.028 | 27.9 | 98.7 | 16864 | 6 |
| Wood products | Durable materials and parts | 321 | 32.4 | 34.2 | 0.027 | 32.3 | 125.2 | 12222 | 6 |
| Printing | Nondurable goods | 323 | 16.9 | 14.1 | 0.027 | 18.5 | 69.4 | 21423 | 6 |
| Hardware, springs, machine shops | Durable materials and parts | 3322+3326+3327 | 11.7 | 10.7 | 0.027 | 20.7 | 76.3 | 17210 | 6 |
| Structural metals | Durable materials and parts | 3323 | 14.3 | 17.7 | 0.026 | 22.9 | 81.3 | 7397 | 6 |
| Other fabricated metal | Durable materials and parts | 3325+3329 | 32.5 | 33.4 | 0.026 | 32.1 | 128.6 | 13329 | 6 |
| Instruments and electromedical | Durable final goods | 3345 | 38.9 | 39.5 | 0.026 | 38.3 | 152.2 | 3850 | 6 |
| Iron and steel | Durable materials and parts | 3311+3312 | 45.0 | 52.4 | 0.025 | 37.1 | 154.2 | 2823 | 6 |
| Nonferrous metals | Durable materials and parts | 3313+3314 | 46.2 | 48.0 | 0.025 | 24.7 | 100.4 | 1265 | 6 |
| Asphalt and other petroleum | Nondurable goods | 32412+32419 | 45.0 | 43.3 | 0.024 | 6.7 | 27.6 | 1113 | 6 |
| Paint and adhesives | Nondurable goods | 3255 | 35.5 | 39.9 | 0.023 | 14.5 | 62.6 | 1837 | 6 |
| Forging and stamping | Durable materials and parts | 3321 | 29.8 | 23.9 | 0.021 | 3.0 | 14.8 | 1358 | 4 |
| Glass | Durable materials and parts | 3272 | 49.1 | 53.8 | 0.019 | 5.5 | 29.2 | 1481 | 6 |
| Foundries | Durable materials and parts | 3315 | 40.0 | 41.3 | 0.018 | 4.4 | 24.7 | 1085 | 6 |
| Dairy products | Nondurable goods | 3115 | 37.3 | 37.3 | 0.018 | 11.9 | 68.1 | 809 | 6 |
| Semiconductors and components | Durable materials and parts | 3344 | 38.5 | 40.6 | 0.017 | 51.9 | 298.5 | 3813 | 6 |
| Cut and sew apparel | Nondurable goods | 3152 | 17.5 |  | 0.016 | 4.4 | 26.8 | 6015 | 2 |
| Other electrical equipment | Durable final goods | 3359 | 41.3 | 48.7 | 0.014 | 9.5 | 67.8 | 3707 | 6 |
| Heating and air conditioning | Durable final goods | 3334 | 32.1 | 28.1 | 0.013 | 8.9 | 64.6 | 1699 | 6 |
| Soap and toiletries | Nondurable goods | 3256 | 54.4 | 50.6 | 0.012 | 13.5 | 120.5 | 1517 | 6 |
| Meat and seafood | Nondurable goods | 3116+3117 | 46.9 | 48.1 | 0.011 | 20.7 | 192.0 | 3401 | 6 |
| Rubber products | Nondurable goods | 3262 | 47.5 | 44.7 | 0.009 | 5.7 | 62.7 | 1069 | 5 |
| Ships and boats | Durable final goods | 3366 | 52.9 | 53.5 | 0.005 | 2.7 | 56.0 | 1391 | 5 |
| Apparel accessories | Nondurable goods | 3159 | 28.0 | 19.1 | 0.000 | 0.0 | 2.0 | 1625 | 6 |

## 5. Bulow's two-period model

Source: `results/bulow_model.csv`. Rental demand p = 1 − Q per period, zero cost, no depreciation. The renter sells
the use of 0.5 units in each period at a price of 0.5.

| δ | Renter profit | Seller q1 | Seller p1 | Seller q2 = p2 | Seller profit | Seller ÷ renter |
|---|---|---|---|---|---|---|
| 0.5 | 0.3750 | 0.4444 | 0.6944 | 0.2778 | 0.3472 | 0.926 |
| 0.8 | 0.4500 | 0.4167 | 0.8167 | 0.2917 | 0.4083 | 0.907 |
| 0.9 | 0.4750 | 0.4082 | 0.8582 | 0.2959 | 0.4291 | 0.903 |
| 1.0 | 0.5000 | 0.4000 | 0.9000 | 0.3000 | 0.4500 | 0.900 |

## 6. Giants and the rest, by group (extension)

Source: `results/giants_summary.csv`. Industries whose largest asset class is folded into a lower class or withheld
by the IRS are dropped for that year.

| Cut | Year | Group | Industries | Giants | Giants' share % | Rest's share % | Median gap | Mean gap | Gaps > 0 |
|---|---|---|---|---|---|---|---|---|---|
| $2.5 billion+ | 2007 | Durable final goods | 15 | 144 | 2.235 | 0.093 | 0.126 | 1.081 | 11 |
| $2.5 billion+ | 2007 | Durable materials and parts | 6 | 66 | 0.036 | 0.051 | -0.012 | -0.003 | 3 |
| $2.5 billion+ | 2007 | Nondurable goods | 21 | 168 | 0.147 | 0.049 | 0.038 | 0.213 | 13 |
| $2.5 billion+ | 2012 | Durable final goods | 15 | 162 | 1.589 | 0.091 | 0.105 | 1.125 | 8 |
| $2.5 billion+ | 2012 | Durable materials and parts | 8 | 65 | 0.059 | 0.032 | -0.000 | 0.025 | 4 |
| $2.5 billion+ | 2012 | Nondurable goods | 20 | 167 | 0.071 | 0.045 | -0.007 | 0.078 | 8 |
| $2.5 billion+ | 2013 | Durable final goods | 17 | 173 | 1.510 | 0.083 | 0.011 | 0.960 | 10 |
| $2.5 billion+ | 2013 | Durable materials and parts | 8 | 69 | 0.055 | 0.045 | -0.007 | 0.005 | 3 |
| $2.5 billion+ | 2013 | Nondurable goods | 20 | 178 | 0.069 | 0.042 | -0.001 | 0.077 | 10 |
| $500 million+ | 2007 | Durable final goods | 15 | 416 | 1.922 | 0.042 | 0.198 | 1.052 | 11 |
| $500 million+ | 2007 | Durable materials and parts | 7 | 205 | 0.035 | 0.057 | 0.005 | -0.018 | 4 |
| $500 million+ | 2007 | Nondurable goods | 23 | 414 | 0.140 | 0.037 | 0.029 | 0.194 | 13 |
| $500 million+ | 2012 | Durable final goods | 16 | 434 | 1.386 | 0.033 | 0.141 | 0.994 | 11 |
| $500 million+ | 2012 | Durable materials and parts | 10 | 226 | 0.052 | 0.031 | 0.000 | 0.004 | 5 |
| $500 million+ | 2012 | Nondurable goods | 20 | 407 | 0.051 | 0.036 | -0.003 | 0.014 | 9 |
| $500 million+ | 2013 | Durable final goods | 17 | 461 | 1.312 | 0.036 | 0.086 | 0.919 | 11 |
| $500 million+ | 2013 | Durable materials and parts | 9 | 222 | 0.060 | 0.035 | 0.014 | 0.021 | 5 |
| $500 million+ | 2013 | Nondurable goods | 21 | 430 | 0.051 | 0.034 | -0.001 | 0.014 | 10 |

## 7. Tests of the gap (extension)

Source: `results/giants_regressions.csv`. The regression pools 2007, 2012 and 2013 with year effects coded as
deviations from their average, so the intercept is the nondurable gap averaged over the three years. "Mean gap,
durable final goods" is the intercept plus the durable-final-goods coefficient. For the Wilcoxon rows, the estimate
is the median gap.

| Cut | Test | Term | Estimate | SE | p | N |
|---|---|---|---|---|---|---|
| $2.5 billion+ | gap on group, year effects | Intercept | 0.1233 | 0.1138 | 0.279 | 130 |
| $2.5 billion+ | gap on group, year effects | group[T.final] | 0.9308 | 0.5376 | 0.083 | 130 |
| $2.5 billion+ | gap on group, year effects | group[T.parts] | -0.1086 | 0.1117 | 0.331 | 130 |
| $2.5 billion+ | gap on group, year effects | mean gap, durable final goods | 1.0541 | 0.5252 | 0.045 | 130 |
| $2.5 billion+ | Wilcoxon signed-rank, TY2013 | Durable final goods | 0.0112 |  | 0.159 | 17 |
| $2.5 billion+ | Wilcoxon signed-rank, TY2013 | Nondurable goods | -0.0006 |  | 0.674 | 20 |
| $2.5 billion+ | Wilcoxon signed-rank, TY2013 | Durable materials and parts | -0.0066 |  | 0.945 | 8 |
| $500 million+ | gap on group, year effects | Intercept | 0.0758 | 0.0548 | 0.166 | 138 |
| $500 million+ | gap on group, year effects | group[T.final] | 0.9124 | 0.4674 | 0.051 | 138 |
| $500 million+ | gap on group, year effects | group[T.parts] | -0.0650 | 0.0524 | 0.215 | 138 |
| $500 million+ | gap on group, year effects | mean gap, durable final goods | 0.9882 | 0.4632 | 0.033 | 138 |
| $500 million+ | Wilcoxon signed-rank, TY2013 | Durable final goods | 0.0863 |  | 0.007 | 17 |
| $500 million+ | Wilcoxon signed-rank, TY2013 | Nondurable goods | -0.0014 |  | 0.338 | 21 |
| $500 million+ | Wilcoxon signed-rank, TY2013 | Durable materials and parts | 0.0144 |  | 0.359 | 9 |

## 8. Giants and the rest by industry, tax year 2013

Source: `results/giants_industries.csv` (all three years are in the file).

| Industry | Group | Giants | Rest | Giants' assets $bn | Giants' rents $mn | Giants' share % | Rest's share % | Gap |
|---|---|---|---|---|---|---|---|---|
| Lighting and household appliances | final | 7 | 1453 | 854.6 | 7535.3 | 6.312 | 0.018 | 6.294 |
| Commercial and service machinery | final | 4 | 2296 | 42.6 | 1382.1 | 5.754 | 0.106 | 5.647 |
| Motor vehicles and parts | final | 25 | 4202 | 815.4 | 11678.0 | 2.145 | 0.054 | 2.091 |
| Tobacco | nondur | 4 | 20 | 56.5 | 634.8 | 1.404 | 0.000 | 1.404 |
| Farm, construction and mining machinery | final | 14 | 3466 | 282.2 | 1715.0 | 1.272 | 0.064 | 1.209 |
| Computers and peripherals | final | 11 | 1190 | 343.6 | 1730.9 | 0.920 | 0.047 | 0.873 |
| Engines and turbines | final | 7 | 228 | 66.0 | 297.9 | 0.685 | 0.006 | 0.679 |
| Aerospace | final | 22 | 1290 | 414.8 | 573.8 | 0.192 | 0.046 | 0.146 |
| Animal food and grain milling | nondur | 5 | 1872 | 82.5 | 138.8 | 0.141 | 0.010 | 0.131 |
| Nonferrous metals | parts | 4 | 1072 | 139.4 | 39.4 | 0.141 | 0.013 | 0.128 |
| Electrical equipment | final | 4 | 1340 | 88.9 | 37.2 | 0.095 | 0.027 | 0.068 |
| Other food | nondur | 6 | 2498 | 504.0 | 116.8 | 0.102 | 0.043 | 0.058 |
| Soft drinks and ice | nondur | 3 | 188 | 56.9 | 40.7 | 0.127 | 0.075 | 0.051 |
| Bakeries and tortillas | nondur | 3 | 3090 | 10.7 | 7.2 | 0.053 | 0.016 | 0.037 |
| Glass | parts | 4 | 1583 | 46.8 | 6.6 | 0.052 | 0.021 | 0.031 |
| Iron and steel | parts | 15 | 938 | 93.7 | 57.3 | 0.065 | 0.035 | 0.031 |
| Pharmaceuticals | nondur | 40 | 1470 | 1205.9 | 174.6 | 0.055 | 0.031 | 0.025 |
| Other miscellaneous manufacturing | final | 4 | 16472 | 26.9 | 6.9 | 0.062 | 0.051 | 0.011 |
| Audio and video equipment | final | 3 | 288 | 50.1 | 4.0 | 0.023 | 0.014 | 0.008 |
| Paint and adhesives | nondur | 6 | 1622 | 32.5 | 10.1 | 0.034 | 0.026 | 0.007 |
| Resins and synthetic fibers | nondur | 7 | 436 | 97.0 | 24.4 | 0.055 | 0.049 | 0.006 |
| Pulp and paper mills | nondur | 5 | 304 | 86.3 | 8.9 | 0.024 | 0.023 | 0.001 |
| Basic chemicals | nondur | 25 | 460 | 362.8 | 184.7 | 0.115 | 0.115 | 0.000 |
| Soap and toiletries | nondur | 11 | 1989 | 297.8 | 18.9 | 0.025 | 0.027 | -0.001 |
| Fruit and vegetable preserving | nondur | 6 | 410 | 107.3 | 7.5 | 0.034 | 0.036 | -0.002 |
| Wineries and distilleries | nondur | 5 | 1663 | 45.9 | 4.7 | 0.022 | 0.025 | -0.003 |
| Other fabricated metal | parts | 7 | 13254 | 233.8 | 3.6 | 0.012 | 0.017 | -0.004 |
| Semiconductors and components | parts | 22 | 4237 | 241.4 | 31.6 | 0.024 | 0.032 | -0.009 |
| Rubber products | nondur | 5 | 1469 | 30.9 | 6.5 | 0.017 | 0.026 | -0.010 |
| Other chemicals | nondur | 7 | 1706 | 53.7 | 4.8 | 0.014 | 0.026 | -0.012 |
| Boilers and tanks | parts | 5 | 1400 | 18.8 | 4.4 | 0.031 | 0.050 | -0.019 |
| Meat and seafood | nondur | 6 | 3553 | 39.9 | 11.9 | 0.018 | 0.038 | -0.019 |
| Plastics products | nondur | 3 | 7671 | 18.0 | 0.5 | 0.005 | 0.027 | -0.022 |
| Other electrical equipment | final | 4 | 3472 | 54.7 | 0.0 | 0.000 | 0.025 | -0.025 |
| Furniture | final | 4 | 8864 | 13.7 | 0.8 | 0.008 | 0.035 | -0.028 |
| Heating and air conditioning | final | 3 | 1005 | 12.7 | 0.3 | 0.006 | 0.035 | -0.028 |
| Hardware, springs, machine shops | parts | 5 | 17238 | 51.8 | 0.3 | 0.003 | 0.031 | -0.029 |
| Petroleum refineries | nondur | 20 | 184 | 2460.3 | 865.6 | 0.042 | 0.076 | -0.034 |
| Dairy products | nondur | 3 | 1186 | 8.7 | 2.7 | 0.015 | 0.052 | -0.036 |
| Converted paper | nondur | 8 | 2226 | 112.3 | 5.5 | 0.010 | 0.057 | -0.046 |
| Medical equipment and supplies | final | 21 | 8260 | 162.1 | 25.9 | 0.036 | 0.086 | -0.051 |
| Cement and concrete | parts | 7 | 3504 | 67.0 | 45.2 | 0.177 | 0.267 | -0.090 |
| Instruments and electromedical | final | 21 | 4502 | 250.7 | 30.5 | 0.049 | 0.147 | -0.098 |
| Communications equipment | final | 8 | 398 | 69.3 | 17.0 | 0.042 | 0.151 | -0.109 |
| Other general machinery | final | 11 | 3847 | 86.1 | 2.3 | 0.008 | 0.372 | -0.365 |

