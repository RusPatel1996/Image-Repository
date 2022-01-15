from cryptography.fernet import Fernet


class Encryption:
    __instance = None
    __fernet_instance = None

    @staticmethod
    def get_instance():
        if Encryption.__instance:
            return Encryption.__instance
        else:
            Encryption.__instance = Encryption()
            key = Fernet.generate_key()
            Encryption.__fernet_instance = Fernet(key)
            return Encryption.__instance

    @staticmethod
    def encrypt(message):
        instance = Encryption.get_instance()
        return instance.__fernet_instance.encrypt(message.encode())

    @staticmethod
    def decrypt(message):
        instance = Encryption.get_instance()
        return instance.__fernet_instance.decrypt(message).decode()
