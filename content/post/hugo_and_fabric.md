+++
comments = true
date = "2018-07-14T15:33:19-05:00"
draft = false
share = true
title = "Hugo and Fabric"
+++

Python Fabric is a denatured version of ansible and, if you enjoy python, fabric makes a small scale devops strategy a whole lot less painful.
Combined with hugo static website generator, fabic makes testing and promoting a website a whole lot easier.

I have struggled in the past with one challenge that made promoting website code from my workbench to dev, staging, and ultimately production tricky.
The matter of URL always played havoc when I sent code up from one server to another for testing. Hugo offers a simple solution. When I promote website
code it goes through this workflow process:

<!--more-->

- requirements and design
- code development
- workbench (my laptop or desktop) testing
- git add, git commit
- promote code to dev server(s) - with rsync or git 
- test dev website
- promote code to staging
- test staging website
- promote to production server(s)
- test production website

If I am working on code for a website it resides in development directory with the website domain name for the base directory... for example:

```
domain = "companionway.net"
base_dir = $HOME/dev/www/{domain}
```
This works cleanly for me. In hugo config.toml file you have to declare the url so I give it the full domain name ie:

```
baseURL = "http://companionway.net"
```

The problem, of course, manifests with promoting code to another server at a level that is not the fully qualified domain (FQD) production url.
That is where hugo allows the -b [your_base_url] option to save the day. To show an example, I have my development server document root as 
`/var/www/html` and each website I am working on has its name off of that. My development server(s) and raspberry pi (cheap) so they have clever names
like `rasp01`, `rasp02`, etc. So the code for "companionway.net" resides at `raspXX:/var/www/html/companionway.net`. The hugo build command of
`hugo -d "https://raspXX/companionway.net` allows me to go to that url to test the code and all the links will work properly. When the code goes to the production
level with a fully qualified domain name with a DNS A record the hugo build command simply is `hugo` and the default baseURL is used from the config.toml file.

The fabric process I use has a lot of steps but might be worth something to someone out there... once gain it comes with my standard "it can be dome better' clause:

Here is my fabfile.py that allows promoting ... read'em and weap ...

