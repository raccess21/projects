# AXE: TWEET SCRAPER AND ANALYSER
        #### Video Demo:  [https://www.youtube.com/watch?v=15uf2FrUxUc](https://www.youtube.com/watch?v=15uf2FrUxUc)
        #### Description: Read below for description and documentation

## AXE Main Project Documentation

### Overview

The project.py acts as the main control script for scraping and analyzing tweets. It provides a menu-driven interface for users to choose between scraping tweets without login, scraping tweets with login for more data and filters, and analyzing tweet data. The project also includes functions for initializing required folders and handling user input.

The project.py includes functions for calculating and analysing word and pattern usage by fetching tweet data from local 'tdata' folder and plotting graphs accordingly as per specified attributes.

### Project Structure

- graphs folder is used for saving graphs
- tdata folder is used for saving scraped tweet data.
- drivers folder is used for keeping webdrivers.
- File names in tdata is coded username_of_account.json

### Dependencies

- `os` module
- 'glob` module
- 'time` module
- 'sys` module
- 're` module
- 'datetime` module
- 'json` module
- 'random` module
- 'selenium` module
- 'numpy` module
- 'matplotlib` module
- 'dateutil` module
- 'pytest` module


### 1. Configuration

- The `initialise_folder` function creates folders ("graphs" and "tdata") if they do not already exist.

- The `scrape_menu` function provides a menu-driven interface for scraping tweets. Users can choose between scraping without login (limited to 100 tweets per person) or logging in for more data and filters.

- wait_time is time in seconds that selenium will wait before generating error. Defaults to 50.

- The `analyse_menu` function allows users to input a list of words and select a mode for analysis (ranged or all). If ranged, users can input date ranges for analysis.

- The `main_menu` function serves as the main control menu. Users can choose between scraping tweets, analyzing tweets, or exiting the program.

### 2. Running the Script

To use the functions in your own script, import the `main_script` module and call the required functions as needed.

### 3. Functions

#### a. `initialise_folder()`

- Creates folders ("graphs" and "tdata") if they do not already exist.

#### b. `scrape_menu()`

- Provides a menu-driven interface for scraping tweets.
- Users can choose between scraping without login (limited to 100 tweets per person) or logging in for more data and filters.

#### c. `analyse_menu()`

- Allows users to input a list of words and select a mode for analysis (ranged or all).
- If ranged, users can input date ranges for analysis.

#### d. `main_menu()`

- Serves as the main control menu.
- Users can choose between scraping tweets, analyzing tweets, or exiting the program.

#### e. `occurence(word: list, data: str) -> int`

- Counts the occurrences of specified words within a given sample of string data.
- Counts word surrounded by quotes e;g counts shyam and Shyam's or plurals or hyphens and slashed
- Returns the count as an integer.

#### f. `calc_word_volume(words: list, data: dict) -> dict`

- Calculates the total instances of word usage for each specified word throughout the dataset for a given usser.
- Returns a dictionary with users as keys and a sub-dictionary containing words and their respective counts.

#### g. `calc_word_time(words: list, data: dict, dates: list) -> dict`

- Calculates the use of words over time for each user account.
- Returns a dictionary with users as keys, and for each user, there is a sub-dictionary containing words and their respective counts at different time intervals.

#### h. `saver(name, plt)`

Saves the generated plot with the specified name and timestamp as a PNG file in the `graphs` directory.

#### h. `get_words(cdata)`

Retrieves a list of unique words from the provided word usage data (`cdata`).

#### i. `plot_word_volume(cdata, save=False)`

Generates and displays a bar graph representing the volume of word usage for different users. Optionally, saves the plot as a PNG file if save is equal to True.

#### j. `plot_word_time(cdata, dates=None, save=False)`

Generates and displays line graphs illustrating the change in word usage over time for different users. Optionally, saves the plots as PNG files if save is True. If no dates are provided, it falls back to the `plot_word_volume` function.

## human.py

