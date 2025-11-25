import yfinance as yf
import pandas as pd
import numpy as np

weight_list = [
    (1.0, 0.0), (0.9, 0.1), (0.8, 0.2), 
    (0.7, 0.3), (0.6, 0.4),(0.5, 0.5), 
    (0.4, 0.6), (0.3, 0.7), (0.2, 0.8), 
    (0.1, 0.9), (0.0, 1.0)
]

def get_data():   ###downloads the data and makes two dfs, one for leverage and one regular
    df = yf.download("^NDX", start="1985-10-01", end="2025-10-01", auto_adjust=True)
    df["r"] = df["Close"].pct_change()
    df["lev_d"] = df["r"] * 2.9269

    mnorm = df.groupby(pd.Grouper(freq="ME")).apply(
        lambda x: (1 + x["r"]).prod() - 1
    ).to_frame("norm_m")

    mlev = df.groupby(pd.Grouper(freq="ME")).apply(
        lambda x: (1 + x["lev_d"]).prod() - 1
    ).to_frame("lev_m")

    return pd.concat([mlev, mnorm], axis=1).dropna()   ###groups both dfs into one

def calculate_balance(joined_df, weight_list, rebalance_every_n_months):   ###creates the balanced returns of wl and wn; which could then be compounded monthly for final returns.
    lev = joined_df["lev_m"].values
    nor = joined_df["norm_m"].values
    n = len(joined_df)
    out = {}

    for wl, wn in weight_list:
        lev_val = wl
        nor_val = wn
        port_val = lev_val + nor_val
        monthly_factors = []

        for i in range(n):
            port_before = lev_val + nor_val
            lev_val *= (1 + lev[i])
            nor_val *= (1 + nor[i])
            port_after = lev_val + nor_val
            factor = port_after / port_before
            monthly_factors.append(factor)

            if (i + 1) % rebalance_every_n_months == 0:
                port_val = lev_val + nor_val
                lev_val = port_val * wl
                nor_val = port_val * wn

        out[(wl, wn)] = monthly_factors

    df_out = pd.DataFrame(out)
    df_out.columns = [f"leverage_{w[0]}_normal_{w[1]}" for w in weight_list]
    return df_out

def rolling_returns(df, windows):   ###this takes the values from balanced and rolls them for the desired timeline.
    out = {}
    for col in df.columns:
        d = pd.DataFrame({"balanced_growth": df[col]})
        for w in windows:
            d[f"rolling_{w//12}y"] = d["balanced_growth"].rolling(w).apply(
                np.prod, raw=True
            ) - 1
        out[col] = d
    return out

joined_df = get_data()
rebalancing_period = 18
balanced_df = calculate_balance(joined_df, weight_list, rebalancing_period)
outputs = rolling_returns(balanced_df, windows=[12, 36, 60, 120])
with open(f"rebalancing_for_18_months.txt", "w") as f:  ###writes the results to a text doc.
    for col, df in outputs.items():
        f.write(f"==== {col} ====\n")
        f.write(df.describe().to_string())
        f.write("\n\n")

