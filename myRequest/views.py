from django.shortcuts import render
import requests
from django.conf import settings as config
from mpesa.api.utils import get_timestamp
from mpesa.api.encode import generate_password
from requests.auth import HTTPBasicAuth
from mpesa.api.access_token import generate_access_token
from requests import Session
from zeep import Client
from zeep.transports import Transport
from requests.auth import HTTPBasicAuth
from django.http import HttpResponseRedirect
import base64
from cryptography.fernet import Fernet

# Create your views here.
session = requests.Session()
session.auth = config.AUTHS

def get_object_method(endpoint):
    response = session.get(endpoint, timeout=10).json()
    return response
def one_filter_method(endpoint,property,filter,field_name):
        Access_Point = config.O_DATA.format(f"{endpoint}?$filter={property}%20{filter}%20%27{field_name}%27")
        response = get_object_method(Access_Point)['value']
        count=len(response)
        return count,response
class UserObjectMixin(object):
    model =None
    session = requests.Session()
    session.auth = config.AUTHS
    cipher_suite = Fernet(config.ENCRYPT_KEY)

    def get_object(self,endpoint):
        response = self.session.get(endpoint, timeout=10).json()
        return response
    
    def one_filter(self,endpoint,property,filter,field_name):

        Access_Point = config.O_DATA.format(f"{endpoint}?$filter={property}%20{filter}%20%27{field_name}%27")
        response = self.get_object(Access_Point)['value']
        count=len(response)
        return count,response
   
    def double_filtered_data(self,endpoint,property_x,filter_x,filed_name_x,operater_1,property_y,filter_y,field_name_y):

        Access_Point = config.O_DATA.format(f"{endpoint}?$filter={property_x}%20{filter_x}%20%27{filed_name_x}%27%20{operater_1}%20{property_y}%20{filter_y}%20%27{field_name_y}%27")
        response = self.get_object(Access_Point)['value']
        count=len(response)
        return count,response

    def triple_filtered_data(self,endpoint,property_x,filter_x,filed_name_x,operater_1,property_y,filter_y,field_name_y,operater_2,property_z,filter_z,field_name_z):

        Access_Point = config.O_DATA.format(f"{endpoint}?$filter={property_x}%20{filter_x}%20%27{filed_name_x}%27%20{operater_1}%20{property_y}%20{filter_y}%20%27{field_name_y}%27%20{operater_2}%20{property_z}%20{filter_z}%20%27{field_name_z}%27")
        response = self.get_object(Access_Point)['value']
        count=len(response)
        return count,response
    def zeep_client(self):
        AUTHS = Session()
        AUTHS.auth = HTTPBasicAuth(config.WEB_SERVICE_USER, config.WEB_SERVICE_PWD)
        CLIENT = Client(config.BASE_URL, transport=Transport(session=AUTHS))
        return CLIENT

    def comparison_double_filter(self,endpoint,property_x,filter_x,field_name,operater_1,property_y,filter_y,property_z):
        Access_Point = config.O_DATA.format(f"{endpoint}?$filter={property_x}%20{filter_x}%20%27{field_name}%27%20{operater_1}%20{property_y}%20{filter_y}%20{property_z}")
        response = self.get_object(Access_Point)['value']
        count=len(response)
        return count,response
    def pass_encrypt(self,password):
        encrypted_text = self.cipher_suite.encrypt(password.encode('ascii'))
        encrypted_password = base64.urlsafe_b64encode(encrypted_text).decode("ascii")
        return encrypted_password
    def pass_decrypt(self,password):
        try:
            Portal_Password = base64.urlsafe_b64decode(password)
            decoded_text = self.cipher_suite.decrypt(Portal_Password).decode("ascii")
            return decoded_text
        except Exception as e:
            return e

    def lipa_na_mpesa(Amount,phone_number,CallBackURL,AccountReference,TransactionDesc):
        formatted_time = get_timestamp()
        decoded_password = generate_password(formatted_time)
        access_token = generate_access_token()

        api_url = "http://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

        headers = {"Authorization": "Bearer %s" % access_token}

        request = {
            "BusinessShortCode": config.MPESA_EXPRESS_SHORTCODE,
            "Password": decoded_password,
            "Timestamp": formatted_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": Amount,
            "PartyA": phone_number,
            "PartyB": config.MPESA_EXPRESS_SHORTCODE,
            "PhoneNumber": phone_number,
            "CallBackURL": CallBackURL,
            "AccountReference":AccountReference,
            "TransactionDesc": TransactionDesc,
        }

        response = requests.post(api_url, json=request, headers=headers)
        return response.json()



class HTTPResponseHXRedirect(HttpResponseRedirect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self["HX-Redirect"] = self["Location"]
    status_code = 200