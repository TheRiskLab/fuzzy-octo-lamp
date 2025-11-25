# fuzzy-octo-lamp
Leveraged_ETF_Simulator
Glossary(super simple, skip if familiar):
Leveraged ETF — A fund that tries to give 2× or 3× the DAILY return of an index.
TQQQ — A 3× leveraged version of the NASDAQ-100.
Rebalancing — Putting your money back into the same percentages you chose at the start.
Weights — What percent you put into each asset.
Rolling returns — Checking returns for every possible start month, not just one.
________________________________________
What This Program Does
This project simulates how a portfolio behaves when you mix a leveraged ETF (synthetic TQQQ) with the regular NASDAQ-100 index.
It downloads daily NASDAQ-100 data, builds synthetic leveraged data from that NASDAQ data, then it convers it into monthly factors, and applies different combinations of weights. It then rebalances the portfolio for an amount of months that can be input, and then calculates returns for one year, three year, five year and ten year intervals, and outputs basic statistics of the results – max drawdown, highest return, average return for each interval, and percentiles of returns.
The goal of this project is to have data to help analyze and find the optimal amount of TQQQ to hold, how often to rebalance, and what weights to use. There is no objective answer – there is no “best” – but, there are amounts that are better than others in all categories. For example, rebalancing every month underperforms rebalancing every other month.
The practical use of this is obvious. I would like to construct a portfolio of the optimal amount of each, and rebalance when needed.
This is my first project, and I am really excited about the possibilties and where this can go.

The code is as follows: Firstly, it imports the nessecary libraries: yfinance (for importing financial data), pandas (for making dfs and doing calculations on them), and numpy (for the line of .prod in rolling).
Then, the weights are set with a variable - the weights are set at (1,0) to (0,1), in .1 increments.
Function "get_data" downloads the data, makes dataframes (a table used to hold data and perform fast calculations on it; a pandas object), and calcualtes the monthly return for both the regular NASDAQ 100 and the leveraged.
Fuction "calculate_balance" then calculates the monthly return for the weighted portfolio. The eqaution is simple - the monthly (when the rebalancing is monthly) return of normal NASDAQ times the weight of the normal NASDAQ, plus the monthly return of the leveraged ETF times the weight of it. The function returns monthly returns for the weighted version. It operates on a for loop, so it calls the retunrs for al the given weights, and returns many sets of returns, each for a different weight.
Function "rolling_returns" takes the data of the function "calculate_balance", and creates the compounded returns of them for intervals of 12 months, 36, 72 and 120 (1, 3,5, and 10 years, respectively).
The code after that calls the functions, creates a description of the retults, and saves it to a file.

Several things I learned while making this project: Firstly, the pandas library was a great help, and made things way easier than they would have been. Also, I shouldv'e had a clearer picture of how I wanted this to look when I started. Each rewrite and change takes a long time, and then there's bugs...


                                                                _________technical specs and issues________
1) The leverage factor for the ETF was set at 2.9269, which was set by using a simple regression (made by chatgpt). There are several issues. Firstly, the levergae factor is not static, and the regression and input I did does not capture that. Also, the sample size was small - only ten years - and therefore may not capture future amounts.
2) To invest in the NASDAQ 100, there are usuually small fees - around .2 percent. This model does not reflect those fees. While this is not a big deal, it is possible that this significantly changes the eqaution, as I attempt to show the best amount of weights - deciding between .2 or .3, for example; and a difference of .2 percent annualy, combined with the issue discussed about the leverage factor, could affect this.
3) Data was ran from 1985-10-01 to 2025-10-01. This was done because the data started only in 85. While forty years may seem like a lot, the NASDAQ has had extremtly high returns for that period, and the future may not reflect this. Therefore, all results are dependent on this.
4) The code did not run the different rebalancing periods inside the script - it needs to be adjusted mannualy. A fuller, better version of this code would have a "for loop" for this.
5) I intended to make a monto-carlo simulation to run the different possible outcomes. However, due to time constraints, it was not feasible. A good simulation would need to find the corolation in periods and calculate from that. I made a simple monto-carlo, which just takes the monthly returns and randomly creates new periods. In the simulation, there were zero negative 10 year periods! This shows the amount of corolation that there is, and how the monto-carlo would need to reflect it.

It is important to remember that this is my first finance tool, and, while it has some use, it is not a complete product, and it is only as good as its inputs. It should not be used for financial desicions.
                                                       ----------------------Further Research``--------------------
Further research should be done on this topic, including finding the optimal rebalancing technique, which should be based on violity as opposed to historic max drawdowns and std. In addition, the leverage rate should be dynamic, and not set as one number throughout.
In addition, the historical returns may not reflect future returns, as the past 40 years have been a strong bull market in tech, and does not signify the future.




