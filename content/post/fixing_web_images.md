+++
date = "2021-07-17T19:46:42-04:00"
draft = false
title = "Fixing_web_images"
slug = ""
tags = []
image = ""
comments = false	# set false to hide Disqus
share = false	# set false to hide share buttons
#menu= ""		# set "main" to add this content to the main menu
author = ""
+++

# Quick Fix for Web images

The tool of choice is mogrify which come from the imagemagic package on your linux platform.

I had one image that looked fine when I displayed it using display tools in linux but when placed into a webpage the image would be reversed.

I tried using css style transform: auto-orient; but all attempts failed. My css files are complicated to the point where even I get lost. So  I needed to find another external solution.

It seems that the jpg image file had an internal orientation that refused to be respected by any web server. 

The solution was to transform the file using:

```bash
mogrify -rotate 180 path/to/file.jpg
```

This reversed the image externally and now both bash display command and any web server displays the file correctly. Problem solved.



<!--more-->
