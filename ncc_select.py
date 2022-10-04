from ncc_library import types
import json

class ncc_select():
    def __init__(self, org_name, site_name = ""):
        from auth import auth
        from basic import basic
        m_auth = auth()
        m_basic = basic()
        m_basic.set_auth_token(m_auth.get_token())
        response = m_basic.nebula_raw(types.REQ_POST, "/nebula/v9/organization", "/", "{}")
        j_response = json.loads(response.content.decode("utf-8").replace("\u00f6", "ö").replace("\u00e4", "ä").replace("\u00e5", "å"))
        self.org_id = ""
        for n in j_response['body']:
            if(str(n['organization_name']).lower().find(org_name.lower()) == 0):
                self.org_id = n['organization_id']
                self.org = n['organization_name']

        if(len(self.org_id) < 5):
            return
        
        url = "/nebula/v9/organization/*ORG*/sites".replace("*ORG*", self.org_id)

        response = m_basic.nebula_raw(types.REQ_POST, url, "/", '{"privilege_required":false}')
        j_response = json.loads(response.content.decode("utf-8").replace("\u00f6", "ö").replace("\u00e4", "ä").replace("\u00e5", "å"))
        if(len(j_response['body']['sites']) == 1 or site_name == ""):
            self.site_id = j_response['body']['sites'][0]['site_id']
            self.site = j_response['body']['sites'][0]['site_name']
        else:
            for n in j_response['body']['sites']:
                if(str(n['site_name']).lower().find(site_name.lower()) == 0):
                    self.site_id = n['site_id']
                    self.site = n['site_name']

    def get(self):
        return {
            "org_id":self.org_id,
            "site_id":self.site_id
        }
