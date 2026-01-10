
class email_store:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(email_store, cls).__new__(cls)
            cls._instance.reset()
        return cls._instance

    def reset(self):
        self.verified_email = None
        self.sent_otp = None
