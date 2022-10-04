import requests
from ncc_library import page_struct, types

class basic():
    def __init__(self):
        self.header = {
            "Content-Type":"application/json",
            "x-auth-token":"",
            "x-refer-page":"",
            "authority":"ccapi.nebula.zyxel.com"
        }

        self.org = ""
        self.site = ""
        self.base_url = "https://ccapi.nebula.zyxel.com"
    def set_auth_token(self, key):
        self.header['x-auth-token'] = key

    def nebula_req(self, page:page_struct):
        if(page.type == types.REQ_POST):
            return self.nebula_post(page, page.data)
        elif(page.type == types.REQ_GET):
            return self.nebula_get(page)

    def nebula_get(self, page:page_struct):
        get_url = self.base_url + page.url
        self.header['x-refer-page'] = page.ref
        self.header['page'] = page.url
        response = requests.get(url=get_url, headers=self.header)
        return response

    def nebula_post(self, page:page_struct, data):
        get_url = self.base_url + page.url
        self.header['x-refer-page'] = page.ref
        self.header['page'] = page.url
        response = requests.post(url=get_url, headers=self.header, data=data)
        return response

    def nebula_put(self, page:page_struct, data):
        get_url = self.base_url + page.url
        self.header['x-refer-page'] = page.ref
        self.header['page'] = page.url
        response = requests.put(url=get_url, headers=self.header, data=data)
        return response
    def nebula_raw(self, type:types, url, ref, data=""):
        if(type == types.REQ_POST):
            get_url = self.base_url + url
            self.header['x-refer-page'] = ref
            self.header['page'] = url
            response = requests.post(url=get_url, headers=self.header, data=data)
            return response
        elif(type == types.REQ_GET):
            get_url = self.base_url + url
            self.header['x-refer-page'] = ref
            self.header['page'] = url
            response = requests.get(url=get_url, headers=self.header)
            return response