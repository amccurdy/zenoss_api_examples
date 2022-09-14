#!/usr/bin/env python3
import requests
import json


### THESE NEED TO BE SET BEFORE USING THIS SCRIPT ###
api_key = ''
api_url = ''
#####################################################


api_ssl = True
api_headers = {'Content-Type': 'application/json', 'z-api-key': api_key}
api_action = 'DeviceRouter'
devs_to_report = []
vsphere_endpoints = []
vsphere_devs = []

def callMethod(api_method, api_data):
    payload = json.dumps({'action': api_action, 'method': api_method, 'data': api_data, 'tid': 1})
    #print('Making request: {}'.format(payload))
    response = requests.post(api_url, payload, headers=api_headers, verify=api_ssl)
    return response

post_data = [{'params':{},'uid':'/cz0/zport/dmd/Devices','keys':['name','deviceClass','ipAddressString','uid','productionState','pythonClass'],'page':1,'start':1,'limit':8000,'sort':'name','dir':'ASC'}]

resp = callMethod('getDevices', post_data)
content = json.loads(resp.content)
devs = content['result']['devices']

for item in devs:
    if 'vSphere' in item['pythonClass']:
        vsphere_endpoints.append(item)
    devs_to_report.append(item)

vsphere_post_data = [{'uid':'','keys':['uid','name','monitored','uuid', 'guestDevices'],'meta_type':'vSphereVirtualMachine','page':1,'start':0,'limit':3500,'sort':'name','dir':'ASC'}]

for vsphere_endpoint in vsphere_endpoints:
    uid = vsphere_endpoint['uid']
    vsphere_post_data[0]['uid']=uid
    vresp = callMethod('getComponents', vsphere_post_data)
    vcontent = json.loads(vresp.content)
    vlist = vcontent['result']['data']
    for guest in vlist:
        vsphere_devs.append(guest)

print('name, deviceClass, productionState, ipAddressString, pythonClass, uid')
for device in devs_to_report:
    print('{}, {}, {}, {}, {}, {}'.format(device.get('name'), device.get('deviceClass').get('uid'), device.get('productionState'), device.get('ipAddressString'), device.get('pythonClass'), device.get('uid')))

print('*********************************************************************')
print('*********************************************************************')
print('******************* BEGIN VSPHERE DEVICES ***************************')
print('*********************************************************************')
print('*********************************************************************')
print('name, monitored, guestDevice')
for vdevice in vsphere_devs:
    if vdevice['guestDevices'] != None:
        guestDevice = vdevice['guestDevices'][0]['uid']
    else:
        guestDevice = None
    print('{}, {}, {}'.format(vdevice.get('name'), vdevice.get('monitored'), guestDevice))
