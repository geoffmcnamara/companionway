+++
date = "2018-08-08T09:30:10-04:00"
draft = false
title = "Vim ALE"
slug = "" 
tags = []
image = "/img/ale-logo.jpg"
comments = false	# set false to hide Disqus
share = false	# set false to hide share buttons
#menu= ""		# set "main" to add this content to the main menu
author = ""
+++


VIM is a standard for me. My UNIX career hung on my "vi" savvy which I learned appreciate from mentors who 
encouraged me to learn the tips and tricks of using vi. My learning curve with vi/vim has never leveled 
off, but rather, always gives me new features and tricks that energize me again. The latest vim "trick" 
is ALE (Asynchronous Lint Engine).

<!--more-->

ALE came to light for me while working on building git hooks (especially pre-commit hooks) that force me
to test and run a linter against my code before it gets committed. It has forced me (in a good way) to clean
up my python code. It wasn't as hard as I had expected and the gain is worth it. All this work using
python doctest (which I love) and autopeg8 and flake8 has made me realize that much of my "after-the-fact" pain
could be drastically reduced if my editor alerted me as I typed and assisted me in discovering or avoiding 
syntax or simple coding errors. It wasn't until I started to work the myriad of shell scripts that I found
shellcheck and in turn vim ALE. 

Vim ALE can be found here [Vim ALE](https://github.com/w0rp/ale]) but it can easily be installed with these
commands:

```
mkdir -p  ~/.vim/pack/git-plugins/start
git clone https://github.com/w0rp/ale.git ~/.vim/pack/git-plugins/start/ale
```

Now while you edit vim ALE will run in the background (hence the ALEngine) while you edit and
sets up a "gutter" on the left column to alert or notify you of issues from underlying "linters".
The initial problem I ran into was the highlighting of specific characters which needed attention. It made
reading the underlying character is difficult for my old eyes so I needed a way to leave the "gutter"
alerts but turn off the highlighting. So I added a line to my .vimrc to turn ALE highlighting off by default.
I also run into a problem with ALE trying to run a linter against some of my plain text files so I added
a line to easily toggle ALE on or off. Here is my .vimrc section for using ALE


```
""""""""" for ale """"""
" Install ALE with:
" mkdir -p ~/.vim/pack/git-plugins/start
" git clone https://github.com/w0rp/ale.git ~/.vim/pack/git-plugins/start/ale

" next line turns off the highlighting for ALE (it makes code hard to read)
" but leaves the "gutter" notifications
let g:ale_set_highlights = 0
map <leader>at :ALEToggle<CR>

"""""""""""""""""""""""""
```

Only 2 active lines here but I documented how to use ALE for when I move to a new system.


BTW: A recent article discussing the history of VIM is posted here (VIM History)[[200~https://twobithistory.org/2018/08/05/where-vim-came-from.html].
It is an interesting read. 

Enjoy
-g-

