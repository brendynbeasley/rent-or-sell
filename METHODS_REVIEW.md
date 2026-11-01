# Methods review: Bulow (1982), "Durable-Goods Monopolists"

Jeremy I. Bulow, "Durable-Goods Monopolists," *Journal of Political Economy* 90(2), April 1982, pp. 314–332.

**What this review is based on.** The full text sits behind the publisher's paywall and was not read for this review.
The review draws on the paper's published abstract (as indexed by OpenAlex for DOI 10.1086/261058), on a set of
graduate lecture notes that reproduce the paper's two-period linear model step by step (posted on the Southern
Methodist University economics faculty site), and on the bibliographic record. Statements below about specific
pages, propositions or equation numbers are therefore not made. Every claim attributed to the paper comes from the
abstract or from the model as the lecture notes reproduce it. The model values in this repository
(`results/bulow_model.csv`) were recomputed from that textbook version. They are not an independent reproduction of
the paper's own results, which this review did not see.

## Methods summary

The paper is a theoretical analysis of a monopolist producing a durable good. In the version reproduced in teaching
notes, there are two periods, the good lasts both periods without depreciation and becomes worthless afterward,
production cost is zero, and a continuum of consumers values one period of use according to the linear demand
p = 1 − Q, where Q is the stock in use. The monopolist either rents the good period by period or sells it, and a
seller cannot commit in the first period to its second-period output. The equilibrium is found by backward induction.
The abstract reports four results, that a monopolist who rents (or can make binding promises about future output)
avoids the problems a seller faces because of the second-hand market; that a seller unable to rent produces goods
less durable than competitive firms or monopolist renters; that sellers may invest less in fixed costs, including
plant modernization and research and development, than renters (a reverse Averch-Johnson result); and that although
sellers have less monopoly power than renters, they can cause a greater deadweight loss.

Research design is formal modeling. Sampling strategy, sample size, inclusion and exclusion criteria, missing data
treatment, confidence intervals and p-values do not apply, because the paper estimates nothing from data. Its
"independent variables" are the model's primitives (the discount factor, the demand curve, durability and the
contracting regime, renting or selling), and its "dependent variables" are equilibrium output, prices, profit,
chosen durability, investment and deadweight loss. Its "statistics" are closed-form equilibrium values and
comparisons between regimes.

## Statistics extraction table

| Statistic | Value and unit | Source location | What it measures | What it does not establish |
|---|---|---|---|---|
| Renter's discounted profit | (1 + δ)/4, model units; 0.50 at δ = 1 | Two-period linear model as reproduced in lecture notes; not located in the paper's pages for this review | Profit of a monopolist renting at the monopoly rental price 1/2 in each period | That real firms face linear demand, zero cost or two periods |
| Seller's first-period sales | q₁* = 2/(4 + δ); 0.40 at δ = 1 | Same | Output a seller chooses when buyers anticipate the second-period price | Any empirical quantity |
| Seller's first-period price | (2 + δ)²/(2(4 + δ)); 0.90 at δ = 1 | Same | Price the marginal first-period buyer will pay, given the expected second-period price | That a seller with commitment would choose it (it would charge (1 + δ)/2) |
| Seller's second-period output and price | q₂* = p₂* = (1 − q₁)/2; 0.30 at δ = 1 | Same | Second-period best response once first-period units are in the market | Behavior over more than two periods |
| Seller's discounted profit | (2 + δ)²/(4(4 + δ)); 0.45 at δ = 1 | Same | Profit when the seller cannot commit | The size of the loss for real goods, which depends on demand, durability and the frequency of price changes |
| Seller-to-renter profit ratio | 0.90 at δ = 1 (computed here; 0.926 at δ = 0.5) | Derived from the two rows above | How much of the renter's profit a seller keeps in this example | That firms that rent are more profitable in practice, or that renting is always feasible |
| Durability result | Qualitative, sellers choose durability below that of competitive firms or renters | Abstract | Direction of the incentive to shorten product life | How large the reduction is, or that observed product lives are shorter for this reason |
| Investment result | Qualitative, sellers may invest less in fixed costs and R&D than renters | Abstract ("reverse Averch-Johnson") | Direction of the investment incentive | Any measured investment gap |
| Deadweight loss result | Qualitative, a seller may cause greater deadweight loss than a renter or a nondurable monopolist | Abstract | Possibility, not a general ranking | Which regime is worse in any specific market |

## Interpretation notes

- The central result is a comparison of regimes within one model. It shows that the inability to commit costs a
  durable-goods monopolist money and that renting removes that cost. It does not show that firms which rent are
  observed to earn more, because firms choose whether to rent, and the ones that can rent may differ in other ways.
- The two-period linear example is the standard teaching version. The paper's general results are stated in the
  abstract in qualitative terms. The 0.45 versus 0.50 comparison should be read as an illustration of the direction
  and rough size of the effect under the simplest assumptions, not as an estimate.
- The durability and investment results depend on the seller being unable to rent or to commit. Where leasing,
  buy-back promises or reputation are available, the model predicts these distortions shrink.
- The model has no costs of renting. Moral hazard by renters, the cost of remarketing returned goods, and adverse
  selection among those who choose to lease are outside the model, and later literature (for example, Waldman's 2003
  survey in the *Journal of Economic Perspectives*) treats them as central to real leasing markets.
- A testable implication used in this repository is that renting should be concentrated where durability and market
  power coincide. That implication is an inference from the model, not a test the paper itself proposed.

## Unanswered questions

- How sensitive is the seller-renter profit gap to depreciation, to more than two periods and to costly production,
  in the paper's own general treatment, which this review did not read?
- Under what conditions does the paper's durability result hold when the seller can choose durability and price
  jointly over many periods, as in Bulow's 1986 *Quarterly Journal of Economics* paper on planned obsolescence?
- How does the analysis change with oligopoly, where one firm's leasing does not commit its rivals?
- What share of observed manufacturer leasing reflects commitment, as opposed to finance, tax treatment or
  information about used goods? The paper does not address measurement, and the data in this repository cannot
  separate these motives.

## Items requiring expert verification

- The exact statement, page and numbering of each proposition, and whether the paper presents the linear example
  with the same normalization (p = 1 − Q, zero cost) that the lecture notes use.
- Whether the paper's durability result is stated relative to competitive firms, renters or both in all cases, beyond
  the abstract's wording.
- The precise conditions for the reverse Averch-Johnson result and for the deadweight-loss ranking.
- Whether the paper discusses leasing in antitrust cases such as United Shoe Machinery directly, or whether that
  connection was drawn by later readers.
- No published correction or formal comment identifying an analytical error in the paper was found in the sources
  consulted. That is a statement about the search, not a finding that none exists.
