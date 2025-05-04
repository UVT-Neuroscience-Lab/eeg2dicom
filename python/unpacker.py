import pathlib

import matplotlib.pyplot as plt
from pydicom import dcmread
import argparse
import get_data
import os
from get_data import name_instance_dict


parser = argparse.ArgumentParser(description='Unpack a DICOM file containing EEG waveform data')
parser.add_argument('--file', required=False, type=str, default='', help='DICOM file location')
parser.add_argument('--name', required=False, type=str, default='', help='Patient ID')
parser.add_argument('--server', action = "store_true", help='Flag for getting data from server')

args = parser.parse_args()

path = parser.parse_args().file
name = parser.parse_args().name

if args.server:
    get_data.get_patient_data(name_instance_dict[name])
    path = f"../data/downloaded_data/{name_instance_dict[name]}.dcm"

ds = dcmread(path)

output_path = "data/unpacked/csvs/"

# Normal mode:
print()
print(f"File path........: {path}")
print(f"SOP Class........: {ds.SOPClassUID} ({ds.SOPClassUID.name})")
print()

sopUID = ds.SOPClassUID
sopUIDname = ds.SOPClassUID.name

pat_name = ds.PatientName


p_name = pat_name.family_comma_given()
print(f"Patient's Name...: {pat_name.family_comma_given()}")
p_id = ds.PatientID
print(f"Patient ID.......: {ds.PatientID}")
mod = ds.Modality
print(f"Modality.........: {ds.Modality}")
sd = ds.StudyDate
print(f"Study Date.......: {ds.StudyDate}")
print(f"Image size.......: {ds.Rows} x {ds.Columns}")

csv_tag = (0x9999, 0x1010)
csv_bytes = ds[csv_tag].value
csv_text = csv_bytes.decode('utf-8')
print("CSV Data from tag: ")
print(csv_text)
#
# with open(os.path.join("data/unpacked/csvs", pid), "w") as f:
#     f.write(csv_text)



plt.imshow(ds.pixel_array, cmap=plt.cm.gray)
plt.show()
