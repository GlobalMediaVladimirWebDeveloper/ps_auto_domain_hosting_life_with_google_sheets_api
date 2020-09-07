import os
import sys
import requests
import json
from google_api_v4.google_api import GoogleApi
from time import sleep

API_USERNAME = os.getenv('API_PS_USERNAME')
API_PASSWORD = os.getenv('API_PS_PASSWORD')
API_FIRST_PART_OF_URL = f"https://api.ps.kz/"
API_AUTH_CALL_URL_PART = f"?username={API_USERNAME}&password={API_PASSWORD}&input_format=https&output_format=json " 

SPREAD_SHEETS = {

    "service_spreadsheet": {
        "id": "1KzQLkz3u7kDbjZ-o42LjdC7tW-MiB0LXuoDi8BpATLk",
        "name": "sheet1"
    },

}

def compile_url(part_of_url: str):
    return f"{API_FIRST_PART_OF_URL}{part_of_url}{API_AUTH_CALL_URL_PART}"

def get_results_in_json(url):
    try:
        return json.loads(requests.get(url).text)
    except Exception as e:
        sys.exit("Cannot compile result\n\t", e)

def write_statistics(statistics_list: dict) -> str:
    try:

        google_api = GoogleApi()

        values = google_api.get_values_of_spreadsheet(SPREAD_SHEETS['service_spreadsheet'])

        domains = []
        for url in google_api.get_specific_values_in_list([2], values):
            domains.append(url[0])

        domains_not_included = []

        range_query_part = f"{SPREAD_SHEETS['service_spreadsheet']['name']}!"

        update_data = []

        for statistics_type_key, statistics_type_value in statistics_list.items():
                for key, value in statistics_type_value.items():
                    try:
                        range_number = domains.index(key) + 1
                        if statistics_type_key == "hosting_data":
                            range_query = range_query_part + "Q" + str(range_number)
                        else:
                            range_query = range_query_part + "O" + str(range_number)

                        range_query_body = [[
                            *value.values()
                        ]]

                        intermidiate_dict = {
                            "range": range_query,
                            "values": range_query_body,


                        }
                        update_data.append(intermidiate_dict)

                    except Exception:
                        domains_not_included.append(key)
                        continue
        
        google_api.write_data_to_spread_sheet(SPREAD_SHEETS['service_spreadsheet'], update_data)

    except Exception as e:
        print(e)

    # l = google_api.write_data_to_spread_sheet(SPREAD_SHEETS['service_spreadsheet'])
    
    # access_schema = {

    #     "key_column_number": 2,
    #     "login_path": 3,
    #     "login_name": 4,
    #     "login_password": 5,

    # }

    # access_data = google_api.convert_values_to_dict(access_schema, values)

    # get_only = google_api.get_specific_values_in_list([2,3,4,5], values)



def main() -> None:
    middle__hosting_api_url_part = "client/get-product-list"
    api_hosting_call_url = compile_url(middle__hosting_api_url_part)
    api_hosting_request = get_results_in_json(api_hosting_call_url)

    statistics = {
        "hosting_data": {},
        "domain_data": {}
    }

    if api_hosting_request['result'] == 'success':
        
        products = api_hosting_request['answer']['products']

        for product in products:
            statistics["hosting_data"][product["domain"]] = {

                'enddate': product['nextinvoicedate'],
                'status': product['status'],
                'amount': product['amount'],
                'billingcycle': product['billingcycle'],
                'description': product['description'].replace('&quot;', ''),


            }

    middle_domain_api_url_part = "client/get-domain-list"

    api_domain_call_url = compile_url(middle_domain_api_url_part)
    api_domain_request = get_results_in_json(api_domain_call_url)

    if api_domain_request['result'] == 'success':
        domains = api_domain_request['answer']
        for domain in domains:
            statistics["domain_data"][domain["domain"]] = {
                'enddate': domain['expirydate'],
                'status': domain['status'],
            }

    write_statistics(statistics)


if __name__ == '__main__':
	main()




