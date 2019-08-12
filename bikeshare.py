import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['January', 'February', 'March', 'April', 'May', 'June','All']
dayofweek = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','All']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('\nWould you like to see the data from Chicago, New York City or Washington?\n').lower()
    while not city in CITY_DATA:
        city = input('Please enter the correct city name\n').lower()        
    # TO DO: get user input for month (all, january, february, ... , june)
    month = input('Would you like to filter the data by month? Please select a month from January to June, or type "all" for no filter.\n').title()
    while not month in months:
        month = input('Please input a correct month. Select from January to June, or type "all" for no filter.\n').title()
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Would you like to filter the data by day of the week? Please select a day from Monday to Sunday, or type "all" for no filter.\n').title()
    while not day in dayofweek:
        day = input('Please input a correct day. Select from Monday to Sunday, or type "all" for no filter.\n').title()

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
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'All':
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'All':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df,month,day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # TO DO: display the most common month
    if month == 'All':
        df['month'] = df['Start Time'].dt.month
        popular_month = df['month'].mode()[0]
        popular_month_frequency = df['month'].value_counts().max()
        print('Most Frequent Month: {}\n Frequency: {}\n'.format(months[popular_month-1],popular_month_frequency))

    # TO DO: display the most common day of week
    if day == 'All':
        df['day'] = df['Start Time'].dt.dayofweek
        popular_day = df['day'].mode()[0]
        popular_day_frequency = df['day'].value_counts().max()
        print('Most Frequent Day of Week: {}\n Frequency: {}\n'.format(dayofweek[popular_day],popular_day_frequency))


    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    popular_hour_frequency = df['hour'].value_counts().max()
    print('Most Frequent Start Hour: {}\n Frequency: {}\n'.format(popular_hour,popular_hour_frequency))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    # TO DO: display most commonly used end station
    # TO DO: display most frequent combination of start station and end station trip
    
    commonstart = df['Start Station'].mode()[0]
    commonend = df['End Station'].mode()[0]
    df['comb'] = df['Start Station'] + ' -> ' + df['End Station']
    commoncomb = df['comb'].mode()[0]
    print("\nThe most commonly used start station: {}\nThe most commonly used end station: {}\nThe most frequent combination of start station and end station trip: {}\n".format(commonstart,commonend,commoncomb))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    # TO DO: display mean travel time
    totaltime = df['Trip Duration'].sum()
    meantime = df['Trip Duration'].mean()
    print("\nTotal travel time (s): {}\nMean travel time (s): {}\n".format(totaltime,meantime))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The counts of each user type: \n', user_types.to_csv(sep='\t'))

    # TO DO: Display counts of gender
    # TO DO: Display earliest, most recent, and most common year of birth
    if city == 'chicago' or city == 'new york city':
        gender = df['Gender'].value_counts()
        print('\nThe counts of each gender: \n', gender.to_csv(sep='\t'))
        commonyear = int(df['Birth Year'].mode()[0])
        earlistyear = int(df['Birth Year'].min())
        mostrecent = int(df['Birth Year'].max())
        print("\nUser's earliest year of birth: {}\nUser's most recent year of birth: {}\nUser's most common year of birth: {}\n".format(earlistyear,mostrecent,commonyear))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    """Display the result of the above analysis. Also provides raw data if required by the user.   """
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df,month,day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)        
        
        n=0
        raw = input('\nType "yes" if you want to see individual trip data.\n').lower()
        while raw == 'yes':
            print(df[['Start Time','End Time','Trip Duration','Start Station','End Station','User Type','Gender','Birth Year']].iloc[n:n+5])
            n = n+5
            raw = input('\nType "yes" if you want to see more individual trip data.\n').lower()                  

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
