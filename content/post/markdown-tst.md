+++
date = 2019-04-07T17:28:29-04:00
draft = true
title = "Markdown-n-Such Testing"
slug = ""
tags = []
image = ""
comments = false    # set false to hide Disqus
share = true        # set false to hide share buttons
# menu= ""          # set to "main" to add to the main menu
author = "Name"
+++

{{% lshadowbox-nomd %}}
This is _%lshadowbox-nomd%_ shortcode
This specific test should show _markdown_ **correctly**.
{{% /lshadowbox-nomd %}}

-------

# KEEP THIS AS A DRAFT - FOR TESTING MARKDOWN AND SHORTCODE ONLY

## Code
You can insert `code`

Or 
```
a code block
```

## Emphasis
Emphasis, aka italics, with *asterisks* or _underscores_.

Strong emphasis, aka bold, with **asterisks** or __underscores__.

Combined emphasis with **asterisks and _underscores_**.

Strikethrough uses two tildes. ~~Scratch this.~~

## Links
[I'm an inline-style link](https://www.google.com)

[I'm an inline-style link with title](https://www.google.com "Google's Homepage")

[I'm a reference-style link][Arbitrary case-insensitive reference text]

[I'm a relative reference to a repository file](../blob/master/LICENSE)

[You can use numbers for reference-style link definitions][1]

Or leave it empty and use the [link text itself].

URLs and URLs in angle brackets will automatically get turned into links. 
http://www.example.com or <http://www.example.com> and sometimes 
example.com (but not on Github, for example).

Some text to show that the reference links can follow later.

[arbitrary case-insensitive reference text]: https://www.mozilla.org
[1]: http://slashdot.org
[link text itself]: http://www.reddit.com

## Images
Inline-style: 
![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")

Reference-style: 
![alt text][logo]

[logo]: https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 2"


## Tables
Colons can be used to align columns.

| Tables        | Are           | Cool  |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned | $1600 |
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |

There must be at least 3 dashes separating each header cell.
The outer pipes (|) are optional, and you don't need to make the 
raw Markdown line up prettily. You can also use inline Markdown.

Markdown | Less | Pretty
--- | --- | ---
*Still* | `renders` | **nicely**
1 | 2 | 3

## Pull-Quote
This is not markdown. It uses class additions to css/custom.css and HTML5. This uses an html5 aside.

<aside class="pullquote dropfirst">
This is an aside with paragraph tags but does have dropdownfirst and pullquote.
It is not an exaggeration to say that peas are perfect spheres of joy.
</aside>

And this next one uses blockquote inside of aside class=pullqupte

<aside class="pullquote dropfirst">
<blockquote style="margin: 0; border-left:5px solid #428bca;">
It is not an exaggeration to say that peas are perfect spheres of joy.
</blockquote>
</aside>

The insert is Italicised, a set font size and box in a 30% width.
More info would of course go here.
<p>
Lot of additional info actually.


## Blockquotes


> Blockquotes are very handy in email to emulate reply text.
> This line is part of the same quote.

Quote break.

> This is a very long line that will still be quoted properly when it wraps. Oh boy let's keep writing to make sure this is long enough to actually wrap for everyone. Oh, you can *put* **Markdown** into a blockquote. 

<blockquote>
<p>But the text needs to go on and on</p>
<p>Last paragraph</p>
</blockquote>


-------

# Shortcodes


Got to add some info here just to make markdown look real

<!--more-->

{ {< myimage src="/img/resolverjpg" style=width: 90%" >} }
{{< myimage src="/img/nodeinfo-screens.png" style="width: 90%" >}}

---------


Don't use this for single tag (no markdown .Inner) shortcode.

```
.{% shortcode %}.
```

-----------

{{% lshadowbox  %}}
_This is an **lshadowbox** with markdown_
<br>
use { {% %} } If the inner is markdown
<p>
use { {< >} } If the inner in NOT markdown
<p>
## All my lovin'
Belongs to you...
{{%/ lshadowbox  %}}

------------

{{< lshadowbox-nomd >}}
This is `[lt]lshadowbox-nomd[gt]` shortcode
This should _ignore_ markdown
{{< /lshadowbox-nomd >}}

------------

{{% lshadowbox %}}
{{% tst %}}
This is _tst_ %shortcode% 
{{% /tst %}}
{{% /lshadowbox %}}

------

{{% shadowbox  %}}
_This is an **shadowbox** with markdown_
<br>
use { {% %} } If the inner is markdown
<p>
use { {< >} } If the inner in NOT markdown
<p>
## All my lovin'
Belongs to you...
{{%/ shadowbox  %}}

-------------------

{{< shadowbox  >}}
NO MARKDOWN RECOGNIZED IN THIS BOX
_This is an **shadowbox** with markdown_
<br>
use { {% %} } If the inner is markdown
<p>
use { {< >} } If the inner in NOT markdown
<p>
## All my lovin'
Belongs to you...
{{</ shadowbox  >}}

---------

<div class="lsboxit">
This is not shortcode<br>
This is just a div with class=lsboxit<br>

_Some **markdown** here_

# Yes

No 
</div>

------------

{{< shadowbox  >}}
Combining shortcodes<p>
This works 20190409<br>
myimage of nodeinfo in shadowbox
<p>
{{< myimage src="/img/nodeinfo-screens.png" style="width: 90%" >}}
{{< /shadowbox  >}}

------------

{{<warning>}}
This is a **warning**
uses a class from bootstrap
{{</warning>}}

-------------

{{%warning%}}
This is a **warning**
uses a class from bootstrap
{{%/warning%}}


<hr>



