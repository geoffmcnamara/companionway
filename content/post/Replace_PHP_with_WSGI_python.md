+++
date = "2018-11-20T10:54:24+02:00"
draft = false
title = "Replace PHP with WSGI python"
slug = ""
tags = ["bottle","wsgi","php","devops","fabric"]
image = "img/bottle.png"
comments = false	# set false to hide Disqus
share = false	# set false to hide share buttons
author = ""
+++


This post is a brief description of replacing PHP code with python using WSGI (Web Server Gateway Interface). The journey here comes from how I monitor my servers (mostly raspberry pi's). I used a PHP script on all my servers that delivered the hostname and basic server information and I use [xymon monitoring](http://xymon.sourceforge.net/) to poll that PHP script on all the servers and test to see if the hostname is contained in the returned page. My focus lately has been on python and my interest in PHP has waned. The goal was to replace my PHP script with a python script. The end result provides a simple means of delivering dynamic web pages. I will be using [bottlepy](http://bottlepy.org) as the wsgi web-framework. My development was done on an ubuntu 18.10 ("cosmic" release).

<!--more-->

-------
## Contents: ##
- [Screen shots](#screens)
  [Requirements and why](#reqs)
- [Code](#code) - [because that's probably why you are here]
- [Download](#download)
- [Code Analysis](#analysis)
- [Troubleshooting](#debug)
- [Going forward from here](#postface)

<hr>

<a name="screens"></a>
### Screens ###
  <img src='/img/nodeinfo-screens.png' style="width: 90%">

  {{< image src="/img/nodeinfo-screens.png" >}}
  {{< myimage src="/img/nodeinfo-screens.png" style="width: 90%" >}}



<a name="reqs"></a>
### Requirements ###

- pip install bottle
- apt install apache2 liibapache2-mod-wsgi  
<div class="sboxit">
<b>Note:</b> This will expect all your python code to be python2 (as for Ubuntu repositories moving libapache2-mod-wsgi to python 3... well, not yet - so this leaves us somewhere back in the middle-ages)
</div>

- [optionally] python fabric (because you will want to promote your new code seamlessly and repeatedly (aka devops)


### Python script and apache2 config file ###

Needed steps...

- `sudo mkdir -p /usr/local/www/wsgi-scripts`
- `cp nodeinfo.py /usr/local/www/wsgi-scripts/`
- `cp wsgi.conf /etc/apache2/conf-available/`
- `sudo a2enconf wsgi`
- `sudo systemctl restart apache2`
- browser to http://localhost/chkit/nodeinfo  # this is the WSGI Alias name used in wsgi.conf to invoke the script
- you can also browse to: .../chkit/nodeinfo/inxi or .../chkit/inxifull


I elected to use python bottle  micro web framework because it is small, fexible, launches a built-in web server, and self contained in one file. The syntax used by bottle is very easy to learn. The built-in web server allows quick testing of code. The apache WSGI module provides the ability to run python scripts within apache.

 
<a name="code"></a>
### Code ###

The following script has lots of documentation in it so it looks long.

Also, I have included templates with css style code and a class called HtmlWrap all of which could be separated out into other files. They are all here to allow ease of deployment and to allow single file search and troubleshooting. 

Here is the **nodeinfo.py** script:
```

#!/usr/bin/env python2
# ########################
# nodeinfo.py 
# bootle app for cli or wsgi
# companionway.net 
# 
# vim: nospell
####
# This script can be run from the commandline as is or through WSGI
# ########################
"""
nodeinfo.py
requires: bottlepy
for auto install (gwm): use fab -H<myhost> webit
To run from webserver (eg apache2) - this is out of fabfile.py file that I use...
# install wsgi, web.py, and config wsgi alias /chkit/nodeinfo  # note: uses python2 !!
      sudo('apt install python-pip')
      put('/home/geoffm/dev/www/skel/wsgi.conf', '/etc/apache2/conf-available/', use_sudo=True)
      # sudo('pip install web.py')
      sudo('pip install bottle')
      sudo('apt install libapache2-mod-wsgi')
      sudo('a2enmod wsgi')
      sudo('a2enconf wsgi')
      sudo('systemctl restart apache2')
# ## or ###
sudo pip install python pip bottle
sudo apt install libapache2-mod-wsgi
sudo a2enmod wsgi
# with the proper permissions:
#  scp /home/geoffm/dev/www/skel/wsgi.conf remote_host:/etc/apache2/conf-available/
sudo a2enconf wsgi
sudo systemctl restart apache2
# #####################
## Contents of wsgi.conf: ##
# http://<servername>/chkit/nodeinfo
WSGIScriptAlias /chkit/nodeinfo /var/www/html/chkit/nodeinfo.py/
<directory /usr/local/www/wsgi-scripts>
  <IfVersion < 2.4>
    Order allow,deny
    Allow from all
  </IfVersion>

  <IfVersion >= 2.4>
    Require all granted
  </IfVersion>
</Directory>
"""
# ###########################

# imports #
import socket
import subprocess
import shlex
import os
import sys
import datetime
from bottle import default_app, route, run, request, SimpleTemplate


# setup environment # 
os.chdir(os.path.dirname(__file__))
sys.path.append(os.path.dirname(__file__))
from wraphtml import WrapHtml
  

# WSGI #
# the name "application" is needed for wsgi
application = default_app()


# globals #
tpl = SimpleTemplate("""
    <html>
    <head>
        <style>
            body {
                    background: #000;
            }
            .container {
                    background: -webkit-linear-gradient(top, #ACBDC8 0.0%, #6C7885 100.0%) no-repeat;
                    border: 3px solid #333;
            }
            .center_box {
                    // `font-family: Philosopher;
                    background-color: lightgrey;
                    margin: auto;
                    width: 75%;
                    border: 3px solid black;
                    padding: 10px;
                    margin-top: 20px;
                    margin-bottom: 20px;
                    }
            h2 {
                    // font-family: Helvetica;
                    font-family: Architects Daughter;
                    text-align: center;
            }
            div.title {
            margin-left: 5px;
            margin-right: 5px;
            margin-top: 10px;
            border-top: solid black 3px;
            text-align: center;
            font-size: 35px;
            border-bottom: solid black 2px;
            margin-bottom: 4px;
            }
            table, th, td {
                border: 1px solid black;
            }
            .grid-container {
                display: grid;
                grid-template-columns: auto auto auto;
            }
            .grid-item {
                text-align: center;
            }
           .footer {
                border-top: solid lightgrey 1px;
                padding-top: 3px;
                padding-left: 3px;
                padding-right: 3px;
                margin-right: 5px;
                margin-left: 5px;
                color: white;
                padding-bottom: 3px;
                border-bottom: solid lightgrey 1px;
                margin-bottom: 1px;
            }
               .rc_nav {
                overflow: hidden;
                background-color: #363841;
                text-align: center;
                z-index: 6;
                margin: 4px 4px 4px 4px;
              }
              .rc_nav a {
                display: inline-block;
               margin-right: -4px;  /* inline-block gap fix */
               color: #fff;
               padding: 5px 10px 5px 10px;
               text-decoration: none;
               font-family: Poppins;
               font-size: 16px;
               -webkit-transition: background 0.3s linear;
               -moz-transition: background 0.3s linear;
               -ms-transition: background 0.3s linear;
               -o-transition: background 0.3s linear;
               transition: background 0.3s linear;
               z-index: 9;
          }
          .rc_nav a:hover {
            background-color: #575b69;
            color: #bdfe0e2;
          }
          .rc_nav .icon {
            display: none;
          }

            .rc_content {
              text-align: center;
              padding-left:14px;
              font-family: Poppins;
              margin-top: 100px;
              color: #8e909b;
             }
            @media screen and (max-width: 820px) {
              .rc_nav a {display: none;}
              .rc_nav a.icon {
              float: right;
              display: block;
              width: 60px;
              }
            }
            @media screen and (max-width: 820px) {
              .rc_nav.responsive {position: relative; top: 73px;}
              .rc_nav.responsive .icon {
              position: fixed;
              right: 0;
              top: 0;
            }
            .rc_nav.responsive a {
              float: none;
              display: block;
              text-align: center;
            }
        }
        </style>
    </head>
    <body>
      <div class='container'>
        <div class='title'>
        {{title}}
        </div>
          <!-- Top navigation -->
      %if nav_d:
      <!--
      <div id="rc_logo">
        <a href="/" title="Organization">{{org}}</a>
      </div>
      -->
      <div class="rc_nav">
        % for k,v in nav_d.iteritems():
                 <a href="{{v}}">{{k}}</a>
        % end
      </div>
      <br>
      % end

        <div class='center_box'>
          {{!content}}
        </div>
        <div class='footer'>
          <div class='grid-container'>
          <div class='grid-item' style='text-align: left;'>  {{!left}}  </div>
          <div class='grid-item' style='text-align: center'> {{center}} </div>
          <div class='grid-item' style='text-align: right;'> {{right}}  </div>
          </div> <!-- class=grid-container -->
        </div> <!-- class=footer -->
    </div class='container'>
    </body>
    </html>
""")

# these are used to filter out warnings and errors from inxi 
#   - see def acceptible below
reject_strings = [
            "Use of uninitialized value",
            "Error",
            "print()",
            ]


# functions #
def acceptable(line):
    """
    determines if the line is acceptible based
    on a list of unacceptible strings (reject_strings)
    expects to find global defined reject_strings
    """
    for string in reject_strings:
        if string in line:
            return False  # line is not acceptable
    return True  # line is acceptible
    # end of def acceptible(line) #


def run_cmd(cmd, ret_type="str"):
    """
    run a command and return either a str or a list
    """
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]
    # proc is now a list of lines
    if ret_type != "str":
        return proc.split("\n")
    return proc
    # end of def run_cmd(cmd, ret_type="str") #


# classes #
class HtmlWrap:
    """
    This is basically and unskillfully used as a data container.
    Purpose: Allows setting of template vars and then renders the template when requested
    for the most part this class is just a data container (python2)
    there is not a real need for unique instance values - it gets set, and then called once, then dies with the end of a page rendering
    Use:
    @route('/')
    def index():
        content = "My Content"
        page = HtmlWrap(content=content,
                        title="System Info",
                        center="Awesome!")  # instantiates a class named page and sets the content
        page.org = "my.org"         # example
        return page.render()        # returns a template driven rendered html page
    """
    def __init__(self, content="I need content!", title="Title", center="Enjoy!", nav_d={}):
        self.content = content
        self.title = title
        self.nav_d = nav_d

        # footer vars
        self.org = "companionway.net"
        self.year = datetime.datetime.now().strftime('%Y')
        self.dtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

        self.left = self.org + " &copy; " + self.year
        self.center = center
        self.right = self.dtime

    def render(self):
        """
        render the html page using the var values inserted into global template (tpl)
        """
        output = tpl.render(title=self.title, 
                            content=self.content, 
                            nav_d=self.nav_d,
                            left=self.left, 
                            center=self.center, 
                            right=self.right,
                            org=self.org,)
        return output
    # end of class HtmlWrap #


# routes #
@route('/')
def index():
    """
    default route
		displays simple server environment and host information
    """
    content = ""  # initialiaze var
    hostinfo = socket.gethostbyname_ex(socket.gethostname())
    # deal with None type when run from CLI ...
    request_uri = request.environ.get('REQUEST_URI') if request.environ.get('REQUEST_URI') is not None else ""
    lines = [
        ['Remote IP:', request.environ.get('REMOTE_ADDR')],
        ['IP Address:', str(hostinfo[2])],
        ['Server Port:', request.environ.get('SERVER_PORT')],
        ['File:', os.path.basename(__file__)],
        ['Request URI:', request.environ.get('REQUEST_URI')],
        ['Document Root:', str(request.environ.get('DOCUMENT_ROOT'))],
        ['Referer:', request.environ.get('HTTP_REFERER')],
        ['HTTPS Protocol:', request.environ.get('HTTPS')],
        ['Server Software:', request.environ.get('SERVER_SOFTWARE')],
        ['Server Admin:', request.environ.get('SERVER_ADMIN')],
        ['uptime:', str(subprocess.check_output(shlex.split("uptime")).decode("utf-8"))],
        ['uname -a:', str(subprocess.check_output(shlex.split("uname -a")).decode("utf-8"))],
        ['User Agent:', request['HTTP_USER_AGENT']],
        # ['top:', "<br>" + run_cmd("top -bn 1 | head").replace('\n','<br>')],
        ['<hr>Date Time:', datetime.datetime.now().strftime('%Y%m%d-%H:%M')],
        ]

    for line in lines:
        content += "<b>" + str(line[0]) + "</b> " + str(line[1]) + "<br>"  
    page = HtmlWrap(content=content, title="System Info")
    page.nav_d={"Home":"/",
                "inxi": request_uri + '/inxi',
                "inxifull": request_uri + '/inxifull'
                }
    return page.render()


@route('/<new_route>')
def new_route(new_route):
    """
    This is a way to maintain use in as both a CLI application and a WSGI application in that the routes
    don't have to get muddled when you use a WSGIAlias with a subdir.
    All this does is take the route supplied to the script (that is not the root "/" and to match it to 
    any routes we want. Then it builds the content desired based on that route and finally runs it through HtmlWrap class
    which fills in defaults or set variables and pumps it through a template to return the html.
    Because all the routes are build directly off of the original requestes uri we can easily work with that to 
    construct other routes (as seen in the nav_d).
    """
    content = cmd = ""  # initialiaze vars
    # deal with None type when run from CLI ... yes, this is slightly different from above but it is because CLI doesn't like "" here.
    request_uri = request.environ.get('REQUEST_URI') if request.environ.get('REQUEST_URI') is not None else "/"
    base_request_uri = request_uri.replace("/" + new_route, '')  # for use in nav_d
    if new_route == "inxi":
        cmd = "inxi -F -c0"  # make sure you include -c0 for no ansi color codes which messes up html
    elif new_route == "inxifull":
        cmd = "inxi -wiFoldc0"
    else:
        content += "Not sure what you want... check your requested uri of [" + request_uri + "] please."
    if cmd != "":
        proc = run_cmd(cmd, "list")  # list is needed to make filtering easier (next step)
        lines = [line for line in proc if acceptable(line)]  # gotta love list comprehensions
        content += "<pre>" + "\n".join(lines) + "</pre>"  # maintains the output format and end of line feeds
    page = HtmlWrap(content=content, title="System Info", center=cmd)
    page.nav_d = {"nodeinfo": base_request_uri,
                  "inxi" : base_request_uri + '/inxi',
                  "inxifull" : base_request_uri + '/inxifull'
                  }
    return page.render()


if __name__ == '__main__':
    run(port=8080, debug=True, reloader=True)
# End of code #
```

You need to place this out of the Docroot to add some degree of security to this deployment.

## Apache Configuration ##

The second (and last) file needed is required to configure WSGI (in this case, for apache2).

Here is the file **wsgi.conf**:

```

##############
# vim: nospell
##############

WSGIScriptAlias /chkit/nodeinfo  /usr/local/www/wsgi-scripts/nodeinfo.py

<Directory /usr/local/www/wsgi-scripts>
	<IfVersion < 2.4>
		Order allow,deny
		Allow from all
	</IfVersion>

	<IfVersion >= 2.4>
		Require all granted
	</IfVersion>
</Directory>
```

<div class="sboxit">
This config file is configured establishes an alias as /chkit/nodeinfo - change as you desire.
</div>

Copy this file to /etc/apache2/confs-available (or similarly on other platforms). 

Then run: 

```sudo a2enconf wsgi```

and finally run:

```sudo systemctl restart apache2```  


<a name="download"></a>
## Download ##

Here you can find these files with a tar.gz compressed archive file.

- nodeinfo.zip <a href="/dlfiles/nodeinfo.zip" download>[download here]</a>


<a name="analysis"></a>
### Code Analysis ###
- description of python nodeinfo.py script 
	- The goal is to dynamically build a system info page.
	- I need to get one thing off the table right away. There is a problem with this script that, for the life of me, I can not seem to resolve.
		It calls through python's subprocess routine "inxi -Fc0". The -c0 is needed to prevent ansi color codes bleeding through into the html page.
		But the more serious issue is that when the run through WSGI on your server it drops errors that are ENVIRONMENT related. I tried lots of WSGI options (see below) to try to work around this issue but to no avail. So this code does a work-around... it filters out warnings and erros leaving cleaner output for html display. All working suggestions welcomed.
	- I am also offering another disclaimer: I like simple so everything needed for this script is all in one file. This is not ideal. One servers I actually wrote a separate python script module to hold a class that wraps the html and template code around the content built by the main script. It is all in one file here for simplicity.

- description of apache wsgi configuration
	- The wsgi.conf Establish an WSGIAlias to the nodeinfo.py script
	- It also sets the directory accessability for the script execution.
	- There are many options that can be configured using a WSGIDaemon directive [WSGIDaemon process](https://modwsgi.readthedocs.io/en/develop/configuration-directives/WSGIDaemonProcess.html)

<a name="debug"></a>
### Troubleshooting ###

- troubleshooting
	- run the code from the command-line and view with a browser
		- set bottle debug to get tracebacks
		- I use tilix for my terminal and it allows you to Ctrl-[Click] on the link and open the browser to that link. Your terminal probably has a similar shortcut capability
	- afer configuring apache2 and restarting (or reloading) the apache server view the apache error log to see any errors and tracebacks.
	- I also use linters (in this case pylint or similar) within vim that alerts you are you code to potential issues... [post: Vim ALE]( https://www.companionway.net/post/vim_ale/ )

<a name="postface"></a>
### Going further ###
- bottle - simply and amazing... simply amazing for small web based projects. Plugins are available to enhance bootle with many additional features or to ease adding new dimensions. Examples include authentication modules, session management, sqlalchemy, logging etc [bottle plugins](http://bottlepy.org/docs/dev/plugins/index.html).
- sqlite can easily be incorporated into a web application using bottle
- more info on WSGIDaemon
- separation of codei, templates, css files, etc
- one file vs many - the never ending debate that I constantly wrestle with.
	- one time use vs sharing amongst many
	- looking in one place or following the rabbit
	- sometimes small is beautiful
- launch another application and return sqlbrowser -> redirect... see app.py
- I am a "force" developer - I "refactor it" until it works - I force it to work. Sometimes I go back and "refactor it" to be pretty, or efficient, or, most often, to look cleaner (simple). Sometimes.
