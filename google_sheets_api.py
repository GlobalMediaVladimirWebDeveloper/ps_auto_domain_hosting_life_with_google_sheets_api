from google_api import GoogleApi



SPREAD_SHEETS = {

    "service_spreadsheet": {
        "id": "1KzQLkz3u7kDbjZ-o42LjdC7tW-MiB0LXuoDi8BpATLk",
        "name": "sheet1"
    },

}



def main():
    google_api = GoogleApi()

    # values = google_api.get_values_of_spreadsheet(SPREAD_SHEETS['service_spreadsheet'])
    l = google_api.discovey_auth(SPREAD_SHEETS['service_spreadsheet'])
    # access_schema = {

    #     "key_column_number": 2,
    #     "login_path": 3,
    #     "login_name": 4,
    #     "login_password": 5,

    # }

    # access_data = google_api.convert_values_to_dict(access_schema, values)

    # get_only = google_api.get_specific_values_in_list([2,3,4,5], values)

    print()

if __name__ == '__main__':
    main()


