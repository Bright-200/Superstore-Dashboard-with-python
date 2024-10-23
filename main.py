import streamlit as st
import warnings
import os
import plotly.express as px
import pandas as pd
from pathlib import Path
# creating an title and front text
THIS_PATH=Path(__file__).parent
CSV_FILE=THIS_PATH/'style'/'style.css'

st.set_page_config(page_title='SuperStore',page_icon=':bar_chart:',layout='wide',initial_sidebar_state="expanded")
with open(CSV_FILE) as f:
    st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)
warnings.filterwarnings("ignore")
st.title(':bar_chart: SuperStores')
st.markdown('<style>div.block-container{padding-top:3rem;}</style>',unsafe_allow_html=True)
# creating an import button
def get_person_name():
    query_params=st.experimental_get_query_params()
    return query_params.get("name",["Friend"])[0]
PERSON=get_person_name()
fl=st.file_uploader(':file_folder: **Click to Upload a File**',type=['csv', 'txt','zip','xls','xlsx'])

if fl is not None:
    filename=fl.name
    st.write(filename)
    df=pd.read_csv(filename,encoding='ISO-8859-1')    
else:
    os.chdir(r'C:\Users\HP\Downloads\Video\Dashboard with stream\Companies_Dashboard')
    df=pd.read_csv('Superstores.csv',encoding='ISO-8859-1')

# converting a date of the file 

col1,col2=st.columns((2))
df['Order Date']=pd.to_datetime(df['Order Date'])
starting_date=pd.to_datetime(df['Order Date']).min()
ending_date=pd.to_datetime(df['Order Date']).max()

with col1:
    data=pd.to_datetime(st.date_input('Starting Date',starting_date))

with col2:
    data_1=pd.to_datetime(st.date_input('Ending Date',ending_date))
df=df[(df['Order Date'] >= data) & (df['Order Date']<=data_1)].copy()
# creating a side bar
st.sidebar.header(":book: Choose these to filter the data")
region=st.sidebar.multiselect('Choose the Region',df['Region'].unique())
if not region:
    df2=df.copy()
else:#this will make the column produce only regions
    df2=df[df['Region'].isin(region)]

state=st.sidebar.multiselect('Choose the State',df2['State'].unique())
if not state:
    df3=df2.copy()
else:
    df3=df2[df2['State'].isin(state)]

city=st.sidebar.multiselect('Choose the City',df3['City'].unique())
if not city:
    df4=df3.copy()
else:
    df4=df3[df3['City'].isin(city)]
#creating boldly filter option on all 
if not city and not state and not region:
    filtered_df=df
elif not city and not state:
    filtered_df=df[df['Region'].isin(region)]
elif not region and not city:
    filtered_df=df[df['State'].isin(state)]
elif state and city:
    filtered_df=df3[df['State'].isin(state) & df['City'].isin(city)]
elif region and state:
    filtered_df=df3[df['State'].isin(state) & df['Region'].isin(region)]
elif region and city :
    filtered_df=df3[df['City'].isin(city) & df['Region'].isin(region)]
    
elif city:
    df3[df['City'].isin(city)]
else:
    filtered_df=df3[df3['State'].isin(state) & df3['City'].isin(city) & df3['Region'].isin(region)]

# making a plot on the the other categories using px that is plotly express to build
# creating a columns
category_df=filtered_df.groupby('Category',as_index=False)['Sales'].sum()
with col1:
    st.subheader(f'Category Data {PERSON}',divider='rainbow')
    fig_1=px.bar(category_df,x='Category',y='Sales',text=['${:,.2f}'.format(x) for x in category_df['Sales']],template='seaborn')
    st.plotly_chart(fig_1,use_container_width=True)

with col2:
    st.subheader('Region View Data',divider='rainbow')
    fig_2=px.pie(filtered_df,values='Sales',names='Region')
    fig_2.update_traces(text=filtered_df['Region'],textposition='outside',hole=0.5)
    st.plotly_chart(fig_2,use_container_width=True)

cl1,cl2=st.columns(2)
with cl1:
    with st.expander('Categories Sampling'):
        st.write(category_df.style.background_gradient(cmap='Oranges'))
        csv=category_df.to_csv(index=False).encode('utf8')
        st.download_button('download category',data=csv,mime='text/csv',file_name='Category.csv',help='Click here to download csv')
