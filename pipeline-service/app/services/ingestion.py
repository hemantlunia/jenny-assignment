import requests

FLASK_API = "http://mock-server:5000/api/customers"

def fetch_all_customers():
    page = 1
    limit = 10
    all_data = []

    while True:
        res = requests.get(f"{FLASK_API}?page={page}&limit={limit}")
        data = res.json()

        if not data["data"]:
            break

        all_data.extend(data["data"])

        if len(all_data) >= data["total"]:
            break

        page += 1

    return all_data