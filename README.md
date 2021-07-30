[#](#) companionway
master branch
public = website www.companionway.net

Use something like this to make images usable:
convert static/img/fab_discover_sar.jpg -resize 750x375 static/img/fab_discover_sar-resized.jpg
or
mogrify -rotate 180 path/to/file.jpg

20210718-1508
To publish:
All done from the base dir: /home/geoffm/dev/www/companionway.net
hugo  <-- to build public
netlify deploy  <-- builds a dev site - you should QA it
then finally:
netlify deploy --prod

netlify failed to respect everything I tried for authorization with github
Ended up adding a special ssh key (defined in their docs) to my online netlify acnt and downloaded the npm netlify command (globally)
All of this was not easy - but I now can deploy directly with the ability to test the dev link before going to prod.

Enjoy!

------- README.md -------
    
Created on: 20181001-1617
Created by: geoffm
    
----- Last Code Changes -----
    
Modified on: 20210718-1507
Modified by: geoffm
   
------- README.md -------
