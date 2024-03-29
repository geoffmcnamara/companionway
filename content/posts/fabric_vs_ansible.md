+++
date = "2018-07-10T09:30:14-04:00"
draft = false
title = "Fabric_vs_ansible"
slug = ""
tags = []
image = "/img/fabric_vector_logo.svg"
comments = true	# set false to hide Disqus
share = true	# set false to hide share buttons
author = ""
+++

I have wrestled with ansible for too long. It is an awesome tool but you need to learn the syntax of three
different languages (ansible, yaml, and maybe some python) to hold it down and control it. Every time I go 
to use it I have to learn how to do what I need to do. But the most frustrating aspect of ansible when learning
to do something new is that your first attempt rarely succeeds - at least for me. So you resort to "force programming"
to get through it. By "force programming" I mean you try this and that and then something else until it works, and
I end up with a hodgepodge of debug lines commented out.

<!--more-->

Following the bunny trail to find an alternative, I ran across python ["fabric"](200~http://www.fabfile.org/). I am a committed python code minion.
So much so lately, that I have converted many of my bash scripts to python. But all that is a different topic for a rainy day.
Put ansible away in a dark closet somewhere and start using fabric. If you are starting out with fabric or going to
explore it now, don't just type "how to use fabric" in your search engine because the obvious will happen. So precede your mention 
of "fabric" with "python"... so "how to use python fabric". 


Using pip you can install fabric. Python fabric is a module that comes along with a python tool called "fab".
If you run `fab -h` you will see a healthy list of options/arguments. Don't let that put you off. A working
knowledge of python is all you need to master fabric. The fabric module is designed to provide you with ssh tools out of the box. It allows running
any process remotely or locally, without any headaches. If you have been using ansible, then this exercise will be a little like 
subjecting a Windows user to the linux command line (well maybe not quite that bad). 

Here's a quick one-liner:

~~~
fab -H rpi01,rpi02,192.168.1.40 -- df -h
~~~ 

Pretty obvious... until it fails. If one of those hosts is down this process will break.
The fab tool by default looks for a file called fabfile.py. So lets create a simple one to overcome the failure problem just mentioned.

Write a file called fabfile.py  You can use any filename but we are sticking with the default.

~~~
from fabric.api import run,settings

def df_h():
	with settings(warn_only=True):
		run('df -h')
~~~


To run this:
~~~
fab -H rpi01,rpi02 df_h
~~~

<!--more-->

If one of the hosts is down  then the df_h "task" will still be run on the other hosts. We are still far from what ansible has to offer but we
have only used python. No yaml, no ansible freak out without a trace-back stack dump. This is unadulterated python.
On the command line you have to tell it what method/function to run. The fab tool calls this a "task". More on this later. 

Given a great number of hosts you naturally want to declare groups of hosts and a list of tasks to perform. Fabric accommodates these desires
by using "roles" and, because this is python, one function can call other functions. The term "roles" might seem a bit off but it is more powerful than
just name groups; I leave it to you to find out more about fab roles. Assume you want to run a set of tasks to give you an informed status
of a group of hosts. Here is an example fabfile.py:

~~~
from fabric.api import run,settings,env

env.roledefs={
	'rpis'=['rpi01','rpi02','rpi03'],
	'containers'=['node01','node02','node03']
	}


def uname():
	run('uname -a')

def df():
	run('df -H | grep "dev"')

def status():
	with settings(warn_only=True):
		uname()
		df()
~~~

Call `fab -R "rpis" status` to get the status of the servers in the 'rpis' role (hence the `-R "rpis"). You could list several roles comma delimited.
Here is a way to declare a set of hosts like "all" which demonstrates how you can leverage python within a fabfile. Note that "env" was added to the import list.

~~~
from fabric.api import run,settings,env

env.roledefs={
	'rpis':['rpi01','rpi02','rpi03'],
	'containers':['node01','node02','node03'],
	'debian':['rpi01','rpi02'],
	'rhat':['node03']
	}

all=env.roledefs['rpis'] + env.roledefs['containers']


def sethosts(group="list"):
    """
    sethosts(group=list) 
    use: fab sethosts:"rpis" status  # run status against the 'rpis' hosts
			   fab sethosts:"all" status     # run status against "all" servers
		     fab sethosts  # will list all the host groups and their values
    """
    if group == "all":
        env.hosts = all
        dbug(f"hosts all:{env.hosts}")
        
    if group == "list":
        for k,v in env.roledefs.items():
            print(f"{k}={v}")
    else:
        try:
            env.hosts=env.roledefs[group]
            print(f"Selected group:{env.hosts}")
        except:
            print(f"Unrecognized group[{group}]...")


def uname():
	run('uname -a')

def df():
	run('df -H | grep "dev"')

def status():
	with settings(warn_only=True):
		uname()
		df()
~~~


Surely other coders out there can improve on this. Here are some of the highlights regarding changes made. I added some additional "roles" for future use. I also
added a variable called "all" that pulls in selected role groups for use with the sethosts function/task. The command line for fab allows passing arguments with
the function name followed by a ":". Here are some examples of using the sethosts function/task.

~~~
fab sethosts:"all" status  # will run status on "all" hosts
fab sethosts:"rpis" status # will run status on "rpis" hosts
fab sethosts               # will run sethosts and list the roles defined.
~~~

Now the power of fabric starts to emerge. That power is just python with a smart way of calling ssh using fabric. The fabric.api has lots of others useful calls
like put("/source/filename","/target/", use_sudo=True), get(), sudo(), local(), run(), etc. 

One other thing here. You will see that within the fabfile you can use decorators that come with fabric like "@roles('rpis')", @task and others. You can list all
the available "task" in the fabfile by using `fab -l`. Running that on the above file lists all the tasks as shown here:

~~~
fab -l
Available commands:

    df
    sethosts  sethosts(group=list)
    status
    uname
~~~

Perhaps you only want to have listed the status and sethosts tasks - use the @tasks wrapper. The @task decorator can also be used to create namespaces, see the docs.
Here is a modified fabfile.py:

~~~
from fabric.api import run,settings,env

env.roledefs={
	'rpis':['rpi01','rpi02','rpi03'],
	'containers':['node01','node02','node03'],
	'debian':['rpi01','rpi02'],
	'rhat':['node03']
	}

all=env.roledefs['rpis'] + env.roledefs['containers']


@task
def sethosts(group="list"):
    """
    sethosts(group=list) 
    use: fab sethosts:"rpis" status  # run status against the 'rpis' hosts
			   fab sethosts:"all" status     # run status against "all" servers
		     fab sethosts  # will list all the host groups and their values
    """
    if group == "all":
        env.hosts = all
        dbug(f"hosts all:{env.hosts}")
        
    if group == "list":
        for k,v in env.roledefs.items():
            print(f"{k}={v}")
    else:
        try:
            env.hosts=env.roledefs[group]
            print(f"Selected group:{env.hosts}")
        except:
            print(f"Unrecognized group[{group}]...")



def uname():
	"""
	runs uname -a 
	"""
	run('uname -a')


def df():
	"""
	runs df -H | grep "dev"
	"""
	run('df -H | grep "dev"')


@task
def status():
	with settings(warn_only=True):
		uname()
		df()

@task
def lxcstart():
	with settings(warn_only=True):
	  run('lxc start --all')

@task
def aptupdate():
	with settings(warn_only=True):
		sudo('apt update')

@task
def buildweb():
	sudo('apt -y install apache2 php')
	put("/home/myself/dev/www/skel", "/var/www/html/", use_sudo=True)
~~~

I added just a few tasks so you can can see other simple examples.

Enjoy

-g-
