import requests
import datetime
from typing import *
import json
import base64

"""
Example of raw account
{
    'id': 'e4af30e11033405ebb6826d038e56173',
    'name': 'LeDevBloog_e',
    'properties': [
        {
            'name': 'textures',
            'value': 'ewogICJ0aW1lc3RhbXAiIDogMTY5ODY1MjQzMTAwMiwKICAicHJvZmlsZUlkIiA6ICJlNGFmMzBlMTEwMzM0MDVlYmI2ODI2ZDAzOGU1NjE3MyIsCiAgInByb2ZpbGVOYW1lIiA6ICJMZURldkJsb29nX2UiLAogICJ0ZXh0dXJlcyIgOiB7CiAgICAiU0tJTiIgOiB7CiAgICAgICJ1cmwiIDogImh0dHA6Ly90ZXh0dXJlcy5taW5lY3JhZnQubmV0L3RleHR1cmUvYjRlZjdlOTljYjY0YWNmM2E1NDk5OTNmNDJlNWIxYmI0ZTc3MzBhNjRkMmYzZDQyNDE5NWUxOWJjYjVhMWEzYSIKICAgIH0KICB9Cn0='
            }
        ], 
    'profileActions': []
}
"""
class ProfileTextures:
    def __init__(self,value:str): # value is the value field of the textures in properties
        details = json.loads(base64.b64decode(value).decode())
        try:
            self.timestamp = datetime.datetime.fromtimestamp(details["timestamp"])
        except:
            try:
                self.timestamp = datetime.datetime.fromtimestamp(details["timestamp"]/1000)
            except:
                self.timestamp= datetime.datetime.now()
        self.textures = details["textures"]
    def _get_texture_url(self,texture:str) -> str:
        for i in self.textures:
            if i.lower() == texture.lower():
                return self.textures[i]["url"]
        return None # In case we didn't found the texture
    def get_texture_data(self,texture) -> str:
        url = self._get_texture_url(texture)
        if not url:
            return None
        return requests.get(url).text
class ProfileProperties:
    def __init__(self,properties:list[dict]):
        for i in properties:
            if i["name"] == "textures": # We got a textures
                setattr(self,i["name"],ProfileTextures(i["value"]))
            else:
                setattr(self,i["name"],i["value"])
class Profile:
    def __init__(self,details:dict[Any]):
        self.name = details["name"]
        self.id = details["id"]
        self.properties = ProfileProperties(details["properties"])
        self.actions = details["profileActions"]

class Account:
    def __init__(self,name:str="",id:str="",invalid:bool=False):
        self.invalid = invalid
        self.name = name
        self.id = id
        
class MojangApi:
    """
    MojangApi
    Communicate with the mojang servers
    Here, an account is a class with an id or a name, or both, and
    a Profile is a class with every properties that we can gather about a minecraft profile
    """
    def get_profile_from_id(self,id):
        data = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{id}?unsigned=false").text
        if not data or "Not a valid UUID" in data:
            raise TypeError("This id is invalid")
        data = json.loads(data)
        return Profile(data)

    def get_multiples_account_from_ids(self,ids:list[str]):
        if type(ids) not in [list,tuple]:
            raise TypeError("The \"ids\" argument must be a list or a tuple of ids.")
        data = requests.post(
            "https://sessionserver.mojang.com/session/minecraft/profile/lookup/bulk/byname",
            json = ids
        )
        not_found_list = list(set(ids) ^ set([x["id"] for x in data]))
        invalid_accounts = [Account(id=i,invalid=True) for i in not_found_list]

        valid_accounts = [Account(name=i["name"],id=i["id"]) for i in data]
    
    def get_account_from_name(self,name):
        data = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{name}").text
        if not data or "Couldn't find any profile with name " in data:
            raise TypeError("This name is invalid")
        data = json.loads(data)
        return Account(**data)

    def get_profile_from_account(self,account:Account) -> Profile:
        if account.invalid:
            raise TypeError("This account is not valid")
        return self.get_profile_from_id(account.id)
        
        

if __name__ == "__main__":
    m = MojangApi()
    p=(m.get_profile_from_account(m.get_account_from_name("LeDevBloog_e")))
    print(p.properties.textures._get_texture_url("skin"))