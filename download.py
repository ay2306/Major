import os
def download(fileid, filename):
    os.system(f"wget --no-check-certificate \'https://drive.google.com/drive/uc?export=download&id={fileid}\' -O {filename}")
download("1U982UYw8AIkWhXJVqLrl08qK8ZzBboOS", "ABC")

# https://drive.google.com/file/d/1cGNCjQoXmb0eNjwc2HLb5VYhI6k18QUg/view?usp=sharing
# https://drive.google.com/drive/folders/1U982UYw8AIkWhXJVqLrl08qK8ZzBboOS?usp=sharing