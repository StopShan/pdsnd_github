import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Which city's bikeshare data would you like to see: Chicago, New York, or Washington?\n").lower()
    while city not in ("washington", "chicago", "new york", "new york city"):
        city = input("You've entered a city not in our database. Please enter Chicago, New York, or Washington.\n").lower()

    time_filter = input("Would you like to filter the data by month, day, or both? Type 'none' for no time filter.\n").lower()
    while time_filter not in ('month', 'day', 'both', 'none'):
        time_filter = input("You've entered an invalid value. Try 'month', 'day', or 'both'? Type 'none' for no time filter.\n").lower()
    month = "all"
    day = "all"

    if time_filter == "month" or time_filter == "both":
        # get user input for month (all, january, february, ... , june)
        month = input("Which month would you like to see? Select from January through June.\n").lower()
        while month not in MONTHS:
            month = input("Please enter a valid month, e.g. 'April'.\n").lower()

    if time_filter == "day" or time_filter == "both":
        # get user input for day of week (all, monday, tuesday, ... sunday)
        day = input("Which day of week would you like to see?\n").lower()
        while day not in DAYS:
            day = input("Please enter a valid day, e.g. 'Monday'.\n").lower()

    print("Calculating...")
    print('-'*40)
    return city, month, day


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
    if city == "new york":
        city = "new york city"

    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if len(df['month'].unique()) != 1:
        popular_month = MONTHS[df['month'].mode()[0] - 1]
        print('The most popular month for traveling is: {}'.format(popular_month.title()))

    # display the most common day of week
    if len(df['day_of_week'].unique()) != 1:
        popular_day = df['day_of_week'].mode()[0]
        print('The most popular day of week for traveling is: {}'.format(popular_day))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    if popular_hour < 12:
        am_pm = 'am'
    else:
        am_pm = 'pm'
    print('The most popular hour for traveling is: {}{}'.format(popular_hour, am_pm))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station is: {}'.format(popular_start_station))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station is: {}'.format(popular_end_station))

    # display most frequent combination of start station and end station trip
    popular_trip = ('from ' + df['Start Station'] + ' to ' + df['End Station']).mode()[0]
    print('The most common trip from start to end is: {}'.format(popular_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = round((df['Trip Duration'].sum())/60**2,2) # Hours
    print('The total travel time for the selected time filter is: {val:,} hours.'.format(val=total_travel_time))

    # display mean travel time
    mean_travel_time = round((df['Trip Duration'].mean())/60,2) # Minutes
    print('The average travel time for the selected time filter is: {val:,} minutes.'.format(val=mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    user_types = user_types.append(pd.Series(df['User Type'].isna().sum(), index=['No info']))
    print('Counts of user types: \n{}\n'.format(user_types.to_string(name=False, dtype=False)))

    # Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        gender = gender.append(pd.Series(df['Gender'].isna().sum(), index=['No info']))
        print('Counts of gender: \n{}\n'.format(gender.to_string(name=False, dtype=False)))
    except:
        print('There is no gender information for this city.\n')

    # Display earliest, most recent, and most common year of birth
    try:
        print('The earliest year of birth is: {}'.format(int(df['Birth Year'].min())))
        print('The most recent year of birth is: {}'.format(int(df['Birth Year'].max())))
        print('The most common year of birth is: {}'.format(int(df['Birth Year'].mode()[0])))
    except:
        print('There is no birth year information for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """Displays raw data if the user's answer is yes."""
    pd.set_option('display.max_columns',200)
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    start_loc = 0
    while (view_data == 'yes'):
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_data = input("Do you wish to continue?: ").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
