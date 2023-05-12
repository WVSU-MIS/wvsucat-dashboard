#Input the relevant libraries
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
#rom sklearn.preprocessing import LabelEncoder
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
    new_df = pd.DataFrame(filtered_df)
    new_df = new_df.copy().reset_index(drop=True)
    return new_df

def show_result(df, course, passing_score):
        
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
    result = pd.DataFrame(result)
    st.dataframe(result.reset_index(drop=True), use_container_width=True)
    plot_result(df1, course)

def show_summary(df, college):
    tab_title = 'Distribution of Applicants by Priority Course For the college: ' + college
    st.write(tab_title)
    
    #select only the needed columns
    df_courses = df.loc[:, ['First Priority', 'Slots']]
    df_courses = df_courses.drop_duplicates()
        
    course_counts = df['First Priority'].value_counts()
    course_perc = course_counts.apply(lambda x: (x / course_counts.sum()).round(2) * 100)
    df_courses['Applicants'] = list(course_counts)
    df_courses['Share of College \nApplicants (%)'] = list(course_perc)
    df_courses['Applicant to Slots Ratio'] = df_courses['Applicants'] / df_courses['Slots']                                                 
    def getPopularity(ratio):
        if ( ratio > 4.0 ):
            return 'very high'
        if ( ratio > 3.0 ):
            return 'high'
        if ( ratio > 2.0 ):
            return 'moderate'
        if ( ratio > 1.0):
            return 'low'
        else: 
            return 'very low'
    
    df_courses['Popularity'] = df_courses.apply(lambda x : getPopularity(x['Applicant to Enrollment Slots Ratio']), axis=1)
    
    st.dataframe(df_courses.reset_index(drop=True), use_container_width=True)
    st.write('Popularity Index Reference \
                               \n\tless than 1.0 - very low \
                               \n\t1.0 to 1.99 - low \
                               \n\t2.0 to 2.99 - moderate \
                               \n\t3.0 to 3.99 - high \
                               \n\t4.0 and higher - very high')

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
                 
    st.write("This dashboard is managed by: Mrs. Mardy Ledesma \nUniversity Registrar\nregistrar@wvsu.edu.ph")
                 
    st.write("WVSUCAT is the admission examination meant to screen the applicants and short-list them so that only eligible applicants may proceed to the next steps in the admission process.")

    #load the data from file
    df = loadcsvfile()
    
    st.subheader("WVSUCAT Examination Results of the Main Campus")
    year = '2018'
    options = df['Year'].unique()
    selected_option = st.selectbox('Select the year', options)
    if selected_option=='2018':
        year = selected_option
        df = filterByYear(df, year)
    else:
        year = selected_option
        df = filterByYear(df, year)
    
    st.write("Summary info for the year: " + str(year))
    desc = pd.DataFrame(df.describe().T)
    st.dataframe(desc.reset_index(drop=True), use_container_width=True)
    
    from statistics import mode
    
    df['Score'] = df['Score'].astype(int)
    # calculate the mean, min, and max values of column Score
    mean_values = df['Score'].mean()
    min_values = df['Score'].min()
    max_values = df['Score'].max()
    median_values = df['Score'].median()
    mode_values = mode(df['Score'])
    
    info = { 'Measure': ['Average', 'Lowest', 'Highest', 'Median', 'Mode'], 
              'Score': [ round(mean_values, 0), min_values, max_values, median_values, mode_values]}
    st.write('Some statistics about the applicant scores for the selected year: lowest, highest, mean, stc.')
    info = pd.DataFrame(info)
    st.dataframe(info.reset_index(drop=True), use_container_width=False)
              
    # Add the college column to the dataset
    df_colleges = pd.read_csv('courses.csv', header=0, sep = ",", encoding='latin')
    #create the college column by merging the college courselist
    merged = pd.merge(df, df_colleges, on='First Priority', how='left')
    
    # create new column in dataframe1 
    df['College'] = merged['College']
    df['Slots'] = merged['Slots']
    
    #This section will filter by college
    college = 'CAS'
    options = []
    for college in list(df['College'].unique()):
        options.append(college)
        
    selected_option = st.selectbox('Select the college', options)
    if selected_option != 'All':
        college = selected_option
        df = filterByCollege(df, college)
    
    if st.button('College Summary Report'):  
        show_summary(df, college)
     
    options = ['All']
    for course in list(df['First Priority'].unique()):
        options.append(course)
    
    st.subheader('Passing Score')
    st.write('The passing score determine what number of students are marked as "eligible" \
        to continue the admission process to WVSU.  Students whose scores are below the \
        passing score are ineligible for admission to their selected course.')
             
    st.write('Move the slider below to set the passing score')
    passing_score = st.slider('Passing Score', 50, 160, 80, 5)
    # add a new column Eligible/Not Eligible
    # If the value in score is equal to or greater than tha passing_score
    df['Result'] = df['Score'].apply(lambda x: 'Eligible' if int(x) >= int(passing_score) else 'Not Eligible') 
    #df = pd.DataFrame(df)
        
    #Select the course
    selected_option = st.selectbox('Select the course', options)
    if selected_option=='All':
        #filter again in case the user started over
        df = filterByCollege(df, college)
    else:
        course = selected_option
        df = filterByCourse(df, course)
        
    if st.button('Per Course Report for the Selected College'):  
        for course in df['First Priority'].unique():
            show_result(df, course, passing_score)

#run the app
if __name__ == "__main__":
    app()
