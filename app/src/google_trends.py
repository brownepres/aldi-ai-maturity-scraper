
import pandas as pd                        
from pytrends.request import TrendReq

#Companies = pd.read_excel('Céglista.xlsx')
#Companies['Cég neve + AI'] = Companies['Cég neve'] + ' AI'
#Companies = Companies[['Cég neve','Cég neve + AI']]

def get_trends():
    # ALDI
    pytrends = TrendReq()
    suggs = pytrends.suggestions("ALDI")
    print(suggs)
    
    pytrends.build_payload([suggs[1]['mid']], cat=0, timeframe="today 1-m", geo="")
    ALDI = pytrends.interest_over_time()
    
    pytrends.build_payload(["Aldi AI"], cat=0, timeframe="today 1-m", geo="")
    ALDI_AI = pytrends.interest_over_time()


    return ALDI, ALDI_AI

# Other companies
"""
for company in Companies['Cég neve']:
    pytrends.build_payload([company], cat=0, timeframe="today 1-m", geo="")
    trend_data[company] = pytrends.interest_over_time()
    
for companyAI in Companies['Cég neve + AI']:
    pytrends.build_payload([companyAI], cat=0, timeframe="today 1-m", geo="")
    trend_AI_data[companyAI] = pytrends.interest_over_time()
"""



