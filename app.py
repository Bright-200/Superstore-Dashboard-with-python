import streamlit as st
import pandas as pd

import warnings
import plotly.express as px

from pathlib import Path

warnings.filterwarnings('ignore')
st.set_page_config(page_title='SupperStore',page_icon=':bar_chart:',layout='wide')
# import css
THIS_PATH=Path(__file__).parent
CSV_FILE=THIS_PATH/'style'/'style.css'
st.cache_resource()
st.title (":bar_chart: Supper Store Data")
st.markdown('''

            <style>div.block-container{padding-top:2rem;}
            </style>

''',unsafe_allow_html=True
)
fl=st.file_uploader(":file_folder: Upload a file ",type=(['txt','csv','xls','xlsx']))
if fl is not None:
    filename=fl.name
    st.write(filename)
    df=pd.read_csv(filename,encoding='ISO-8859-1')
else:
 
    df=pd.read_csv('Superstores.csv',encoding='ISO-8859-1')
with open(CSV_FILE) as f:
    st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)   
#converting order data to data format
# creating columns for the starting date and the ending date
Col1,Col2=st.columns(2)
df['Order Date']=pd.to_datetime(df['Order Date'])

Starting_date=pd.to_datetime(df['Order Date']).min()
End_date=pd.to_datetime(df['Order Date']).max()
# creating column for Start date
with Col1:
    date1=pd.to_datetime(st.date_input('Start Date',Starting_date))

with Col2:
    date2=pd.to_datetime(st.date_input('End Date',End_date))

df=df[(df['Order Date']>=date1)&(df['Order Date']<=date2)].copy()
st.sidebar.header('Choose Your Filter: ')
# creating a Region option
region=st.sidebar.multiselect('Choose your Region',df['Region'].unique())
#st.cache
if not region:
    df2=df.copy()
else:
    df2=df[df["Region"].isin(region)]

# creating a state option
state=st.sidebar.multiselect('Select the State',df2['State'].unique())
if not state:
    df3=df2.copy()
else:
    df3=df2[df2['State'].isin(state)]
    
city=st.sidebar.multiselect('Choose your City',df3['City'].unique())
if not city:
    df4=df3.copy()
else:
    df4=df3[df3['City'].isin(city)]
    
# Creating a filter option of vailidation 
if not region and not city and not state:
    filtered_df=df
elif not city and not state:
    filtered_df=df[df['Region'].isin(region)]
elif not region and not city: 
    filtered_df=df[df['State'].isin(state)]
elif state and city:
    filtered_df=df3[df['State'].isin(state) & df['City'].isin(city)]
elif region and city:
    filtered_df=df3[df['Region'].isin(region) & df['City'].isin(city)]
elif region and state:
    filtered_df=df3[df['Region'].isin(region) & df['State'].isin(state)]
elif city:
    filtered_df=df3[df3['City'].isin(city)]
else:
    filtered_df=df3[df3['Region'].isin(region) & df3['State'].isin(state) & df3['City'].isin(city)]

category_df=filtered_df.groupby(by='Category',as_index=False)['Sales'].sum()

with Col1:
    st.subheader("The Category of Sales")
    fig_1=px.bar(category_df,x="Category",y="Sales",text=['${:,.2f}'.format(x) for x in category_df['Sales']],template='gridon')
    st.plotly_chart(fig_1,use_contanier_width=True,height=200)

with Col2:
    st.subheader("Region total Sales",divider='green')
    fig_2=px.pie(filtered_df,values='Sales',names='Region',hole=0.5,template='gridon')
    fig_2.update_traces(text=filtered_df['Region'],textposition='outside')
    st.plotly_chart(fig_2,use_contanier_width=True,height=200)
    
# creating the download buttons
cl1,cl2 =st.columns(2)
with cl1:
    with st.expander("Category View Data"):
        st.write(category_df.style.background_gradient(cmap='plasma_r'))
        csv=category_df.to_csv(index=False).encode('utf8')
        st.download_button('Download Data',data=csv,file_name='Category.csv',mime='text/csv',
                           help='Click here to download data as CSV file'
                           )

