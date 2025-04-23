import requests
from django.conf import settings
 
DUFFEL_BASE_URL = "https://api.duffel.com/air/offer_requests"
 
 
def get_duffel_schedules():
     headers = {
         "Authorization": f"Bearer {settings.DUFFEL_API_TOKEN}",
         "Accept": "application/json",
         "Content-Type": "application/json",
         "Duffel-Version": "v1"
     }
 
     data = {
         "data": {
             "slices": [
                 {
                     "origin": "LHE",
                     "destination": "DXB",
                     "departure_date": "2025-05-15"
                 }
             ],
             "passengers": [
                 {
                     "type": "adult"
                 }
             ],
             "cabin_class": "economy"
         }
     }
 
     try:
         print("Sending Duffel Payload:", data)
         response = requests.post(DUFFEL_BASE_URL, json=data, headers=headers)
         if response.status_code != 201:
             print("Duffel API Error Details:", response.json())
             response.raise_for_status()
         offer_request = response.json()
         return offer_request.get("data", {}).get("offers", [])[:5]
     except Exception as e:
         print("Duffel API Error:", e)
         return []