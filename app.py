import re
from os.path import exists
from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

# /encode
padding_char = '0'
dict_values = {}

#Method to complete the 6 digits
def setLenght(s, max_lenght):
    return (str(s) + padding_char * max_lenght)[:max_lenght]

## Exemple of request --> http://127.0.0.1:5000/encode?number=5
class Encode(Resource):
    def get(self):
        args = request.args
        mybytes = args['number'].encode('utf-8')
        myint = int.from_bytes(mybytes, 'little')
        r = re.compile("[0-9]{6}")
        chave = r.findall(str(myint))
        if(len(chave) == 0):
            chave.append(setLenght(myint, 6))
            dict_values = {args['number']: chave[0]}

        #Not allowed have the same numbers in the file
        with open('dictionaries.txt', 'r') as read:
            lines = read.readlines()
            for line in lines:
                if((args['number'] + ":" + chave[0]) in line):
                    return chave[0]
        #if not, we can write the new value
        with open('dictionaries.txt', 'a') as f:
            f.writelines(args['number'] + ":" + chave[0]+'\n')
            f.close()
            return chave[0]

## Example of request --> http://127.0.0.1:5000/decode?number=530000
class Decode(Resource):
    def get(self):
        args = request.args
        file_exists = exists('dictionaries.txt')
        if (file_exists):
            # Open the file that contains the values
            with open('dictionaries.txt', 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if(args['number'] in line.split(':')[1]):
                        return line.split(':')[0]
                return "There's no encoded number"
        # We return when file not exists
        else:
            return "There's no encoded number"

# api.com/users
api.add_resource(Encode, '/encode')
api.add_resource(Decode, '/decode')

if __name__ == "__main__":
    app.run(debug=True)