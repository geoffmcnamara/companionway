+++
date = 2019-04-07T16:07:46-04:00
draft = true
title = "SHORTCODE TESTING"
slug = ""
tags = []
image = "/img/img_ext"
comments = false    # set false to hide Disqus
share = true        # set false to hide share buttons
# menu= ""          # set "main" to add this content to the main menu
author = "Name"
+++


# KEEP THIS AS A DRAFT - FOR TESTING SHORTCODE ONLY

Got to add some info here just to make markdown look real

<!--more-->

{ {< myimage src="/img/resolverjpg" style=width: 90%" >} }
{{< myimage src="/img/nodeinfo-screens.png" style="width: 90%" >}}
<hr>


{ {% img-post "/img/" "nodeinfo-screens.png" %} }
{{% img-post "/img/" "nodeinfo-screens.png" %}}
<hr>

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
<hr>

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
<hr>


{{< shadowbox  >}}
Combining shortcodes
<p>
{{< myimage src="/img/nodeinfo-screens.png" style="width: 90%" >}}
{{</ shadowbox  >}}

<hr>

{{<warning>}}
This is a **warning**
uses a class from bootstrap
{{</warning>}}


<hr>



