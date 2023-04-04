#Input the relevant libraries
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from scipy.stats import chi2_contingency
from PIL import Image

def filterBy(df, campus):
    if campus=='All':
        return df
    else:  
        filtered_df = df[df['Campus'] == campus]  
        return filtered_df

def loadcsvfile(campus):
    csvfile = 'employee_cleaned.csv'
    df = pd.read_csv(csvfile, dtype='str', header=0, sep = ",", encoding='latin') 
    return df

#Define the Age Brackets
def getAgeBracket(age):
    age = int(age)

    if ( age > 59 ):
        return '60 to 65'
    if ( age > 49):
        return '50 to 59'
    if ( age > 39):
        return '40 to 49'
    if ( age > 29):
        return '30 to 39'
    if ( age > 19):
        return '20 to 29'
    else: 
        return 'invalid age'

#Define the Age Brackets
def getServiceBracket(years):
    years = int(years)    
    if ( years > 45 ):
        return '46 to 50'
    if ( years > 40 ):
        return '41 to 45'
    if ( years > 35 ):
        return '36 to 40'
    if ( years > 30 ):
        return '31 to 35'   
    if ( years > 25 ):
        return '26 to 30'
    if ( years > 20):
        return '21 to 25'
    if ( years > 15):
        return '16 to 20'
    if ( years > 10):
        return '11 to 15'
    if ( years > 5):
        return '5 to 10'
    if ( years > 0):
        return '1 to 5'
    else: 
        return 'invalid years'

def createPlots(df, columnName):
    st.write('Employee Distribution by ' + columnName)
    scounts=df[columnName].value_counts()
    labels = list(scounts.index)
    sizes = list(scounts.values)
    custom_colours = ['#ff7675', '#74b9ff']

    fig = plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    plt.pie(sizes, labels = labels, textprops={'fontsize': 10}, startangle=140, autopct='%1.0f%%', colors=custom_colours)
    plt.subplot(1, 2, 2)
    sns.barplot(x = scounts.index, y = scounts.values, palette= 'viridis')
    st.pyplot(fig)

    # get value counts and percentages of unique values in column 
    value_counts = df[columnName].value_counts(normalize=True)
    value_counts = value_counts.mul(100).round(2).astype(str) + '%'
    value_counts.name = 'Percentage'

    # combine counts and percentages into a dataframe
    result = pd.concat([df[columnName].value_counts(), value_counts], axis=1)
    result.columns = ['Counts', 'Percentage']
    st.write(pd.DataFrame(result))
    
    return

def createTable(df, columnName):
    
    st.write('Employee Distribution by ' + columnName)
    # get value counts and percentages of unique values in column 
    value_counts = df[columnName].value_counts(normalize=True)
    value_counts = value_counts.mul(100).round(2).astype(str) + '%'
    value_counts.name = 'Percentage'

    # combine counts and percentages into a dataframe
    result = pd.concat([df[columnName].value_counts(), value_counts], axis=1)
    result.columns = ['Counts', 'Percentage']
    st.write(pd.DataFrame(result))
    
    return

def twowayPlot(df, var1, var2):
    fig = plt.figure(figsize =(10, 3))
    p = sns.countplot(x=var1, data = df, hue=var2, palette='bright')
    _ = plt.setp(p.get_xticklabels(), rotation=90) 
    st.pyplot(fig)

# Define the Streamlit app
def app():
    
    # Load image from file
    img = Image.open("wvsu_logo.png")
    new_size = (200, 200)
    img = img.resize(new_size)
 
    # Create a container element and center it vertically
    container = st.container()
    container.horizontal_alignment = "center"

    # Display the image inside the container element and align it to the center
    with container:
        st.image(img)
        st.title("Welcome to the WVSU Human Resource Dashboard")
        
    st.subheader("(c) 2023 WVSU Management Information System")
                 
    st.write("This dashboard is managed by: \nAgustin C. Cabahug, Jr. \nSAO, WVSU Human Resource Office \nhrmo@wvsu.edu.ph")
                 
    st.write("A Human Resource Management (HRM) dashboard is a tool that provides a comprehensive visual representation of key HR metrics and data in real-time. It is used by HR professionals to monitor and analyze important HR information, such as employee turnover rates, performance metrics, and workforce demographics. The dashboard can display graphs, charts, tables, and other visual elements that help HR professionals quickly and easily understand the data and identify trends and patterns.")

    #create a dataframe
    df = pd.DataFrame()
    
    st.subheader("Employee Demographics")
    campus = 'Main'
    options = ['All', 'Main Campus', 'CAF Campus', 'Calinog Campus', 'Himamaylan Campus', 'Janiuay Campus', 'Lambunao Campus', 'Pototan Campus', 'WVSU Medical Center']
    
    selected_option = st.selectbox('Select the campus', options)
    if selected_option=='All':
        campus = selected_option
        df = loadcsvfile(campus)
    else:
        campus = selected_option
        df = loadcsvfile(campus)
        df = filterBy(df, campus)
        
    df['Age Bracket'] = df.apply(lambda x : getAgeBracket(x['Age']), axis=1)
    df['Years in Service Bracket'] = df.apply(lambda x : getServiceBracket(x['Years of Service']), axis=1)

    if st.button('Distribution By Gender'):
        df = filterBy(df, campus)
        createPlots(df, 'Gender')

    if st.button('Distribution By Employee Type'):
        df = filterBy(df, campus)  
        createPlots(df, 'Type')
   
        
    if st.button('Distribution By Employment Status'):
        df = filterBy(df, campus)  
        createPlots(df, 'Employment Status')

    if st.button('Distribution By Age Bracket'):
        df = filterBy(df, campus)  
        createPlots(df, 'Age Bracket')
        
    if st.button('Distribution By Years in Service Bracket'):
        df = filterBy(df, campus)  
        createPlots(df, 'Years in Service Bracket')

    if st.button('Distribution By Position'):
        df = filterBy(df, campus)  
        createTable(df, 'Position')
    
    if st.button('Distribution By Gender across Age Brackets'):
        df = filterBy(df, campus)  
        twowayPlot(df, 'Age Bracket', 'Gender')
        
    if st.button('Distribution By Gender across Employment Status'):
        df = filterBy(df, campus)  
        twowayPlot(df, 'Employment Status', 'Gender')
        
#run the app
if __name__ == "__main__":
    app()
