# Asset Universe

## Purpose

The asset universe is designed to represent the major building blocks of a total portfolio.

Each asset is selected because it has a specific economic role in portfolio construction. The goal is not to pick random ETFs, but to define clear portfolio sleeves.

## Initial ETF Proxies

| Sleeve | Ticker | Role |
|---|---:|---|
| US Equity | SPY | Core growth exposure |
| Global Equity | ACWI | Global diversified equity exposure |
| Investment Grade Credit | LQD | Defensive credit and income |
| High Yield Credit | HYG | Credit beta and risk appetite signal |
| Treasury Duration | TLT | Defensive duration and risk off hedge |
| Gold | GLD | Crisis hedge and alternative store of value |
| Real Estate | VNQ | Real asset exposure and rate sensitive income |
| AI Infrastructure | SMH | Semiconductor and AI infrastructure growth sleeve |
| Technology | XLK | Broad technology exposure |
| Cash | 3 Month Treasury Bill | Liquidity buffer and defensive allocation |

## Key Portfolio Roles

Equity is the primary growth engine.

Investment grade credit provides income and lower risk credit exposure.

High yield credit is both an asset class and a market risk signal.

Treasury duration is used as a defensive asset during risk off environments.

Gold is included as a crisis hedge.

Real estate represents real asset exposure but is sensitive to rates.

AI infrastructure is treated as a thematic growth sleeve. It may improve upside potential, but it can also increase equity beta, valuation risk, concentration risk, and drawdown risk.

Cash provides liquidity and reduces portfolio volatility.

## First Version Universe

The first working version will use:

| Asset | Ticker |
|---|---:|
| US Equity | SPY |
| Investment Grade Credit | LQD |
| High Yield Credit | HYG |
| Treasury Duration | TLT |
| Gold | GLD |
| AI Infrastructure | SMH |
| Cash | 3 Month Treasury Bill |

This smaller universe keeps the first version clean and easier to debug.

After the first version works, the project can add ACWI, VNQ, XLK, QQQ, GRID, and other thematic exposures.