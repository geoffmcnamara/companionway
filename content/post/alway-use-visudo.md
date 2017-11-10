+++
author = ""
comments = false
date = "2016-12-14T10:59:38-05:00"
draft = false
image = "/img/visudo.jpg"
menu = ""
share = true
tags = ["sudo"]
title = "Always Use Visudo"

+++

>>"Familiarity breeds contempt"

I get very comfortable with using the vim editor (take cover... flame way ensuing) so
comfortable that using any other editor leaves me just a bit unnerved. I constantly use it
to update sudoers. The best way to modify sudoers is to add a supplimental inclusion file under
/etc/sudoers.d/whatevername - so the other day I needed to add an entry to allow the user for my
simple monitoring program (xymon) to be able to run "sudo ufw status" without a password and report
back to the monitor server.

I fired up ```sudo vim /etc/sudoers.d/xymon``` and started to add the needed line:
``` xymon ALL = NOPASSWD: /usr/sbin/ufw status``` but I got halfway through and could remember the exact location
<!--more-->
of the ufw binary file.. so I saved got out and I just sawed off the limb I  was standing on. Sudo is not totally broken so I had togo to the phsical machine (which happened to be a raspberry pi) hook up a monitor and keyboard and fix it by logging in as root and finish editing the sudoers supplimental file correctly. I did it the proper way this time; I used visudo which protects you from yourself.

Lesson: *Always use visudo*

By the way, to change the default editor from nano to vim for visudo (on unbuntu at least) you can run:
```sudo update-alternatives --config editor```

On my systems that exchange looks like this:
```
$ sudo update-alternatives --config editor
There are 4 choices for the alternative editor (providing /usr/bin/editor).

  Selection    Path                Priority   Status
------------------------------------------------------------
* 0            /bin/nano            40        auto mode
  1            /bin/ed             -100       manual mode
  2            /bin/nano            40        manual mode
  3            /usr/bin/vim.basic   30        manual mode
  4            /usr/bin/vim.tiny    10        manual mode

Press <enter> to keep the current choice[*], or type selection number: 3
update-alternatives: using /usr/bin/vim.basic to provide /usr/bin/editor (editor) in manual mode
```
   
Enjoy
-g-
