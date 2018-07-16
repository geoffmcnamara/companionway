+++
comments = true
date = "2018-07-15 14:00:00"
draft = false
share = true
title = "Vim Scriptable Templates"
image = "img/vim-dynamic-templates.png"
+++

### Dynamic vim Templates

Vim (or vi in the anceint past) has been my partner in getting things done. Like an rich tool it
has lots of features that go untapped or undiscovered. A few days ago I decided I wanted a script within
a tempate to help build the "front matter" to my markdown (.md) files.

The front matter looks like this:

```
+++
author = ""
comments = true
date = "2018-07-15 14:45:19"
draft = false
image = ""
share = true
# slug = 
# tags = [ "tag1", "tag2" ]
title = "vim_scriptable_templates"

+++
```

The challenge was to have vim write in the date for me in the needed format. And if you use hugo as your static web site generator as I do
you may have found that it will silently ignore a new markdown file if the date is not formated correctly. It some testing to discover that
but the bottom line is that I needed a way to script it for to avoid mistakes.

Research to me to this tip source: [ vim embedded scripts ](http://vim.wikia.com/wiki/Use_eval_to_create_dynamic_templates)

<!--more-->

I use autocommands in vim to load templates. The strategy here is to have vim recognize and respond when I start to write a new
markdown (.md) file and run vim scripts where needed to dynamically fill in needed data. I will start here with writing the 
template. All my templates are in a directory I call `~/vinrc-files/`.  Here is the contents of my .md file template named 
`~/vimrc-files/vimrc-md.tem`:

```
+++
# author = "-g-"
comments = true
date = "[:VIM_EVAL:]strftime("%Y-%m-%d %T")[:END_EVAL:]"
draft = false
# image = "img/myimage"
share = true
# slug = 
# tags = [ "tag1", "tag2" ]
# Watch the title below and change as you desire
title = "[:VIM_EVAL:]expand("%:t:r")[:END_EVAL:]"

+++


```

For what it is worth, the inclusion of `<!--more-->` is hugo's trigger for cutting of a summary block.

Two embedded scripts are here and I will leave it to you to research cypher their workings.

Now within the `~/.vimrc` file I need two things.

-  auto load the template into any .md file that I start to write. The added code looks like this:
```
autocmd BufNewFile *.md 0r~/vimrc-files/vimrc-md.tem
```

- run a process to substiture the embedded vim evaluation code with processed data. 
```
" parse special text in the templates after the read - this MUST be after the autocmd to load the template
autocmd BufNewFile * %substitute#\[:VIM_EVAL:\]\(.\{-\}\)\[:END_EVAL:\]#\=eval(submatch(1))#ge
```

Hope this offers help to someone.

Enjoy
-g-


" parse special text in the templates after the read
  autocmd BufNewFile * %substitute#\[:VIM_EVAL:\]\(.\{-\}\)\[:END_EVAL:\]#\=eval(submatch(1))#ge



<!--more-->

