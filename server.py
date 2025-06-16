from flask import Flask , render_template, request, jsonify
from ngsiOperations.ngsildOperations.ngsildEntityCreator import*
from ngsiOperations.ngsildOperations.ngsildSensorProvision import*
from AD import*
from CEP import*
from waitress import serve
import queue
import os
import numpy as np
import time
import json
import ngsiOperations.ngsildOperations.ngsildCrudOperations as v1
import helperFunctions.helperFunctions as hp
import bioTools.emgTools as emg
import paho.mqtt.client as mqtt
import numpy as np 
import helperFunctions.helperFunctions as hp


IOTA_NAME= os.getenv("IOTA_CONTAINER_NAME","localhost")
IOTA_PORT = os.getenv("IOTA_CONTAINER_PORT","4041")
ORION_NAME = os.getenv("ORION_NAME","localhost")
ORION_PORT = os.getenv("ORION_PORT","1026")
MINTAKA_NAME= os.getenv("MINTAKA_NAME","localhost")
MINTAKA_PORT= os.getenv("MINTAKA_PORT","8080")
CONTEXT_NAME = os.getenv("CONTEXT_CONTAINER_NAME","context")
CONTEXT_PORT = os.getenv("CONTEXT_PORT","5051")
BROKER_IP = os.getenv("MOSQUITTO_CONTAINER_NAME","mosquitto")
BROKER_PORT = os.getenv("MOSQUITTO_CONTAINER_PORT",1883)
TOPIC = os.getenv("TOPIC","json/danishabbas1/Robotstate")
ENTITY_FATIGUE = os.getenv("ENTITY_FATIGUE","urn:ngsi-ld:EmgFrequencyDomainFeatures:001")
#none

app = Flask(__name__)

def mqtt_payload(Rob_state):
    current_time = time.strftime("%Y-%m-%dT%H:%M:%S.", time.localtime()) + '{:03d}'.format(int(round(time.time() * 1000)) % 1000)
    payload = {
        "ts": current_time,
        "automatic": Rob_state
    }
    return payload

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print(f"Connection failed with code {rc}")

def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT broker")

#########Routes for the web app#########


@app.route('/')
@app.route('/index')

def index():
    return render_template('index.html')

@app.route('/setup')

def create_Trial():
    trial_name = request.args.get("trial_name")
    orion = ORION_NAME
    orion_port = ORION_PORT
    context = CONTEXT_NAME
    context_port = CONTEXT_PORT
    resp_entities_patch  = ngsi_start_trial_UC1(trial_name,orion,orion_port,context,context_port=context_port)
    
    if resp_entities_patch.status_code==201:
        entity_status ="OK!"
    else: 
        entity_status = "Failed!"
    
    return render_template(
        '2_run_AD.html',
        entity_create_code= entity_status,
            
                           )

@app.route('/setup_0', methods=['GET', 'POST'])
def day_0():
    iota_container_name= IOTA_NAME
    iota_container_port = IOTA_PORT
    orion = ORION_NAME
    orion_port = ORION_PORT
    context = CONTEXT_NAME
    context_port = CONTEXT_PORT
    resp_entities_create  = ngsi_create_trial_UC1(orion,orion_port,context,context_port=context_port)
    
    if resp_entities_create.status_code==201:
        entity_status ="OK!"
    else: 
        entity_status = "Failed!"

    servicepath_provision_response , sensor_provision_response = sensor_provision_UC1(iota_container_name,iota_container_port,orion, orion_port) ##
    
    if servicepath_provision_response.status_code==201:
        servicepath_status ="OK!"
    else: 
        servicepath_status = "Failed!"
    
    if sensor_provision_response.status_code==201:
        sensor_provision_status ="OK!"
    else: 
        sensor_provision_status = "Failed!"
    
    return jsonify({
        'entity_create_code': entity_status,
        'prov_servicepath_status': servicepath_status,
        'prov_sensor_status': sensor_provision_status
    })


@app.route("/processEMG")
def anomaly_detector(orion=ORION_NAME,orion_port=ORION_PORT,mintaka=MINTAKA_NAME,mintaka_port=MINTAKA_PORT, context=CONTEXT_NAME,context_port=CONTEXT_PORT):
    '''The looped part has an execution time of ~0.065 seconds'''
    window_length = 5000
    script_dir = os.path.dirname(os.path.abspath(__file__))
    params_path = os.path.join(script_dir, 'parms.json')
    with open(params_path, 'r') as json_file:
        parms = json.load(json_file)
      # add context/ context port here
    data = v1.ngsi_get_historical(entity='urn:ngsi-ld:sEMG:EMG1000',window_length=window_length,mintaka=mintaka,mintaka_port=mintaka_port,context=context,context_port=context_port)

    if data:
        data_arr= hp.data_to_np(data) # convert data from timescaleDB to np array shape (6, window length) this is transposed
        filter_data = emg.data_filter(data_arr,sampling_frequency=1000,band_lower=20,band_upper=450) # applies band pass filter shape is still (6,window lenght) check if it works
        median_frequency , mean_frequency, mean_power_frequency, zero_cross_frequency = emg.out_stft(np.transpose(filter_data),sampling_frequency=1000) # extracted features , these should be 3 (1x6) lists 

        s_mean, s_med, s_mpower, s_zcf = emg.stress_out(mean_frequency, median_frequency, mean_power_frequency,zero_cross_frequency, parms) # stress level 
        #print(s_mean, s_med, s_mpower, s_zcf)
        payload_raw = v1.stress_payload(s_mean.tolist(), s_med.tolist(), s_mpower.tolist(), s_zcf.tolist() )    
        json_data = json.dumps(payload_raw)
        print(payload_raw)
        resp = v1.ngsi_patch(data=payload_raw,entity="urn:ngsi-ld:EmgFrequencyDomainFeatures:001", orion=orion,orion_port=orion_port,context=context,context_port=context_port)
        if resp.status_code == 204:
            return jsonify({"status": "OK"})
        else:
            return jsonify({"status": "Failed"})
    else:
        return jsonify({"status": "No data available"}) 


