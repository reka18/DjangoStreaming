# json_viewer/views.py
from django.http import JsonResponse
import requests

# json_viewer/views.py
from django.shortcuts import render
import requests


def json_viewer(request):
    # Replace 'local_endpoint_url' with the actual URL of the local endpoint you want to query
    local_endpoint_url = 'http://127.0.0.1:8000/activity/feed/json/'

    headers = {'Cookie': 'csrftoken=b1aQrPzDBgWJjvVid9hWfOFy3pwhY0Jx; sessionid=pccsmfk8r9e0uqrnuelyovjh27vrxqpn'}

    # Make a request to the local endpoint
    response = requests.get(local_endpoint_url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract 'items' from the JSON response
        items = response.json().get('items', [])

        # Pass 'items' to the template for rendering
        return render(request, 'json_viewer/viewer.html', {'items': items})

    # In case of an error, return an empty list
    return render(request, 'json_viewer/viewer.html', {'items': []})
