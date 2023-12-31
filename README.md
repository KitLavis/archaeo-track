# ArchaeoTrack
ArchaeoTrack is an archaeological finds manager which tracks the number of finds from each day of excavation, calculates the daily and all time totals of each material type, then stores the data on Google Sheets.

ArchaeoTrack is a Python terminal application, which runs in the Code Institute mock terminal on Heroku.

[Live deployment link](https://archaeo-track-cd104451ef31.herokuapp.com/)
![Am I Responsive image](docs/images/am-i-responsive.webp)

## Planning

### Project Aims

The first phase of planning was centred around who the target audience is, the aims of the project, and how these aims will be met:

- Who is the project for?
    - The project is for archaeologists, commercial archaeological companies, and researchers.
- The aims of the project:
    - To provide an application that efficiently recieves, stores, and analyses finds data.
- How will the aims be met?
    - Unnecessary information will be kept to a minimum.
    - Total number of pieces of each material type will be automatically calculated.

### Flowchart
Before work began on the coding side of the project, a flowchart was produced to clearly map the route the user takes in order to use the application, and how any invalid input will be handled.
![ArchaeoTrack Flowchart](docs/images/archaeo-track-flowchart.webp)

### Design
Due to the use of the application being function rather than fun, visual design was kept to a minimum. Headings are emphasised using ASCII art, red text is used to highlight invalid data, green text is used to highglight valid data and successful updates, and yellow text is used when printing totals.

## Features

### Existing Features

- Introduction Screen

![Introduction Screen](docs/images/intro.webp)

The introduction screen is shown when the user starts the program. The name of the program is emphasised at the top of the screen with ASCII art, and a brief description of the program is underneath. If a log for the excavation area exists, it is shown in the list. The user is asked whether the area they want to update already exists. If so they enter "y" and are asked to enter the name of the area. If they answer "n" they are asked to enter the name of the excavation area they to create a log for. If they answer incorrectly they are warned and are asked to input again. Examples of this can be seen in the [invalid data handling section](#Invalid-Data-Handling).

- Finds data collection

![Data collection](docs/images/data_collection.webp)

Once an area is selected or created, the user moves onto the data collection screen. Here they can enter the number of pieces of each material type found today in that excavation area. Instructions are given on how to input this data correctly. If inputted incorrectly, the user is warned and are asked to input again. This can be seen in the [invalid data handling section](#Invalid-Data-Handling).

- Succesfull Update Screen

![Successfull Update Screen](docs/images/session_so_far.webp)

Once the data is inputted correctly, the relevant worksheet is updated (see example below) and the user arrives at the next screen. Here they are told the log was successfully updated, which is emphasised by the use of green text, they are shown the running report in yellow, so they have a reminder of what has already been inputted, and finally they are asked whether or not they would like to update another area. If yes, they return to the beginning of the program. If no they move on to the final screen.

![Stored data example](docs/images/sheet_example.webp)

- Exit Screen

![Exit Screen](docs/images/end_of_session.webp)

Once the user has decided all of the finds data for the day is inputted they are moved on to the exit screen. Here they area thanked for using the service, and are shown both the total finds from the session and the total finds to date.

### Invalid Data Handling

- Area Already Exists

![Area already exists warning](docs/images/invalid_new_area.webp)

If the user has decided to create a log for a new area, but they enter the name of an area that already exists, they are thrown this warning. They are then asked whether or not they would like to update an existing area.

- Area doesn't exist

![Area doesn't exist warning](docs/images/invalid_existing_area.webp)

If the user has decided to update an area for which a log already exists, but they enter an incorrect area name, this warning is given. They are then asked whether or not they would like to create a new area.

- Empty Input

![Nothing inputted error](docs/images/empty_input_error.webp)

If the user leaves the input field empty when creating or selecting an excavation area, this warning is given and they are asked to input again.

- Data can't be converted to integer

![ValueError: data can't be converted](docs/images/invalid_data_int.webp)

If the user inputs an incorrect data type which cannot be converted to an integer, the user is thrown this error and asked to input the data again.

- Not enough values inputted

![ValueError: not enough values](docs/images/invalid_data.webp)

If the user does not input enough values during data collection, they are thrown this error message and asked to input the data again.

- Yes or no questions invalid input

![Invalid y/n answer](docs/images/invalid_answer.webp)

As has been explained throughout the features section, often the user is asked to answer a quesiotn with either "y" representing yes, or "n" representing no. In each case, if something other than "y" or "n" is entered, the user is given this warning, and asked to answer again.

### Future Features

Due to time constraints, there are a number of features yet to be implemented. For example:
- In future the user will have the ability to edit the existing rows of data from within the program. This will then automatically update the relevant sheets.
- The user will also be able to delete logs/sheets from the terminal.
- If the user attempts to update an area for which a log for the day already exists, they will be shown the day's log and asked if they still want to update it. This is to prevent data being inputted twice.
- To do all of the above, the user must also have the ability to view all existing data from within the terminal, so that is also a feature to be implemented in the future.
- The all time totals and daily total sheets can currently be manually updated in the program. The user is warned not to do this, however it is still possible. In future, this ability will be removed.

#### Ease of Future Development

A number of steps were taken in order to make future development as simple as possible. One of these is that each function is clearly commented with concise detail, in order to explain what each part of the function does. This helps any future developer to understand what they are looking at, even if they have never read the code before. All variables and functions are named according to what they represent or what they do, and the code is well spaced and adheres to the PEP 8 python standards, to keep the readability of the code at a high standard.

## Tools and Technologies

- Python was the programming language used.
- The Code Institute's mock terminal template was used to create the terminal.
- ASCII art was used to create the header styling in the terminal.
- Google Sheets was used to store the data.
- google.oauth2.service_account was used to allow the program to access data held in Google Sheets.
- gspread was imported to the project to allow manipulation of the Google Sheets spreadsheet from the terminal.
- pyfiglet was imported to the project for constant [validation](#Validation).
- datetime was imported to the project to allow for the data to be inputted into the spreadsheet with date information.
- colorama was imported to allow for coloured text within the terminal.
- os was imported to clear the terminal when called.
- Git was used for version control.
- GitHub was used to store the code.
- GitPod was the online IDE used.
- Heroku was used for [deployment](#Deployment).
- Am I Responsive was used to create the image at the top of this document.

## Testing and Validation

### Validation

As previously mentioned in the [tools and technologies secion](#Tools-and-Technologies), pyfiglet was used for constant linting and validation during the coding process, making sure all code is syntactically and stylistically correct, according to the standard PEP 8 style.

Code Institute's python linter was also used for validation, and returned the message "All clear, no errors found".

### Bug Finding and Fixing

Throughout the coding process whenever a new feature was added, it was thoroughly manually tested to ensure correct functionality. A number of different data types were inputted, correct and incorrect, valid and invalid, so that all possible bases were covered. This testing process gave light to a small number of issues that needed to be resolved in order the project to move forward. These included:
- All time totals would throw an error and not calculate when the user inputted data for the first time. This was because the first row of cells of the all time totals sheet had no values, therefore no total could be calculated. This was solved by adding zeroes to these cells before inputting any data into the application.
- Invalid names being accepted as an existing area. At first when choosing an existing area, if the user inputted part of an area name but not the full name e.g. *trench_0* the program would accept it as a valid input, and then throw an error saying the relevant sheet doesn't exist. This was solved by splitting and enumerating the sheet names, so they went from something like this: "worksheet 'trench_02' id:03", to this: "trench_02". The program then only recognised exact matches as valid inputs.

## Deployment

The application was deployed on Heroku, using the Code Institute mock terminal. The process used is as follows:

1. Create a Heroku account or sign in.
2. Click "create new app".
3. Enter app name and your region.
4. Navigate to the "settings" section and click "reveal Config Vars" in the "config vars" section.
5. Enter the key "PORT" with a value of "8000".
6. Add Python and NodeJS buildpacks.
7. Navigate to the "Deploy" section at the top of the page.
8. Choose GitHub as the deployment method.
9. Connect to Github and type in your repository name, or alternatively search for the repository.
10. Choose either automatic or manual deployment and then click "deploy".

## Credits

| Source | Usage |
| -------| ----- |
| Code institute | Four functions from the Love Sandwiches walkthrough project: get_finds_date, validate_data, update_worksheet and calculate_all_time_totals  |
| Code Institute | Mock terminal template for deployment |
| [Stack Overflow](https://stackoverflow.com/questions/28883769/remove-odd-indexed-elements-from-list-in-python) | Code for the list comprehension on lines 41, 76, 127, 236 and 251 |