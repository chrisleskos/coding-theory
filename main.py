from lz77 import LZ77Compression
import codification      
import requests

# prev_compressed=""
# while True:
#     c = input("Select action:\n  1. Compress\n  2. Decompress\n  3. Encode\n  0. Exit\n")
#     if c == '0':
#         break
#     elif c == '1':
#         x = input("input file path\n")
#         print(prev_compressed)
#     elif c == '2':
#         # x = input("input binary array\n")
#         print(lz.decompress(prev_compressed))
#     elif c == '3':
#         prev_compressed = code_ification.encodeData(prev_compressed, "1101") 
#         print(prev_compressed)


lz = LZ77Compression()

# 1. Choose file 
file_path = input("Input file path\n")
# 2. Compress file
compressed_file = lz.compress(file_path)
# 3. crc
key = "1101"
data = codification.encodeData(compressed_file, key) 
# 4. Add error
error_index = -1
while int(error_index) >= 0 and int(error_index) < len(data):
    error_index = input("Choose an index from 0-" + str(len(data)) + ": ")

data = data[:int(error_index)] + str((int(data[int(error_index)]) - 1)**2) + data[int(error_index)+1:] # if 0: (0-1)^2 = 1, if 1: (1-1)^2 = 0
# 5. Encode data base64
# encoded_message = codification.b64Encode(data)
# 6. Send json to host
json_data = {
    "encoded_message": data,
    "noise": 2,
    "compression_algorithm": "lz77",
    "encoding": "cyclic",
    "parameters": ["param_list"],
    "errors": 1
}

s = socket.socket() # Create a socket object
 
port = '5000'
host = '127.0.0.1'
url = "http://" + host + ":" + port

res = requests.post(url, json = json_data)

print(res.text)
 
# 7. Server decodes the message base64
# 8. Check for errors
# 9. Error correction
# 10. Decode crc
# 11. Decompress