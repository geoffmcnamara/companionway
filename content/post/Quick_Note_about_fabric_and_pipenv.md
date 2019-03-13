+++
date = "2019-03-13T10:56:05-04:00"
draft = false
title = "Quick_Note_about_fabric_and_pipenv"
slug = ""
tags = []
image = "/img/posted-keep-out.jpg"
comments = false	# set false to hide Disqus
share = false	# set false to hide share buttons
#menu= ""		# set "main" to add this content to the main menu
author = ""
+++


I have posted several articles about python fabric and yet I failed to warn you about the dangers of
version chaos.

Initially, fabric came as a python2 only application. They added support for python3 later. Here is the version
I am using in a virtual environment (more about that in a minute). From within my pipenv project directory with pipenv shell loaded
this is what I get running fab --version

```
fab --version
Fabric3 1.14.post1
Paramiko 2.4.2
```

Here is how I created my virtual environment. I have used almost all of python's virtual environment tools (and there a quite a few).
And there has been a steady progression of improvements in those tools. My current goto for a python virtual environment is pipenv.
It is simple, clean, and almost fool proof which is essential for me. 

<!--more-->

I don't remember exactly but I think I initially installed pipenv using apt. For my fabric use I created my fabric development project
directory with `mkdir -p ~/dev/python/fabric`. Here are the easy steps to establish your virtual environment:
```
cd ~/dev/python/fabric
pipenv --three install # do this once. It establishes everything needed for the virtual environment. The --three option makes it python3
pipenv shell
```
Now you should be in your virtual environment using python3. When you are in the pipenv shell there is an addition to your prompt to let you
know. ie: [fabric3]

Make sure you have pip installed for python3 and use it while your are in the pipenv shell to install fabric...
```
pip install fabric3
 # or
pip3 install fabric3  # pip3 is not necessary as pipenv shell is already using pip3
```

The virtual (pipenv) environment is using python3 (not the default on ubuntu 2019-03-13) here is your proof:
```
python --version
Python 3.7.2rc1
```

From within my pipenv shell for my fabric project these are the modules that pip list shows:
```
pip list
Package      Version   
------------ ----------
asn1crypto   0.24.0    
bcrypt       3.1.6     
cffi         1.11.5    
colorama     0.4.1     
cryptography 2.4.2     
docopt       0.6.2     
Fabric3      1.14.post1
idna         2.8       
paramiko     2.4.2     
pip          18.1      
pyasn1       0.4.5     
pycparser    2.19      
PyNaCl       1.3.0     
setuptools   40.6.3    
six          1.12.0    
wheel        0.32.3    
```
Notice fabric is listed as Fabric3

To make things really easy for me to get going on a fabric task I have an alias set up in my ~.bashrc that looks like this:
```
alias pyfab="cd ~/dev/python/pipenv/fabric3; pipenv shell"
```

All that is needed is to type "pyfab" and I am in the pipenv shell in the fabric directory and all is good in the world.

Then main file in this directory is my fabfile.py which is the default fabric task declaration file.
To launch fabric of course you just type `fab -l` while in the pipenv shell. This command will list all the tasks you have written in
your fabfile.py If you don't have a fabfile.py set up yet you will get this error:
```
fab -l
Fatal error: Couldn't find any fabfiles!
Remember that -f can be used to specify fabfile path, and use -h for help.
Aborting.
```

I code everything I can in python3 vs python2 because python3 is so much better. I made it my default platform when f-strings
became available in python3.6? This allows something like this:
```
name = "geoff"
print(f"My name is {name:>30}. You can print python directly like this {3 + 4} from within function {__name__}")
```

So it was a must for me to have fabric work in python3. Because fabric is an indispensable tool in my life I need to make sure it is safe
from outside changes. That requires placing it in a virtual environment, isolated away from version and module changes made elsewhere.

