import pathlib
import matplotlib.pyplot as plt
from pydicom import dcmread
import argparse
import get_data
import os

# Set up argument parser
parser = argparse.ArgumentParser(description='Unpack a DICOM file containing EEG waveform data')
parser.add_argument('--file', type=str, default='', help='DICOM file location')
parser.add_argument('--p_id', type=str, default='', help='Patient ID')
parser.add_argument('--server', action='store_true', help='Flag for getting data from server')

auth = ('edi', '123')
args = parser.parse_args()

# Set path and patient ID from args
path = args.file
pid = args.p_id

# If fetching from server
if args.server:
    if not pid:
        raise ValueError("You must provide --p_id when using --server")
    print(pid)
    get_data.get_patient_data(pid)  # Your function should download the DICOM file
    path = f"BCI-to-DICOM/data/downloaded_data/{pid}.dcm"

# Load DICOM file
ds = dcmread(path)

# Prepare CSV output path
output_dir = "data/unpacked/csvs/"
os.makedirs(output_dir, exist_ok=True)
csv_filename = f"{pid}.csv"
csv_output_path = os.path.join(output_dir, csv_filename)

# Print metadata
print()
print(f"File path........: {path}")
print(f"SOP Class........: {ds.SOPClassUID} ({ds.SOPClassUID.name})")
print(f"Patient's Name...: {ds.PatientName.family_comma_given()}")
print(f"Patient ID.......: {ds.PatientID}")
print(f"Modality.........: {ds.Modality}")
print(f"Study Date.......: {ds.StudyDate}")

# Optional: check if it's an image
if hasattr(ds, 'Rows') and hasattr(ds, 'Columns'):
    print(f"Image size.......: {ds.Rows} x {ds.Columns}")
else:
    print("No image data available.")

# Extract and save CSV data
csv_tag = (0x9999, 0x1010)
if csv_tag in ds:
    csv_bytes = ds[csv_tag].value
    csv_text = csv_bytes.decode('utf-8')
    print("CSV Data from tag:")
    print(csv_text)

    # Save to file
    with open(csv_output_path, "w") as f:
        f.write(csv_text)
    print(f"CSV saved to: {csv_output_path}")
else:
    print("CSV tag not found in DICOM file.")

# Display image if pixel data exists
if hasattr(ds, 'pixel_array'):
    plt.imshow(ds.pixel_array, cmap=plt.cm.gray)
    plt.title("DICOM Image Preview")
    plt.show()
else:
    print("No pixel data to display.")
