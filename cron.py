#!/usr/bin/python3.7
import time
import os
# Cron Sanity Test
#with open('/home/jonpizza/PYTHON/RVN/ravenvotes/cron.log', 'a') as c:
#    c.write(f'Accessed on {time.time()}\n')

os.environ["DJANGO_SETTINGS_MODULE"] = "ravenvotes.settings"

import django
django.setup()

from ravenrpc import Ravencoin

# this is where cron gets fed up
# from votes.models import Vote

import importlib.util
spec = importlib.util.spec_from_file_location("votes.models", "/home/jonpizza/PYTHON/RVN/ravenvotes/votes/models.py")
foo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(foo)
Vote = foo.Vote

rvn = Ravencoin('user', 'B4bgfdWk11e')

def valid_name(name):
    name = name.lower().replace('0', 'o').replace('1', 'l').replace('3', 'e')
    no_good = ['porn', 'sex', 'cock', 'dick', 'penis', 'boob', 'vagina', 'xxx', 'std', 'nigg', 'dildo']
    for i in no_good:
        if i in name:
            return False
    return True

def create_votes():
    print('creating...')
    known_assets = [vote.asset_name for vote in Vote.objects.all()]
    for asset in rvn.getaddressbalance('RSendHereToGetListedRavenvotecTNQG', True)['result']:
        print(asset)
        if asset['assetName'] not in known_assets and asset['assetName'] != 'RVN':
            if not valid_name(asset['assetName']):
                continue
            v = Vote(asset_name=asset['assetName'])
            v.save()
            print('\tCreated a vote.')

def update_votes():
    for vote in Vote.objects.all():
        vote.update_data()

create_votes()
update_votes()
print('done!')
