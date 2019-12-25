import time
import pandas as pd
import numpy as np
import json
from collections import Counter

CITY_DATA = { 
               'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' 
            }
cities = ['chicago', 'new york city', 'washington']

months = ['all','january', 'february', 'march', 'april', 'may', 'june']

days = ['all','sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday' ]

def get_filters():
    
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city = input('Enter city to explore \n (options: chicago, new york city, washington): ').lower()
            # TO DO: get user input for month (all, january, february, ... , june)
    month = input('Enter month to explore \n (options: all, january, february, ... , june): ').lower()
                # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Enter week day \n (options: all, monday, tuesday, ... , sunday): ').lower()
    while day not in days or month not in months or city not in cities:
        print('invalid inputs')
        get_filters()
        
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
    # load chosen city data file into dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and weekday and hour from Start Time to add new columns
    df['month'] = df['Start Time'].dt.month
    df['week_day'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    # filter by month if applicable
    if month != 'all':
        #obtain month integer value using index
        month =  months.index(month) 
        df = df[ df['month'] == month ]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[ df['week_day'].str.lower() == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month = df['month'].value_counts().idxmax()
    print("{} is the most common month of travels".format(months[most_common_month].title()))
    # TO DO: display the most common day of week
    most_common_week = df['week_day'].value_counts().idxmax()
    print("{} is the most common week day of travels".format(most_common_week))
    # TO DO: display the most common start hour
    most_common_hour = df['hour'].value_counts().idxmax()
    print("{} is the most common hour of travels".format(most_common_hour))    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].value_counts().idxmax()
    print("The most commonly used start station :", most_common_start_station.title())

    # display most commonly used end station
    most_common_end_station = df['End Station'].value_counts().idxmax()
    print("The most commonly used end station :", most_common_end_station.title())
    #  display most frequent combination of start station and end station trip
    df['Start End Station'] = df[['Start Station', 'End Station']].apply(lambda x: ' - '.join(x), axis=1)
    most_common_start_end_stations = df['Start End Station'].value_counts().idxmax()

    print("The most commonly used pair of start - end stations used are : {}" \
            .format(most_common_start_end_stations))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def convert_to_hh_mm_ss(seconds): 
    return time.strftime("%H:%M:%S", time.gmtime(seconds))
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time is: ', convert_to_hh_mm_ss(total_travel_time))
    #  display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The average trip duration is: ', convert_to_hh_mm_ss(mean_travel_time))
    min_travel_time = df['Trip Duration'].min()
    print('Lowest trip duration is: ', convert_to_hh_mm_ss(min_travel_time))
    max_travel_time = df['Trip Duration'].max()
    print('The highest trip duration is: ', convert_to_hh_mm_ss(max_travel_time))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_count = df['User Type'].value_counts()
    print('User types count \n',user_types_count)
    if 'Gender' in df.columns:    
        # Display counts of gender
        gender_counts = df['Gender'].value_counts()
        print("Counts of gender:\n", gender_counts)
    if 'Birth Year' in df.columns:
        birth_year = df['Birth Year']
        # Display earliest, most recent, and most common year of birth
        earliest_birth_year = birth_year.min()
        print('The earliest birth year is: ', earliest_birth_year)
        most_recent_birth_year = birth_year.max()
        print('The most recent birth year is: ', most_recent_birth_year)
        most_common_birth_year = birth_year.value_counts().idxmax()
        print('The most common birth year is:',  most_common_birth_year)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Displays raw bikeshare data."""
    num_rows = df.shape[0]
    #To display each column in full
    pd.set_option('display.max_columns',len(df.columns))
    # iterate from 0 to the number of rows in steps of 5
    for i in range(0, num_rows, 5):
        
        confirm = input('\nWould you like to view raw data of this trip? Type \'yes\' or \'no\'\n> ')
        if confirm.lower() != 'yes':
            break
        
        #Get sets of next 5 datapoints 
        row_data = df.iloc[i: i + 5]
        print(row_data)
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
