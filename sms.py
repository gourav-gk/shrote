from twilio.rest import Client

def send():
    # Twilio API credentials
    account_sid = 'ACd059465757b5bb8f3e7b540e17af4d6a'
    auth_token = '8d87aa61fc0ba05719cac14e5f154791'

    # Create a Twilio clien
    client = Client(account_sid, auth_token)

    # Send SMS
    message = client.messages.create(
        body='Hello, this is shrote your friend need you help!',
        from_='+15178782554',  # Your Twilio phone number
        to='+917991133447'      # Recipient's phone number
    )
