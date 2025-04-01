import base64
import logging
from django.utils import timezone
import secrets
from django.conf import settings
from cryptography.fernet import Fernet


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

def incoming_request_checks(request) -> bool:
    try:
        request_type = request.headers.get("requestFrom", None)

        if not request_type:
            return False, "'requestFrom' field is required"

        if request_type not in ["mobile", "web"]:
            return False, "Invalid 'requestFrom' value"

        logging.info(msg=f"requestfrom: {request_type}")
        return True
    except (Exception,) as err:
        return False, f"{err}"


def incoming_formdata_request_checks(request) -> bool:
    try:
        # x_api_key = request.headers.get("X-Api-Key", None) or request.META.get(
        #     "HTTP_X_API_KEY", None
        # )
        
        request_type = request.headers.get("requestFrom", None)
       
        if not request_type:
            return False, "'requestFrom' field is required"

        if request_type not in ["mobile", "web"]:
            return False, "Invalid 'requestFrom' value"

        logging.info(msg=f"requestfrom: {request_type}")
        return True
    except (Exception,) as err:
        return False, f"{err}"


def get_incoming_request_checks(request) -> tuple:
    try:
        request_type = request.headers.get("requestFrom", None)
        if not request_type:
            return False, "'requestFrom' field is required"

        if request_type not in ["mobile", "web"]:
            return False, "Invalid 'requestFrom' value"
        
        logging.info(msg=f"requestfrom: {request_type}")
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

