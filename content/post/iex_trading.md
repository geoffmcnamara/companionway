+++
date = 2019-05-16T13:22:24-04:00
draft = true
title = "Using python to grab stock info from iextrading"
slug = ""
tags = []
image = ""          # /img/name.ext
comments = true     # set false to hide Disqus
share = true        # set false to hide share buttons
# menu= ""          # set "main" to add this content to the main menu
author = "Name"
+++

I am a conservative options trader. I limit myself to trading only cash secured puts (CSP) and stock secured calls. Just for reference
I only sell my options for at least 1% of the value of my secured investment and for a period of between 20-40 days. But I do agood deal
of homework before making a trade. I gather current information from the free data site <https://iextrading.com>. You can even gather most information without an API key.

I wrote a python module for myself that allows quick access to stock data for the iextrading site.

As a quick example:

```python
import requests
import json

def get_pr(sym):
    base_url = "https://api.iextrading.com/1.0"
    query = f"/stock/{sym}/price"
    qurl = f"{base_url}/{query}"
    try:
      r = requests.get(qurl)
    except Exception as ex:
      print(f"Failed to retrieve data for {sym} - received error: {ex}")
      return False
    return r

r = get_pr(sym)
print(r)
```
 
