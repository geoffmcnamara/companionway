+++
author = ""
comments = false
date = "2016-12-10T20:38:12-05:00"
draft = false
image = "/img/chrome-frame-n-ball.jpg"
share = true
tags = ["xargs", "sed"]
title = "Recursively Replace Text"

+++

Recently I had to do a find and replace text on multiple files recursively. I had to look up how to do it to remind myself of the exact syntax. If I had to look it up, you have to suffer seeing it in my blog post... [smile]

```
find ./ -name \*.md -print0 | xargs -0 sed -i 's/header-img/img/'
```

Be careful here. I used the -0 option to deal with any filename that have spaces in the name BUT it really requires that the find command contain the -print0 option otherwise things will not operate in the manner expected.
 
<!--more-->

Enjoy
-g-
