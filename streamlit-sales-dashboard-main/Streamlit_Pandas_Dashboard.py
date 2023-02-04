#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt
st.set_option('deprecation.showPyplotGlobalUse', False) ## Streamlit prompts an annoying error when i insert my barchart. This removes the error

data = 'C:/My Files/Python_Projects/Python Tutorials/Python Stuff/Interactive dashboard design using Streamlit/streamlit-sales-dashboard-main/supermarket_sales.xlsx'

## This sets the basic building block for my dashboard - 'title', layout etc...
st.set_page_config(
                    page_title = 'Sales Dashboard',  ## Title of the page/dashboard
                    page_icon = ':bar_chart:',       ## Icon for the dashboard/webpage
                    layout = 'wide'                  ## Layout of the webpage
)

## Caching the dataframe so that whenever we run the filter, streamlit does not re-read the entire excel/dataframe again. (Its lets our filter go through faster, cause streamlit
## no longer needs to re-read everything everytime we filter.)

## This is the data frame to be placed into my dashboard/webpage
@st.cache
def get_data_from_excel():
    df = pd.read_excel(data,                  
                       skiprows = 3,          ## Skip the rows in the excel sheet.
                       usecols = 'B:R',       ## The 'B:R' specifies the "B column" to "R Column"
                       sheet_name = 'Sales',  ## Specifies the desired sheetname from the excel to load
                       nrows = 1000           ## Specifies the number of rows you want to FULL DATAFRAME to show
                      ) 
    df['Hour'] = pd.to_datetime(df['Time'], format = '%H:%M:%S').dt.hour
    return df

df = get_data_from_excel()

## Inserting my dataframe into streamlit dashboard/webpage
#st.dataframe(df)

## Contructing my sidebar filters:
st.sidebar.header('Filter here: ')
city = st.sidebar.multiselect('Select the city: ',             # Title of the multiselect filter
                              options = df['City'].unique(),   # Options for my multiselect filter
                              default = df['City'].unique()    # Setting the default values of my multiselect filter
                             )

branch = st.sidebar.multiselect('Select the branch: ',             # Title of the multiselect filter
                              options = df['Branch'].unique(),   # Options for my multiselect filter
                              default = df['Branch'].unique()    # Setting the default values of my multiselect filter
                             )

gender = st.sidebar.multiselect('Select the gender: ',             # Title of the multiselect filter
                              options = df['Gender'].unique(),   # Options for my multiselect filter
                              default = df['Gender'].unique()    # Setting the default values of my multiselect filter
                             )

customer_type = st.sidebar.multiselect('Select the customer_type: ',             # Title of the multiselect filter
                                       options = df['Customer_type'].unique(),   # Options for my multiselect filter
                                       default = df['Customer_type'].unique()    # Setting the default values of my multiselect filter
                                      )

# Using the query() method from pandas, i assign my variables to my desired columns to enable the filters to work
df_filters = df.query(
    'City == @city & Branch == @branch & Gender == @gender & Customer_type == @customer_type '
)

df_filters['Hour'] = pd.to_datetime(df_filters['Time'], format = '%H:%M:%S').dt.hour


# Inserting my new data frame with embedded filter functions into my dashboard
# st.dataframe(df_filters)

### Building my MAINPAGE (Instead of showing the dataframe, I want the mainpage to show KPIs/Indicators instead)
st.title('Sales Dashboard')
st.markdown('---')


#Using pandas to build and show the Total KPIs
total_sales = round(df_filters['Total'].sum(),2)
average_rating = round(df_filters['Rating'].mean(),1) ## The 'round' and 1 after means rounding up the final value to 1 decimal place!!
star_rating = ':star:' * int(average_rating)
average_sale_by_transaction = round(df_filters['Total'].mean(),2)


left, middle, right = st.columns(3) ## st.columns allows streamlit to allocate space and insert our necessary KPIs together
with left:    # within the the column 'left' (defined in the previous line by st.columns)
    st.subheader(":bar_chart: Total Sales: ")  # Title of the subheader
    st.subheader(f'USD {total_sales}')
with middle:
    st.subheader("Average Rating: ")  # Title of the subheader
    st.subheader(f'{average_rating} {star_rating}')
with right:
    st.subheader("Average Sales: ")  # Title of the subheader
    st.subheader(f'USD {average_sale_by_transaction}')    

st.markdown('---') # Giving a long line to make it look neater using the markdown() method!



### Plotting the dang graphs but i use matplotlib instead of plotly because i can

df3 = df_filters.pivot_table(index = 'Product line', values = 'Total', aggfunc = sum).reset_index() ## Sorting into a new dataframe that shows the product group with the sum of sales for each product group

x = df3['Product line']
y = df3['Total']


plt.figure(figsize = (5,5))


barchart = plt.barh(x,y) ## .barh() plots out a HORIZONTAL BAR CHART
plt.title('Sales by Product Group USD')
plt.ylabel('Product Group')
plt.xlabel('Sales by Product Group (USD)', fontsize = 10)
plt.xticks(size = 12)
plt.yticks(size = 15)

for index,value in enumerate(y): ## THIS FOR LOOP HELPS TO PUT THE VALUES FOR HORIZONTAL BAR CHART
    plt.text(value, index, round(int(value)), size=10, ha='right',color = 'red')

plt.show()

left2, right2 = st.columns(2)

with left2:
	st.pyplot()

## BarChart for Sales VS Time:

Total_Sales_By_Hour = df_filters.pivot_table(index = ['Hour'], values = ['Total'], aggfunc = sum).reset_index()
Total_Sales_By_Hour.sort_values('Total', ascending = False)

plt.figure(figsize = (5,5))

x = Total_Sales_By_Hour['Hour']
y = Total_Sales_By_Hour['Total']

plt.bar(x,y)
plt.title ('Sales against Time (USD)')
plt.xticks(x)
plt.xlabel('Hours')
plt.ylabel("Sales (USD)")

for index in range(len(x)): ## THIS FOR LOOP HELPS TO PUT THE VALUES ON TOP OF THE BAR CHART

    plt.text(x[index], y[index], round(y[index]), size=7, ha='center',color = 'r')

plt.show()

with right2:
	st.pyplot()
	st.markdown('---')

## I can add in another plot in streamlit as long as i specify 'st.pyploy()' So streamlit will show 2 graphs
#barchart2 = plt.barh(x,y) ## .barh() plots out a HORIZONTAL BAR CHART
#plt.title('2nd Graph', fontsize = 30)
#plt.ylabel('Product Group', fontsize = 20)
#plt.xlabel('Sales by Product Group (USD)', fontsize = 20)
#plt.xticks(size = 15)


#st.pyplot()

st.markdown('---')

st.dataframe(df_filters)


## We are done with the dashboard, now we begin styling the dashboard!!!
# STYLING THE WEB APP (Will be using some custom CSS code)
# ---- HIDE STREAMLIT STYLE ----

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Then create a '.streamlit' folder and create a txtfile called 'config.toml' and paste the color and style codes from the tutorial inside. This will change the overall colors of the webpage.



