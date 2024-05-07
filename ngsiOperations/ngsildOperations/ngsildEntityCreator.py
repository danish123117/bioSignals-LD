import requests

def ngsi_create_entity(d):#updates latest values
    url = 'http://localhost:1026/v2/entities'

    headers = {
    'Content-Type': 'application/json'
    }

    data = d
    response = requests.post(url, json=data, headers=headers)
    return response
 
def ngsi_create_trial(sensor , stress):
    d_stress = {
    "id": stress,
    "type": "Stress",
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
    "id": sensor,
    "type": "Sensor",
    "TimeStamp": {
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
    "Feaisability":{
      "type":"array",
      "value":[True,True,True,True,True,True,True,True]}
    }

    d_ecg = {
    "id": sensor,
    "type": "Sensor",
    "TimeStamp": {
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
    "Feaisability":{
      "type":"array",
      "value":[True,True,True,True,True,True,True,True]}
    }

    d_hr = {
    "id": sensor,
    "type": "Sensor",
    "TimeStamp": {
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
    "Feaisability":{
      "type":"array",
      "value":[True,True,True,True,True,True,True,True]}
    }

    d_acc = {
    "id": sensor,
    "type": "Sensor",
    "TimeStamp": {
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
    "Feaisability":{
      "type":"array",
      "value":[True,True,True,True,True,True,True,True]}
    }

    resp_stress= ngsi_create_entity(d_stress)
    resp_sensor= ngsi_create_entity(d_emg)
    resp_sensor= ngsi_create_entity(d_ecg)
    resp_sensor= ngsi_create_entity(d_hr)
    resp_sensor= ngsi_create_entity(d_acc)
    return resp_stress, resp_sensor

# finish this 