### Overview

human.py provides functions for configuring web drivers, specifically for Chrome and Firefox. The goal is to simulate human-like interactions by setting specific options, such as disabling features associated with automated control and configuring window size and user agent.

### Functions

#### a. `chrome_human()`

- Configures a Chrome web driver with specific options to simulate human-like interactions.
- Options include disabling features associated with automated control, setting the window size, and configuring a user agent.
- Returns a configured `webdriver.Chrome` object.

#### b. `firefox_human()`

- Configures a Firefox web driver with similar options as the `chrome_human` function.
- Returns a configured `webdriver.Firefox` object.

### Functions

## timemodes.py

### Overview

timemodes.py includes utility functions for handling and manipulating datetime objects. It provides convenient tools for working with dates, generating time periods, and standardizing datetime inputs.

### Functions

#### a. `daily()`, `monthly()`, `yearly()`

- Return `relativedelta` objects representing a 1-day, 1-month, and 1-year change in time, respectively.

#### b. `in_interval(date, st_date, end_date)`

- Check if a date falls within the specified date range (lower limit inclusive, upper limit exclusive).

#### c. `input_date(name="the", dt=' ')`

- Standardize user input for date values.
- Return a datetime object.

#### d. `input_period(period='l')`

- Take user input for selecting a time period (daily, monthly, or yearly).
- Return the corresponding function.

#### e. `tperiod(startdate='', enddate='')`

- Generate a list of date values for the x-axis of a graph.
- Specify start and end dates, and select a time period, daily, monthly or yearly.

#### f. `datetime_encoder(dt)`

- Serialize datetime objects to string format.

#### g. `datetime_decoder(dt)`

- Deserialize string-format datetime values to datetime objects.

# f#iles.py

## O#verview

files.py includes utility functions for loading, dumping, and manipulating tweet data stored in JSON format. It facilitates the management of tweet data for analysis and visualization purposes.

### Functions

#### a. `loader(fname, conv=False)`

- Loads tweet data from the specified file (`fname`).
- Optionally converts date strings to datetime objects if `conv` is set to `True`.

#### b. `dumper(fname, data=[])`

- Writes tweet data to the specified file (`fname`) in JSON format.
- Returns `True` if the operation is successful, `False` otherwise.

#### c. `get_ac_names(fpath = "tdata/")`

- Returns a list of all available Twitter account names based on the files in the specified directory (`fpath`).

#### d. `get_int(nums, mx, mn=0)`

- Checks for and returns a set of valid integers within a given range.
- The lower limit is included, and the upper limit is excluded.

#### e. `ac_selector()`

- Allows the user to select Twitter accounts from a list of available accounts based on partial or complete matches with entered usernames.
- Returns a list of selected account names.

## tscrape.py

### Overview

tscrape.py is a Python script designed to scrape tweets from specified Twitter accounts. It utilizes the Selenium web scraping library and includes functionalities for logging into a Twitter account, retrieving tweets from a specified user's timeline. It can also work without logging in with reduced capabilities

### Functions

#### a. `slowenter(val, ele)`

Simulates human-like slow typing of a given value into a specified web element.

#### b. `login(driver, user)`

Logs into a Twitter account using the provided Selenium WebDriver (`driver`) and user credentials.

#### c. `ptweet(driver, name)`

Scrapes tweets from the specified Twitter user's timeline using Selenium WebDriver. It saves the scraped data to a local file in JSON format as a list of tweets where every tweet is a dict.

#### d. `getdriver()`

Creates and returns a Selenium WebDriver with simulated human-like interaction.

#### e. `scrape(user=None)`

Main function to initiate the scraping process. It takes an optional user dictionary for login credentials. Inputs list of twitter usernames to scrape from.


### Conclusion

The Tweet Analyser provides a simple menu-driven interface for scraping and analyzing tweets. Users can easily navigate through the menu options to perform tasks such as scraping tweets, analyzing word usage, and visualizing the results.
