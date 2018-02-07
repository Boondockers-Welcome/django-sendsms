#-*- coding: utf-8 -*-

"""
this backend requires the twilio python library: http://pypi.python.org/pypi/twilio/
"""
from twilio.rest import Client

from django.conf import settings
from sendsms.backends.base import BaseSmsBackend

TWILIO_ACCOUNT_SID = getattr(settings, 'SENDSMS_TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = getattr(settings, 'SENDSMS_TWILIO_AUTH_TOKEN', '')
TWILIO_MESSAGING_SID = getattr(settings, 'SENDSMS_TWILIO_MESSAGING_SID', '')


class SmsBackend(BaseSmsBackend):
    def send_messages(self, messages):
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        for message in messages:
            for to in message.to:
                try:
                    if TWILIO_MESSAGING_SID:
                        client.messages.create(
                            to=to,
                            messaging_service_sid=TWILIO_MESSAGING_SID,
                            body=message.body
                        )
                    else:
                        client.messages.create(
                            to=to,
                            from_=message.from_phone,
                            body=message.body
                        )
                except:
                    if not self.fail_silently:
                        raise
