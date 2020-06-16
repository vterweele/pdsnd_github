import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('OK, let\'s find out some stuff on bikesharing in 3 major cities in the US! AND PLACE FILE ON GITHUB IN ANOTHER BRANCH')

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = input('Are we going to look at chicago, new york city or washington? Tell me!\n').lower()
    while city not in ('chicago', 'new york city', 'washington'):
        print('check again!')
        city = input('Are we going to look at chicago, new york city or washington?\n').lower()

    # TO DO: get user input for month (all, january, february, ... , june)

    month = input('Which month would you like to see data from, please?\nPlease choose from january, february, march, april, may, june or all.\n').lower()
    while month not in('january', 'february', 'march', 'april', 'may', 'june', 'all'):
        print('Please key in a correct month name\n')
        month = input('Which month would you like to see data from?\nPlease choose from january, february, march, april, may, june or all.\n').lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']
    day = input('\nSelect the day of the week you want to filter the bikeshare data by. \n Choose from the list: (sunday, monday, tuesday, wednesday, thursday, friday, saturday, all): ').lower()

    while True:
        if day in days:
            print('\nWe are working with {} data\n'.format(day.upper()))
            break
        else:
            print('\nPlease choose a valid day of the week from the list (sunday, monday, tuesday, wednesday, thursday, friday, saturday, all)\n')
            break

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

    # load data file into a dataframe

    data_file = CITY_DATA[city]
    df = pd.read_csv(data_file)

    # Convert 'Start Time' column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':

        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    try:
        popular_month = df['month'].mode()[0]
        print('The most popular month for travelling is:', popular_month)
    except Exception as e:
        print('Couldn\'t calculate the most common month, as an Error occurred: {}'.format(e))

    # display the most common day of week
    try:
        day_of_week = df['day_of_week'].mode()[0]
        print('Most popular day of the week for travelling is: ',day_of_week)
    except Exception as e:
        print('Couldn\'t calculate the most common day of week, as an Error occurred: {}'.format(e))


    # display the most common start hour
    try:
        popular_hour = df['hour'].mode()[0]
        print('The most popular starting hour for travelling is:',popular_hour)
    except Exception as e:
        print('Couldn\'t calculate the most common start hour, as an Error occurred: {}'.format(e))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    try:
        popular_start_station = df['Start Station'].mode()[0]
        popular_start_station_amount = df['Start Station'].value_counts()[0]
        print('The most popular start station is:',popular_start_station, 'and was used', popular_start_station_amount, 'times.')
    except Exception as e:
        print('Couldn\'t calculate the most used start station, as an Error occurred: {}'.format(e))
    #display most commonly used end station
    try:
        popular_end_station = df['End Station'].mode()[0]
        popular_end_station_amount = df['End Station'].value_counts()[0]
        print('The most popular end station is:',popular_end_station, 'and was used', popular_end_station_amount, 'times.')
    except Exception as e:
        print('Couldn\'t calculate the most used end station, as an Error occurred: {}'.format(e))

    # display most frequent combination of start station and end station trip
    try:
        popular_trip = df.loc[:, 'Start Station':'End Station'].mode()[0:]
        popular_trip_amt = df.groupby(["Start Station", "End Station"]).size().max()
        print('The most popular trip is:\n', popular_trip, '\n and was driven', popular_trip_amt,'times')
    except Exception as e:
        print('Couldn\'t calculate the most frequent combination of start station and end station, as an Error occurred: {}'.format(e))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    try:
        df['Time Delta'] = df['End Time'] - df['Start Time']
        total_time_delta = df['Time Delta'].sum()
        print('The total travel time was:', total_time_delta)
    except Exception as e:
        print('Couldn\'t calculate the total travel time of users, as an Error occurred: {}'.format(e))
    # display mean travel time
    try:
        total_mean = df['Time Delta'].mean()
        print('The mean travel time was:', total_mean)
    except Exception as e:
        print('Couldn\'t calculate the mean travel time of users, as an Error occurred: {}'.format(e))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    try:
        print('The amount and type of users are:\n', df['User Type'].value_counts())
    except Exception as e:
        print('Couldn\'t calculate the type of users, as an Error occurred: {}'.format(e))
    # Display counts of gender
    try:
        print('The amount and gender of users are:\n', df['Gender'].value_counts())
    except Exception as e:
        print('Couldn\'t calculate the amount and gender of users, as an Error occurred: {}'.format(e))
     # Display earliest, most recent, and most common year of birth
    try:
        earliest_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()
        most_common_year = df['Birth Year'].mode()
        print('The age structure of our customers is:\n' 'oldest customer was born in:', int(earliest_year),'\n' 'youngest customer: was born in:', int(most_recent_year),'\n' 'most of our customer are born in:', int(most_common_year))
    except Exception as e:
        print('Couldn\'t calculate the age structure of our customers, as an Error occurred: {}'.format(e))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):

    print('\nDisplay the raw data, if you want...\n')
    start_time = time.time()

    raw_data = 0
    while True:
        answer = input("Are you interested to see raw data? Yes or No").lower()
        if answer not in ['yes', 'no']:
            answer = input("try again! Yes or No").lower()
        elif answer == 'yes':
            raw_data += 6
            print(df.iloc[raw_data : raw_data + 6])
            again = input("You want six more? Yes or No").lower()
            if again == 'no':
                break
        elif answer == 'no':
            return

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
