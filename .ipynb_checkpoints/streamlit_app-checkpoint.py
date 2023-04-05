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
    res = 'Result for the course: ' + course
    st.write(res)
    st.write(pd.DataFrame(result))
    plot_result(df1, course)

def show_summary(df, college, passing_score):
    
    # add a hew column Eligible/Not Eligible
    # If the value in score is equal to or greater than tha passing_score
    df['Result'] = df['Score'].apply(lambda x: 'Eligible' if int(x) >= int(passing_score) else 'Not Eligible')
    
    st.write('Distribution of Applicants by Priority Course')    
    course_counts = df['First Priority'].value_counts()
    course_perc = course_counts.apply(lambda x: (x / course_counts.sum()).round(2) * 100)
    result = pd.concat([course_counts, course_perc], axis=1)
    result.columns = ['frequency', 'percentage']
    res = 'Result for the college: ' + college
    st.write(res)
    st.write(pd.DataFrame(result))
    
    for course in df['First Priority']:
        #filter the dataframe on the first priority
        df1 = df[df['First Priority'] == course]

        #count result per course
        res_counts = df1['Result'].value_counts()
        res_perc = res_counts.apply(lambda x: (x / res_counts.sum()).round(2) * 100)
        result = pd.concat([res_counts, res_perc], axis=1)
        result.columns = ['frequency', 'percentage']
        res = 'Result for the course: ' + course
        st.write(res)
        st.write(pd.DataFrame(result))
        
def plot_result(df1, course):
    scounts=df1['Result'].value_counts()
    labels = list(scounts.index)
    sizes = list(scounts.values)
    custom_colours = ['#ff7675', '#74b9ff']

    fig = plt.figure(figsize=(8, 3))

    plt.subplot(1, 2, 1)
    plt.pie(sizes, labels = labels, textprops={'fontsize': 10}, startangle=90, 
        autopct='%1.0f%%', colors=custom_colours)
    plt.subplot(1, 2, 2)
    p = sns.barplot(x = scounts.index, y = scounts.values, palette= 'viridis')
    _ = plt.setp(p.get_xticklabels(), rotation=90)
    plt.title('Results for the course ' + course)
    st.pyplot(fig)
    
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
    
    st.subheader("WVSUCAT Examination Results")
    year = '2018'
    options = df['Year'].unique()
    selected_option = st.selectbox('Select the year', options)
    if selected_option=='2018':
        year = selected_option
        df = filterByYear(df, year)
    else:
        year = selected_option
        df = filterByYear(df, year)
    
    st.write("Set the passing score")
    
    passing_score = st.slider("Passing Score", 50, 160, 80, 10)
    # Add the college column to the dataset
    df_colleges = pd.read_csv('courses.csv', header=0, sep = ",", encoding='latin')
    
    #create the college column by merging the college courselist
    merged = pd.merge(df, df_colleges, on='First Priority', how='left')
    # create new column in dataframe1 
    df['College'] = merged['College']
    
    #save a copy of the unfiltered dataframe
    df_copy = df
        
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
    
    if st.button('Show College Summary'):  
        df = filterByCollege(df_copy, college)
        show_summary(df, college, passing_score)
        
    #Select the course
    selected_option = st.selectbox('Select the course', options)
    if selected_option=='All':
        #filter again in case the user started over
        df = filterByCollege(df, college)
    else:
        course = selected_option
        df = filterByCourse(df, course)
        
    if st.button('Show WVSUCAT Report'):  
        for course in df['First Priority'].unique():
            show_result(df, course, passing_score)

#run the app
if __name__ == "__main__":
    app()
