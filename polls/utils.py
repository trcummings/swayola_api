import os
import requests

def validate_email(email, ip_address=None):
    # Pull API key
    api_key = os.getenv('ZEROBOUNCE_API_KEY')
    # Generate request URL
    url = f"https://api.zerobounce.net/v2/validate?api_key={api_key}&email={email}"

    # If we got an IP address with it, pass it along
    if ip_address:
        url += f"&ip_address={ip_address}"
    
    # Fire off request
    response = requests.get(url)
    
    # Handle response
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'valid':
            return True
        else:
            return False
    else:
        raise Exception("Issue connecting to email validation server, please try again later.")
