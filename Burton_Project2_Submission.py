#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Matt Burton Submission via Udacity Terminal 8/20/2020
#resubmitted 8/21/2020
#refactored on 8/24/2020

import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

city_list = ['chicago','new york city','washington']

month_list = ['all','january','february','march','april','may','june']

day_list = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']

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
    city = input("What city can I get data for you on?  We currently have data for Chicago, Washington, and New York City: ").lower()

    
    while city not in city_list:
        #print('Sorry, we don\'t currently have data on',city.capitalize(), '!  Please enter either Chicgo, Washington or New York City.')
        print('Sorry, we don\'t currently have data on {} !  Please enter either Chicgo, Washington or New York City.'.format(city.capitalize()))
        print('\n')
        city = input("Let\'s try again, what city can I get data for you on?").lower()
    
   
    # get user input for month (all, january, february, ... , june)
    month = input("Enter a month between January through June or just enter \'all\' to display data for all of the months : ").lower()
    
    while month not in month_list:
        print('\n')
        print('Sorry, that is not a valid month choice. For example \'March\'')
        print('\n')
        month = input("Let\'s try again, enter Month Needed or \'all\' to display all of the months: ").lower()
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Enter Day of Week Needed or \'all\' to display all days : ").lower()

    while day not in day_list:
        print('\n')
        print('Sorry, that is not a valid day of week choice. Enter, for example \'Monday\'')
        print('\n')
        day = input("Let\'s try again, enter Day of Week Needed or \'all\' to display all days : ").lower()
     
    
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

    #Load csv data file into programe - this is from the city input above
    df = pd.read_csv(CITY_DATA[city])
    
    #Additional Columns to Dataframe 
    #convert to month text name from start date column
    df['Month_Name'] = pd.to_datetime(df['Start Time']).dt.strftime('%B').str.capitalize()
    #convert to year from start time column
    df['Year']  = pd.to_datetime(df['Start Time']).dt.year
    #convert to month int value for analytics from start time
    df['month'] = pd.to_datetime(df['Start Time']).dt.month
    #convert to weekday name from start time
    df['day_of_week'] = pd.to_datetime(df['Start Time']).dt.strftime('%A').str.lower()
    #covert to start hour from start time
    df['start_hour'] = pd.to_datetime(df['Start Time']).dt.strftime('%I %p')
    #create journey
    df['start_end_station'] = df['Start Station'] +' to ' + df['End Station']
    
    
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month,:]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day,:]
    
    
    return df



        
def time_stats(df, city, month, day):
    """Displays statistics on the most frequent times of travel."""
    
           
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the month that displays most often using mode function
    if month == 'all':
        print("The most common month is: {}".format(str(df['Month_Name'].mode().values[0])))
    
    # display the most common day of week
    if day == 'all':
        print("The most common day of the week is: {}".format(str(df['day_of_week'].mode().values[0]).capitalize()))
        
    
    # display the most common start hour
    print("The most common start hour is: {}".format(str(df['start_hour'].mode().values[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df, city):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most common start station is: {} ".format(df['Start Station'].mode().values[0]))

    # display most commonly used end station
    print("The most common end station is: {} ".format(df['End Station'].mode().values[0]))

    # display most frequent combination of start station and end station trip
    print("The most common route taken is: {} ".format(df['start_end_station'].mode().values[0]))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, city):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    days = ((df['Trip Duration'].div(86400)).sum()).round(2)
    hours = ((df['Trip Duration'].div(3600)).sum()).round(2)
    minutes = ((df['Trip Duration'].div(60)).sum()).round(2)

    print('The total time traveled if converted to days for this city would be {} days.'.format(days))
    print('The total time traveled if converted to hours for this city would be {} hours'.format(hours))
    print('The total time traveled if converted to minutes for this city would be {} minutes'.format(minutes))
    
    # display mean travel time
    print('The average trip duration is {} minutes long.'.format(str(df['Trip Duration'].div(60).mean())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    #city, month, day = get_filters()
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User Types: \n')
    value_no_dtype_users = (df['User Type'].value_counts())

    #Prints number of user types without the dtype or name
    print(value_no_dtype_users.to_csv(header=None, sep='\t'))
    
    print('Breakdown by gender and birth year: \n')
    # Display counts of gender - only in chicago and nyc, exludes washington data
    if city != 'washington':
        value_no_dtype_gender = (df['Gender'].value_counts())
        #Prints number of user types without the dtype or name
        print(value_no_dtype_gender.to_csv(header=None, sep='\t'))
        print('\n')
        print("The oldest riders were born in: {}".format(str(int(df['Birth Year'].min()))))
        print("The youngest riders were born in: {}".format(str(int(df['Birth Year'].max()))))
        print("The most common year of birth is: {}".format(str(int(df['Birth Year'].mode()))))
    else:
        print('The ',city.capitalize(),'data set does not contain gender or birth information.')
    
   # Display earliest, most recent, and most common year of birth

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#added per code reviewer comments 8/21/2020 and per rubric to ask user if they want raw data displayed
def raw_data_option(df):
    
    #validate responses for raw data option
    raw_data_list = ['yes','no']
       
    max_row = 5
    raw_data = input(('Would you like to see the raw data? Please enter yes or no: ').lower())
    
    #validate user response
    while raw_data not in raw_data_list:
        raw_data = input(('That is not a valid choice, please enter yes or no: ').lower())
        
    if raw_data == 'yes':
        #displays the first 5 rows of data
        print(df.iloc[0:max_row])
        while True:
                raw_data = input(('Would you like to see five more rows? Please enter yes or no: ').lower())
                if raw_data not in raw_data_list:
                     raw_data = print('That is not a valid choice, please enter yes or no: ')
                #takes user back to start
                elif raw_data == 'no':
                    return
                #keeps displaying the data until user says no
                elif raw_data == 'yes':
                    #changes the end index
                    max_row += 5
                    #establishes a new starting point for the index
                    new_start = max_row - 5
                    print(df.iloc[new_start:max_row])
    #exits if no raw data is needed
    elif raw_data == 'no':
        return
    
    
#Main fuction to display the inputs and results to end users
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, city, month, day)
        station_stats(df, city)
        trip_duration_stats(df, city)
        user_stats(df, city)
        raw_data_option(df) #added to show raw data 8/21/2020

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()


# In[ ]:




