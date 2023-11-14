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

def check_log():
    """
    While loop asks if the excavation area already exists.
    If yes then choose_area is triggered. If no then create_excavation_area
    is triggered. If the answer is invalid then it returns true and starts again.
    """
    current_excavation_areas = str(SHEET.worksheets()).split("'")
    area_titles = [v for i, v in enumerate(current_excavation_areas) if i % 2 == 1]
    print(f"Current excavation areas:\n")

    for area_title in area_titles:
        print(area_title)
    
    while True:
        area_name = input(f"\nDoes a log for the area already exist? (y/n): ")

        if area_name == "y":
            choose_existing_area()
            return "y"
        elif area_name == "n":
            create_excavation_area()
            return "n"
        else:
            print(f"\nAnswer invalid. Please enter either 'y' or 'n'")
    return True

def choose_existing_area():
    """
    List of worksheets is converted into a string
    In the while loop the string is checked to see if it inclues the area
    inputted by the user. If so get_finds_data is triggered.
    If not then returns true and loop starts at again.
    """
    current_excavation_areas = str(SHEET.worksheets()).split("'")
    area_titles = [v for i, v in enumerate(current_excavation_areas) if i % 2 == 1]
    global worksheet_to_update
    
    while True:

        chosen_area = input("Name of excavation area: ")

        if chosen_area in area_titles:
            print(f"{chosen_area} chosen")
            worksheet_to_update = SHEET.worksheet(f"{chosen_area}")
            break
        else:
            print(f"{chosen_area} doesn't exist. Please choose an existing area.")
    return True

def create_excavation_area():
    """
    Creates new worksheet for the excavation area based on
    data inputted by the user
    """
    standard_headings = ["ceramic", "flint", "bone", "metal", "other"]
    new_area_name = input("Name of new excavation area: ")
    print(f"\nCreating {new_area_name}...\n")
    new_area = SHEET.add_worksheet(title = f"{new_area_name}", rows=100, cols=20)
    new_area.append_row(standard_headings)
    new_area.format('1', {'textFormat': {'bold': True}})
    print(f"{new_area_name} successfully created\n")
    global worksheet_to_update
    worksheet_to_update = SHEET.worksheet(f"{new_area_name}")

def get_finds_data():
    """
    Get finds data from the user.
    While loop repeatedly requests data from the user until
    they input a valid string of 5 numbers seperated by commas
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
    worksheet.append_row(data)
    print(f"{worksheet} finds updated")

def update_another_area():
    """
    While loop asks whether or not the user would like to update another area.
    if 'y' then main() runs again and the program restarts.
    If no then a goodbye message is printer and the program exists.
    Loops until a correct answer is given
    """
    while True:

        update_again = input("Update another area? (y/n): ")

        if update_again == "y":
            main()
            break
        elif update_again == "n":
            print("Thank you for choosing the ArchaeoTrack finds manager.")
            print("Happy digging!")
            break
        else:
            print("Invalid answer. Please answer either 'y' or 'n'.")
    return True
 
def calculate_totals(finds_data):
    """
    Calculates the total number of finds across the site by adding the
    new finds_data inputted to the current values in the final row
    of the whole_site worksheet.
    """
    whole_site = SHEET.worksheet("whole_site").get_all_values()
    current_total = whole_site[-1]

    new_totals = []

    for total, finds in zip(current_total, finds_data):
        totals = int(total) + finds
        new_totals.append(totals)
    
    return new_totals

def main():
    """
    Run all Program functions
    """
    check_log()
    data = get_finds_data()
    finds_data = [int(num) for num in data]
    update_worksheet(finds_data, worksheet_to_update)
    new_totals = calculate_totals(finds_data)
    whole_site = SHEET.worksheet("whole_site")
    update_worksheet(new_totals, whole_site)
    update_another_area()

print(f"Welcome to the ArchaeoTrack finds manager\n")
main()