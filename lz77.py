import math

class LZ77Compression:

    def __init__(self):
        self.sb_size = 255
        self.la_size = 10
        self.counter = 0


    def compress(self, file_path):
        data = None
        try:
            with open(file_path, 'rb') as file:
                data = file.read()
        except IOError: 
            print("File not found")
            raise

        print(data)

        token_array = self.lz77(data=data)
        return self.binary_representation(token_array)


    def decompress(self, bin_str):
        tokens_array = self.token_representation(bin_str)
        outcome = ''

        for token in tokens_array:
            offset = max(token[0], 1)
            offset_index = len(outcome) - offset
            length = token[1]
 
            
            quont = length//offset
            mod = length%offset
            outcome += outcome[offset_index::] * quont + outcome[offset_index:offset_index+mod] +chr(token[2])
            

        return outcome



    def lz77(self, data):
        
        outcome=[]
        search_buffer=[-1] * self.sb_size   
        start_index=0

        while True:
            exit_recursion = True
            self.counter += 1
            end_index = min(len(data), start_index + self.la_size)

            look_ahead_buffer = data[start_index : end_index]
            print("Iteration: ", self.counter)
            print("   start:", start_index)
            print("   end:", end_index)
            print("   Look Ahead Buffer:", look_ahead_buffer)
            print("   Search Buffer:", search_buffer)
            matched = [x for x in range(self.sb_size)] # start by incliding all of the indexes

            for i in range(len(look_ahead_buffer)):
                new_matched = []
                for match in matched:
                    if search_buffer[match] == look_ahead_buffer[i]:
                        print("      I found that: ", search_buffer[match], "==", look_ahead_buffer[i])
                        new_matched.append(match)
                
                search_buffer.pop(0)
                search_buffer.append(look_ahead_buffer[i])
                
                if new_matched != []:
                    matched = new_matched.copy()
                    if i == len(look_ahead_buffer)-1:
                        if i == 0:
                            jmp = 0
                        else:
                            jmp = self.sb_size - matched[-1]
                        outcome.append([jmp, i, look_ahead_buffer[i]])
                        if end_index != len(data):
                            start_index += i + 1
                            exit_recursion = False
                            break

                else:
                    if i == 0:
                        jmp = 0
                    else:
                        jmp = self.sb_size - matched[-1]

                    outcome.append([jmp, i, look_ahead_buffer[i]])
                    print("   - added: ", outcome[-1])
                    start_index += i + 1
                    exit_recursion = False
                    break

            if exit_recursion:
                break

            
        return outcome

    def binary_representation(self, token_array):
        get_binary = lambda x, n: format(x, 'b').zfill(n)
        bin_str = ''
        for token in token_array:
            jump = get_binary(token[0], math.ceil(math.log(self.sb_size, 2)))
            length = get_binary(token[1],  math.ceil(math.log(self.la_size, 2)))
            next_char = get_binary(token[2], 8)
            bin_token = jump + length + next_char
            bin_str += bin_token

        return bin_str
        
    def token_representation(self, bin_str):
        outcome = []
        jump_size = math.ceil(math.log(self.sb_size, 2))
        length_size = jump_size + math.ceil(math.log(self.la_size, 2))
        for i in range(0, len(bin_str), length_size + 8):
            jump = int(bin_str[i:i+jump_size], 2)
            length = int(bin_str[i+jump_size:i+length_size], 2)
            next_char = int(bin_str[i+length_size:i+length_size+8], 2)

            outcome.append([jump, length, next_char])

        return outcome


lz = LZ77Compression()
prev_compressed=""
while True:
    c = input("Select action:\n  1. Compress\n  2. Decompress\n  0. Exit\n")
    if c == '0':
        break
    elif c == '1':
        x = input("input file path\n")
        prev_compressed = lz.compress(x)
        print(prev_compressed)
    elif c == '2':
        # x = input("input binary array\n")
        print(lz.decompress(prev_compressed))