from lz77 import LZ77Compression
import codification      
import requests
from PIL import Image
import random

# 1. Choose file 
file_path = input("Input file path\n")

# 2. Compress file
lz = LZ77Compression()
compressed_file = lz.compress(file_path)

# 3. crc
key = "1101"
data = codification.encodeData(compressed_file, key) 

# 4. Add noise
noise = -1
while int(noise) < 0 or int(noise) >= 100:
    noise = input("Give noise percentage%: ")

errors = int(noise)*len(data)//100

visited_indexes = []
for i in range(errors):
    bit_index = random.randrange(len(data))
    while bit_index in visited_indexes:
        bit_index = random.randrange(len(data))
    
    visited_indexes.append(bit_index)
    data = data[:bit_index] + str( (int(data[bit_index])-1)**2 ) + data[bit_index+1:] # if data[bit_index] =0 -> (0-1)^2 = 1, =1 -> (1-1)^2 = 0

# 5. Encode data base64
encoded_message = codification.b64Encode(data)

# 6. Send json to host
json_data = {
    "encoded_message": encoded_message.decode(),
    "noise": noise,
    "compression_algorithm": "lz77",
    "encoding": "cyclic",
    "parameters": ["param_list"],
    "errors": errors
}
 
port = '5000'
host = '127.0.0.1'
url = "http://" + host + ":" + port

res = requests.post(url, json = json_data)

print("Compressed file length:", len(compressed_file))
print("Encoded message length:", len(data))
print("Base64 Encoded message length:", len(encoded_message))
print("JSON response:", res.text)