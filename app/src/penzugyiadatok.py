import yfinance as yf
import pandas as pd
import numpy as np
# Évek, amelyekre az adatokat kérjük
years = ["2021", "2022", "2023", "2024"]

companies = {
    "Amazon": "AMZN",
    "McDonald’s": "MCD",
    "KFC": "YUM",
    "Starbucks": "SBUX",
    "Nestlé": "NESN.SW",
    "Unilever": "UL",
    "Procter & Gamble": "PG",
    "Coca-Cola": "KO",
    "PepsiCo": "PEP",
    "Heineken": "HEIA.AS",
    "Diageo": "DEO",
    "Carlsberg": "CARL-B.CO",
    "IBM": "IBM",
    "Accenture": "ACN",
    "Cognizant": "CTSH",
    "Tata Consultancy Services": "TCS.NS",
    "Capgemini": "CAP.PA",
    "Genpact": "G",
    "Deloitte": "",
    "PWC": "",
    "EY": "",
    "KPMG": "",
    "Wipro": "WIT",
    "Infosys": "INFY",
    "HCL Technologies": "HCLTECH.NS",
    "DXC Technologies": "DXC",
    "SAP": "SAP",
    "Oracle": "ORCL",
    "Microsoft": "MSFT",
    "ServiceNow, Inc.": "NOW",
    "Siemens": "SIEGY",
    "Market Research Future": "",
    "SSON": "",
    "ThinkHDI": "",
    "Wired": "",
    "Service Desk Institue": "",
    "Gartner,": "IT",
    "IKEA": "",
    "Shell": "SHEL",
    "BP": "BP",
    "Tesco": "TSCO.L", 
    "Auchan": "",
    "Lidl": "",
    "Spar": "",
}



def get_financial_data(company_name):
    company = companies[company_name]
    ticker = yf.Ticker(company)
    financials = ticker.financials
    total_revenue_list, gross_profit_list, profit_rate_list = [], [], []        

    for date in financials.columns:
        year_str = str(date.year)

        if year_str in years:
            total_revenue = financials.loc["Total Revenue", date] if "Total Revenue" in financials.index else np.nan
            total_revenue_list.append(total_revenue)
            gross_profit = financials.loc["Gross Profit", date] if "Gross Profit" in financials.index else np.nan
            #gross_profit = gross_profit.iloc[0]
            gross_profit_list.append(gross_profit)
            profit_rate = round(gross_profit / total_revenue * 100, 2)
            profit_rate_list.append(profit_rate)
       
        
    return total_revenue_list, gross_profit_list, profit_rate_list

