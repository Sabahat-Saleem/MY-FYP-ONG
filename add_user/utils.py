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
            "cabin_class": "economy"
        }
    }

    try:
        # Step 1: Create offer request
        response = requests.post(f"{DUFFEL_BASE_URL}/offer_requests", json=payload, headers=HEADERS)
        response.raise_for_status()
        offer_request = response.json()

        offer_request_id = offer_request.get("data", {}).get("id")
        passenger_id = offer_request.get("data", {}).get("passengers", [])[0].get("id")

        if not offer_request_id or not passenger_id:
            print("❌ Offer request or passenger ID missing.")
            return {
                "offer_request_id": None,
                "passenger_id": None,
                "offers": []
            }

        # Step 2: Fetch offers using the offer request ID
        offers_response = requests.get(
            f"{DUFFEL_BASE_URL}/offers?offer_request_id={offer_request_id}",
            headers=HEADERS
        )
        offers_response.raise_for_status()
        offers_data = offers_response.json().get("data", [])

        # Step 3: Format offers
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
            "passenger_id": passenger_id,
            "offers": formatted_offers
        }

    except Exception as e:
        print("Duffel API Error:", e)
        return {
            "offer_request_id": None,
            "passenger_id": None,
            "offers": []
        }

def create_duffel_order(offer_id, offer_request_id, passenger_id,
                        given_name, family_name, email, phone_number, born_on, gender, title):
    try:
        offer_response = requests.get(f"{DUFFEL_BASE_URL}/offers/{offer_id}", headers=HEADERS)
        offer_response.raise_for_status()
        offer_data = offer_response.json()["data"]  # ✅ FIXED

        amount = offer_data["total_amount"]
        currency = offer_data["total_currency"]

        print("💰 Payment info from Duffel:", amount, currency)

    except Exception as e:
        print("❌ Failed to fetch offer:", e)
        return None
    print("✅ Confirmed Offer ID:", offer_id)
    print("💰 Sending amount:", amount)
    print("💰 Sending currency:", currency)
    payload = {
        "data": {
            "selected_offers": [offer_id],
            "type": "order",
            "payments": [
                {
                    "type": "balance",
                    "amount": amount,
                    "currency": currency
                }
            ],
            "passengers": [
                {
                    "id": passenger_id,
                    "title": title,
                    "gender": gender,
                    "given_name": given_name,
                    "family_name": family_name,
                    "born_on": born_on,
                    "phone_number": phone_number,
                    "email": email
                }
            ],
            "offer_request": offer_request_id
        }
    }

    try:
        response = requests.post(f"{DUFFEL_BASE_URL}/orders", json=payload, headers=HEADERS)
        print("✅ Duffel Order Created:", response.status_code)
        print("🔽 Response:", response.text)
        response.raise_for_status()
        return response.json().get("data")
    except Exception as e:
        print("❌ Duffel Order Creation Error:", e)
        if hasattr(e, 'response') and e.response is not None:
            print("🔽 Duffel Response:", e.response.text)
        return None




def cancel_duffel_order(order_id):
    try:
        response = requests.post(f"{DUFFEL_BASE_URL}/orders/{order_id}/cancel", headers=HEADERS)
        return response.status_code == 202
    except Exception as e:
        print("Duffel Cancellation Error:", e)
        return False
