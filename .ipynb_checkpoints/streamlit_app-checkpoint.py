#Input the relevant libraries
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from PIL import Image

def filterByCourse(df, course):
    if course=='All':
        return df
    else:  
        filtered_df = df[df['First Priority'] == course]  
        return filtered_df

def filterByCollege(df, college):
    if college=='All':
        return df
    else:  
        filtered_df = df[df['College'] == college]  
        return filtered_df

def filterByYear(df, year): 
    filtered_df = df[df['Year'] == year]  
    return filtered_df

def show_result(df, course, passing_score):
    
    # add a hew column Eligible/Not Eligible
    # If the value in score is equal to or greater than tha passing_score
    df['Result'] = df['Score'].apply(lambda x: 'Eligible' if int(x) >= int(passing_score) else 'Not Eligible')
    
    #filter the dataframe on the first priority
    df1 = df[df['First Priority'] == course]
    # get value counts and percentages of unique values in the column 
    value_counts = df1['Result'].value_counts(normalize=True)
    value_counts = value_counts.mul(100).round(2).astype(str) + '%'
    value_counts.name = 'Percentage'

    # combine counts and percentages into a dataframe
    result = pd.concat([df1['Result'].value_counts(), value_counts], axis=1)
    result.columns = ['Counts', 'Percentage']
    print('\n\n\nResult for the course ' + course)
    st.write(pd.DataFrame(result))


def loadcsvfile():
    csvfile = 'wvsucat.csv'
    df = pd.read_csv(csvfile, dtype='str', header=0, sep = ",", encoding='latin') 
    return df

# Define the Streamlit app
def app():
    st.title("Welcome to the WVSUCAT Dashboard")      
    st.subheader("(c) 2023 WVSU Management Information System")
                 
    st.write("This dashboard is managed by: Dr. Mardy Ledesma \nUniversity Registrar\nregistrar@wvsu.edu.ph")
                 
    st.write("WVSUCAT is the admission examination meant to screen the applicants and short-list them so that only eligible applicants may proceed to the next steps in the admission process.")

    #load the data from file
    df = loadcsvfile()
    
    st.subheader("Licensure Examination Results")
    year = '2018'
    options = df['Year'].unique()
    selected_option = st.selectbox('Select the year', options)
    if selected_option=='2018':
        year = selected_option
        df = filterByYear(df, year)
    else:
        year = selected_option
        df = filterByYear(df, year)
        
    # Add the college column to the dataset
    df_colleges = pd.read_csv('courses.csv', header=0, sep = ",", encoding='latin')
    
    #create the college column by merging the college courselist
    merged = pd.merge(df, df_colleges, on='First Priority', how='left')
    # create new column in dataframe1 
    df['College'] = merged['College']
    
    #This section will filter by college
    college = 'All'
    options = []
    for college in list(df['College'].unique()):
        options.append(college)
        
    selected_option = st.selectbox('Select the college', options)
    if selected_option=='CAS':
        #filter again in case the user started over
        college = selected_option
        df = filterByYear(df, year)
    else:
        college = selected_option
        df = filterByCollege(df, college)
     
    options = ['All']
    for course in list(df['First Priority'].unique()):
        options.append(course)
        
    selected_option = st.selectbox('Select the course', options)
    if selected_option=='All':
        #filter again in case the user started over
        df = filterByCollege(df, college)
    else:
        course = selected_option
        df = filterByCourse(df, course)
        
    passing_score = st.slider("Passing Score", 50, 160, 80)
    if st.button('Show Licensure Exam Report'):  
        for course in df['First Priority'].unique():
            show_result(df, course, passing_score)
        
#run the app
if __name__ == "__main__":
    app()
