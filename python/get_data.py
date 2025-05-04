import requests
from requests.auth import HTTPBasicAuth

# Orthanc server configuration
ORTHANC_SERVER = "http://localhost"
PORT = 8042
USERNAME = "edi"  # default username (change if needed)
PASSWORD = "123"  # default password (CHANGE THIS!)

# Configure authentication
auth = HTTPBasicAuth(USERNAME, PASSWORD)
BASE_URL = f"{ORTHANC_SERVER}:{PORT}"

name_instance_dict = {}

def get_patient_names():
    url= f"{BASE_URL}/instances"
    response = requests.get(url, auth=auth)
    if response.status_code == 200:
        instances = response.json()
        for instance in instances:
            instance_url = f"{BASE_URL}/instances/{instance}/simplified-tags"
            instance_response = requests.get(instance_url, auth=auth)
            patient_id = instance_response.json().get("PatientID")
            patient_name = instance_response.json().get("PatientName")
            if patient_id and patient_name:
                print(f"Patient ID: {patient_id}, Patient Name: {patient_name}")
                name_instance_dict[patient_name] = instance

    else:
        print(f"Error: {response.status_code}")

def get_patient_data(patient_id):
    url= f"{BASE_URL}/instances/{patient_id}/file"
    response = requests.get(url, auth=auth)
    if response.status_code == 200:
        with open(f"BCI-to-DICOM/data/downloaded_data/{patient_id}.dcm", "wb") as f:
            f.write(response.content)
        print(f"Patient data saved to {patient_id}.dcm")
    else:
        print(f"Error fetching data for patient {patient_id}: {response.status_code}")

#get_patient_names()
#get_patient_data(name_instance_dict["Edi"])
