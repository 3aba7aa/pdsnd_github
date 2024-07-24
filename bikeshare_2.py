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
    cities = ['chicago', 'washington', 'new york city']
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        print("Enter the city you want to investigate information about it\n")
        city = input().lower()
        if city not in cities:
            print("invalid input!\n")
        else:
            break

    # get user input for month (all, january, february, ... , june)
    months = ["all", "january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
    while True:
        print("Enter the month you want to filter by it, you can choose to not use a filter by choosing 'all'\n")
        month = input().lower()
        if month not in months:
            print("invalid input!\n")
        else:
            break
    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ["all", "sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
    while True:
        print("Enter the day you want to filter by it, you can choose to not use a filter by choosing 'all'\n")
        day = input().lower()
        if day not in days:
            print("invalid input!\n")
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_of_week

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        days = ['saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        day = days.index(day) + 1
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    days = {1: 'saturday', 2: 'sunday', 3: 'monday', 4: 'tuesday', 5: 'wednesday', 6: 'thursday', 7: 'friday'}
    months = {1: 'january', 2:'february', 3:'march', 4:'april', 5:'may', 6:'june'}
    # display the most common month
    popular_month = df['month'].mode()[0]
    print("most common month: {}".format(months[popular_month]))
    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print("most common day of week: {}".format(days[popular_day]))
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("most common start hour: {}".format(popular_hour))
    


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].value_counts().sort_values(ascending = False)
    print("most commonly used start station: {}, {}".format(popular_start_station.index[0], popular_start_station.iloc[0]))
    # display most commonly used end station
    popular_end_station = df['End Station'].value_counts().sort_values(ascending = False)
    print("most commonly used end station: {}, {}".format(popular_end_station.index[0], popular_end_station.iloc[0]))

    # display most frequent combination of start station and end station trip
    df['Start_End_Station'] = df['Start Station'] + '-->' + df['End Station']
    most_start_end_station = df['Start_End_Station'].value_counts().sort_values(ascending=False)
    print("most frequent combination of start and end stations: {}".format(most_start_end_station.index[0]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    print("Total Travel Time: {}".format(total_duration))
    # display mean travel time
    mean_duration = df['Trip Duration'].mean()
    print("Travel Time mean: {}".format(mean_duration))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    
    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)
    # Display counts of gender
    if city != 'washington':
        user_genders = df['Gender'].value_counts()
        print(user_genders)
    else:
        print("Washington city has no specified Gender for people")
    # Display earliest, most recent, and most common year of birth
    if city != 'washington':
        birth_years = df['Birth Year'].value_counts().sort_values(ascending=False)
        print("earliest year of birth: {}".format(df['Birth Year'].min()))
        print("most recent year of birth: {}".format(df['Birth Year'].max()))
        print("most common year of birth: {}".format(birth_years.index[0]))
    else:
        print("Washington city has no specified year of birth for people")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def prompt(df):
    ans = None
    start = 0
    while True:
        print("do you want to see five more line of data?")
        ans = input().lower()
        if ans == 'yes':
            print(df.iloc[start: start+5])
            start+=5
            continue
        elif ans == 'no':
            break
        else:
            print('invlaid inpu!')
            continue


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)      
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
    

    prompt(df)
if __name__ == "__main__":
	main()
