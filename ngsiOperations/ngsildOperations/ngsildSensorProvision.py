import requests

def sensor_provision(sensor_entity,api_key='placeholder_api_key'):
# provision service path
    url = 'http://iot-agent:4041/iot/services'
    headers = {
        'Content-Type': 'application/json',
        'fiware-service': 'openiot',
        'fiware-servicepath': '/'
    }
    data = {
        "services": [
            {
                "apikey": "danishabbas1",
                "cbroker": "http://orion:1026",
                "entity_type": "sEMG",
                "resource": "/iot/json",
                "transport": "MQTT",
                "attributes": [
                    {"object_id": "timeStamp", "name": "timeStamp", "type": "Text"},
                    {"object_id": "data", "name": "data", "type": "array"},
                    {"object_id": "index", "name": "index", "type": "Integer"},
                    {"object_id": "feaisability", "name": "feaisability", "type": "array"}]
               
            },
            {
                "apikey": "danishabbas2",
                "cbroker": "http://orion:1026",
                "entity_type": "PolarH10TopicECG",
                "resource": "/iot/json",
                "transport": "MQTT",
                "attributes": [
                    {"object_id": "timeStamp", "name": "timeStamp", "type": "Integer"},
                    {"object_id": "sensorTimeStamp", "name": "sensorTimeStamp", "type": "Integer"},
                    {"object_id": "ecg", "name": "ecg", "type": "array"},
                    {"object_id": "sessionId", "name": "sessionId", "type": "Integer"}
                    ],
                "static_attributes": [
                    {"object_id": "clientId", "name": "clientId", "type": "string"},
                    {"object_id": "deviceId", "name": "deviceId", "type": "string"},
                    {"object_id": "sampleRate", "name": "sampleRate", "type": "Integer"}                    

                ]
            },
            {
                "apikey": "danishabbas2",
                "cbroker": "http://orion:1026",
                "entity_type": "PolarH10TopicACC",
                "resource": "/iot/json",
                "transport": "MQTT",
                "attributes": [
                    {"object_id": "timeStamp", "name": "timeStamp", "type": "Integer"},
                    {"object_id": "sensorTimeStamp", "name": "sensorTimeStamp", "type": "Integer"},
                    {"object_id": "acc", "name": "acc", "type": "array"},
                    {"object_id": "sessionId", "name": "sessionId", "type": "Integer"},
                    {"object_id": "sampleRate", "name": "sampleRate", "type": "Integer"}
                ],
                "static_attributes": [
                    {"object_id": "clientId", "name": "clientId", "type": "string"},
                    {"object_id": "deviceId", "name": "deviceId", "type": "string"},
                ]
            },
            {
                "apikey": "danishabbas2",
                "cbroker": "http://orion:1026",
                "entity_type": "PolarH10TopicHR",
                "resource": "/iot/json",
                "transport": "MQTT",
                "attributes": [
                    {"object_id": "timeStamp", "name": "timeStamp", "type": "Integer"},
                    {"object_id": "sensorTimeStamp", "name": "sensorTimeStamp", "type": "Integer"},
                    {"object_id": "hr", "name": "hr", "type": "Integer"},
                    {"object_id": "hrv", "name": "hrv", "type": "Integer"},
                    {"object_id": "rr", "name": "rr", "type": "Integer"},                    
                    {"object_id": "sessionId", "name": "sessionId", "type": "Integer"},

                ],
                "static_attributes": [
                    {"object_id": "clientId", "name": "clientId", "type": "string"},
                    {"object_id": "deviceId", "name": "deviceId", "type": "string"},
                    {"object_id": "sampleRate", "name": "sampleRate", "type": "Integer"}
                ]
            }
        ]
    }

    servicepath_provision_response = requests.post(url, json=data, headers=headers)
    #print(servicepath_response.status_code)
    #print(servicepath_response.text)
    #provision EMG sensor
    url = 'http://iot-agent:4041/iot/devices'
    headers = {
        'Content-Type': 'application/json',
        'fiware-service': 'openiot',
        'fiware-servicepath': '/'
    }
    data = {
        "devices": [
            {
                "device_id": "EMG1000",
                "entity_name": "urn:ngsi-ld:EMG1000",
                "entity_type": "sEMG"
            },
                        {
                "device_id": "ecg",
                "entity_name": "urn:ngsi-ld:ecg",
                "entity_type": "PolarH10TopicECG"
            },
                        {
                "device_id": "hr",
                "entity_name": "urn:ngsi-ld:hr",
                "entity_type": "PolarH10TopicHR"
            },
                        {
                "device_id": "acc",
                "entity_name": "urn:ngsi-ld:acc",
                "entity_type": "PolarH10TopicACC"
            }


        ]
    }
    sensor_provision_response = requests.post(url, json=data, headers=headers)
    #print(sensor_response.status_code)
    #print(sensor_response.text)
    return servicepath_provision_response , sensor_provision_response