@app.route("/send_robot_state", methods=["GET", "POST"])
def send_robot_state():
    entityStress = ENTITY_FATIGUE
    orion = ORION_NAME
    orion_port = ORION_PORT
    broker_address = BROKER_IP
    broker_port = int(BROKER_PORT)
    topic = TOPIC

    try:
        indices = np.array([0, 1, 4, 5])
        Rob_state = False

        stress_state = ngsi_get_current(entity=entityStress, orion=orion, orion_port=orion_port)

        mean = np.array(stress_state["meanFrequencyState"]['value'])[indices]
        median = np.array(stress_state["medianFrequencyState"]['value'])[indices]
        pow = np.array(stress_state["meanPowerFrequencyState"]['value'])[indices]
        zcf = np.array(stress_state["zeroCrossingFrequencyState"]['value'])[indices]
        cumulative = (pow + mean) / 2

        Rob_state = not np.any(cumulative > 1)
        print(f"Robot state: {Rob_state}")
        payload = json.dumps(mqtt_payload(Rob_state))

        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        client.connect(broker_address, broker_port, 60)
        client.loop_start()

        client.publish(topic, payload)
        client.loop_stop()
        client.disconnect()

        return jsonify({"status": "MQTT message sent", "robot_state": Rob_state})
    except Exception as e:
        return jsonify({"status": "Error", "error": str(e)})


@app.route('/get_emg_data', methods=['GET'])
def get_emg_data(orion=ORION_NAME, orion_port=ORION_PORT, context=CONTEXT_NAME, context_port=CONTEXT_PORT):
    entity_id = "urn:ngsi-ld:sEMG:EMG1000"
    url = f"http://{orion}:{orion_port}/ngsi-ld/v1/entities/{entity_id}"
    payload = {}
    headers = {
  'Link': f'<http://{context}:{context_port}/ngsi-context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"',
  'Fiware-service': 'openiot',
  'servicepath': '/'
    }
    try:
        response = requests.get(url, headers=headers, data=payload)
        response.raise_for_status()
        entity_data = response.json()
        data_values = entity_data.get('data', {}).get('value', ["---"] * 6)  # Default to "---" if unavailable
    except Exception:
        data_values = ["---"] * 6  

    return jsonify({"data": data_values})

@app.route('/stopTrial', methods=['GET', 'POST'])
def stop_trial():
    response = ngsi_stop_trial_UC1(orion=ORION_NAME, orion_port=ORION_PORT, context=CONTEXT_NAME, context_port=CONTEXT_PORT)
    if response.status_code == 204:
        return jsonify({"status": "Trial stopped successfully"})
    else:
        return jsonify({"status": "Failed to stop trial", "error": response.text}), response.status_code

###################################### old routes ######################################
""" 
@app.route('/runAD')
def run_AD():
    global stop_thread_event_AD
    stop_thread_event_AD.clear()
    client_thread_1 = threading.Thread(target=anomaly_detector_thread, args=(stop_thread_event_AD,))
    client_thread_1.start()
    return render_template('CEP.html')
def anomaly_detector_thread(stop_thread_AD):
    orion = os.getenv("ORION_NAME")
    orion_port = os.getenv("ORION_PORT")
    mintaka= os.getenv("MINTAKA_NAME")
    mintaka_port= os.getenv("MINTAKA_PORT")
    anomaly_detector(orion,orion_port,mintaka,mintaka_port,stop_thread_AD)

@app.route('/runCEP')
def run_CEP():
    global stop_thread_event_CEP
    stop_thread_event_CEP.clear()
    client_thread_2 = threading.Thread(target=CEP_UC1_thread, args=("urn:ngsi-ld:EmgFrequencyDomainFeatures:001",stop_thread_event_CEP,))
    client_thread_2.start()
    return render_template('3_stop_trial.html' )
def CEP_UC1_thread(entityStress,stop_thread_CEP):
    orion = os.getenv("ORION_NAME")
    orion_port = os.getenv("ORION_PORT")
    CEP_UC1(entityStress=entityStress,orion=orion,orion_port=orion_port,stop_thread_CEP=stop_thread_CEP)
@app.route('/stop')
def stop():
    global stop_thread_event_AD
    global stop_thread_event_CEP
    stop_thread_event_CEP.set()
    stop_thread_event_AD.set()
    ret = sensor_prov_kill(device_id='EMG100',api_key='danishabbas1')
    return render_template('index.html') 
    
    """

@app.route('/historypage')
def go_to_history():
    print("this gives me a list of historical")

@app.route('/download')
def download_trial_data():
    print('this downloads the data of a trial')

@app.route('/detachsensors')
def download_trial_data_2():
    print('this downloads the data of a trial')


    

if __name__ == "__main__":
    serve(app, host= "0.0.0.0", port= 3002)


