#!/usr/bin/env python3
# vim: set syntax=none nospell expandtab ts=4 sw=4:
# ###################################### #
# Author: geoffm.companionway@gmail.com  #
# ###################################### #
#       -*- coding: utf-8 -*-            #

# ###################################### #
#              WIP TODO                  #
# ###################################### #


# ### IMPORTS ### #
import sys
from datetime import datetime
from docopt import docopt
# export PYTHONPATH=$PYTHONPATH:/home/geoffm/dev/python/gmodules
from dbug import dbug
from gtools3 import do_edit, printit, do_close, do_logo, run_cmd, askYN
import http.server
import socketserver
import os


# ### GLOBALS ### #
dtime = datetime.now().strftime("%Y%m%d-%H%M")

# ### CLASSES ### #

# ### FUNCTIONS ### #

# ###################
def handleOPTS(args):
    # ###############
    """
    Usage:
        myprog [-hTE]

    Options:
        -h --help    show this help
        -T           test
        -E           edit this file
    """
    dbug(args)  # comment this line out 
    do_logo("", 'center', 'box', 'shadow', box_color='red')
    if args['-E']:
        do_edit(__file__)
        sys.exit()
    if args['-T']:
        """
        see in vimrc:
        nmap <Leader>dc <Esc>:! % -t "
        """
        import doctest
        doctest.testmod(verbose=True, report=False, raise_on_error=False, exclude_empty=False)
        sys.exit()
    # ### EOB def handleOPTS(args): ### #

def handler_from(directory):
    def _init(self, *args, **kwargs):
        print(f"Directory: {directory}")
        return http.server.SimpleHTTPRequestHandler.__init__(self, *args, directory=self.directory, **kwargs)
    return type(f'HandlerFrom<{directory}>',
                (http.server.SimpleHTTPRequestHandler,),
                {'__init__': _init, 'directory': directory})



# #################
# ### Main Code ###
# #################
def main(args):
    # #############
    """
    >>> do_close()
    Enjoy!

    """
    rc = 0
    handleOPTS(args)
    cmd = "hugo --gc --minify"
    printit(f"Building out ./public dir ... Running: {cmd}")
    run_cmd(cmd)
    askYN()
    printit("Check the site first!")
    PORT = 1313
    DIRECTORY = "./public"
    printit(f"Launching python HTML server on ./public dir...")
    with socketserver.TCPServer(("", PORT), handler_from(DIRECTORY)) as httpd:
        print("Please clear your cache... refresh the page...")
        print(f"Serving at: http://localhost:{PORT}")
        httpd.serve_forever()
    cmd = "netlify deploy"
    run_cmd(cmd)
    askYN()
    printit("Make sure you have checked the site!")
    cmd = "netlify deploy --prod"
    run_cmd(cmd)
    return rc


if __name__ == '__main__':
    args = docopt(handleOPTS.__doc__, version=" 0.9")
    rc = main(args)
    do_close(rc=rc)
