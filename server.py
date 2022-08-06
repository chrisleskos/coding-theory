from flask import Flask, request
from lz77 import LZ77Compression
import codification


app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    key = "1101"
    content = request.json

    # Decode
    decoded_message = codification.b64Decode(content["encoded_message"])

    # Check for Errors
    errors = codification.decodeData(decoded_message, key)

    # Error Correction
    
    # -------------- Not Needed -------------- #
        #### decompress
        #### lz = LZ77Compression()
        #### message = lz.decompress('')
    # ---------------------------------------- #
    
    return errors

if __name__ == "__main__":
    app.run(debug=True)