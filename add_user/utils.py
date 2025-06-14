import requests
from django.conf import settings

DUFFEL_BASE_URL = "https://api.duffel.com/air"
HEADERS = {
    "Authorization": f"Bearer {settings.DUFFEL_API_TOKEN}",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Duffel-Version": "v2"  # ✅ Use supported version
}


def get_duffel_schedules():
    payload = {
        "data": {
            "slices": [
                {
                    "origin": "LHE",
                    "destination": "DXB",
                    "departure_date": "2025-06-20"
                }
            ],
            "passengers": [
                {
                    "type": "adult"
                }
            ],
            "cabin_class": "economy"  # ✅ MUST be lowercase
        }
    }

    try:
        # Step 1: Create offer request
        response = requests.post(f"{DUFFEL_BASE_URL}/offer_requests", json=payload, headers=HEADERS)
        response.raise_for_status()
        offer_request = response.json()
        offer_request_id = offer_request.get("data", {}).get("id")

        if not offer_request_id:
            print("Offer request ID not found.")
            return []

        # Step 2: Fetch offers using the request ID
        offers_response = requests.get(
            f"{DUFFEL_BASE_URL}/offers?offer_request_id={offer_request_id}",
            headers=HEADERS
        )
        offers_response.raise_for_status()
        offers_data = offers_response.json().get("data", [])

        # Step 3: Extract and format offer info for template
        formatted_offers = []
        for offer in offers_data[:5]:
            formatted_offer = {
                "id": offer["id"],
                "total_amount": offer.get("total_amount"),
                "total_currency": offer.get("total_currency"),
                "cabin_class": offer.get("cabin_class"),
                "slices": offer.get("slices", [])
            }
            formatted_offers.append(formatted_offer)

        return {
            "offer_request_id": offer_request_id,
            "offers": formatted_offers
        }

    except Exception as e:
        print("Duffel API Error:", e)
        return []
    
def create_duffel_order(offer_id, offer_request_id):
    payload = {
        "data": {
            "selected_offers": [offer_id],
            "type": "order",
            "payments": [
                {
                    "type": "balance",
                    "amount": "1.00",
                    "currency": "GBP"
                }
            ],
            "passengers": [
                {
                    "id": "passenger_1",
                    "title": "mr",
                    "gender": "male",
                    "given_name": "Test",
                    "family_name": "Passenger",
                    "born_on": "1990-01-01",
                    "phone_number": "+441234567890",
                    "email": "test@example.com"
                }
            ],
            "offer_request": offer_request_id  # ✅ critical!
        }
    }

    try:
        response = requests.post(f"{DUFFEL_BASE_URL}/orders", json=payload, headers=HEADERS)
        print("✅ Duffel Order Created:", response.status_code)
        response.raise_for_status()
        return response.json().get("data")
    except Exception as e:
        print("❌ Duffel Order Creation Error:", e)
        return None




def cancel_duffel_order(order_id):
    try:
        response = requests.post(f"{DUFFEL_BASE_URL}/orders/{order_id}/cancel", headers=HEADERS)
        return response.status_code == 202
    except Exception as e:
        print("Duffel Cancellation Error:", e)
        return False