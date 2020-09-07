from __future__ import print_function
import sys
import pickle
import os.path
import requests
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient import discovery
from oauth2client import client, tools, file


class GoogleApi:
    """
        GoogleAPi
            Needs to be an credentials file called only like "credentials.json"        
    """

    SHEET = ""
    CREDS = 'credentials.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    API_KEY = "AIzaSyACFRyobBkIAxJTarjFN3NCiwO7-VVi8Us"
    API_URL = "https://sheets.googleapis.com/v4/spreadsheets/{id}/values/{range_}?includeValuesInResponse=true&responseDateTimeRenderOption=FORMATTED_STRING&responseValueRenderOption=FORMATTED_VALUE&valueInputOption=RAW&key={api}"


    def __init__(self) -> None:
        super(GoogleApi, self).__init__()
        self.google_api_auth()

    def google_api_auth(self) -> None:
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                    self.CREDS , self.SCOPES)
                    creds = flow.run_local_server(port=0)
                except Exception as e:
                    print(e)
                    return False

            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        try:
            service = build('sheets', 'v4', credentials=creds)
        except Exception as e:
            print(e)
            return False

        # Call the Sheets API
        try:
            self.SHEET = service.spreadsheets()
        except Exception as e:
            print(e)
            return False

        if not self.SHEET: return False



    def get_spreadsheet(self, spreadsheet_creds: dict) -> 'An api object':
        try:
            get_spread_sheet = self.SHEET.values().get(
                                                        spreadsheetId=spreadsheet_creds['id'],
                                                        range=spreadsheet_creds['name']
                                                    ).execute()
            return get_spread_sheet
        except Exception as e:
            print(e)
            return False

    def get_values_of_spreadsheet(self, spreadsheet_creds: dict) -> list:

        get_spreadsheet_object = self.get_spreadsheet(spreadsheet_creds)
        if not get_spreadsheet_object: return False
        try:
            values = get_spreadsheet_object.get('values', [])
            if values:
                return values
            else:
                return False
        except Exception as e:
            print(e)
            return False

    def check_schema_on_integer_value(self, schema: dict):

        
        try:
            if isinstance(schema, dict):
                for index, (_, value) in enumerate(schema.items()):
                    if index == 0: continue
                    if not str(value).isnumeric(): return False
            else:
                for value in schema:
                    if not str(value).isnumeric(): return False
        except Exception as e:
            print(e)
            return False
        return True

    def get_specific_values_in_list(self, schema: list, values: list):

        data = list()
        try:
            for index, row in enumerate(values):
                if index == 0: continue
                intermideate_list = list()
                for needed_value in schema:
                    intermideate_list.append(row[needed_value])
                data.append(intermideate_list)
            return data
        except Exception as e:
            print(e)
            return False



    def convert_values_to_dict(self,schema: "dict {'param': 2} value must be an integer", values: list) -> dict:

        """convert_values_to_dict

        Accepts:
            schema: dict {'param': 2} value must be an integer,
            values: list
        
        @schema
            {
                'key_column_number': 2 # "key_column_number" also can be number of row in spreadsheet represents the name of key paramets in returning dict and valu eof that key param will be also dict
                "login_path": 3,
                "login_name": 4,
                "login_password": 5,
            } 
        
        """


        if not isinstance(schema, dict) or not self.check_schema_on_integer_value(schema): return False

        data = dict()



        for index, row in enumerate(values):
            if index == 0: continue
            try:
                key_name = row[int(schema['key_column_number'])]
            except Exception:
                key_name = schema['key_column_number']

            data[key_name] = {}
                        
            for schema_index, (name, column_number) in enumerate(schema.items()):
                if schema_index == 0: continue
                try:
                    data[key_name][name] = row[column_number]
                except Exception as e:
                    print(e)
                    continue

        return data

    def write_data_to_spread_sheet(self, spreadsheet_creds: dict, data: list):
        try:

            spreadsheet_id = spreadsheet_creds['id']

            # data = [
            #     {
            #         'range': range_,
            #         'values': values
            #     },
            #     # Additional ranges to update ...
            # ]
            value_input_option = "RAW"
                
            body = {
                'valueInputOption': value_input_option,
                'data': data
            }
            

            result = self.SHEET.values().batchUpdate(
            spreadsheetId=spreadsheet_id, body=body).execute()

        except Exception as e:
            print(e)
            return False



"""
    @How to Work
    google_api = GoogleApi()

    # values = google_api.get_values_of_spreadsheet(SPREAD_SHEETS['service_spreadsheet'])
    l = google_api.write_data_to_spread_sheet(SPREAD_SHEETS['service_spreadsheet'])
    
    # access_schema = {

    #     "key_column_number": 2,
    #     "login_path": 3,
    #     "login_name": 4,
    #     "login_password": 5,

    # }

    # access_data = google_api.convert_values_to_dict(access_schema, values)

    # get_only = google_api.get_specific_values_in_list([2,3,4,5], values)


"""



