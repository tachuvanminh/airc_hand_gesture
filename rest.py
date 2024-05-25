import requests

def call_api_with_post_form_data(url, form_data):
    """
    Call an API with the POST method and send parameters as form data.

    Parameters:
        url (str): The URL of the API endpoint.
        form_data (dict): The form data parameters to send.

    Returns:
        requests.Response: The response object returned by the API.
    """
    try:
        # Make a POST request with form data
        response = requests.post(url, data=form_data)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error calling API: {e}")
        return None

