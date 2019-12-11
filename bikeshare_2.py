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
    #Ask user which city's data they want to see - Chicago, New York City or Washington
    city = input("Which city would you like to explore? Chicago, New York City or Washington? ").lower()

    #Use while loop to validate user's input is one of the 3 cities
    while city not in ('chicago', 'new york city', 'washington'):
        city = input("Please enter only Chicago, New York City or Washington. ").lower()

    #Ask user what filter they want - month, day or not at all
    month = input('Which month would you like to filter by? January, February, March, April, May, June or All? ')

    #Ask user to enter specific month
    while month not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
       month = input('Please enter a month: January, February, March, April, May or June. ').lower()

    #Ask user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Which day of the week would you like to filter by?  All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday? ')

    #Ask user to enter specific day of week or all
    while day not in ('all', 'monday',' tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
        day = input('Please enter All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday ').lower()

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
    #Load data file into dataframe
    df = pd.read_csv(CITY_DATA[city])

    #Convert Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Extract month and day from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    #Filter by month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    #Filter by day of week
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #Convert Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Extract month from Start Time to create new column
    df['month'] = df['Start Time'].dt.month

    #Find most common month
    common_month = df['month'].mode()[0]
    print('Most common month: ', common_month)

    #Extract day of week from Start Time to create new column
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    #Find most common day of the week
    common_day = df['day_of_week'].mode()[0]
    print('Most common day of the week: ', common_day)

    #Extract hour from Start Time to create new column
    df['hour'] = df['Start Time'].dt.hour

    #Find most common start hour
    common_hour = df['hour'].mode()[0]
    print('Most common start hour of the week: ', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #Find and display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Most commonly used Start Station:', common_start_station)

    #Find and display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('Most commonly used End Station:', common_end_station)

    #Display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + ' and ' + df['End Station']
    print('Most frequent combination of Start Station and End Station is:', df['Trip'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #Display total travel time
    total_trip_duration = df['Trip Duration'].sum()
    print('Total trip duration:', total_trip_duration)

    #Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel time:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    print(df['User Type'].value_counts().to_frame())

    #Display earliest, most recent, and most common year of birth
    if 'Gender' in df.columns:
	    print(df['Gender'].value_counts().to_frame())
    else:
        print('Gender column does not exist for Washington')

    if 'Birth Year' in df.columns:
        print('\nThe earliest birth year:', df['Birth Year'].min().astype(int))
        print('\nMost recent year of birth:', df['Birth Year'].max().astype(int))
        print('\nMost common birth year:', df['Birth Year'].mode().astype(int))
    else:
        print('Birth Year column does not exist for Washington')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    while True:
        ans = input('Would you like to see 5 records of raw data? ')
        if ans == 'yes':
            print('\nTop 5 records: \n', df.head(5))
            break
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
