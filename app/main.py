import streamlit as st
import pandas
import utils
import os
from jinja2 import Environment, FileSystemLoader
import plotly.express as px
import plotly.graph_objects as go
from time import strptime
import numpy


task_dict = {
    "Total Registrations":"Registrations",
    "Vehicle Makers Infographics":"Makers",
    "Vehicle Category Infographics":"Category"
}

inputs={}

with st.sidebar:
    st.write('## Geographic Area')
    geography = st.selectbox("Select a Region",['India','Maharashtra'])


    st.write('## Task')
    task = st.selectbox("Type of Infographic",["Total Registrations","Vehicle Makers Infographics","Vehicle Category Infographics"])


template_sidebar = utils.import_from_file("template_sidebar",os.path.join("templates",task_dict[task],"sidebar.py")).show()


# env = Environment(
#     loader=FileSystemLoader(
#     os.path.join('templates',task_dict[task])),trim_blocks=True, lstrip_blocks=True
# )

if geography == 'India':
    if task == 'Total Registrations':
        df = pandas.read_excel('assets/India/Vehicle_Category_India.xlsx')
        df.drop(columns=['Sr.No'],inplace=True)
        for i in df:
            if i not in ['Vehicle Category','Month','Year']:
                df[i] = df[i].astype(str).apply(lambda x: x.replace(',','')).astype(int)
        df['Year'] = df['Year'].astype(str).apply(lambda x: x.replace(',','')).astype(int)
        df['Month'] = df['Month'].apply(lambda x: strptime(x, "%b").tm_mon)
        df_groupby = df.groupby(by ='Year').sum()
        y = []
        year_lis = []
        fig = go.Figure()
        for i in df_groupby.index:
            # print(df_groupby.loc[[i]]['ELECTRIC(BOV)'])
            y.append(df_groupby.loc[[i]]['ELECTRIC(BOV)'].values[0])
            year_lis.append(i)
        fig.add_trace(go.Scatter(x=year_lis,y=y,line_shape='spline',line=dict(color='blue',dash='dot')))
        fig.update_layout(height=600,width=600)
        st.plotly_chart(fig)
        df_groupby = df.groupby(by=['Year','Month']).sum()
        y=[]
        month_lis = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
        for i,j in enumerate(df_groupby.loc[[template_sidebar]]['ELECTRIC(BOV)'].values):
            y.append(j)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=month_lis,y=y))
        fig.update_layout(height=800,width=800)
        st.plotly_chart(fig)
    if task=='Vehicle Makers Infographics':
        df = pandas.read_excel('assets/India/Makers_India_Major_Electric.xlsx')
        df.drop(columns=['Sr.No'],inplace=True)
        for i in df:
            if i not in ['Maker','Month','Year','Month_Year','Time']:
                df[i] = df[i].astype(str).apply(lambda x: x.replace(',','')).astype(int)
        df['Year'] = df['Year'].astype(str).apply(lambda x: x.replace(',','')).astype(int)
        df['Month'] = df['Month'].apply(lambda x: strptime(x, "%b").tm_mon)
        df = df.sort_values(by=['Year','Month'])
        df_groupby = df.drop(columns=['Month_Year']).groupby(by=['Maker','Year','Month']).sum()
        df_groupby = df_groupby.sort_index()
        y = []
        year_lis = df[df['Maker']==template_sidebar]['Year'].unique()
        year_lis = year_lis[::-1]
        for i in year_lis:
            y.append(df_groupby.loc(axis=0)[pandas.IndexSlice[template_sidebar,i]]['ELECTRIC(BOV)'].sum())
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=year_lis,y=y,line_shape='spline',line=dict(color='blue',dash='dot')))
        fig.update_layout(height=600,width=600)
        st.plotly_chart(fig)
        with st.sidebar:
            year = st.selectbox('Select a Year',year_lis)
        months = len(df_groupby.loc(axis=0)[pandas.IndexSlice[template_sidebar,year]]['ELECTRIC(BOV)'])
        month = df_groupby.loc(axis=0)[pandas.IndexSlice[template_sidebar,year]]['ELECTRIC(BOV)'].index.values
        month_lis = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
        month_lis = month_lis[month[0]-1:month[-1]]
        y=[]
        for i in df_groupby.loc(axis=0)[pandas.IndexSlice[template_sidebar,year]]['ELECTRIC(BOV)']:
            y.append(i)
            print(y,template_sidebar,year)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=month_lis,y=y))
        fig.update_layout(height=800,width=800)
        st.plotly_chart(fig)
inputs = {
    'geography':geography,
    'task':task,
    'template_sidebar':template_sidebar
}

# template = env.get_template("code-template.py.jinja")
# code = template.render(
#     **inputs
# )





