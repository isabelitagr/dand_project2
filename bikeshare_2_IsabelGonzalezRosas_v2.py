import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
dash = "------------------------------------------------------------------"
short_dash = "----------------------"
months = ['january', 'february', 'march', 'april', 'may', 'june']
chosen_city = ""

#----------------------------- GET FILTERS & LOAD DATA -----------------------------
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\n\n{} Hello! Let\'s explore some US bikeshare data! {}\n\n'.format(short_dash, short_dash))

    city = getCity()
    type_of_filter = getTypeOfFilters()   
    month, day = "", ""

    if type_of_filter == 'month':
    	month = getMonth()
    elif type_of_filter == 'day':
   	    day = getDay()
    elif type_of_filter == 'both':
   		month = getMonth()
   		day = getDay()
   	#no need for evaluating none since no filter needs to be applied
    print('-'*40)
    return city, month, day


def getCity():
	# get user input for city (chicago, new york city, washington).
	cities = list(CITY_DATA.keys())
	message = "- Which city would you like to see data from?\nPlease enter: 'chicago', 'new york city' or 'washington':  "
	error_message = "That's not a valid input please enter 'chicago', 'new york city' or 'washington':  "
	return getUserInput(message, error_message, cities)


def getTypeOfFilters():
	# ge user input for type of filter wanted
	filters = ['month', 'day', 'both', 'none']
	message = "\n- Would you like to filter the data by 'month', 'day', 'both' or not at all? Type 'none' for no filter:  "
	error_message = "That's not a valid input please enter 'month', 'day', 'both' or 'none':  "
	return getUserInput(message, error_message, filters)


def getMonth():
	# get user input for month    
    message = "\n- Which month?\nPlease enter: 'january', 'february', 'march', 'april', 'may' or 'june':  "
    error_message = "That's not a valid input please enter 'january', 'february', 'march', 'april', 'may' or 'june':  "
    return getUserInput(message, error_message, months)


def getDay():
	# get user input for day of week 
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    message = "\n- Which day?\nPlease enter: 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday' or 'sunday':  "
    error_message = "That's not a valid input please enter 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday' or 'sunday':  "
    return getUserInput(message, error_message, days)
	

def getUserInput(message, error_message, ls):
	"""
	Asks for users input, returns error adn requests new input in case input is not on list of possible values and rechecks selection
	Args:
		(str) message - the message that requests input from the user
		(str) error_message - the error message to show to the user in case of wrong input
		(str) ls - list with correct values that can be input
	Returns:
		(str) string with input
	"""
	is_correct = False
	str_input = input(message).lower()

	while is_correct == False:
		if str_input not in ls:
			str_input = input(error_message).lower()
		else:
			correct = input("You chose {}. \nIf it's not correct please enter N or press any key to continue. ". format(str_input)).lower()
			
			if correct == 'n':
				str_input = input(message).lower() # I ask for data again
			else:
				is_correct = True
				
	return str_input

#-----------------------------
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month, day of week and hour from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month 
    df['Day of Week'] = df['Start Time'].dt.weekday_name
    df['Start Time Hour'] = df['Start Time'].dt.hour     

    if month != "":     	
    	mon = months.index(month)+1 #to match january starting at 1 at dataframe
    	df = df[df['Month'] == mon] #http://cmdlinetips.com/2018/02/how-to-subset-pandas-dataframe-based-on-values-of-a-column/
    
    if day != "":
        df = df[df['Day of Week']==day.title()] 
    
    #print(df)

    return df


#----------------------------- TIME STATS -----------------------------
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # display the most common month
    displayCommonMonth(df)
    # display the most common day of week
    displayCommonWeekDay(df)
    # display the most common start hour
    displayCommonHour(df)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def displayCommonMonth(df):
	"""Calculates mode from df's Month column to get most popular month, calculates count and displays the information """
	common_month = df['Month'].mode()[0]
	count_common_month = df[df['Month'] == common_month]['Month'].count()
	print("- Most common month for travelling is: {} with {} records.\n".format(months[common_month-1].title(), count_common_month))


def displayCommonWeekDay(df):
	"""Calculates mode from df's 'Day of Week' column to get most popular day, calculates count and displays the information """
	common_day = df['Day of Week'].mode()[0]
	count_common_day = df[df['Day of Week'] == common_day]['Day of Week'].count()
	print("- Most common day for travelling is: {} with {} records.\n".format(common_day.title(), count_common_day))


def displayCommonHour(df):
	"""Calculates mode from df's 'Start Time Hour' column to get most popular hour, calculates count and displays the information """
	common_hour = df['Start Time Hour'].mode()[0]
	count_common_hour = df[df['Start Time Hour'] == common_hour]['Start Time Hour'].count()
	print("- Most common hour for travelling is: {} with {} records.\n".format(common_hour, count_common_hour))


