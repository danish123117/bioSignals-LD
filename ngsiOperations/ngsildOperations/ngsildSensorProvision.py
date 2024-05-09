import requests

def sensor_provision():
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
                    {"object_id": "timeStamp", "name": "timeStamp", "type": "Property"},
                    {"object_id": "data", "name": "data", "type": "Property"},
                    {"object_id": "index", "name": "index", "type": "Property"},
                    {"object_id": "feaisability", "name": "feaisability", "type": "Property"}]
               
            },
            {
                "apikey": "danishabbas2",
                "cbroker": "http://orion:1026",
                "entity_type": "PolarH10TopicECG",
                "resource": "/iot/json",
                "transport": "MQTT",
                "attributes": [
                    {"object_id": "timeStamp", "name": "timeStamp", "type": "Property"},
                    {"object_id": "sensorTimeStamp", "name": "sensorTimeStamp", "type": "Property"},
                    {"object_id": "ecg", "name": "ecg", "type": "Property"},
                    {"object_id": "sessionId", "name": "sessionId", "type": "Property"}
                    ],
                "static_attributes": [
                    {"object_id": "clientId", "name": "clientId", "type": "Property"},
                    {"object_id": "deviceId", "name": "deviceId", "type": "Property"},
                    {"object_id": "sampleRate", "name": "sampleRate", "type": "Property"}                    

                ]
            },
            {
                "apikey": "danishabbas2",
                "cbroker": "http://orion:1026",
                "entity_type": "PolarH10TopicACC",
                "resource": "/iot/json",
                "transport": "MQTT",
                "attributes": [
                    {"object_id": "timeStamp", "name": "timeStamp", "type": "Property"},
                    {"object_id": "sensorTimeStamp", "name": "sensorTimeStamp", "type": "Property"},
                    {"object_id": "acc", "name": "acc", "type": "Property"},
                    {"object_id": "sessionId", "name": "sessionId", "type": "Property"},
                    {"object_id": "sampleRate", "name": "sampleRate", "type": "Property"}
                ],
                "static_attributes": [
                    {"object_id": "clientId", "name": "clientId", "type": "Property"},
                    {"object_id": "deviceId", "name": "deviceId", "type": "Property"},
                ]
            },
            {
                "apikey": "danishabbas2",
                "cbroker": "http://orion:1026",
                "entity_type": "PolarH10TopicHR",
                "resource": "/iot/json",
                "transport": "MQTT",
                "attributes": [
                    {"object_id": "timeStamp", "name": "timeStamp", "type": "Property"},
                    {"object_id": "sensorTimeStamp", "name": "sensorTimeStamp", "type": "Property"},
                    {"object_id": "hr", "name": "hr", "type": "Property"},
                    {"object_id": "hrv", "name": "hrv", "type": "Property"},
                    {"object_id": "rr", "name": "rr", "type": "Property"},                    
                    {"object_id": "sessionId", "name": "sessionId", "type": "Property"},

                ],
                "static_attributes": [
                    {"object_id": "clientId", "name": "clientId", "type": "Property"},
                    {"object_id": "deviceId", "name": "deviceId", "type": "Property"},
                    {"object_id": "sampleRate", "name": "sampleRate", "type": "Property"}
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
                "device_id": "sEMG",
                "entity_name": "urn:ngsi-ld:sEMG:001",
                "entity_type": "sEMG"
            },
                        {
                "device_id": "ecg",
                "entity_name": "urn:ngsi-ld:PolarH10TopicECG:001",
                "entity_type": "PolarH10TopicECG"
            },
                        {
                "device_id": "hr",
                "entity_name": "urn:ngsi-ld:PolarH10TopicHR:001",
                "entity_type": "PolarH10TopicHR"
            },
                        {
                "device_id": "acc",
                "entity_name": "urn:ngsi-ld:PolarH10TopicACC:001",
                "entity_type": "PolarH10TopicACC"
            }


        ]
    }
    sensor_provision_response = requests.post(url, json=data, headers=headers)
    #print(sensor_response.status_code)
    #print(sensor_response.text)
    return servicepath_provision_response , sensor_provision_response