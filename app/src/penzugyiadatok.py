import yfinance as yf
import pandas as pd

# Cégek listája
companies = [ 
    "AMZN", "MCD", "YUM", "SBUX", "NESN.SW", "UL", "PG", "KO", "PEP", "HEIA.AS", "DEO", 
    "CARL-B.CO", "IBM", "ACN", "CTSH", "TCS.NS", "CAP.PA", "G", "WIT", "INFY", 
    "HCLTECH.NS", "DXC", "SAP", "ORCL", "MSFT", "NOW", "SIEGY", "IT", "SHEL", "BP", "TSCO.L"
]

# Évek, amelyekre az adatokat kérjük
years = ["2021", "2022", "2023", "2024"]

def get_financial_data():

    # Adatok tárolására
    results = []

    for company in companies:
        try:
            ticker = yf.Ticker(company)
            financials = ticker.financials
            
            for year in years:
                if year in financials.columns:
                    total_revenue = financials.loc["Total Revenue", year] if "Total Revenue" in financials.index else None
                    gross_profit = financials.loc["Gross Profit", year] if "Gross Profit" in financials.index else None
                    
                    results.append({
                        "Company": company,
                        "Year": year,
                        "Total Revenue": total_revenue,
                        "Gross Profit": gross_profit
                    })
        except Exception as e:
            print(f"Error fetching data for {company}: {e}")

    return results
    # Adatok DataFrame-be
    #df = pd.DataFrame(results)
    #print(df)

    # Mentés CSV-be
    #df.to_csv("financial_data.csv", index=False)