with cl2:
    with st.expander('Regions Sampling'):
        regions=filtered_df.groupby('Region',as_index=False)['Sales'].sum()
        st.write(regions.style.background_gradient(cmap='inferno_r'))
        csv=regions.to_csv(index=False).encode('utf8')
        st.download_button('Download Region Data',data=csv,mime='text/csv',file_name='Regions.csv',help='Click here to download csv')
# creating a columns for the timeseries analysis
st.subheader(':watch: Time Series Analysis',divider='rainbow' )
filtered_df['month_year']=filtered_df['Order Date'].dt.to_period('M')
lineChart=filtered_df.groupby(filtered_df['month_year'].dt.strftime('%Y : %b'))['Sales'].sum().reset_index()
fig_3=px.line(lineChart,x='month_year',y='Sales',template='gridon')
fig_3.update_layout(title='Time Series',titlefont=dict(size=28),yaxis=dict(titlefont=dict(size=28)),xaxis=dict(titlefont=dict(size=28)))
st.plotly_chart(fig_3,use_container_width=True)
# creating a download chart
st.subheader("Download Chart",divider='rainbow')
with st.expander("Download options"):
    csv=lineChart.to_csv().encode('utf8')
    st.write(lineChart.T)
    st.download_button('download',file_name='Time_series.csv',mime='text/csv',data=csv,use_container_width=True,icon='📚',help='Click here to download all the time series analysis data')


# creating a treemap for the data
fig_4=px.treemap(filtered_df,path=['Region','Category','Sub-Category'],values='Sales',template='seaborn',hover_data='Sales')
fig_4.update_traces(text=['${:,.2f}'.format(x) for x in filtered_df['Sales']])
fig_4.update_layout(height=650,width=800,title='Tree Map Of All Sales For Regions And Categories ',titlefont=dict(size=20),bargap=1)
st.plotly_chart(fig_4,use_container_width=True)
# creating a pie chart for the segment and the category

c1l,c2l=st.columns((2))
with c1l:
    st.subheader('Segment of wise Sales')
    # creating a pie chart for the segment sales
    
    fig_5=px.pie(filtered_df,template='gridon',names='Segment',values='Sales',hole=0.1)
    fig_5.update_traces(text=filtered_df['Segment'],textposition='inside')
    st.plotly_chart(fig_5,use_container_width=True,use_container_height=True)   
with c2l:
    st.subheader('Regions of wise Sales')
    # creating a pie chart for the segment sales
    
    fig_5=px.pie(filtered_df,template='gridon',names='Region',values='Sales',hole=0.1)
    fig_5.update_traces(text=filtered_df['Region'],textposition='inside',)
    st.plotly_chart(fig_5,use_container_width=True,)   
    
# creating a pivot fot the chart or data
import plotly.figure_factory as ff
st.header(':point_right: Summary of data',divider='green')
with st.expander("Summary of Data of the chart"):
    
    fig_6= ff.create_table(df[0:5][['Region','Category','Sub-Category','Segment','Sales','Quantity']],colorscale='haline')
    st.plotly_chart(fig_6,use_container_width=True)
    st.subheader(':dollar: Mark of wise Sales',divider='green')
    filtered_df['month_name']=filtered_df['Order Date'].dt.month_name()
    sub_categories_table=pd.pivot_table(filtered_df,columns='month_name',index=['Sub-Category'],values='Sales')
    st.write(sub_categories_table.style.background_gradient(cmap=('Oranges')))
    
#st.cache()    
# -------------------------------- Creating a Scatter plot for the chart 
st.subheader('This  is a scatter plot',help='Below is the scatter plot for all the data')
scatter_plot=px.scatter(filtered_df,x='Sales',y='Profit',hover_data='Sales',hover_name='Region',size_max=12,size='Quantity',animation_group='Sales')
scatter_plot.update_layout(title='Scatter Plot of Profit and Sales ',titlefont=dict(size=27),yaxis=dict(titlefont=dict(size=24)),xaxis=dict(titlefont=dict(size=24)))
st.plotly_chart(scatter_plot,use_container_width=True)
st.header('Download the original data used to create this data')
csv=df.to_csv().encode('utf-8')
st.download_button('Download the original data',data=csv,file_name='Original_Data.csv',mime='text/csv')
