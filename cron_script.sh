#! /bin/bash

#####
# Script to automate sitebuilding for heuteinmannheim.de on the server
#####

cd ~/heuteinmannheim
git checkout master
git pull
python3 ~/heuteinmannheim/heuteinma.py
cp -r ~/heuteinmannheim/static/* /srv/www/heuteinmannheim.de/
exit
