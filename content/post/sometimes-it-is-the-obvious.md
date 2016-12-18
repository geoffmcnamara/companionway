+++
author = ""
comments = false
date = "2016-12-15T16:36:42-05:00"
draft = false
image = ""
menu = ""
share = true
slug = "post-title"
tags = ["tag1", "tag2"]
title = "Sometimes It Is The Obvious"

+++

This was one of those "problems" that nagged me for many hours until the obvious dawned on me.
I wrote a pythone script to grab the temperature and humidiy from a DHT22 sensor and then write the
output with the proper syntax to send to my monitoring program [xymon]. The wrapper bash script ran
every 5 minutes and used a redirection to write out a file ie:
```
*/5 * * * * /usr/local/bin/temphum.sh >/tmp/temphum.dat
```
The wrapper script grabs output and sends it to the server. Having this wrapper script lets me run the 
python script independantly for testing or for curiousity.

<!--more-->
It all worked fine but sometimes the temp would jump in one direction or another for brief period and that
skewed the graphed - it was ugly so I decided to fix it.

I added code to the python script to look at the temperature that got recorded on the last run into the /tmp/temphum.dat
file and then judged if the measured temperature greater or less than the "last" temp by a amount greater than a "trigger" amount (I orignally set the trigger to be a full degree, that is 1.0). If the difference between the last and the measured temp was greater 
than the "trigger" then I adjusted the measured temp up or down appropriately by and adjustment amount (0.2). This would smooth
out the graph and with the readings being taken each 5 minutes everything would work out fine over time.

It all worked fine each time I ran it from the command line. But when the the temperature recorded into the /tmp/temphum.dat
file was always the measured temp. The adjusted temperature never made it into the file unless I ran it from the command line.
I assumed the problem was with the environment - this is a natural assumption given that when a cron job runs it inherits no
environment settings. I adapated the python script to have its own environment PATH and I also changed the bash wrapper script
to preset it's own PATH settings. But all to no avail.

Then I realized the problem. As soon as the wrapper script runs, it opens a redirection out to >/tmp/temphum.dat. That is also the
file that the python script reads but as soon as the redirection starts it "zeros out" the file - it builds an empty file. Now the
python script has no "last" temperature to read and my script rightfully drops a null last temperature reading and therefore does no adjusting. 

The solution was to drop the redirection from the cron entry and have the python script first open the /tmp/temphum.dat file for reading the last temperature, close the file, do the adjustment calculation, then re-open the file for "w"rite which empties the file for writing new content, then write the needed message lines to the file, and then close the file.

All is good now. So easy to overlook the simple/obvious show stopper.

Enjoy
-g-
