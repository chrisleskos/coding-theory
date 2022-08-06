from lz77 import LZ77Compression
import codification      
import requests
from PIL import Image


# 1. Choose file 
file_path = input("Input file path\n")

# 2. Compress file
lz = LZ77Compression()
compressed_file = lz.compress(file_path)

# 3. crc
key = "1101"
data = codification.encodeData(compressed_file, key) 

# 4. Add error
error_index = -1
while int(error_index) < 0 or int(error_index) >= len(data):
    error_index = input("Choose an index from 0-" + str(len(data) - 1) + ": ")

data = data[:int(error_index)] + str((int(data[int(error_index)]) - 1)**2) + data[int(error_index)+1:] # if 0: (0-1)^2 = 1, if 1: (1-1)^2 = 0

# 5. Encode data base64
encoded_message = codification.b64Encode(data)

# 6. Send json to host
json_data = {
    "encoded_message": encoded_message.decode(),
    "noise": 2,
    "compression_algorithm": "lz77",
    "encoding": "cyclic",
    "parameters": ["param_list"],
    "errors": 1
}
 
port = '5000'
host = '127.0.0.1'
url = "http://" + host + ":" + port

res = requests.post(url, json = json_data)

print("Compressed file length:", len(compressed_file))
print("Encoded message length:", len(data))
print("Base64 Encoded message length:", len(encoded_message))
print("JSON response:", res.text)