#----------------------------- STATION STATS -----------------------------
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    displayCommonStartStation(df)
    # display most commonly used end station
    displayCommonEndStation(df)
    # display most frequent combination of start station and end station trip
    displayCommonFrequentCombination(df)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def displayCommonStartStation(df):
	"""Calculates mode from df's 'Start Station' column to get most popular start station, calculates count and displays the information """
	common_start_station = df['Start Station'].mode()[0]
	count_common_start_station = df[df['Start Station'] == common_start_station]['Start Station'].count()
	print("- Most common start station for travelling is: {} with {} records.\n".format(common_start_station, count_common_start_station))


def displayCommonEndStation(df):
	"""Calculates mode from df's 'End Station' column to get most popular end station, calculates count and displays the information """
	common_end_station = df['End Station'].mode()[0]
	count_common_end_station = df[df['End Station'] == common_end_station]['End Station'].count()
	print("- Most common end station for travelling is: {} with {} records.\n".format(common_end_station, count_common_end_station))


def displayCommonFrequentCombination(df):
	"""Calculates mode from combination od 'Start Station' and 'End Station' to get most popular combination, calculates count and displays the information """
	df['Combination'] = df['Start Station'] + ' - ' + df['End Station'] #local
	common_combination = df['Combination'].mode()[0]
	count_common_combination = df[df['Combination'] == common_combination]['Combination'].count()
	print("- Most common combination for travelling is: {} with {} records.\n".format(common_combination, count_common_combination))
	

#----------------------------- DURATION STATS -----------------------------
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    displayTotalTimeTravel(df)
    # display mean travel time
    displayMeanTime(df)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def displayTotalTimeTravel(df):
	"""Calculates sum of seconds travelled to get total time travelled and displays the information """
	total_seconds = df['Trip Duration'].sum()
	print("- Total travel time is: {} seconds.\n".format(total_seconds))	
	days, hours, minutes, seconds = getTimeFromSeconds(total_seconds)
	print("  That means: {} days, {} hours, {} minutes and {} seconds.\n".format(days, hours, minutes, seconds))


def displayMeanTime(df):
	"""Calculates mean of seconds travelled to get total time travelled, converts to  days, hours, minutes, seconds and displays the information """
	average_duration = 	df['Trip Duration'].mean()
	days, hours, minutes, seconds = getTimeFromSeconds(average_duration)
	if days <= 0:
		print("- Average travel time is: {} hours, {} minutes and {} seconds.\n".format(hours, minutes, seconds))	
	else:
		print("- Average travel time is: {} days, {} hours, {} minutes and {} seconds.\n".format(days, hours, minutes, seconds))	


def getTimeFromSeconds(total_seconds):
	#https://www.w3resource.com/python-exercises/python-basic-exercise-65.php
	time = total_seconds
	day = time // (24 * 3600)
	time = time % (24 * 3600)
	hour = time // 3600
	time %= 3600
	minutes = time // 60
	time %= 60
	seconds = time
	return day, hour, minutes, seconds



#----------------------------- USER STATS -----------------------------
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("- Count of users types:")
    print("{}\n".format(df.groupby('User Type')['User Type'].count()))
    
    if chosen_city != 'Washington':
    	# Display counts of gender
    	print("- Count of Gender:")
    	print("{}\n".format(df.groupby('Gender')['Gender'].count()))
    	# Display earliest, most recent, and most common year of birth
    	print("- Earliest year of birth: {}".format(int(df['Birth Year'].min())))
    	print("- Most recent year of birth: {}".format(int(df['Birth Year'].max())))
    	print("- Most common year of birth: {}".format(int(df['Birth Year'].mode()[0])))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
 

#----------------------------- DISPLAY RAW DATA -----------------------------
def displayRawData(df):
	"""Asks user if he wants to display raw data and acts accordingly to users input"""
	print("\n- Do you want to see raw data? ")
	yes_no = input("Please enter Y to see raw data or press any key to continue.").lower()
	last_index  = 0

	while yes_no == 'y':
		#display raw data
		print(df[last_index : last_index+5])
		last_index += 5
		#ask if continue
		yes_no = input("Please enter Y to see more raw data or press any key to continue: ").lower()


#----------------------------- MAIN -----------------------------
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        global chosen_city
        chosen_city = city.title()
        print(chosen_city)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        displayRawData(df)
		
        restart = input('\nWould you like to restart? Enter Y to restart or any key to finish.\n')
        if restart.lower() != 'y':
            break
        else:
        	print("\n{}{}\n".format(dash, dash))


if __name__ == "__main__":
	main()
