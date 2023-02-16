#!/usr/bin/env python3
import requests, json, sys

# read apikey.txt for our api key; this will exit if it's not there
try: 
    apikey = open('apikey.txt', 'r').read()
except: 
    print('make sure apikey.txt exists and contains only your api key')
    sys.exit(1)

# read endpoint.txt for a CZ url; this will exit if it's not there
try: 
    api_endpoint = open('api_endpoint.txt', 'r').read()
except:
    print('make sure api_endpoint.txt exists and contains only your CZ url')
    sys.exit(1)

api_headers = {'Content-Type': 'application/json', 'z-api-key': apikey}
api_ssl = True


call1 = {'action':'DeviceRouter','method':'getDevices','data':[{'params':{},'uid':'/zport/dmd/Devices/vSphere','keys':['name','ipAddress','uid','productionState','ipAddressString'],'page':1,'start':0,'limit':100,'sort':'name','dir':'ASC'}],'type':'rpc','tid':1}

call2 = [{'action':'DeviceRouter','method':'getComponents','data':[{'uid':'placeholder','keys':['uid','name','usesMonitorAttribute','monitored','locking','powerState','guestDevices','resourcePool','host','uid','meta_type','monitor'],'meta_type':'vSphereVirtualMachine','page':1,'start':0,'limit':10000,'sort':'name','dir':'ASC'}],'type':'rpc','tid':2}]

def list_vspheres():
    call1_json = json.dumps(call1)
    resp = requests.post(api_endpoint, call1_json, headers=api_headers, verify=api_ssl)
    return(resp.json())

def get_components(vsphere):
    call2_distinct = call2
    call2_distinct[0]['data'][0]['uid'] = vsphere
    call2_json = json.dumps(call2_distinct)
    resp = requests.post(api_endpoint, call2_json, headers=api_headers, verify=api_ssl)
    return(resp.json())

if __name__ == '__main__':
    vspheres_raw = list_vspheres()['result']
    vspheres_list = [x['uid'] for x in vspheres_raw['devices']]
    for vsphere in vspheres_list:
        vmcomponents = get_components(vsphere)['result']['data']
        for vm in vmcomponents: 
            print('{name}, {uid}, {monitored}, {guestDevices}'.format(name=vm['name'], uid=vm['uid'], monitored=vm['monitored'], guestDevices=vm['guestDevices']))
