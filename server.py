from flask import Flask , render_template, request, jsonify
from ngsiOperations.ngsildOperations.ngsildEntityCreator import*
from ngsiOperations.ngsildOperations.ngsildSensorProvision import*
#from ngsiOperations.ngsildOperations.ngsildSubscriptions import createSubscriptions
from AD import*
from CEP import*
from waitress import serve
import threading
import queue
import os

stop_thread_event_AD = threading.Event()
stop_thread_event_CEP = threading.Event()

app = Flask(__name__)

@app.route('/')
@app.route('/index')

def index():
    return render_template('index.html')

@app.route('/setup')

def create_Trial():
    trial_name = request.args.get("trial_name")
    iota_container_name= os.getenv("IOTA_CONTAINER_NAME")
    iota_container_port = os.getenv("IOTA_CONTAINER_PORT")
    orion = os.getenv("ORION_NAME")
    orion_port = os.getenv("ORION_PORT")
    context = os.getenv("CONTEXT_CONTAINER_NAME")
    context_port = os.getenv("CONTEXT_PORT")
    resp_entities_create  = ngsi_create_trial_UC1(trial_name,orion,orion_port,context,context_port=context_port)
    
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
    
    return render_template(
        '2_run_AD.html',
        entity_create_code= entity_status,
        prov_servicepath_status= servicepath_status,
        prov_sensor_status= sensor_provision_status,
             
                           )
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

@app.route('/get_emg_data', methods=['GET'])
def get_emg_data():
    context = os.getenv("CONTEXT_CONTAINER_NAME")
    context_port = os.getenv("CONTEXT_PORT")  
    orion = os.getenv("ORION_NAME")
    orion_port = os.getenv("ORION_PORT")
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
        data_values = entity_data.get('data', {}).get('value', ["---"] * 8)  # Default to "---" if unavailable
    except Exception:
        data_values = ["---"] * 8  

    return jsonify({"data": data_values})

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


