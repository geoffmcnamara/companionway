#!/usr/bin/env python3

from os import listdir
from os.path  import isfile, join
import random

mypath = "/home/geoffm/dev/www/companionway.net/static/img/misc"
base = "/img/misc/"

files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

# print(f"files: {files}")

pic = random.choice(files)
pic = base + pic

print(f"{pic}")


