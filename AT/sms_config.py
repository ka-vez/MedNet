import os
import africastalking
from dotenv import load_dotenv

load_dotenv()

class SMS:
    def __init__(self):
        # Set your app credentials
        self.username = "sandbox"
        self.api_key = os.getenv("AFRICAS_TALKING_API_KEY")

        # Initialize the SDK
        africastalking.initialize(self.username, self.api_key)

        # Get the SMS service
        self.sms = africastalking.SMS

    def send(self, message):
            # Set the numbers you want to send to in international format
            recipients = ["+2348106422202"]

            # Set your shortCode or senderId
            sender = "41018"
            try:
				# Thats it, hit send and we'll take care of the rest.
                response = self.sms.send(message, recipients, sender)
                print (response)
            except Exception as e:
                print ('Encountered an error while sending: %s' % str(e))

if __name__ == '__main__':
    SMS().send("I'm a lumberjack and it's ok, I sleep all night and I work all day")