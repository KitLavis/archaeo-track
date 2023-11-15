import gspread
import os
import pyfiglet
from datetime import date
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
SESSION_REPORT = [0, 0, 0, 0, 0]
UPDATE_HISTORY = []

def print_header(header):
    T = header
    ASCII_art_1 = pyfiglet.figlet_format(T)
    print(ASCII_art_1)

def check_log():
    """
    While loop asks if the excavation area already exists.
    If yes then choose_area is triggered. If no then create_excavation_area
    is triggered. If the answer is invalid then it returns true and starts again.
    """
    current_excavation_areas = str(SHEET.worksheets()).split("'")
    area_titles = [v for i, v in enumerate(current_excavation_areas) if i % 2 == 1]
    area_titles.sort()
    print(f"\nCurrent excavation areas:\n")

    for area_title in area_titles:
        print(area_title)
    
    while True:
        area_name = input(f"\nDoes a log for the area already exist? (y/n): ")

        if area_name == "y":
            choose_existing_area()
            break
        elif area_name == "n":
            create_excavation_area()
            break
        else:
            print(f"\nAnswer invalid. Please enter either 'y' or 'n'")
    return True

def choose_existing_area():
    """
    List of worksheets is converted into a string and list comprehension is used
    to remove the unnecessary data, leaving purely the area titles.
    In the while loop the list is checked to see if it includes the area
    inputted by the user. If so get_finds_data is triggered.
    If not then returns true and loop starts again.
    """
    current_excavation_areas = str(SHEET.worksheets()).split("'")
    area_titles = [v for i, v in enumerate(current_excavation_areas) if i % 2 == 1]
    
    while True:

        chosen_area = input("Name of excavation area: ")

        if chosen_area in area_titles:
            print(f"\n{chosen_area} chosen\n")
            os.system('cls' if os.name == 'nt' else 'clear')
            print_header(f"{chosen_area}")
            UPDATE_HISTORY.append(chosen_area)
            return(chosen_area)
        else:
            print(f"{chosen_area} doesn't exist. Please choose an existing area.")
    return True

def create_excavation_area():
    """
    Creates new worksheet for the excavation area based on
    data inputted by the user
    """
    standard_headings = ["date", "ceramic", "flint", "bone", "metal", "other"]
    new_area_name = input("Name of new excavation area: ")
    print(f"\nCreating {new_area_name}...\n")
    new_area = SHEET.add_worksheet(title = f"{new_area_name}", rows=100, cols=20)
    new_area.append_row(standard_headings)
    new_area.format('1', {'textFormat': {'bold': True}})
    print(f"{new_area_name} successfully created\n")
    os.system('cls' if os.name == 'nt' else 'clear')
    print_header(f"{new_area_name}")
    UPDATE_HISTORY.append(new_area_name)

def get_finds_data():
    """
    Get finds data from the user.
    While loop repeatedly requests data from the user until
    they input a valid string of 5 numbers seperated by commas
    """
    while True:
        print("Enter number of each material type from the day's excavation.")
        print("Data should be 5 numbers seperated by commas in this order:")
        print(f"ceramic,flint,bone,metal,other.\n")

        data_str = input("Enter finds numbers here: ")

        finds_data = data_str.split(",")

        if validate_data(finds_data):
            print(f"\nFinds data is valid!\n")
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
    List comprehension removes unneccessary info and leaves the area title.
    For loop gets area title from the list and prints.
    """
    worksheet_str = str(worksheet).split("'")
    worksheet_name = [v for i, v in enumerate(worksheet_str) if i % 2 == 1]
    for area_name in worksheet_name:
        print(f"Updating {area_name} finds...\n")
        worksheet.append_row(data)
        print(f"{area_name} finds updated!\n")


def update_another_area():
    """
    While loop asks whether or not the user would like to update another area.
    if 'y' then main() runs again and the program restarts.
    If no then a whole site updates and goodbye message is printed.
    Program then exists.
    Loops until a correct answer is given
    """
    while True:

        update_again = input("Update another area? (y/n): ")

        if update_again == "y":
            os.system('cls' if os.name == 'nt' else 'clear')
            main()
            break
        elif update_again == "n":
            update_whole_site()
            os.system('cls' if os.name == 'nt' else 'clear')
            print_header("Thank You")
            print("for choosing the ArchaeoTrack finds manager.\n")
            print("Total finds this session:\n")
            print(f"{SESSION_REPORT}\n")
            print("Happy digging!")
            break
        else:
            print("Invalid answer. Please answer either 'y' or 'n'.")
    return True
 
def calculate_totals():
    """
    Calculates the total number of each find type for the session
    and adds them to the existing totals from the whole_site worksheet.
    """
    whole_site = SHEET.worksheet("whole_site").get_all_values()
    current_total = whole_site[-1]
    current_total.pop(0)

    new_totals = []

    for total, todays_data in zip(current_total, SESSION_REPORT):
        totals = int(total) + todays_data
        new_totals.append(totals)
    
    return new_totals

def update_session_report(data):
    """
    Adds new finds data to existing session total and then appends to
    SESSION_REPORT list
    """
    new_total = [x + y for x, y in zip(SESSION_REPORT, data)]
    SESSION_REPORT.clear()

    for x in new_total:
        SESSION_REPORT.append(x)

def update_whole_site():
    """
    Triggers calculate_totals function. The new totals are then added
    to the whole_site worksheet.
    """
    totals = calculate_totals()
    date_totals = [str(date.today())] + totals
    whole_site = SHEET.worksheet("whole_site")
    update_worksheet(date_totals, whole_site)

def main():
    """
    Run all Program functions
    """
    print_header("ArchaeoTrack")
    print("The archaeological finds tracker!")
    today = str(date.today())
    check_log()
    data = get_finds_data()
    finds_data = [int(num) for num in data]
    date_finds_data = [today] + finds_data
    
    grab_sheet_for_updating = UPDATE_HISTORY[-1]
    worksheet_to_update = SHEET.worksheet(f"{grab_sheet_for_updating}")
    
    update_worksheet(date_finds_data, worksheet_to_update)
    update_session_report(finds_data)

    update_another_area()

main()