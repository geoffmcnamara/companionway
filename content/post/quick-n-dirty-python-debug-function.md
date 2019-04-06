+++
author = ""
comments = true
date = "2016-12-22T14:08:05-05:00"
draft = false
image = "/img/python-logo.png"
share = true
title = "Quick N Dirty Python Debug Function"
tags = ["python","debug"]
+++


Pdb is a great debugger for python but I like to use my own simple debug functions. 
Here is a simple debug function for python which could definitely be improved:

<!--more-->

```python
#!/usr/bin/env python

import os
import sys
from inspect import (getframeinfo, currentframe, getouterframes)


DBUG=2 # will print to stdout if set to 1 -- use 2 to add funcname and funcdocs
#DLOG=os.path.basename(sys.argv[0])+".log" # will append to log to file if this is not commented out

def dbug(msg):
  """
   At the top of your script set these global values:
    from inspect import (getframeinfo, currentframe, getouterframes)
    DBUG=2 # will print to stdout if set to 1 -- use 2 to add funcname and funcdocs
    #DLOG=os.path.basename(sys.argv[0])+".log" # will append to log to file if this is not commented out
   Function: dbug() will print (or log) DEBUG: (datetime) [lineno] msg
   print this function doc with CLI help(dbug) or CODE dbug.__doc__
   needs: from inspect import currentframe.
   Simple to use... dbug("my message here")
   """

  cf = currentframe()
  msg="DEBUG: ["+str(cf.f_back.f_lineno)+"] "+msg

  try:
    if DBUG==2:
      fname=str(getframeinfo(currentframe().f_back).function)
      fdoc=eval(fname+.__doc__
      fdoc=fdoc if fdoc else 'undocumented'
      msg=msg+" Func: "+fname+" Doc: "+fdoc
  except:
    pass

  try:
    if DLOG != "":
      fh_dbug=open(DLOG,"a")
      fh_dbug.write(dtime+" "+msg+"\n")
      fh_dbug.close
  except:
    pass

  try:
    if DBUG>=0:
      print msg
  except:
    pass

def myFunc(myvar="eulav"):
  """
   myFunc("something") -requires one string
   prints out the string backwards - it uses the extended slice operator
   ie [begin:end:step]
   The default here prints "value"
  """
  dbug("how does it work")
  print myvar[::-1]

### Main Code ###
if __name__ == '__main__':
  dbug("Please note that the name of this function is dbug -- not debug just to avoid conflicts elsewhere")

  dbug("How does this work?")
  myFunc("this is my string")

  DBUG=1
  dbug("And now the reverse")
  myFunc("gnirts ym si siht")

  dbug("Let see what the default is...")
  myFunc() # reverses the default
### EOF ####
'''

Output from this should look something like this:
```
DEBUG: [97] Please note that the name of this function is dbug -- not debug just to avoid conflicts elsewhere
DEBUG: [98] How does this work?
DEBUG: [92] how does it work Func: myFunc Doc:
   myFunc("something") -requires one string
   prints out the string backwards - it uses the extended slice operator
   ie [begin:end:step]
   The default here print "value"

gnirts ym si siht
DEBUG: [102] And now the reverse
DEBUG: [92] how does it work
this is my string
DEBUG: [105] Let see what the default is...
DEBUG: [92] how does it work
value
```

Enjoy!
-g-





###
Enjoy
-g-
