+++
date = "2018-10-07T10:05:52-04:00"
draft = false
title = "Using a generic git pre-commit hook"
slug = ""
tags = []
image = "img/hanging-hook.jpg"
comments = false	# set false to hide Disqus
share = false	# set false to hide share buttons
#menu= ""		# set "main" to add this content to the main menu
author = ""
+++

test_it && commit || reject

Using a pre-commit script when committing code makes sense and fits with every respectable dev-ops model.
The goal is to have respectable code *before* it lands in a repository. Git makes this very easy through the use
of "hooks". If you look in any of your git project directories you will find these files in the `./.git/hooks/` directory:

<!--more-->

```
pplypatch-msg.sample
commit-msg.sample
post-update.sample
pre-applypatch.sample
pre-commit.sample
prepare-commit-msg.sample
pre-push.sample
pre-rebase.sample
pre-receive.sample
update.sample
```

These are all obvious sample files. One of the most important steps you can take with your .git project is to force
good practices on your code by creating a pre-commit hook script. Using a pre-commit script will encourage
you to write consistently good code from the very start. 

A pre-commit script will be invoked as soon as you create an executable file with this name:

```bash
./.git/hooks/pre-commit
```

Now that file will run before your git commits and if the return code is not 0 your commit will fail.

Here is a very simple example. You have a clever project called hello.py. Your intent is to have good code before
commit so you write a ./.git/hooks/pre-commit bash script that looks like this:

```bash
#!/bin/bash
flake8 *.py
``` 

The file hello.py contains:

```python
#! /usr/bin/env python3

if __name__ == '__main__':
    # the above line allows this code to run independently or as a module
    """
    Use: hello.py
    Input: The user will be asked his/her name.
    Output: Hello World, may name is {name}
    """

    myname = input("What, pray tell, is your name: ")
    print(f"Hello World!, my name is {myname}")
```

Now, if you run git add -A, followed by git commit will cause the ./.git/hooks/pre-commit to run against the hello.py
and it will return an result code of 0 so all will be good and the commit will be successful.

You can test this yourself by running:

```bash
./git/hooks/pre-commit
echo $?
```

But what if you change line 8 to this:

```python
      myname=input("What, pray tell, is your name: ")
```

Now if you run the pre-commit script it will return something like:

```bash
hello.py:11:11: E225 missing whitespace around operator
```

This will return a non-zero return code. Any attempts to do a git commit will fail as a result. That is a good thing
as you want to learn good coding practices and submitting this code would not be consistent with that goal.

Just a word about using flake8 as a linter. It will drive you crazy. Failing on long lines (over 80 characters)
really drives me nuts, but flake8 and forcing you to play well in the pep8 standards realm. You can control that 
through the $HOME/.config/flake8 file with entires like this:

```bash
[flake8]
max-line-length = 120
```
When I first started using linters to check my coding it was painful. But once you get all your code cleaned up
you find yourself writing better code from the very start. The pain subsides and life is good again.

I use linters on lots of different kinds of files now:

| File ending [type] | linter(s) |
|:------------------:|:------:|
| \*.py              | autopep8, flake8, python -m doctest |
| \*.html            | htmllint |
| \*sh               | shellcheck |
| \*.nts or \*.txt   | write-good |
| \*.css             | stylelint  |

A linter exists for dozens of code or writing formats. It is your adventure to find them and wrestle them into submission for your aspirations.

I try to make is easy on myself so I use a **single** script in every git project directory. The script is a simple bash executable that runs various linters against code before it is committed (hence: pre-commit). Every time I run `git init` on a new project directory I also
copy my standard .gitignore file from my ~/dev/dotfiles directory and I copy this script over

```
cp $HOME/dev/dotfiles/scripts/pre-commit.sh {new project directory}/scripts/pre-commit.sh
```


Actually, I just `cp -r $HOME/dev/dotfiles/scripts {project directory}/`. Now I can
just run `./scripts/pre-commit.sh` and it will check any *.py files and *.sh file and any 
\*.html files etc using the linters above. That one script can be used in any project to
help establish a minimal code quality baseline.

Here is a quick redacted example:

```
#!/bin/bash

function check_sh_files()
{
  LINTER=shellcheck
  LINTER_OPS=""
  find ./ -name \*.sh -print0 |\
    while read -r -d '' file; doere 
      echo Running: shellcheck "$file"
      shellcheck "$file" || exit $?
    done
}

# Note that this function does a "fast-fail" with a non-zero exit
# other functions for check_py_files, check_html_files... etc - even one to
# make sure there is a README with minimal info.

# Main Code #
check_sh_files
check_py_files
check_html_files
check_css_files
# etc...
# EOF #
```

The script is not invoked by git commit yet. Above we directly created an executable file called `./.git/hooks/pre-connect`.
We need to remove the original simple script that only checkec \*.py files and instead soft link this new file in its place.
To do that run:

```
function do_install()
{
	# run this from the project basedir 
  # here is a protection test
	if ! [ -d ./.git ] || ! [ -d ./scripts ] ; then
    echo "Please run this script from the project base directory... exiting..."
    exit 5
  fi

	# changing to the .git/hooks directory first is *important*
	# it allows you to create a "relative" link that git will respect.
	cd ./.git/hooks
	if ! [ -h ./pre-commit ]; then
		# a link does not already exist for this file so we now create one
		ln -s ../../scripts/"$BASENAME"  ./pre-commit
	else
		echo It appears .git/hooks/pre-commit exists ...
	fi
	cd ../..  # return to the project basedir.
}
```

Add this line now just below the `# Main Code #` line:

```
do_install
```

So the fists time you run this script it will install as a link named ./.git/hooks/pre-connect.

My script has much more than I have shown here. It checks README files and it updates itself
if it finds any differences from the master copy:  `~/dev/dotfiles/script/preconnect.sh`.

 
This gives you an idea of how to use a `./.git/hook/pre-connect` script to improve your coding practices.

Enjoy,

-geoffm-

