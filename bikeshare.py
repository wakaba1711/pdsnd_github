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
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("\nWhich city would you like to filter by? New York City, Chicago or Washington?\n").lower()
        if city not in ('new york city', 'chicago', 'washington'):
            print("Invalid input. Please enter either New York City or Chicago or Washington")
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('\nWould you like to filter data by which month or all? Please enter a month from January to June or "all" for all\n').lower()
        if month not in ('january', 'february','march', 'april', 'may', 'june', 'all'):
            print("Invalid input. Please enter a month from January to June or \"all\" for all months.\n")
            continue
        else:
            break
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('\nWould you like to filter data by which day of week or all? Enter "all" for all days.\n').lower()
        if day not in ('monday', 'tuesday','wednesday', 'thursday', 'friday', 'saturday', 'sunday','all'):
            print("Invalid input. Please enter a valid value")
            continue
        else:
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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

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
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('most common month: ', popular_month)

    # display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]
    print('most common day of week: ', popular_day_of_week)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('most common hour: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    start_station = df['Start Station'].value_counts().idxmax()
    print('The most commonly used start station is: ', start_station)
    # display most commonly used end station

    end_station = df['End Station'].value_counts().idxmax()
    print('The most commonly used end station is: ', end_station)

    # display most frequent combination of start station and end station trip
    popular_combination = df.groupby(['Start Station','End Station']).size().idxmax()
    print('The most common route is: ', start_station, ' & ', end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print('Total travel time is: ', total_time)

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print('Mean travel time is: ', total_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nCounts of user types:\n')
    print(user_types)

    # Display counts of gender
    try:
        gender_count = df['Gender'].value_counts()
        print('\nCounts of gender:\n')
        print(gender_count)
    except KeyError:
        print('No data available')

    # Display earliest, most recent, and most common year of birth
    try:
        earliest = df['Birth Year'].loc[df['Birth Year'].idxmin()]
        print('The earliest birth year is: ', earliest)
    except KeyError:
        print('The earliest birth year: No data available')

    try:
        most_recent = df['Birth Year'].loc[df['Birth Year'].idxmax()]
        print('The most recent birth year is: ', most_recent)
    except KeyError:
        print('The most recent birth year: No data available')

    try:
        most_common = df['Birth Year'].mode()[0]
        print('The most common birth year is: ', most_common)
    except KeyError:
        print('The most common birth year: No data available')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

 # Display raw data
def raw_data(df):
    num_rows = df.count()[0]
    answer = input('\nDo you want to view first 5 rows of raw data? Enter yes or no.\n').lower()
    start_row = 0
    end_row = 5
    while True:
        print(df[start_row : end_row].to_string(index=False, header=False))
        input('do you want to view the next 5 rows of raw data? Enter yes or no.\n').lower()
        start_row += 5
        end_row +=5

        if answer != "yes":
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
