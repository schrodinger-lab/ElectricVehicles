import streamlit as st
import numpy
import pandas


def show():
    df = pandas.read_excel('assets/India/Makers_India_Major_Electric.xlsx')
    with st.sidebar:
        st.write('Makers')
        # year_lis = numpy.arange(2022,2013,-1)
        # year = st.selectbox("Select a year",year_lis)
        maker = st.selectbox("Select a Maker",df['Maker'].unique())
    return maker
