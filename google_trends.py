
import pandas as pd                        
from pytrends.request import TrendReq


pytrends = TrendReq()
suggs = pytrends.suggestions("ALDI")
print(suggs[1]['mid'])

pytrends.build_payload([suggs[1]['mid']], cat=0, timeframe="today 3-m", geo="")
  
related_queries = pytrends.related_queries()
interest_over_time = pytrends.interest_over_time()
related_topics = pytrends.related_topics()
  
trend_analysis = pytrends.related_topics()
trend_analysis.get("cruises").get("rising")




