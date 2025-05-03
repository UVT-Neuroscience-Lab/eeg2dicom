import pydicom
import csv
import io
import datetime
import tempfile

# Read the CSV file and encode it as a byte string
csv_file = '../data/sample_recording1.csv'
with open(csv_file, mode='r') as f:
    csv_content = f.read()

# Convert the CSV content to a byte string
csv_bytes = csv_content.encode('utf-8')

# Create a DICOM file with patient information
current_time = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
filename = f'../data/generated_dcm/output{current_time}.dcm'
file_meta = pydicom.Dataset()
file_meta.MediaStorageSOPClassUID = pydicom.uid.SecondaryCaptureImageStorage
file_meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
file_meta.ImplementationClassUID = pydicom.uid.PYDICOM_IMPLEMENTATION_UID

ds = pydicom.FileDataset(filename, {}, file_meta=file_meta, preamble=b"\0" * 128)

# Add some patient/study metadata
ds.PatientName = "Test^Patient"
ds.PatientID = "123456"
ds.StudyInstanceUID = pydicom.uid.generate_uid()
ds.SeriesInstanceUID = pydicom.uid.generate_uid()
ds.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID
ds.Modality = "OT"  # Other modality (or use another if applicable)
ds.StudyDate = datetime.date.today().strftime('%Y%m%d')

# Add the CSV byte content to a private tag (you can choose a specific tag number, here I use 0x9999,0x0010 as an example)
ds.add_new((0x9999, 0x0010), 'OB', csv_bytes)

# Save it
ds.save_as(filename)
print(f"DICOM file created with CSV embedded at: {filename}")
