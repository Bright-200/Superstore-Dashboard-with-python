# how i Startered 
imported 
pandas ,os,plotly.express,warnings
created a Title,topic,
bulid an uploader of csv using conditional statements
>...first condition if you upload a file the file name will be written and also store as dataframe
>...else change directory and upload as dataframe
changed Order Date Time to date Time
introduces two columns of starting date and ending date
creating a side bar for chosing Region
use if to included the region validation 
to ensure the validation you must make sure that the other df2 as use filter will be filter by the next option or state 
||--region--||--state--||:--||--state
where if not region the data will will be copied to a new variable df2 else: df2<-df[df["region"]].isin(region) mean the filter must be 
valid selections
the clue is if is not in region it should be copied to the df2 because the df2 is going to be used for the rest of the selections.
so in the nutshell the filter of one is in the filter of the other
bulid  the filter  on selections the idea is that if the filter of region to select state is deleted the state will be deleted and
so the filter of one thing response to the filter of the other
function {
    if not Any then the original data will be picked
    if not state and not city then your going to choose Region
    if not state and not Region then the original data will be Region
    if state and City then the data should be both selected for codes[&]
    if state and Region then the data should be both selected for codes[&]
    if state and City then the data should be both selected for codes[&]

}
bulild the first plot for the Sales on the Categories
# creating a columns
for Category Data and Region View Data
bulid a download for the Categories and the  Region
intall tabulate using pip or conda
# creating a time series analysis for the data
create column for the filtere_df['month_year'] to get the year and month from Order Date{dt to period}
create lineChart dataframe {dt.strftime()} sum and make reset of index
plot line(data,x and y of sales and months label,height,width template)
then show()
write subheader for the time series analysis
generate a dataframe of linechart
{fig2} means-> you plot
## creating download buttons
create a button for the file
################################
## create  a Treemap for the Regions ,category and Sub-Category
create a sub-header
create a px treemap 
create a update layout
# creating a Segment for Sales
create two columns for the columns
chart1,chart2 one for segment wise Sales and Category wise Sales pie
import plotly.figure
for the table
with expander 
create a five columns for the table
arrange them as id df[0:5][[column1,column2,column3,column4,column5,column6]]
create also a filter month ie that is get the names of the month columns using the dt.month_name( function)
# create also a sub_category_year of a pivot_table
plot it using the pandas pivot_table function 
## create a scatter plot of the sales and the profits of the  sales 
use the layout update to modify the text and title  of the chart use the dict to for the text enlargements

You must create a download for the csv or excel