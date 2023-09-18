from twilio.rest import Client

def send():
    # Twilio API credentials
    account_sid = ''
    auth_token = ''

    # Create a Twilio client
    client = Client(account_sid, auth_token)

    # Send SMS
    message = client.messages.create(
        body='Hello, this is shrote your friend need you help!',
        from_='+15178782554',  # Your Twilio phone number
        to='+917991133447'      # Recipient's phone number
    )
