# import requests


# def get_exchange_rate(api_key="6d47f28acebd699f95158260"):
#     url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/INR"
#     response = requests.get(url)
#     exchange_rate = 0.01198

#     if response.status_code != 200:
#         print("Error fetching exchange rate")
#     else:
#         data = response.json()
#         exchange_rate = data["conversion_rates"]["USD"]

#     return exchange_rate
