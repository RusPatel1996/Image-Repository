from cryptography.fernet import Fernet


class Encryption:
    __instance = None
    __fernet_instance = None
    __key = b'QY96HoHF8VrgcBp6R_MhygtGhDTP_BVG8C7NMOkYTvY='

    @staticmethod
    def get_instance():
        if Encryption.__instance:
            return Encryption.__instance
        else:
            Encryption.__instance = Encryption()
            Encryption.__fernet_instance = Fernet(Encryption.__key)
            return Encryption.__instance

    @staticmethod
    def encrypt(message: str):
        instance = Encryption.get_instance()
        return instance.__fernet_instance.encrypt(message.encode())

    @staticmethod
    def decrypt(message: bytes):
        instance = Encryption.get_instance()
        return instance.__fernet_instance.decrypt(message).decode()
