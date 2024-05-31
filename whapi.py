import requests

url = "https://gate.whapi.cloud/messages/link_preview"

headers = {
    "accept": "application/json",
    "authorization": "Bearer OX6BKm7qrqNxUB9mJS1OwEzyvYjO98Z5",
    "content-type": "application/json"
}

data = {
    "to": "94766201619@s.whatsapp.net",
    "body": "*Development officers across the country take trade union action* - https://en.newswave.lk/53059/",
    "title": "Development officers across the country take trade union action",
    "canonical": "https://en.newswave.lk/",
    "view_once": False,
    "media": "https://en.newswave.lk/wp-content/uploads/2022/06/en.newswave.lk-office-work-state-employee-job.jpg",
    "description": "Hello"
}

response = requests.post(url, headers=headers, json=data)

print(response.json())

