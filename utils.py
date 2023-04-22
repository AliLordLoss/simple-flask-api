import re
from flask import Response

def res(response, status=200):
    return Response(response, status=status, mimetype="application/json")

def validate_data(data):
    try:
        data['name']
    except KeyError:
        raise Exception('"name" is a required field!')

    try:
        data['family_name']
    except KeyError:
        raise Exception('"family_name" is a required field!')
        
    try:
        data['email']
    except KeyError:
        raise Exception('"email" is a required field!')
    
    try:
        data['city']
    except KeyError:
        raise Exception('"city" is a required field!')
    
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if not re.fullmatch(regex, data['email']):
        raise Exception('"email" is invlid, please send a valid email address!')
