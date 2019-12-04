from django.db import models
import json
from ravenrpc import Ravencoin
from ravenvotes.settings import VOTE_ADDRESS_1, VOTE_ADDRESS_2

rvn = Ravencoin('user', 'pass')

def get_num_assets_by_addr(addr : str, asset_name : str) -> float:
    for asset in rvn.getaddressbalance(addr, True)['result']:
        if asset['assetName'] == asset_name:
            return asset['received'] / 1e8
    return 0

class Vote(models.Model):
    data = models.TextField(default='')
    asset_name = models.CharField(max_length=80, unique=True)
    creation_time = models.DateTimeField(auto_now_add=True)

    @property
    def loaded_data(self):
        return json.loads(self.data)

    def update_data(self) -> None:
        self.data = json.dumps({
            'address1_value': get_num_assets_by_addr(VOTE_ADDRESS_1, self.asset_name),
            'address2_value': get_num_assets_by_addr(VOTE_ADDRESS_2, self.asset_name),
        })
        self.save() 
