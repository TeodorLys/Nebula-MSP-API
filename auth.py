import os.path
from urllib import request
from basic import *
import requests
import urllib.parse
import json
import tempfile
from ncc_library import ncc_library

class auth():
    #Stages:
    def set_credentials(self, email, key):
        self.original_url = "utf8=%E2%9C%93&authenticity_token=iamauthentic&user%5Bemail%5D=*EMAIL*&user%5Bpassword%5D=*PASS*&user%5Bremember_me%5D=0&user%5Bremember_me%5D=1"
        self.m_basic = basic()
        self.original_url = self.original_url.replace("*EMAIL*", urllib.parse.quote(email))
        self.original_url = self.original_url.replace("*PASS*", urllib.parse.quote(key))
    
    def get_token(self):
        tmpdir = tempfile.gettempdir()
        tmpfile = tmpdir + "\\tmp_ncc.tmp"
        req = requests.Session()
        if(os.path.isfile(tmpfile)):
            f = open(tmpfile, "r")
            self.token = f.readline()
            m_basic = basic()
            m_json_lib = ncc_library()
            m_basic.set_auth_token(self.token)
            response = m_basic.nebula_req(m_json_lib.get_page("test_token", types.MSP))
            if(response.status_code == 200):
                return self.token
                

        #Retreive zyxel portal token
        req.get("https://accounts.myzyxel.com/oauth2/authorize?response_type=token&client_id=iamindeediclient&redirect_uri=https%3A%2F%2Fnebula.zyxel.com%2Fcc%2Findex.html")
        #get all the nessecary cookies and session data
        req.get("https://accounts.myzyxel.com/users/sign_in")
        #send in the credentials
        req.post("https://accounts.myzyxel.com/users/sign_in", data=self.original_url)
        #get the oauth2 token
        oauth = req.get("https://accounts.myzyxel.com/oauth2/authorize?response_type=token&client_id=d133165ec6634b380bdab3dac436159ed15c0f2de8b1148867e1c1670a7a04d8&redirect_uri=https%3A%2F%2Fnebula.zyxel.com%2Fcc%2Findex.html")
        access_token = oauth.url[oauth.url.find("token=")+6:oauth.url.find("&")]
        #get the zyxel access token
        trigger = req.get("https://accounts.myzyxel.com/api/v1/my?trigger=my_info&tragger_name=my_info", headers={"authorization":"Bearer " + access_token})
        res_json = json.loads(str(trigger.content).replace("b'", "").replace("'", ""))
        #load some session data
        req.options("https://sd-wan.nebula.zyxel.com/nebula/v3/account/auth")
        body = '{"user_info":"' + res_json['result'] + '","zyxel_oauth_token":"' + access_token + '"}'
        #Get the results key
        req.post("https://sd-wan.nebula.zyxel.com/nebula/v3/account/auth", data=body)
        f_body = '{"user_info":"' + res_json['result'] + '"}'
        #Finally get the actual access token
        final = req.post("https://ccapi.nebula.zyxel.com/nebula/v3/account/auth", data=f_body, headers={"authority":"ccapi.nebula.zyxel.com", "Content-Type":"application/json; charset=UTF-8"})
        final_json = json.loads(str(final.content).replace("b'", "").replace("\\n'", "").replace("'", '"'))
        self.token = final_json['body']['authtoken']

        f = open(tmpfile, "w+")
        f.write(self.token)

        return self.token