with cl2:
    with st.expander("Region View Data"):
        Region_view=filtered_df.groupby(by='Region',as_index=False)['Sales'].sum()
        st.write(Region_view.style.background_gradient(cmap='inferno'))
        csv=Region_view.to_csv(index=False).encode('utf8')
        st.download_button('Download Data',data=csv,file_name='Regions.csv',mime='text/csv',
        help='Click here to download data as CSV file'
        )

# creating a time series analysis
filtered_df['month_year']=filtered_df['Order Date'].dt.to_period("M")
# creating a dataframe
linechart=filtered_df.groupby(filtered_df['month_year'].dt.strftime("%Y : %b"))['Sales'].sum().reset_index()
fig_3=px.line(linechart,x='month_year',y='Sales',labels={'Sales':'Amount'},height=500,width=1000,template='gridon'
             )
st.plotly_chart(fig_3,use_container_width=True)
# creating a download option

with st.expander('Download time series analysis'):
        st.write(linechart.T.style.background_gradient(cmap='plasma'))
        csv=linechart.to_csv(index=False).encode('utf-8')
        st.download_button(':watch: Download time series analysis',file_name='time_series_analysis.csv',data=csv,mime='text/csv',help='Click here to download file')
#create a tree map
st.markdown('''
            <style>div.block-container{padding-top:3rem;}</style>''',unsafe_allow_html=True
)
st.subheader('Tree Map of Sales based on Region,Category and Sub-Category')

fig_4=px.treemap(filtered_df,path=['Region', 'Category','Sub-Category'],values='Sales',hover_data='Sales',template='seaborn',color='Sub-Category')
fig_4.update_layout(width=500,height=800)
fig_4.update_traces(text=['${:,.2f}'.format(x) for x in filtered_df['Sales']])
st.plotly_chart(fig_4,use_container_width=True)

# CREATING A PIE FOR SEGEMENTS AND CATEGORIES
chart1,chart2=st.columns((2))
with chart1:
    st.subheader('Segement Wise Sales')
    fig_5=px.pie(filtered_df,values='Sales',names='Segment',template='seaborn')
    fig_5.update_traces(text=filtered_df['Segment'],textposition='inside',hole=0.1)
    st.plotly_chart(fig_5,use_container_width=True)

with chart2:
    st.subheader('Category Wise Sales')
    fig_5=px.pie(filtered_df,values='Sales',names='Category',template='gridon')
    fig_5.update_traces(text=filtered_df['Category'],textposition='inside',hole=0.1)
    st.plotly_chart(fig_5,use_container_width=True)
# creating a summary data 
import plotly.figure_factory as ff
st.subheader(':point_right: Months wise Sales Summary')
with st.expander(' :book: Summary of Data'):
    df_sample = df[0:5][["Region", "State", "City","Category","Sales","Profit","Quantity"]]
    fig_6=ff.create_table(df_sample,colorscale="Cividis")
    st.plotly_chart(fig_6,use_container_width=True)

    st.markdown('### Month wise sub-Category table')
    filtered_df['Month'] =filtered_df['Order Date'].dt.month_name()
    sub_category_year=pd.pivot_table(data=filtered_df,columns='Month',values='Sales',index=['Sub-Category'])
    st.write(sub_category_year.style.background_gradient(cmap='ocean_r'))
    
############# creating a Scatter plot for the filtered data###################
Scatterplot=px.scatter(filtered_df, x='Sales',y='Profit',size='Quantity')
Scatterplot['layout'].update(title='The Relationship between Sales and Profits Using a Scatter Diagram',titlefont=dict(size=27),
                             xaxis=dict(title='Sales',titlefont=dict(size=25)),yaxis=dict(title='Profit',
                 titlefont=dict(size=26))) 
st.plotly_chart(Scatterplot,use_container_width=True)

#creating a view of your dataset
cly1,cly2=st.columns((2))
with cly1:
    with st.expander(":book: View Dataset"):
        st.write(filtered_df.iloc[:500,1:20:2].style.background_gradient(cmap='inferno'))

with cly2:
    with st.expander(":file_folder: Download original Dataset"):
        csv=df.to_csv().encode('utf-8')
        st.download_button("Download Dataset", data=csv,file_name='Original_Data.csv',mime='text/csv')