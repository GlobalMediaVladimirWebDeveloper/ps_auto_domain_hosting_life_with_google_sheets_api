import os
import sys
import requests
import json


API_USERNAME = os.getenv('API_PS_USERNAME')
API_PASSWORD = os.getenv('API_PS_PASSWORD')
API_FIRST_PART_OF_URL = f"https://api.ps.kz/"
API_AUTH_CALL_URL_PART = f"?username={API_USERNAME}&password={API_PASSWORD}&input_format=https&output_format=json " 



def compile_url(part_of_url: str):
    return f"{API_FIRST_PART_OF_URL}{part_of_url}{API_AUTH_CALL_URL_PART}"

def get_results_in_json(url):
    try:
        return json.loads(requests.get(url).text)
    except Exception as e:
        sys.exit("Cannot compile result\n\t", e)

def main():
    middle__hosting_api_url_part = "client/get-product-list"
    api_hosting_call_url = compile_url(middle__hosting_api_url_part)
    api_hosting_request = get_results_in_json(api_hosting_call_url)

    statistics = {
        "hosting_data":{},
        "domain_data": {},
    }

    if api_hosting_request['result'] == 'success':
        
        products = api_hosting_request['answer']['products']

        for product in products:
            statistics['hosting_data'][product['domain']] = {

                'domain': product['domain'],
                'enddate': product['nextinvoicedate'],
                'status': product['status'],
                'amount': product['amount'],
                'billingcycle': product['billingcycle'],
                'description': product['description'],


            }

    middle_domain_api_url_part = "client/get-domain-list"

    api_domain_call_url = compile_url(middle_domain_api_url_part)
    api_domain_request = get_results_in_json(api_domain_call_url)

    if api_domain_request['result'] == 'success':
        domains = api_domain_request['answer']
        for domain in domains:
            statistics['domain_data'][domain['domain']] = {
                'enddate': domain['expirydate'],
                'status': domain['status'],
            }

    return statistics


if __name__ == '__main__':
	main()




