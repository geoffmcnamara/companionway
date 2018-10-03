+++
date = "2018-08-08T11:15:04-04:00"
draft = true
title = "Git pre Commit hook"
slug = ""
tags = []
image = ""
comments = false	# set false to hide Disqus
share = false	# set false to hide share buttons
#menu= ""		# set "main" to add this content to the main menu
author = ""
+++


WIP


<!--more-->
#!/bin/bash
##################################################################
# Script name: t.sh
# Creation by: geoffm
# Creation Date: 20180804
# Last modified: 20180804 geoffm
# Purpose:    used with git to insert creation/modification info in any README.*
# Valid User(s): whoever
# Parameters Expected: none
# How should it be used:
#    cd <prj>
#    mkdir ./scripts
#    cp pre-commit.sh ./scripts/
#    ./scripts/pre-commit.sh -i  # installs the soft link to .git/hooks/pre-commit
#     git checkin # auto invoked whenever you commit code
# Notes:      place script in prj/scripts/pre-commit.sh
#             ln -s scripts/pre-commit.sh .git/hooks/pre-commit
# vim: noai:verbose:ft=bashr:ts=2:expandtab:
###################################################################



###############
return_check()
###############
{
	ERR_FLAG=$1
  echo $FUNCNAME $ERR_FLAG  
	if [ $ERR_FLAG -ne 0 ]; then
		echo FAILURE...
		exit 1
	else
		echo PASSED...
	fi
}

################
check_pyfiles()
################
{
	echo $FUNCNAME
  for i in *.py; do
		echo Running: python3 -m doctest -v $i
		# python3 -m doctest -v -o FAIL_FAST $i
		python3 -m doctest -o FAIL_FAST $i
		return_check $?
		# use autopep8 --in-place --aggressive --aggressive <file>.py to fix some errors first
		echo Running autopep8 --inplace --aggressive --aggressive $i
		autopep8 --in-place --aggressive --aggressive $i  # to fix some errors first
		echo Running flake8 --max-line-length=150 $i
		flake8 --max-line-length=150 $i
    return_check $?
    echo $SLINE
	done
	echo Note: noqa=no quality assurance... can be used on a line to ignore an error eg: lambda: example  # noqa: E731,E123
}


################
check_shfiles()
################
{
	echo $FUNCNAME
	ls *.sh >/dev/null 2>&1 || return
  for i in *.sh; do
	echo Running: shellcheck $i
	shellcheck $i
	return_check $?
    echo $SLINE
  done
}


#############
do_install() 
############
{:
  echo $FUNCNAME
  cd $(dirname $0)
  DIR=$(dirname $0)
  BASENAME=$(basename $0)
	pwd
	ln -s ../../$0  ../.git/hooks/pre-commit
	# echo ln -s $DIR/$BASENAME  ../.git/hooks/pre-commit
  ls -l ../.git/hooks/pre-commit
}


###################
# Main Code
#####################
cat <<EOF
++++++++
This is a pre-commit script
- Looks for and updates any README.* files with modified date info
- pre-processes *.py code etc

To skip this check: git commit --no-verify
++++++++
EOF

# quick-n-dirty test for -i argument
[ x"$1" = x"-i" ] && do_install && exit 1 

update_readmes

check_pyfiles
check_shfiles



ERRFLAG=$?
doEXIT 
### End of Script ###

