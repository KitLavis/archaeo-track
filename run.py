import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('archaeo_track')

def get_finds_data():
    """
    Get finds data from the user.
    """
    print("Enter number of each material type from the day's excavation.")
    print("Data should be 5 numbers seperated by commas in this order:")
    print("ceramic,flint,bone,metal,other.")
    print("e.g. 13,5,0,6,8")

    data_str = input("Enter finds numbers here:\n")

    finds_data = data_str.split(",")

    return finds_data

def main():
    """
    Run all Program functions
    """
    data = get_finds_data()