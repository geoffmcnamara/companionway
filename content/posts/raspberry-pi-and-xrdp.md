+++
author = ""
comments = true
date = "2016-12-16T12:27:36-05:00"
draft = false
image = "/img/raspberry-pi-card.jpg"
share = true
tags = ["raspberry", "rdp"]
title = "Raspberry Pi and Xrdp"

+++

I decided to have some remote desktop fun with one of my raspberry pies. Remote desktop for the raspberry pi (or
any linux machine) can be done so many different ways - but the easiest from my perspective is xrdp. It is available 
really on any linux distro and works with Windows remote desktop protocol (kinda). It requires that you install
xrdp and tightvncserver (under the covers it uses a vnc server - thightvncserver is probably the best choice here).
Then as a client on my laptop I use the very good remote desktop client called remmina; again it is availalbe on
almost any linux distro.

<!--more-->

When you launch remmina it will ask for a username and password for a connection onto the IP machine you declare in the setup.
If the xrdp service is properly running on the remote machine it will server up a personal desktop for the user login 
independant of any other desktop sessions that might be running.
But - I am a fan of enlightment desktop e17 for a whole lot of reasons, many of which are personal history. Enlightenment desktop
is lightweight so it works well on a raspberry pi. My task was to install e17 onto the raspberry pi and it becomes an
alternet desktop and then make it available to me over xrdp. My quick searches on the internet turned up a good deal of bogus
dead ends but I looked over the startup scripts for xsession and noticed it by default looks for and will launch

``` $HOME/.xsession```. 

I am using Raspbian 8.0 debian jessie on my raspberry pi. Well, no, actually, I am using berryboot to launch Rasbian 8.0 but that
has no bearing on this discussion. Rasbian now comes with the pixel desktop which includes the lxterminal program by default
so I call that up in my ```$HOME/.xsession``` script before launching the enlightnement destop. Here is my script

```
#!/usr/bin/env bash
lxterminal &
enlightenment_start
```

Then restart the xrdp service with:
```
sudo systemctl restart xrdp.service
```

If it is your first launch of enightenment you will have to go through the brief setup - for the most part, pick the defaults and happy days are here again.

Oh but then you will run into this rather serious problem - half of your keys won't work! I have a solution but it probably
isn't the best solution - it just happens to be the  only one I came across that worked for me.
Use the mouse in enlightenment and navigate through ```Settings->All->Input->Key Bindings ... click on Delete All```
This works and you lose keybindings that you probably wouldn't use through vnc anyway.
 

Enjoy
-g-
