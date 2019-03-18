+++
date = "2019-03-15T15:07:41-04:00"
draft = false
title = "Vim-Plug Quick Setup"
slug = ""
tags = []
image = "/img/fisa-vimrc.jpg"
comments = false	# set false to hide Disqus
share = false	# set false to hide share buttons
#menu= ""		# set "main" to add this content to the main menu
author = ""
+++

I want you to try this .vimrc setup.

I have had my own .vimrc for years. I recently came across [fisa-vim-config](http://fisadev.github.io/fisa-vim-config/)
and ended up dropping my extensive .vimrc, adopting the one above and adding a few tweaks to make it friendly to me. I 
was actually looking for more ALE-fixers when I found this gem.

It is simple, self installing and very powerful due to the vim Plugins that are installed and loaded.

<!--more-->

Here are the steps I want you to try... trust me here.
* mv ~/.vimrc MyOld.vimrc # or whatever your favorite backup scheme is I actually name mine with a date eg 20190315.vimrc
* mv ~/.vim MyOld.vim
* download fisa-vim-config and replace your old ~/.vimrc
* run vim on any file you want

Much credit to the author of fisa-vim-config: Juan Pedro Fisanotti! 

![Just a small sample of what can be done](/img/vim-plug-sized.gif)


There is more to do here but if you do those steps you will see lots of new Vim Plugins get loaded automagically.

You can actually remove the ~/.vim (it has root owned .git subdirectories so you will have to force remove the directory).  
Run vim again and your ~/.vim directoy will automagically get built out again.

Now tweak your shinny new ~/.vimrc file.
First I want vim to remember where I left off in a file and put the cursor there when I return to that file.  Add this to the end of ~/.vimrc.

```
" ======= remember cursor position and viminfo settings  ========
" Tell vim to remember certain things when we exit using set viminfo=
"  '10  :  marks will be remembered for up to 10 previously edited files
"  \"100 :  will save up to 100 lines for each register
"  :20  :  up to 20 lines of command-line history will be remembered
"  %    :  saves and restores the buffer list
"  n... :  where to save the viminfo files
set viminfo='10,\"100,:20,%,n~/.vim/dirs/viminfo
" now function that restores the cursor position and its autocmd so that it gets triggered:
function! ResCur()
if line("'\"") <= line("$")
  normal! g`"
  return 1
  endif
endfunction
augroup resCur
  autocmd!
  autocmd BufWinEnter * call ResCur()
augroup END
" ======= EOB remember settings ================
```
Note: the file viminfo line is supplanting the viminfo line already in fisa-vim-config vimrc.

You good folks probably know that I am a huge fan of vim ale so lets add that plugin... this so easy!
#end()
You have to add this between the start [`call plug#begin('~/.vim/plugged')`] and the end [`call plug#end()`] of the Vim plugins section.
```
" ALE for vim
Plug 'https://github.com/w0rp/ale.git'
```

I didn't care for the color schemes and some other annoying or problematic Plugs so...
- commented out all the references to it using .vimrc comment character which is the double quote.
- commented out the `set nu` to stop the line numbering.
- commented out the Plug ... syntastic ... line as it caused conflicts on large code files
- commented out some of the backup and swp file settings.

Then I added a few of my own tweaks:
```
" numbers on or off
nnoremap <Leader>nn :set nonumber<CR>
nnoremap <Leader>sn :set number<CR>

" toggle neocomplcache pop up boxes
nnoremap <Leader>nt :NeoComplCacheToggle<CR>

" ALEToggle
nnoremap <Leader>at :ALEToggle<CR>

```

Oh, and one more significant change. For python editing I added this ftplugin file:
```bash
mkdir ~/.vim/ftplugin
```

Then `vim ~/.vim/ftplugin/python.vim` and add:

```
let b:ale_linters = ['flake8']
let b:ale_fixers = [
\   'remove_trailing_lines',
\   'isort',
\   'ale#fixers#generic_python#BreakUpLongLines',
\   'yapf',
\]
" be careful with this - it can get wonky and you may have to :q! to avoid writing out errors
nnoremap <buffer> <silent> <LocalLeader>= :ALEFix<CR>
```
That last line allows me to run the `vim <leader>=` (ie \= ) and automagically lots of fixes occur to my python code.

Within vim you can run `:ALEInfo` and get LOTS of useful information and suggestions.
I loaded all the suggestions and oneof the most useful for python is 'yapf'.
I don;t remeber exatcly how I installed it but my guess is somthing like this:

```
sudo -H pip3 install yapf
```


I might have change Airline status line a bit too, but you do what you want:
```
" Airline ------------------------------
" apt.sh -i powerline fonts-powerline # to get what you will need here
"let g:airline_powerline_fonts = 0
let g:airline_powerline_fonts = 1
"let g:airline_theme = 'bubblegum'
"let g:airline_theme = 'base16'
let g:airline_theme = 'papercolor'
let g:airline#extensions#whitespace#enabled = 0

" to use fancy symbols for airline, uncomment the following lines and use a
" patched font (more info on the README.rst)
if !exists('g:airline_symbols')
   let g:airline_symbols = {}
endif
"let g:airline_left_sep = '⮀'
"let g:airline_left_alt_sep = '⮁'
"let g:airline_right_sep = '⮂'
"let g:airline_right_alt_sep = '⮃'
"let g:airline_symbols.branch = '⭠'
"let g:airline_symbols.readonly = '⭤'
"let g:airline_symbols.linenr = '⭡'
```
And make sure you still have 256 colors:
```
" use 256 colors when possible
if (&term =~? 'mlterm\|xterm\|xterm-256\|screen-256') || has('nvim')
    let &t_Co = 256
"    colorscheme fisa
"else
"    colorscheme delek
endif
```

Add this line to the Tagbar section to have navigation a little less intrusive:
```
let g:tagbar_autoclose = 1
```
Oh, at this point there is one thing you may want to do and that is make a backup copy of your ~./vim/ftplug dir.
The reason is, you can still forcefully remove .vim directory and it will get rebuilt by your .vimrc BUT it won;t
rebuild your.vim/ftplugin directory. 

Take time to appreciate some of the plugins:
- Airline is giving you the status lines Try `:help Airline`
- TagBar is another useful tool for large code files. While editing some code try `:TagBar` and use it to navigate
  through your code.

If you want to see the power you now hold in your knapsack...
`:map` 

Here is some quick fun vim... from the command line:
```
vim -O ~/.vimrc ~/.vim/ftplugin/python.py ./.bashrc
```
Then hit '-', yes, just hit '-'. Very slick!

BTW You can update all these Plugins while in vim with `:PlugUdate`
And you can upgrade vim-plug itself with `:PlugUpgrade`.
You can get help for any of the ALE* commands eg. `:help ALEFixSuggest`

Let me know if I forgot something or should make changes.

-* Enjoy! *-

-g- 
geoff.mcnamara@gmail.com:
