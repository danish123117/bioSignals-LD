import requests
import json
def ngsi_create_entity(d,orion,orion_port,context,context_port=5051):#updates latest values
    url = f'http://{orion}:{orion_port}/ngsi-ld/v1/entityOperations/create'
    #url = 'http://localhost:1026/ngsi-ld/v1/entityOperations/create'
    headers = {
  'Content-Type': 'application/json',
  'Link': f'<http://{context}:{context_port}/ngsi-context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json", "Accept": "application/ld+json"'
    }

    response = requests.request("POST", url, headers=headers, data=d)
    return response
 
def ngsi_create_trial_UC2(orion,orion_port,context,context_port):
    d_stress = {
    "id": "urn:ngsi-ld:EmgFrequencyDomainFeatures:001",
    "type": "EmgFrequencyDomainFeatures",
    "trialName": {
      "type": "Property",
      "value": ""},
    "medianFrequencyState": {
      "type": "Property",
      "value": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]},
    "meanFrequencyState": {
      "type": "Property",
      "value": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] },
    "meanPowerFrequencyState": {
      "type": "Property",
      "value": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]},
    "zeroCrossingFrequencyState": {
      "type": "Property",
      "value": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}
     }  
    d_emg = {
    "id": "urn:ngsi-ld:sEMG:EMG1000",
    "type": "sEMG",
    "trialName": {
      "type": "Property",
      "value": ""},
    "timeStamp": {
      "type": "Property",
      "value": "132"
    },
    "index": {
      "type": "Property",
      "value": 0
    },
    "data":{
      "type":"Property",
      "value":[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
              },
    "feaisability":{
      "type":"Property",
      "value":[True,True,True,True,True,True,True,True]}
    }
    ar = 73*[0]
    d_ecg = {
    "id": "urn:ngsi-ld:PolarH10TopicECG:001",
    "type": "PolarH10TopicECG",
    "trialName": {
      "type": "Property",
      "value": ""},
    "clientId": {
      "type": "Property",
      "value": "0000"
      },
    "deviceId": {
      "type": "Property",
      "value": "0000"
      },
    "sessionId":{
      "type":"Property",
      "value":0
      },
    "timeStamp":{
      "type":"Property",
      "value":0
      },
    "sampleRate":{
      "type":"Property",
      "value":130
      },
    "sensorTimeStamp":{
      "type":"Property",
      "value":0
      },
    "ecg":{
      "type":"Property",
      "value":ar
      }
    }

    d_hr = {
    "id": "urn:ngsi-ld:PolarH10TopicHR:001",
    "type": "PolarH10TopicHR",
    "trialName": {
      "type": "Property",
      "value": ""},
    "clientId": {
      "type": "Property",
      "value": "0000"
      },
    "deviceId": {
      "type": "Property",
      "value": "0000"
      },
    "sessionId":{
      "type":"Property",
      "value":0
      },
    "timeStamp":{
      "type":"Property",
      "value":0
      },
    "sensorTimeStamp":{
      "type":"Property",
      "value":0
      },
    "hr":{
      "type":"Property",
      "value":0
      },
    "hrv":{
      "type":"Property",
      "value":0
      },
    "rr":{
      "type":"Property",
      "value":[0]
      }
    }
    ac = [[0,0,0]]*36
    d_acc = {
    "id": "urn:ngsi-ld:PolarH10TopicACC:001",
    "type": "PolarH10TopicACC",
    "trialName": {
      "type": "Property",
      "value": ""},
    "clientId": {
      "type": "Property",
      "value": "0000"
      },
    "deviceId": {
      "type": "Property",
      "value": "0000"
      },
    "sessionId":{
      "type":"Property",
      "value":0
      },
    "timeStamp":{
      "type":"Property",
      "value":0
      },
    "sampleRate":{
      "type":"Property",
      "value":25
      },
    "sensorTimeStamp":{
      "type":"Property",
      "value":0
      },
    "acc":{
      "type":"Property",
      "value":ac
      }
    }
    payload = json.dumps([d_stress,d_emg,d_acc,d_ecg,d_hr])
    resp= ngsi_create_entity(payload,orion,orion_port,context,context_port)
    return resp

def ngsi_create_trial_UC1(orion,orion_port,context,context_port):
    d_stress = {
    "id": "urn:ngsi-ld:EmgFrequencyDomainFeatures:001",
    "type": "EmgFrequencyDomainFeatures",
    "trialName": {
      "type": "Property",
      "value": ""},
    "medianFrequencyState": {
      "type": "Property",
      "value": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]},
    "meanFrequencyState": {
      "type": "Property",
      "value": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] },
    "meanPowerFrequencyState": {
      "type": "Property",
      "value": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]},
    "zeroCrossingFrequencyState": {
      "type": "Property",
      "value": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}
     }  
    d_emg = {
    "id": "urn:ngsi-ld:sEMG:EMG1000",
    "type": "sEMG",
    "trialName": {
      "type": "Property",
      "value": ""},
    "timeStamp": {
      "type": "Property",
      "value": ""
    },
    "index": {
      "type": "Property",
      "value": 0
    },
    "data":{
      "type":"Property",
      "value":[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
              },
    "feaisability":{
      "type":"Property",
      "value":[True,True,True,True,True,True,True,True]}
    }
    payload = json.dumps([d_stress,d_emg])

    resp= ngsi_create_entity(payload,orion,orion_port,context,context_port)
    return resp

#Done

def _ngsi_patch_st(data,entity,orion,orion_port,context,context_port): # this is fine
    """
    The function update the value on an NGSI-ld entity using patch to orion context broker
    """
    url = f"http://{orion}:{orion_port}/ngsi-ld/v1/entities/{entity}/attrs"
    headers = {
        'Content-Type':"application/json",
        "Link": f'<http://{context}:{context_port}/ngsi-context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
     }
    response = requests.request("PATCH", url, headers=headers, data=data)
    return response

def ngsi_start_trial_UC1(trial_name,orion,orion_port,context,context_port):
    """
    Starts a trial by creating the necessary entities in the NGSI-LD context broker.
    """
    # Create the trial entities
    entity1 = "urn:ngsi-ld:EmgFrequencyDomainFeatures:001"
    entity2 = "urn:ngsi-ld:sEMG:EMG1000"
    data1 = {
        "trialName": {
            "type": "Property",
            "value": trial_name
        }}
    data = json.dumps(data1)
    response_1 = _ngsi_patch_st(data,entity1,orion,orion_port,context,context_port)
    response_2 = _ngsi_patch_st(data,entity2,orion,orion_port,context,context_port)
    
    if response_1.status_code == 204 and response_2.status_code == 204:
        return response_1

def ngsi_stop_trial_UC1(orion,orion_port,context,context_port):
    """
    Starts a trial by creating the necessary entities in the NGSI-LD context broker.
    """
    # Create the trial entities
    entity1 = "urn:ngsi-ld:EmgFrequencyDomainFeatures:001"
    entity2 = "urn:ngsi-ld:sEMG:EMG1000"
    data1 = {
        "trialName": {
            "type": "Property",
            "value": ""
        }}
    data = json.dumps(data1)
    response_1 = _ngsi_patch_st(data,entity1,orion,orion_port,context,context_port)
    response_2 = _ngsi_patch_st(data,entity2,orion,orion_port,context,context_port)
    
    if response_1.status_code == 204 and response_2.status_code == 204:
        return response_1