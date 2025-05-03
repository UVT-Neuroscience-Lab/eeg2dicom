import pydicom
import csv
import datetime
from io import BytesIO
from PIL import Image
import tempfile

# ======================
# CSV DATA HANDLING
# ======================
csv_path = '../data/sample_recording1.csv'
with open(csv_path, 'r') as f:
    csv_data = f.read()
csv_bytes = csv_data.encode('utf-8')

# ======================
# IMAGE HANDLING
# ======================
img_path = '../data/sample_image.jpg'

# Open and convert to RGB
with Image.open(img_path) as img:
    rgb_img = img.convert('RGB')
    
    # Get raw pixel data as bytes
    with BytesIO() as buffer:
        rgb_img.save(buffer, format="BMP")  # BMP gives uncompressed bytes
        pixel_bytes = buffer.getvalue()

# BMP header is 54 bytes (we need to skip it for raw pixel data)
bmp_header_size = 54
raw_pixels = pixel_bytes[bmp_header_size:]

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
ds.PatientName = "David merge"
ds.PatientID = "6969669"
ds.PatientBirthDate = ""

# Study Information
ds.StudyDate = datetime.date.today().strftime('%Y%m%d')
ds.StudyTime = datetime.datetime.now().strftime('%H%M%S')
ds.StudyInstanceUID = pydicom.uid.generate_uid()
ds.SeriesInstanceUID = pydicom.uid.generate_uid()
ds.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID

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