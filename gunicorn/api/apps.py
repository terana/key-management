import logging

from django.apps import AppConfig
from django.conf import settings

from .misc.storage_encryption import StorageEncryption


def first_time():
    try:
        with open("api/migrations/0001_initial.py") as f:
            pass
        return False

    except IOError:
        return True


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        if first_time():

            logging.critical("Starting the KMS for the first time.")

            settings.SHAMIR_MIN_SHARES = 3

            enc, shares = StorageEncryption(2 ** 127 - 1, settings.SHAMIR_MIN_SHARES, 5)
            settings.CRYPTOGRAPHY_KEY = enc._StorageEncryption__master_key

            logging.critical(shares)

        else:
            settings.CRYPTOGRAPHY_KEY = None
            logging.critical("Waiting for the master key assembly.")
