+++
date = "2019-03-12T09:18:43-04:00"
draft = false
title = "Python fabric - Dynamically Discover Hosts"
slug = ""
tags = []
image = "/img/fab_discover_sar.jpg"
comments = false  # set false to hide Disqus
share = false # set false to hide share buttons
#menu= ""   # set "main" to add this content to the main menu
author = ""
+++

Python fabric is a library tool for executing ssh commands remotely and responding as you desire.
I use python fabric for promoting code and web content. Essentially it is my devops tool to satisfy the 
single most important devops rule: never log into a server! I use this over ansible or some of the other
devop tools because fabric only requires knowning one langauge and that is python. 

My network changes a lot as I take servers down or stand them up frequently. Normally that would require changing
the environment roles (host lists) in my fabfile.py with all my changes. In the past I set aside certain IPs in my
network for each role. For example all my raspberry pies get named before I ever introduce them to the network.
Using the option --skip_bad_hosts with fabric is one way to do this but I really want more control.

<!--more-->

So my fabfilei.py would has something like this in it:

```
env.roledefs = {
      'rpis': ['rasp1', 'rasp2', 'rasp3', 'rasp4', 'rasp5', 'rasp6', 'rasp7'],
      'ubuntus': ['192.168.1.72'],
      'prsnl': ['artemis'],
      'rhat': ['f-node01'],
      'containers': ['u-node01', 'u-node02', 'f-node01'],
      'tst': ['rasp2', 'rasp7'],
      'websites': ['cos.tst', 'hype.companionway.net', 'companionway.net'],
      'to_level': {'dev': 'rasp5', 'stage': 'rasp2', 'prod': 'rasp1'}
  }
  env.roledefs['all'] = env.roledefs['rpis'] + env.roledefs['containers'] + env.roledefs['prsnl'] + env.roledefs['ubuntus']  # noqa
  env.roledefs['debs'] = env.roledefs['rpis'] + env.roledefs['containers'] + env.roledefs['prsnl'] + env.roledefs['ubuntus']  # noqa
```

Looks complicated but the point is that I have pre-listed servers whether they exist yet or not. In my /etc/hosts file all the hostname
have an IP assigned.


But what I really need is a way to build a list of servers that are up and have an ssh port open within a range of IPs on the network.
Specifically, I want fabric to scan 192.168.1.60 - 192.168.1.99 for live hosts with an open ssh port and then run a task against each.
That way a server can go up or be down and it has no bearing on fabric executing a selected task.

So here is my crude solution. If nothing else, it does demonstrate the flexibility of fabric.

This function is not declared as a task with the @task decorator. The purpose is just to test the socket on an IP

```
# ###########################
def check_socket(host, port, timeout=2, silent=False):
    # #######################
    """
    This seems to work pretty well for me
    use:
    if check_socket(env.host, int(env.port)) is True:
        with warn_only():
            run('uname -a')
    Note: port must be a string!
    """
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.settimeout(timeout)
        if sock.connect_ex((host, port)) == 0:
              if not silent:
                  print()
                  print("-"*60)
                  print("==== Host: [" + host + "] port: [" + str(port) + "] open ====")
                  print("-"*60)
              return True
          else:
              if not silent:
                  print("="*60)
                  print("==== Host: [" + host + "] port: [" + str(port) + "] closed ====")
                  print("="*60)
                  print()
              return False
```
I also wrote a function to poll a range of IPs on a network segment.
 
```
# ########################################
def poll_netseg(netseg,start_ip,end_ip, silent=False):
   # ###################################
   """
   discovery of live hosts on a selected port
   requires def check_socket
   netseg has to be 3 complete triplets including the last "." for the network segment: eg 192.168.1.
   returns a list of hosts_open
   Note: displays dots as it polls to let the user know that it is in fact scanning IPs
   """
   # flush=True is needed otherwise it won't print until the end of the poll (all at once which defeats the purpose)
   hosts_open = []
   print(f"Checking network segment {netseg} from {start_ip} to {end_ip} ", end='', flush=True)
   for ip in range(start_ip, end_ip):
       host_ip = netseg + str(ip)
       if not silent:
           print(". ", end='', flush=True)
       if check_socket(host_ip, 22, timeout=1, silent=True) is True:
           hosts_open.append(host_ip)
   print()
   return hosts_open
```

So here is the meat in this sandwich. This function allows you to execute the task that you want on the hosts that were
discovered to be alive.

```
# ############################
@task
def discover(func=hname, start_ip=60,end_ip=99):
    # ########################
    """
    purpose: discover hostnames dynamically and allow execution of selected function/task
    requires:
        poll_netseg()
            which requires setting env.netseg
            check_socket()
    input: be aware of the env.netseg, start_ip and end_ip
    """
    live_hosts = poll_netseg(env.netseg, start_ip, end_ip)
    execute(func, hosts=live_hosts)
```

It defaults to running a task called hname which gets the hostname but that can be overridden on the command line.
First lets look at the task called hname just so you can see how this works.

```
# ###################
@task
def hname():
    # ###########
    """
    eg: fab -R all hostname
    """
    with hide('output'), settings(warn_only=True):
        out = run("hostname -f")
        print(out)
```

The sweet nectar in the discover task is that you can tell fabric to run any task that you have written.
Here is how I call a task called sar which runs sar (system activity report from the sysstat package)

```
# ######################
@task
def sar():
    # ################
    """
    assures sar is installed and running and runs  sar | tail -10
    """
    with settings(warn_only=True):
        with hide('output'), settings(warn_only=True):
          sar_out = sudo('sar')
        if sar_out.return_code != 0:
            print(f"running sar failed so installing ...")
            sudo('apt install sysstat')
        r = sudo('grep -E "^ENABLED=.*true" /etc/default/sysstat')
        if r.return_code != 0:
            print("It appears sysstat is not ENABLED ... changing to true ...")
            sudo('sed -i -e \'/^ENABLED="false"/s/false/true/\' /etc/default/sysstat')  # noqa
    sar_out = sar_out.splitlines(True)
    for l in sar_out_l:
        if l.strip() == "":
					# skips blank lines
          print(l.rstrip())
```

To run that on all the live hosts:

```
fab discover:func=sar
 # or
fab discover:sar
```

Done - Enjoy
-g-
