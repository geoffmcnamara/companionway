+++
date = "2021-06-28 14:00:00"
draft = true
title = "Python's all() function"
# image = ""
tags = ["python","financial"]
comments = true
share = true
+++


## Python all() function ##

Much of my coding efforts are directed towards analyzing financial data specifically targeting potential cash secured puts or covered calls. Recently, I had to refine some market overview displays. I needed a listing of the current market "gainers" and market "losers". There is one site which I scrape using panda read_html function to grab a hadful of tables. My problem arises from two factors. One is there are no labels or titles to the tables and they can vary. The a table can arise from special (temporart) events and the weekends or holidays might call for the tables to re-arrange their order. This requires that I look directly at the panda table and derive which table I might be examining. One table I look for lists all the "gainers" currenly in the market. What I do know is that the third column of that table will always contain a plus sign (the % change of all the gainers). I had nested loops initially to do this but I refactored the code to use the "all()" function to discover which table has all "+" signs in the column 3. My standard caveat applies here - there is likely a better way to do this - so let me know.  

'''python 
import pandas as pd
import requests


def get_html_tables(url, timeout=4):
  content = requests.get(url).content
  tables = pd.read_html(content)
  return tables


tables = get_html_tables("/my/url")
for table in tables:
  for x in range(6):
    val = table.iloc[x, 3]
    vals.append(val)
  all_gainers_b = all(["+" in str(v) for v in vals])
  if all_gainers_b:
    gainers_table = table

'''

