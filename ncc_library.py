import time

class page_struct():
    def __init__(self, url, ref, org, site, type, data = ""):
        self.url = str(url).replace("*ORG*", org).replace("*SITE*", site)
        self.ref = str(ref).replace("*ORG*", org).replace("*SITE*", site)
        self.data = data
        self.type = type # POST, GET, PUT etc...

class types():
    #lookup types
    GW_FLEX = 1
    GW = 2
    MSP = 3

    #requests types
    REQ_GET = 4
    REQ_POST = 5
    REQ_PUT = 6


class ncc_library():
    def __init__(self, m_select = {"org_id":"","site_id":""}):
        org = m_select['org_id']
        site = m_select['site_id']
        #gw_flex(USG):
        self.gw_flex = {
            "interface":page_struct("/nebula/v9/organization/*ORG*/site/*SITE*/gw-flex/interface", "/*ORG*/*SITE*/usg/configure/interface", org, site, types.REQ_GET),
            "client_to_site_vpn":page_struct("/nebula/v12/organization/*ORG*/site/*SITE*/gw-flex/client-to-site-vpn", "/*ORG*/*SITE*/usg/configure/remote-access-vpn", org, site, types.REQ_GET),
            "port_group":page_struct("/nebula/v9/organization/*ORG*/site/*SITE*/gw-flex/port-group", "/*ORG*/*SITE*/usg/configure/port", org, site, types.REQ_GET),
            "nat":page_struct("/nebula/v9/organization/*ORG*/site/*SITE*/gw-flex/nat", "/*ORG*/*SITE*/usg/configure/nat", org, site, types.REQ_GET),
            "site_to_site_vpn":page_struct("/nebula/v9/organization/*ORG*/site/*SITE*/gw-flex/site-to-site-vpn", "/*ORG*/*SITE*/usg/configure/site-to-site-vpn", org, site, types.REQ_GET),
            "security_policy":page_struct("/nebula/v9/organization/*ORG*/site/*SITE*/gw-flex/firewall", "/*ORG*/*SITE*/usg/configure/security-policy", org, site, types.REQ_GET),
            "firewall_log":page_struct("/nebula/v3/statistics/site/*SITE*/devices/log", "/*ORG*/*SITE*/usg/monitor/event-log", org, site, types.REQ_POST,'{"start_time":'+str(start_time)+',"end_time":'+ str(end_time) +',"device_type":"GW_FLX"}')
        }
        #gw(NSG):
        self.gw = {
            "devices":page_struct("/nebula/v3/organization/*ORG*/site/*SITE*/devicespage_struct", "/*ORG*/*SITE*/security-gateway/configure/interface-addressing", org, site, types.REQ_GET),
            "wan_interface":page_struct("/nebula/v3/gw/device/*DEV_ID*/wan-interfaces", "/*ORG*/*SITE*/security-gateway/configure/interface-addressing", org, site, types.REQ_GET),
            "lan_interface":page_struct("/nebula/v3/organization/*ORG*/site/*SITE*/gw/subnets/interfaces", "/*ORG*/*SITE*/security-gateway/configure/interface-addressing", org, site, types.REQ_GET),
            "client_to_site_vpn":page_struct("/nebula/v9/organization/*ORG*/site/*SITE*/gw/client-to-site-vpn", "/*ORG*/*SITE*/security-gateway/configure/remote-access-vpn", org, site, types.REQ_GET),
            "firewall_log":page_struct("/nebula/v3/statistics/site/*SITE*/devices/log", "/*ORG*/*SITE*/security-gateway/monitor/event-log", org, site, types.REQ_POST,'{"start_time":'+str(start_time)+',"end_time":'+ str(end_time) +',"device_type":"GW"}')
        }
        #MSP
        end_time = int((time.time() * 1000))
        start_time = end_time - 86400000
        self.msp = {
            "ncc_account":page_struct("/nebula/v3/organization/*ORG*/cloud-auth/user/accounts", "/*ORG*/organization-wide/configure/cloud-authentication", org, site, types.REQ_GET),
            "ssid_settings":page_struct("/nebula/v8/organization/*ORG*/site/*SITE*/wlan-settings", "/*ORG*/*SITE*/access-point/configure/ssid-settings", org, site, types.REQ_GET),
            "monitoring_devices":page_struct("/nebula/v15/statistics/site/*SITE*/clients/monitoring", "/*ORG*/*SITE*/site-wide/monitor/clients", org, site, types.REQ_POST,'{"start_time":'+str(start_time)+',"end_time":'+ str(end_time) +',"features":["lldp_info","ipv4","mac_address","connected_device_id","last_seen","client_info","policy_ap","policy_sw","policy_nsg","policy_usg","manufacturer","os_hostname"]}'),
            "test_token":page_struct("/nebula/v9/group", "/", "", "" , types.REQ_GET),
            "switch_log":page_struct("/nebula/v3/statistics/site/*SITE*/devices/log", "/*ORG*/*SITE*/switch/monitor/event-log", org, site, types.REQ_POST,'{"start_time":'+str(start_time)+',"end_time":'+ str(end_time) +',"device_type":"SW"}'),
            "ap_log":page_struct("/nebula/v3/statistics/site/*SITE*/devices/log", "/*ORG*/*SITE*/access-point/monitor/event-log", org, site, types.REQ_POST,'{"start_time":'+str(start_time)+',"end_time":'+ str(end_time) +',"device_type":"AP"}'),
        }

    def get_page(self, name, type:types):
        if(type == types.GW_FLEX):
            return self.gw_flex[name]
        elif(type == types.GW):
            return self.gw[name]
        elif(type == types.MSP):
            return self.msp[name]
