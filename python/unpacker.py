
import matplotlib.pyplot as plt
from pydicom import dcmread
from pydicom.data import get_testdata_file

path = "/home/davyjones/PycharmProjects/BCI-to-DICOM/data/generated_dcm/output_20250504_102934.dcm"
ds = dcmread(path)

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

# use .get() if not sure the item exists, and want a default value if missing
#print(f"Slice location...: {ds.get('SliceLocation', '(missing)')}")

# plot the image using matplotlib
plt.imshow(ds.pixel_array, cmap=plt.cm.gray)
plt.show()