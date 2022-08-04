from lz77 import LZ77Compression
import importlib

codeification = importlib.import_module("code-ification")
# import code-ification


lz = LZ77Compression()
prev_compressed=""
while True:
    c = input("Select action:\n  1. Compress\n  2. Decompress\n  3. Encode\n  0. Exit\n")
    if c == '0':
        break
    elif c == '1':
        x = input("input file path\n")
        prev_compressed = lz.compress(x)
        print(prev_compressed)
    elif c == '2':
        # x = input("input binary array\n")
        print(lz.decompress(prev_compressed))
    elif c == '3':
        print(codeification.encodeData(prev_compressed, "1101"))