import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cégek listája
companies = [ 
    "AMZN", "MCD", "YUM", "SBUX", "NESN.SW", "UL", "PG", "KO", "PEP", "HEIA.AS", "DEO", 
    "CARL-B.CO", "IBM", "ACN", "CTSH", "TCS.NS", "CAP.PA", "G", "WIT", "INFY", 
    "HCLTECH.NS", "DXC", "SAP", "ORCL", "MSFT", "NOW", "SIEGY", "IT", "SHEL", "BP", "TSCO.L"
]

# Évek, amelyekre az adatokat kérjük
years = ["2021", "2022", "2023", "2024"]

def get_financial_data():
    results = []

    for company in companies:
        try:
            ticker = yf.Ticker(company)
            financials = ticker.financials

            for date in financials.columns:
                year_str = str(date.year)

                if year_str in years:
                    total_revenue = (
                        financials.loc["Total Revenue", date]
                        if "Total Revenue" in financials.index else None
                    )
                    gross_profit = (
                        financials.loc["Gross Profit", date]
                        if "Gross Profit" in financials.index else None
                    )

                    results.append({
                        "Company": company,
                        "Year": year_str,
                        "Total Revenue": total_revenue,
                        "Gross Profit": gross_profit
                    })

        except Exception as e:
            print(f"Error fetching data for {company}: {e}")

    # Adatok DataFrame-be
    df = pd.DataFrame(results)

    # Profitráta számítása
    df["Profit Rate (%)"] = df.apply(
        lambda row: round((row["Gross Profit"] / row["Total Revenue"]) * 100, 2)
        if row["Gross Profit"] not in [None, 0] and row["Total Revenue"] not in [None, 0]
        else None,
        axis=1
    )

    # Betöltjük a tickerekhez tartozó cégneveket
    try:
        ticker_df = pd.read_excel("Yahoo finance tickerek.xlsx")

        if "Ticker" in ticker_df.columns and "Cég neve" in ticker_df.columns:
            ticker_df = ticker_df.rename(columns={"Cég neve": "Company name"})
            merged_df = pd.merge(
                df,
                ticker_df[["Ticker", "Company name"]],
                how="left",
                left_on="Company",
                right_on="Ticker"
            )
            merged_df.drop(columns=["Ticker"], inplace=True)

            # Oszlopok sorrendjének rendezése
            cols = merged_df.columns.tolist()
            new_order = ["Company", "Company name"] + [col for col in cols if col not in ["Company", "Company name"]]
            merged_df = merged_df[new_order]
        else:
            print("Hiba: A 'Yahoo finance tickerek.xlsx' fájl nem tartalmazza a szükséges oszlopokat.")
            merged_df = df
    except FileNotFoundError:
        print("Hiba: A 'Yahoo finance tickerek.xlsx' fájl nem található.")
        merged_df = df

    return merged_df

# Lekérjük az adatokat
merged_df = get_financial_data()

# demo2.xlsx betöltése és merge AI buzz score alapján
try:
    demo_df = pd.read_excel("demo2.xlsx")

    if "Company" in demo_df.columns and "AI buzz score" in demo_df.columns:
        demo_df = demo_df.rename(columns={"Company": "Company name"})
        merged_full = pd.merge(merged_df, demo_df[["Company name", "AI buzz score"]], on="Company name", how="left")
    else:
        print("Hiba: A 'demo2.xlsx' nem tartalmazza a szükséges oszlopokat.")
        merged_full = merged_df
except FileNotFoundError:
    print("Hiba: A 'demo2.xlsx' fájl nem található.")
    merged_full = merged_df

# Eredmény mentése Excel fájlba
merged_full.to_excel("financial_data_with_buzz.xlsx", index=False)

