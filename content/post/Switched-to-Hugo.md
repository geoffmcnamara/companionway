+++
author = ""
comments = false
date = "2016-12-09T10:57:45-05:00"
draft = false
image = "/img/hugo-logo.png"
menu = ""
share = true
tags = ["hugo", "jekyll", "cms"]
title = "Switched to Hugo"

+++

I am swtiching from jekyll to hugo for flat file for a Content Managment System (CMS).
<a href="https://gohugo.io">![alt text](/img/hugo-h.jpg "goHugo.io")</a>

Here is why:

- It comes as a binary file that runs on pretty much any platform. A single file... without a list of dependencies
- I could stop with the last reason and it would be enough... but I have to say that the file tree used in hugo is simple, and simple is beautiful. As Einstein once said: 
>“Make things as simple as possible, but not simpler.”
- It is written in googles go language... so it is fast and portable.
- It is closely tied to git so it can easily be used on github and for version maintence.
- it builds a clean directory [./public/] for the full site deploy and this can be rsync'd to where ever you like.
    or ... just git push it to hithub and use something like netlify.com to host from your github!
- *No frustrating* version incompatiblities (or at least very minimal) - unlike jekyll which seemed to break on me every few months.
- hugo is relatively mature and has a huge developer backing. 
- configurable and changed without challenges
- lots of themes to choose from
- as the Hugo websites states - it makes the web fun again...
- Did I mention that it is a single executable file?

Reference:
[gohugo.io](https://gohugo.io/#intro)

<!--more-->
Enjoy
-g-
