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
    STORE = ""
    DICOVERY_SERVICE = ""

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
            print(service)
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

        # ##############################################
        # self.STORE = file.Storage('diskovery.json')


        # flow = client.flow_from_clientsecrets(
        #     self.CREDS, 
        #     [
        #        'https://www.googleapis.com/auth/drive',
        #        'https://www.googleapis.com/auth/drive.file',
        #        'https://www.googleapis.com/auth/spreadsheets',
        #     ]
        # )

        # self.DICOVERY = tools.run_flow(flow, self.STORE)

        # self.DICOVERY_SERVICE = discovery.build('sheets', 'v4', credentials=creds)


    def get_spreadsheet(self, spreadsheet_creds: dict) -> 'An api object':
        try:
            get_spread_sheet = self.SHEET.values().get(
                                                        spreadsheetId=spreadsheet_creds['id'],
                                                        range=spreadsheet_creds['name']
                                                    ).execute()
            print(get_spread_sheet)
            return get_spread_sheet
        except Exception as e:
            print(e)
            return False

    def get_values_of_spreadsheet(self, spreadsheet_creds: dict) -> list:

        get_spreadsheet_object = self.get_spreadsheet(spreadsheet_creds)
        print(get_spreadsheet_object)
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

    def write_data_to_spread_sheet(self, spreadsheet_creds: dict):


        # The ID of the spreadsheet to update.
        spreadsheet_id = spreadsheet_creds['id']

        # The A1 notation of the values to update.
        range_ = 'sheet1!A2'
        # api_path = self.API_URL.format(id=spreadsheet_creds['id'], range_=range_,api=self.API_KEY)
        # print(api_path)
        # How the input data should be interpreted.
        value_input_option = {}

        
        values = [
            [
                "lol",
                "kek",
                "aplet"
            ]
        ]
        
        data = [
            {
                'range': range_,
                'values': values
            },
            # Additional ranges to update ...
        ]

        value_input_option = "RAW"
            
        body = {
            'valueInputOption': value_input_option,
            'data': data
        }
        
        # r = requests.put(api_path,data=value_range_body).text
        # print(r)

        result = self.SHEET.values().batchUpdate(
        spreadsheetId=spreadsheet_id, body=body).execute()
        print('{0} cells updated.'.format(result.get('totalUpdatedCells')))
    # def write_to_spread_sheet(self, spreadsheet_creds: dict, writable_data: ):

    #     values = [
    #         [
    #             # Cell values ...
    #         ],
    #         # Additional rows ...
    #     ]
    #     body = {
    #         'values': values
    #     }
    #     result = self.SHEET.values().update(
    #         spreadsheetId=spreadsheet_creds['id'], range=spreadsheet_creds['name'],
    #         valueInputOption=value_input_option, body=body).execute()
    #     print('{0} cells updated.'.format(result.get('updatedCells')))










