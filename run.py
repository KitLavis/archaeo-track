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

def choose_excavation_area():
    current_excavation_areas = SHEET.worksheets()
    print("Current excavation areas:")

    for ex_area in current_excavation_areas:
        print(ex_area)
    
    while True:

        area_name = input("Does a log for the area already exist (y/n): ")

        if area_name == "y":
            print("Choose ex area")
            break
        elif area_name == "n":
            create_excavation_area()
            break
        else:
            print("Answer invalid. Please enter either 'y' or 'n'")
    return True
        

def create_excavation_area():
    """
    Creates new worksheet for the excavation area based on
    data inputted by the user
    """
    standard_headings = ["ceramic", "flint", "bone", "metal", "other"]
    new_ex_area_name = input("Name of excavation area: ")
    print(f"\nCreating {new_ex_area_name}...\n")
    new_ex_area = SHEET.add_worksheet(title = f"{new_ex_area_name}", rows=100, cols=20)
    new_ex_area.append_row(standard_headings)
    new_ex_area.format('1', {'textFormat': {'bold': True}})
    print(f"{new_ex_area_name} successfully created\n")


def get_finds_data():
    """
    Get finds data from the user.
    While loop repeatedly requests data from the user until
    they input a valid string of 6 numbers seperated by commas
    """
    while True:
        print("Enter number of each material type from the day's excavation.")
        print("Data should be 5 numbers seperated by commas in this order:")
        print("ceramic,flint,bone,metal,other.")

        data_str = input("Enter finds numbers here:\n")

        finds_data = data_str.split(",")

        if validate_data(finds_data):
            print("Finds data is valid!")
            break

    return (finds_data)

def validate_data(values):
    """
    Converts string values to integers so they can be used.
    If not possible, or if there isn't exactly 5 values,
    ValueError is raised
    """
    try:
        [int(value) for value in values]
        if len(values) != 5:
            raise ValueError(
                f"Exactly 5 values required, you've provided {len(values)}"
            )

    except ValueError as e:
        print(f"Invalid data: {e}, please input again.\n")
        return False
        
    return True

def update_worksheet(data, worksheet):
    """
    Recieves the new data to be inserted in the relevant worksheet
    """
    print(f"Updating {worksheet} finds...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} finds updated")

def main():
    """
    Run all Program functions
    """
    choose_excavation_area()
    # create_excavation_area()
    data = get_finds_data()
    finds_data = [int(num) for num in data]
    update_worksheet(finds_data, "trench_01")

print("Welcome to the ArchaeoTrack finds manager")
main()