import os
from datetime import date
import gspread
import pyfiglet
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
SESSION_TOTALS = [0, 0, 0, 0, 0]
UPDATE_HISTORY = []
RUNNING_REPORT = {}


def print_header(header):
    """
    Prints text as ASCII header style when called
    """
    text = header
    header_text = pyfiglet.figlet_format(text)
    print(header_text)


def check_log():
    """
    While loop asks if the excavation area already exists.
    If yes then choose_area is triggered. If no then create_excavation_area
    is triggered. If the answer is invalid then it returns true and starts again.
    """
    current_excavation_areas = str(SHEET.worksheets()).split("'")
    area_titles = [v for i, v in enumerate(current_excavation_areas) if i % 2 == 1]
    area_titles.sort()
    print("\nCurrent excavation areas:\n")

    for area_title in area_titles:
        print(area_title)
    while True:
        area_name = input("\nDoes a log for the area already exist? (y/n): ")

        if area_name == "y":
            choose_existing_area()
            break
        elif area_name == "n":
            create_excavation_area()
            break
        else:
            print("\nAnswer invalid. Please enter either 'y' or 'n'")
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
            UPDATE_HISTORY.append(chosen_area)
            os.system('cls' if os.name == 'nt' else 'clear')
            print_header(f"{chosen_area}")
            return chosen_area
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
    UPDATE_HISTORY.append(new_area_name)
    os.system('cls' if os.name == 'nt' else 'clear')
    print_header(f"{new_area_name}")


def get_finds_data():
    """
    Get finds data from the user.
    While loop repeatedly requests data from the user until
    they input a valid string of 5 numbers seperated by commas
    """
    while True:
        print("Enter number of each material type from the day's excavation.")
        print("Data should be 5 numbers seperated by commas in this order:")
        print("ceramic,flint,bone,metal,other.\n")

        data_str = input("Enter finds numbers here: ")

        finds_data = data_str.split(",")

        if validate_data(finds_data):
            print("\nFinds data is valid!\n")
            break

    return finds_data


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


def update_running_report(area, finds_data):
    """
    Updates RUNNING_REPORT dictionary and prints so the user sees
    what they have done during the session
    """
    worksheet_str = str(area).split("'")
    worksheet_name = [v for i, v in enumerate(worksheet_str) if i % 2 == 1]

    for area_name in worksheet_name:
        RUNNING_REPORT[area_name] = str(finds_data)
    print("Session so far:\n")
    for keys,values in RUNNING_REPORT.items():
        print(f"{keys} : {values}")


def update_another_area():
    """
    While loop asks whether or not the user would like to update another area.
    if 'y' then main() runs again and the program restarts.
    If no then a whole site updates and goodbye message is printed.
    Program then exists.
    Loops until a correct answer is given
    """
    while True:

        update_again = input("\nUpdate another area? (y/n): ")

        if update_again == "y":
            os.system('cls' if os.name == 'nt' else 'clear')
            main()
            break
        elif update_again == "n":
            update_all_time_totals()
            update_daily_totals_sheet()
            os.system('cls' if os.name == 'nt' else 'clear')
            print_header("Thank You")
            print("for choosing the ArchaeoTrack finds manager.\n")
            print("Total finds this session:\n")
            print("Ceramic | Flint | Bone | Metal | Other")
            print(str(SESSION_TOTALS))
            print("\nHappy digging!")
            break
        else:
            print("Invalid answer. Please answer either 'y' or 'n'.")
    return True


def calculate_all_time_totals():
    """
    Calculates the total number of each find type for the session
    and adds them to the existing totals from the whole_site worksheet.
    """
    all_time_totals = SHEET.worksheet("all_time_totals").get_all_values()
    current_total = all_time_totals[-1]
    current_total.pop(0)

    new_totals = []

    for total, todays_data in zip(current_total, SESSION_TOTALS):
        totals = int(total) + todays_data
        new_totals.append(totals)
    return new_totals


def update_session_totals(data):
    """
    Adds new finds data to existing session total and then appends to
    SESSION_TOTALS list
    """
    new_total = [x + y for x, y in zip(SESSION_TOTALS, data)]
    SESSION_TOTALS.clear()

    for x in new_total:
        SESSION_TOTALS.append(x)


def update_daily_totals_sheet():
    """
    Updates the daily_totals worksheet with todays date and the
    session totals.
    """
    daily_sheet = SHEET.worksheet("daily_totals")
    daily_sheet_vals = daily_sheet.get_all_values()
    previous_day = daily_sheet_vals[-1]
    today_totals = [str(date.today())] + SESSION_TOTALS
    if today_totals[0] != previous_day[0]:
        daily_sheet.append_row(today_totals)
    else:
        previous_day.pop(0)
        previous_day = [int(num) for num in previous_day]
        added_totals = [str(date.today())] + [x + y for x, y in zip(SESSION_TOTALS, previous_day)]
        all_rows = daily_sheet.get_all_records()
        last_row_index = len(all_rows) + 1
        daily_sheet.delete_rows(last_row_index)
        daily_sheet.append_row(added_totals)


def update_all_time_totals():
    """
    Triggers calculate_totals function. The new totals are then added
    to the whole_site worksheet.
    """
    calculated_totals = calculate_all_time_totals()
    date_totals = [str(date.today())] + calculated_totals
    all_time_totals = SHEET.worksheet("all_time_totals")
    update_worksheet(date_totals, all_time_totals)


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
    update_session_totals(finds_data)
    update_running_report(worksheet_to_update, finds_data)
    update_another_area()

main()
