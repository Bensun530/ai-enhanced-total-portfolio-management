# AI Enhanced Total Portfolio Management

## Objective

This project builds a Python based total portfolio management framework that combines strategic asset allocation, dynamic rebalancing, credit market signals, AI infrastructure exposure, stress testing, and AI generated CIO style commentary.

The goal is not to predict short term market returns. The goal is to evaluate how a total portfolio behaves across different market regimes and how risk exposure should be adjusted when credit, equity, and volatility signals change.

## Core Investment Question

Can a dynamic total portfolio framework improve risk adjusted performance and downside control compared with a static benchmark portfolio?

## Project Hypothesis

Credit markets can provide useful early warning signals for total portfolio risk.

When high yield credit weakens relative to investment grade credit, the portfolio may need to reduce risk exposure before equity market drawdowns fully materialize.

The project uses HYG versus LQD, equity trend, and rolling volatility as the first version of the dynamic rebalancing signals.

## Portfolio Framework

The portfolio starts from a strategic asset allocation across equity, credit, Treasury duration, cash, gold, real estate, and AI infrastructure.

A monthly rebalancing process adjusts the portfolio based on market regime:

1. Risk On
2. Credit Warning
3. Risk Off
4. Recovery

The dynamic strategy is compared against a static benchmark portfolio.

## AI Layer

AI is used as a structured interpretation and reporting layer.

Python calculates portfolio returns, risk metrics, correlations, drawdowns, regime signals, and stress test results.

AI converts these structured outputs into CIO style commentary, including portfolio risk assessment, allocation recommendation, and key watchlist items.

AI is not used as an unconstrained return prediction model.

## Expected Outputs

1. Clean asset price and return dataset
2. Asset level risk and return analysis
3. Static portfolio benchmark
4. Dynamic total portfolio strategy
5. Credit signal regime classification
6. AI infrastructure sleeve analysis
7. Stress test results
8. Final CIO style investment memo