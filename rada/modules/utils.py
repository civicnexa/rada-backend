import logging
from django.core.mail import BadHeaderError, send_mail, send_mass_mail
from templated_mail.mail import BaseEmailMessage
from rest_framework.pagination import PageNumberPagination
# from celery import shared_task
import re
import json
import requests
import base64
import logging
from django.utils import timezone
import secrets
from django.conf import settings
from cryptography.fernet import Fernet
from django.utils.crypto import get_random_string
from dateutil.relativedelta import relativedelta



def password_checker(password: str):
    try:
        # Python program to check validation of password
        # Module of regular expression is used with search()

        flag = 0
        while True:
            if len(password) < 8:
                flag = -1
                break
            elif not re.search("[a-z]", password):
                flag = -1
                break
            elif not re.search("[A-Z]", password):
                flag = -1
                break
            elif not re.search("[0-9]", password):
                flag = -1
                break
            elif not re.search("[#!_@$-]", password):
                flag = -1
                break
            elif re.search("\s", password):
                flag = -1
                break
            else:
                flag = 0
                break

        if flag == 0:
            return True, "Valid Password"

        return (
            False,
            "Password must contain uppercase, lowercase letters, '# ! - _ @ $' special characters "
            "and 8 or more characters",
        )
    except (Exception,) as err:
        return False, f"{err}"

def get_next_minute(date, delta):
    next_minute = date + relativedelta(minutes=delta)
    return next_minute

def generate_random_password():
    return get_random_string(length=10)


def generate_random_otp():
    return get_random_string(length=6, allowed_chars="1234567890")


def encrypt_text(text: str):
    key = base64.urlsafe_b64encode(settings.SECRET_KEY.encode()[:32])
    fernet = Fernet(key)
    secure = fernet.encrypt(f"{text}".encode())
    return secure.decode()

def decrypt_text(text: str):
    key = base64.urlsafe_b64encode(settings.SECRET_KEY.encode()[:32])
    fernet = Fernet(key)
    decrypt = fernet.decrypt(text.encode())
    return decrypt.decode()

def incoming_request_checks(request) -> tuple:
    try:
        request_type = request.headers.get("requestType", None)

        if not request_type:
            return False, "'request_type' field is required"

        if request_type != "inbound":
            return False, "Invalid 'request_type' value"

        logging.info(msg=f"request_type: {request_type}")
        return True, ""
    except (Exception,) as err:
        return False, f"{err}"

def incoming_formdata_request_checks(request) -> bool:
    try:
        # x_api_key = request.headers.get("X-Api-Key", None) or request.META.get(
        #     "HTTP_X_API_KEY", None
        # )
        
        request_type = request.headers.get("requestType", None)
       
        if not request_type:
            return False, "'request_type' field is required"

        if request_type != "inbound":
            return False, "Invalid 'request_type' value"

        logging.info(msg=f"request_type: {request_type}")
        return True, ""
    except (Exception,) as err:
        return False, f"{err}"


def get_incoming_request_checks(request) -> tuple:
    try:
        request_type = request.headers.get("requestType", None)
        
        logging.info(msg=f"request_type: {request_type}")
        return True, ""
        # how do I handle requestFrom and also client ID e.g 'inbound', do I need to expect it as a query parameter.
    except (Exception,) as err:
        return False, f"{err}"


def api_response(message, status: bool, data=None, **kwargs) -> dict:
    if data is None:
        data = {}
    try:
        reference_id = secrets.token_hex(30)
        response = dict(
            requestTime=timezone.now(),
            request_type="outbound",
            referenceId=reference_id,
            status=status,
            message=message,
            data=data,
            **kwargs,
        )

        # if "accessToken" in data and 'refreshToken' in data:
        if "accessToken" in data:
            # Encrypting tokens to be
            response["data"]["accessToken"] = encrypt_text(text=data["accessToken"])
            # response['data']['refreshToken'] = encrypt_text(text=data['refreshToken'])
            logging.info(msg=response)

            response["data"]["accessToken"] = decrypt_text(text=data["accessToken"])
            # response['data']['refreshToken'] = encrypt_text(text=data['refreshToken'])

        else:
            logging.info(msg=response)

        return response
    except (Exception,) as err:
        return err


def log_request(*args):
    for arg in args:
        logging.info(arg)

class OneItemPagination(PageNumberPagination):
    page_size = 1

# @shared_task()
def sendEmail(context, template, to):
    try:
        message = BaseEmailMessage(
            template_name=f'{template}',
            context=context)
        # message.at
        message.send(to=to)
        
        return True, {"message": "Email sent"}
    except BadHeaderError:
        print('Bad Headed')
        pass
    except ConnectionRefusedError:
        return False, {"message": "Unable to send Email"}


    pass

def send_email(content, email, subject):
    payload = json.dumps({"Message": content, "address": email, "Subject": subject})
    response = requests.request(
        "POST",
        settings.EMAIL_URL,
        headers={"Content-Type": "application/json"},
        data=payload,
    )
    # log_request(f"Email sent to: {email}")
    log_request(f"Sending email to: {email}, Response: {response.text}")
    return response.text


def sendEmail(context, template, to):
    try:
        message = BaseEmailMessage(
            template_name=f'{template}',
            context=context)
        # message.at
        message.send(to=to)
        
        return True, {"message": "Email sent"}
    except BadHeaderError:
        print('Bad Headed')
        pass
    except ConnectionRefusedError:
        return False, {"message": "Unable to send Email"}


    pass
