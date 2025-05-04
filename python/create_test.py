import pydicom
import datetime
from io import BytesIO
from PIL import Image
import argparse
from pynetdicom import AE, debug_logger
import matplotlib.pyplot as plt

# Enable debugging
debug_logger()

# ======================
# SERVER CONNECTION
# ======================

# Configure Application Entity
ae = AE(ae_title=b'MY_LAPTOP')
ae.add_requested_context(pydicom.uid.SecondaryCaptureImageStorage)

assoc = ae.associate(
    "localhost",  # Orthanc server IP
    4242,         # Orthanc DICOM port
    ae_title=b'ORTHANC_EDI'  # Orthanc's AE Title
)

# ======================
# ARG PARSING
# ======================

parser = argparse.ArgumentParser(description='Create a DICOM file with BCI data.')
parser.add_argument('--name', required=True, type=str, default='John Smith', help='Patient name')
parser.add_argument('--id', required=True, type=str, default='1234567', help='Patient ID')
parser.add_argument('--birthdate', required=True, type=str, default='19900101', help='Patient birth date (YYYYMMDD)')
parser.add_argument('--sex', required=True, type=str, default='O', help='Patient sex (M/F/O)')
parser.add_argument('--size', required=True, type=int, default=170, help='Patient size (cm)')
parser.add_argument('--weight', required=True, type=int, default=70, help='Patient weight (kg)')
parser.add_argument('--address', required=True, type=str, default='123 Main St, Anytown, USA', help='Patient address')
parser.add_argument('--phone', required=True, type=str, default='555-1234', help='Patient phone number')
parser.add_argument('--study_date', type=str, default=f'{datetime.date.today().strftime('%Y%m%d')}', help='Study date (YYYYMMDD)')
parser.add_argument('--study_time', type=str, default=f'{datetime.datetime.now().strftime('%H%M%S')}', help='Study time (HHMMSS)')
parser.add_argument('--study_id', type=str, default='', help='Study ID')
parser.add_argument('--series_number', type=str, default='1', help='Series number')
parser.add_argument('--accession_number', type=str, default='', help='Accession number')
parser.add_argument('--csv', type=str, default='../data/sample_recording1.csv', help='Path to CSV file')
parser.add_argument('--picture', type=str, default='../data/sample_image.jpg', help='Path to picture file')
# parser.add_argument('--server_ip', type=str, default='localhost', help='Server IP address')
# parser.add_argument('--server_port', type=int, default=4242, help='Server port number')
# parser.add_argument('--ae-title', type=str, default='ORTHANC_EDI', help='AE Title of the server')


# ======================
# CSV DATA HANDLING
# ======================
csv_path = parser.parse_args().csv
with open(csv_path, 'r') as f:
    csv_data = f.read()
csv_bytes = csv_data.encode('utf-8')

# ======================
# IMAGE HANDLING
# ======================

img_path = parser.parse_args().picture

with Image.open(img_path) as img:
    rgb_img = img.convert('RGB')
    
    # Fix orientation based on EXIF data
    if hasattr(img, '_getexif'):
        exif = img._getexif()
        if exif:
            # Rotate according to EXIF orientation tag (0x0112)
            orientation = exif.get(0x0112, 1)
            if orientation > 1: 
                rgb_img = Image.Image.rotate(rgb_img, {
                    2: 0,
                    3: 180,
                    4: 0,
                    5: 90,
                    6: 90,
                    7: -90,
                    8: -90
                }[orientation])

    # Convert to numpy array for proper channel handling
    import numpy as np
    img_array = np.array(rgb_img)
    
    # Convert to bytes in correct order (R, G, B interleaved)
    raw_pixels = img_array.tobytes()


# ======================
# DICOM FILE CREATION
# ======================
current_time = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
output_path = f'../data/generated_dcm/output_{current_time}.dcm'

# Create File Meta Information
file_meta = pydicom.Dataset()
file_meta.MediaStorageSOPClassUID = pydicom.uid.SecondaryCaptureImageStorage
file_meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian
file_meta.ImplementationClassUID = pydicom.uid.PYDICOM_IMPLEMENTATION_UID

# Create Main Dataset
ds = pydicom.Dataset()
ds.file_meta = file_meta
ds.is_little_endian = True
ds.is_implicit_VR = False

# ======================
# STANDARD DICOM TAGS
# ======================
# Patient Information
ds.PatientName = parser.parse_args().name
ds.PatientID = parser.parse_args().id
ds.PatientBirthDate = parser.parse_args().birthdate
ds.PatientSex = parser.parse_args().sex
ds.PatientSize = parser.parse_args().size
ds.PatientWeight = parser.parse_args().weight
ds.PatientAddress = parser.parse_args().address
ds.PatientTelephoneNumbers = parser.parse_args().phone

# Study Information
ds.StudyDate = parser.parse_args().study_date
ds.StudyTime = parser.parse_args().study_time
ds.StudyID = parser.parse_args().study_id
ds.SeriesNumber = parser.parse_args().series_number
ds.AccessionNumber = parser.parse_args().accession_number
ds.StudyInstanceUID = pydicom.uid.generate_uid()
ds.SeriesInstanceUID = pydicom.uid.generate_uid()
ds.SOPClassUID = pydicom.uid.SecondaryCaptureImageStorage
ds.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID 

# Temporal context
ds.InstanceCreationDate = datetime.date.today().strftime('%Y%m%d')
ds.InstanceCreationTime = datetime.datetime.now().strftime('%H%M%S.%f') 

# Image Parameters
ds.Modality = "OT"  # Other
ds.Rows = rgb_img.height
ds.Columns = rgb_img.width
ds.SamplesPerPixel = 3
ds.PhotometricInterpretation = "RGB"
ds.BitsAllocated = 8
ds.BitsStored = 8
ds.HighBit = 7
ds.PixelRepresentation = 0
ds.PlanarConfiguration = 0  # Interleaved color
ds.PixelData = raw_pixels
ds.WindowCenter = int(ds.BitsStored/2)
ds.WindowWidth = ds.BitsStored
ds.RescaleIntercept = 0
ds.RescaleSlope = 1


# ======================
# PRIVATE TAGS (For CSV Data)
# ======================
# Private Creator must be defined first
private_creator_tag = (0x9999, 0x0010)
ds.add_new(private_creator_tag, 'LO', 'CSV_STORAGE_V1')

# Actual data storage (using element number > 0x00FF)
csv_tag = (0x9999, 0x1010)
ds.add_new(csv_tag, 'OB', csv_bytes)

# ======================
# FILE SAVING
# ======================
ds.save_as(output_path, write_like_original=False)
print(f"Successfully created DICOM file at: {output_path}")
print(f"CSV size: {len(csv_bytes)} bytes | Image size: {rgb_img.size} pixels")

# ======================
# PUSHING TO SERVER
# ======================

if assoc.is_established:
    dataset = pydicom.dcmread(output_path)
    status = assoc.send_c_store(dataset)
    print(f"C-STORE Status: {status.Status}")
    assoc.release()
else:
    print("Association rejected")