```
from fabric.api import env,run,local,lcd,cd,sudo,put,get,prompt,reboot,roles,settings,task,warn_only,abort,hide
from fabric.colors import *
from fabric.contrib.files import exists
import subprocess
import sys
sys.path.append("/home/geoffm/dev/python/gmodules/")
from dbug import dbug, trace  # my own dbug tools
import functools
from datetime import datetime


dtime = datetime.now().strftime("%Y%m%d-%H%M") 

env.user = "geoffm"

# ####################
env.roledefs = {
    'rpis':['rasp1','rasp2','rasp3','rasp4','rasp5','rasp6','rasp7'],
    'ubuntus':['192.168.1.72'],
    'prsnl':['artemis'],
    'rhat':['f-node01'],
    'containers':['u-node01','u-node02','f-node01'],
    'tst':['rasp2','rasp7'],
    'websites':['cos.tst','hype.companionway.net','companionway.net'],
    'dev':'rasp5',
    'stage':'rasp2',
    'prod':'rasp1'
}
all=env.roledefs['rpis']+env.roledefs['containers']+env.roledefs['prsnl']
# ####################


# Note: @task is just a decorator that adds some features to the wrapped function - ie adds it to "fab -l"
#   this allows use of namespacing
# env.hosts = 'rasp1','rasp2','rasp3','rasp4','rasp5','rasp6','rasp7'

# ###########
def help():
    # #######
    msg = """
    fab sethost:"rpis" udug  # will select the host group "rpis" and run the task udug (update->upgrade dist)
    """
    print(msg)
    dbug(f"task:{task.__doc__}")
    exit


# ##################
def test_site(site):
    # ##############
    """
    test_site(site) # promts the user to run all tests on the site and respond to verifiy question
    """
    try:
        local('hugo server -v -b "http://localhost"')  # forces the baseURL to be at this location
    except KeyboardInterrupt:
        print(f"\n\n\nInterrupted site test for: {site}.\n\n\n")
        r = prompt("Were the results of your testing complete and satisfactory?", default="n")
        # if r == "y" or r == "Y":
        if r:
            proceed = True
        else:
            proceed = False
    return proceed


# ################
def do_title(s,llen=50):
    # ###########    
    """ 
    prints a title block of length llen with supplied string s
    """
    slen = len(s)
    margin = "=" * (int((llen-slen)/2) - 1)
    title = (f"{margin}[    {s }    ]{margin}")
    title_len = len(title)
    print("\n"*3)
    print("=" * title_len)
    print(title)
    print("=" * title_len)
    print("\n"*1)


@task
# #########################################
def promote(to_level="where",stack="websites"):
    # #####################################
    """
    def promote(to_level="where",stack="what") default: stack="websites"
    eg. def promote("staging","websites")
    fab promote:stage,websites  # promotes websites to stage platform
    """
    user=env.user

    # user can deploy just one site eg: fab promote:dev,companionway.net
    sites_dir = f"/home/{user}/dev/www/"
    if stack == "websites":
        sites=env.roledefs['websites']
    else:
        sites = [ stack ]

    # build the test_approved.flag filename, with basename and extention name for use later
    taff_base = "test_approved" # needed for moving the file after a push
    taff_ext = "flag"
    taff = f"{taff_base}.{taff_ext}"  # alias test_approved.flag file
    
    # loop through site(s)
    for site in sites:
        dbug(f"site:{site} user:{user} sites_dir:{sites_dir}")
        do_title(site)
        site_dir = f"{sites_dir}/{site}/"
        with lcd(site_dir):  # change dir to the site to work on
            r = local('pwd')
            cmd = f"test -f {taff}"  # there is a way to do this with a fabric exists call BTW
            # ### turn errors off so script continues through the loop od sites
            with settings(warn_only=True):
                # ### test for existing test-approved.flag file (taff)
                r = local(cmd)
                # dbug(f"r:{r}")
                if r == 0:
                    dbug(f"\nFound the file: {taff}\n")
                    proceed=True
                else:
                    # dbug(f"Failed to find file: {taff}")
                    # dbug(f"need to run a site test")
                    proceed = test_site(site)
                    # ### create test_approved.flag file ### #
                if proceed:
                    # ### create a new test_approved.flag file (taff)
                    msg = f"\n\n\n{dtime} Test successful. Approved by: {user}"
                    cmd = f"echo {msg} > {taff}"
                    local(cmd)

                    # ### rm public ### #
                    local('rm -r ./public')  # remove the /public tree recursively to avoid any left over extraneous files

                    # ### run git commands (after /public removed although /public is in .gitignore as well)
                    local('git add -A')
                    local('git commit')

                    # ### hugo set vars then create public ###
                    if to_level == 'dev': 
                        trgt = env.roledefs['dev']  
                    elif to_level == 'stage': 
                        trgt = env.roledefs['stage']  
                    elif to_level == 'prod': 
                        trgt = env.roledefs['prod']  
                    else:
                        # trgt = "unknown":
                        print(red(f"Unsure of to_level [{to_level}]... exiting"))
                        exit()
                            
                    # hugo build (/public) with specified root/baseURL (domain) name
                    # there is a better way to do this ... by declaring the a key:value pair for each to_level:site... this is an easy cop-out
                    if to_level == 'dev' or to_level == 'stage':
                        cmd = f'hugo -b "http://{trgt}/{site}/"'  # overides the baseURL setting in config.toml
                    elif to_level == 'prod':
                        cmd = 'hugo -v'  # This allows the declared baseURL in config.toml to take effect
                            
                    else:  # this should be dealt with above in creat /public block ... but just in case
                        cmd = ""  # clearing cmd just in case
                        print(red(f"Unsure of to_level [{to_level}]... exiting"))
                        exit()
                    local(cmd)  # run whatever cmd has been set

                    # ### xfer files to promote lvl ### #
                    if to_level == 'dev' or to_level == 'stage':
                        # r = exists('/var/www/html/{site}')
                        # dbug(f"r:{r}"); exit()
                        cmd = f'rsync -av ./public/* {trgt}:/var/www/html/{site}/'  
                    elif to_level == 'prod':
                        if site == "companionway.net":
                            cmd = f"git push origin master"
                        else:
                            cmd = f'rsync -av ./public/* {trgt}:/var/www/html/{site}/'  
                    else:
                        print(red(f"Unsure of to_level [{to_level}]... exiting"));exit()
                        r = True
                        exit()

                    r = local(cmd)

                    if r.failed:
                        print("\n"*3)
                        print(red(f"Houston, there was a problem with: {cmd} result:{r}"))
                        print(f"output:{r.stdout}")
                        print(red(f"Please investigate... removing {taff}"))
                        local(f'rm ./{taff}')
                        print(red("Exiting..."))
                        exit()

                    # ### add msg to test_approved.flag file of msg=f"{site} promoted to {to_level} {dtime}"
                    msg = f"{site} promoted to {to_level} {dtime}"
                    do_title(green(msg))
                    cmd = f"echo {msg} >> ./{taff}"
                    local(cmd)

                    # ### move test_approved.flag file (taff) to {taff}.{dtime}
                    cmd = f'mv {taff} {taff_base}-{dtime}.{taff_ext}'
                    local(cmd) 
                    
                    # ### tell user to go test site on to_level
                    print("\n"*3)
                    print('----------------------------------------------------------')
                    print(f"Please test [{to_level}]: http://{trgt}/{site}  # in tilix: highlight the link and hit Ctrl-click")
                    print('----------------------------------------------------------')
                    print("\n"*1)
                    prompt("Continue? [Y]")

                else:
                    print("\n"*3)
                    print('----------------------------------------------------------')
                    print(f"You need to research and re-test site: {site}.")
                    print('----------------------------------------------------------')
                # end of: if proceed is true or false
            # end of with warn_only=True [encounterred error within script has exit() turned off] so that the loop continues
        # EOLoop
    return

@task
def sethosts(group="list"):
    """
    sethosts(group=list)
    use: fab sethosts:\"rpis\" udug
    """
    if group == "all":
        env.hosts = all
        dbug(f"hosts all:{env.hosts}")
        return
    if group == "list":
        for k,v in env.roledefs.items():
            print(f"{k}={v}")
    else:
        try:
            env.hosts=env.roledefs[group]
            print(f"Selected group:{env.hosts}")
        except:
            dbug(f"Unrecognized group[{group}]...")

@task
def getos():
   with settings( hide('warnings', 'running', 'stdout', 'stderr'),
        warn_only=True):
        if run('ls /etc/lsb-release'):
            os = 'ubuntu'
        elif run('ls /etc/redhat-release'):
            os = 'redhat'
        print(os)
        return os

@task
def lxclist():
    local('lxc list')

@task
def lxcstartall():
    env.warn_only=True
    local('lxc start --all')
    lxclist()

@task
def lxcstopall():
    env.warn_only=True
    local('lxc stop --all')
    lxclist()

@task
def lxcrestartall():
    env.warn_only=True
    local('lxc restart --all')

@task
def createlxcnode(name):
    """ 
    Use fab createlxcnode:myname 
    """
    cmd="lsb_release -r | awk '{print $2}'"
    rel = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    print(rel.stdout.read())
    # rel = subprocess.check_output(cmd.split(),stderr=subprocess.STDOUT)
    cmd=f"echo lxc launch ubuntu:{rel} {name}"
    local(cmd)
    
@task
def updatehosts():
    # use hand writtend script in this dir (for now) WIP
    local('./update-hosts.sh')

def uname_a():
    """
    runs: uname -a 
    """
    with settings(warn_only=True):
        run('uname -a')

def top():
    run('top -b -n 1 | head')

def df():
    run('df -H | grep "dev"')

def uptime():
    run('uptime')

@task
def status():
    with settings(warn_only=True):
        uname_a()
        uptime()
        df()
        top()

@task
def apt_update():
    sudo('apt update')

@task
def aptfullupgrade():
    apt_update()
    sudo('apt -y full-upgrade')

@task
def udug():
    apt_update()
    aptfullupgrade()

@task
def instbasics():
    with settings(warn_only=True):
        r = sudo('apt -y install vim git alpine inxi screen lynx xymon-client')
    if r.failed:
        r = sudo('dnf install vim git alpine inxi screen ') 

# if you run "fab tst" then this next block fires off for all the hosts listed in containers
# this just an example
@task
@roles('containers')
def tst():
    with cd('/tmp'):
        print("Gathering file names from /tmp")
        sudo('ls -l')

@roles('rhat')
def dnfupgrade():
    sudo('dnf upgrade')

@task
def adduser(node, user=""):
    """ use: fab adduser(nodename,username) WARNING: assumes (defaults) username is your username 
        your pub key will be copied over to this account
        gives sudo privileges to the user
        adds ssh passwordless login with your puplic key
    """
    import getpass
    if user == "":
        user=getpass.getuser()  # sets user to current user
    cmd=f'lxc exec {node} -- bash -c "adduser {user}"'
    from fabric.contrib.console import confirm
    print(f"\n\n\nPlease confirm: node:{node} user:{user} ")
    if not confirm("Continue? "):
        abort("Aborting as requested...")
    with warn_only():
        local(cmd)
    cmd=f'echo "{user} ALL=(ALL) NOPASSWD: ALL" > ./{user}'
    local(cmd)
    local("chown root ./{user}")
    cmd=f"lxc file push ./{user} {node}/etc/sudoers.d/{user}"
    local(cmd)
    cmd=f"cat /home/{user}/.ssh/id_rsa.pub >> ./{user}-key.pub"
    local(cmd)
    cmd=f"lxc file push {user}-key.pub {node}/root/{user}-key.pub"
    local(cmd)
    cmd=f'lxc exec {node} -- bash -c "mkdir /home/{user}/.ssh"'
    local(cmd)
    cmd=f'lxc exec {node} -- bash -c "cat /root/{user}-key.pub >> /home/{user}/.ssh/authorized_keys"'
    local(cmd)

@task
def rpibasics():
    """
    install basic apps specific to the needs of rpi like xrdp
    """
    sudo('apt install xrdp')

@task
def webit():
    """
    get apache up and running with skel structure
    """
    sudo('apt -y install apache2 libapache2-mod-php ')
    # sudo('apt install php-pear php-fpm php-dev php-zip php-curl php-xmlrpc php-gd php-mysql php-mbstring php-xml libapache2-mod-php')  # if you want to rule the world
    # sudo('mkdir /var/www/html/chkit')
    put('/home/geoffm/dev/www/skel/chkit','/var/www/html/',use_sudo=True) 
'''

This seems long and ugly but it works for me solidly.

Enjoy,
-g-

