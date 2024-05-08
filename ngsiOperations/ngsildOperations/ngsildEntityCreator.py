import requests
import json
def ngsi_create_entity(d):#updates latest values
    url = 'http://orion:1026/ngsi-ld/v1/entityOperations/create'

    headers = {
  'Content-Type': 'application/json',
  'Link': '<http://context:5051/ngsi-context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json", "Accept": "application/ld+json"'
    }

    response = requests.request("POST", url, headers=headers, data=d)
    return response
 
def ngsi_create_trial_UC2():
    d_stress = {
    "id": "urn:ngsi-ld:EmgFrequencyDomainFeatures:001",
    "type": "EmgFrequencyDomainFeatures",
    "medianFrequencyState": {
      "type": "array",
      "value": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]},
    "meanFrequencyState": {
      "type": "array",
      "value": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] },
    "meanPowerFrequencyState": {
      "type": "array",
      "value": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]},
    "zeroCrossingFrequencyState": {
      "type": "array",
      "value": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}
     }  
    d_emg = {
    "id": "urn:ngsi-ld:sEMG:001",
    "type": "sEMG",
    "timeStamp": {
      "type": "Text",
      "value": "132"
    },
    "index": {
      "type": "Integer",
      "value": 0
    },
    "data":{
      "type":"array",
      "value":[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
              },
    "feaisability":{
      "type":"array",
      "value":[True,True,True,True,True,True,True,True]}
    }
    ar = 73*[0]
    d_ecg = {
    "id": "urn:ngsi-ld:PolarH10TopicECG:001",
    "type": "PolarH10TopicECG",
    "clientId": {
      "type": "Text",
      "value": "0000"
      },
    "deviceId": {
      "type": "Text",
      "value": "0000"
      },
    "sessionId":{
      "type":"Integer",
      "value":0
      },
    "timeStamp":{
      "type":"Integer",
      "value":0
      },
    "sampleRate":{
      "type":"Integer",
      "value":130
      },
    "sensorTimeStamp":{
      "type":"Integer",
      "value":0
      },
    "ecg":{
      "type":"array",
      "value":ar
      }
    }

    d_hr = {
    "id": "urn:ngsi-ld:PolarH10TopicHR:001",
    "type": "PolarH10TopicHR",
    "clientId": {
      "type": "Text",
      "value": "0000"
      },
    "deviceId": {
      "type": "Text",
      "value": "0000"
      },
    "sessionId":{
      "type":"Integer",
      "value":0
      },
    "timeStamp":{
      "type":"Integer",
      "value":0
      },
    "sensorTimeStamp":{
      "type":"Integer",
      "value":0
      },
    "hr":{
      "type":"Integer",
      "value":0
      },
    "hrv":{
      "type":"Integer",
      "value":0
      },
    "rr":{
      "type":"array",
      "value":[0]
      }
    }
    ac = [[0,0,0]]*36
    d_acc = {
    "id": "urn:ngsi-ld:PolarH10TopicACC:001",
    "type": "PolarH10TopicACC",
    "clientId": {
      "type": "Text",
      "value": "0000"
      },
    "deviceId": {
      "type": "Text",
      "value": "0000"
      },
    "sessionId":{
      "type":"Integer",
      "value":0
      },
    "timeStamp":{
      "type":"Integer",
      "value":0
      },
    "sampleRate":{
      "type":"Integer",
      "value":25
      },
    "sensorTimeStamp":{
      "type":"Integer",
      "value":0
      },
    "acc":{
      "type":"array",
      "value":ac
      }
    }
    payload = json.dumps([d_stress,d_emg,d_acc,d_ecg,d_hr])
    resp= ngsi_create_entity(payload)
    return resp

def ngsi_create_trial_UC1():
    d_stress = {
    "id": "urn:ngsi-ld:EmgFrequencyDomainFeatures:001",
    "type": "EmgFrequencyDomainFeatures",
    "medianFrequencyState": {
      "type": "array",
      "value": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]},
    "meanFrequencyState": {
      "type": "array",
      "value": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] },
    "meanPowerFrequencyState": {
      "type": "array",
      "value": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]},
    "zeroCrossingFrequencyState": {
      "type": "array",
      "value": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}
     }  
    d_emg = {
    "id": "urn:ngsi-ld:sEMG:001",
    "type": "sEMG",
    "timeStamp": {
      "type": "Text",
      "value": "132"
    },
    "index": {
      "type": "Integer",
      "value": 0
    },
    "data":{
      "type":"array",
      "value":[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
              },
    "feaisability":{
      "type":"array",
      "value":[True,True,True,True,True,True,True,True]}
    }
    payload = json.dumps([d_stress,d_emg])

    resp= ngsi_create_entity(payload)
    return resp

#Done