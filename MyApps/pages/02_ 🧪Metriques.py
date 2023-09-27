import streamlit as st 
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit.components.v1
from pycaret.classification import*
import numpy as np
import joblib


st.set_page_config(
    "Metriques",
    "🧪",
    layout="wide"
)
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)


hide_footer = """
<style>
#MainMenu {visibility: hidden; }
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_footer, unsafe_allow_html=True)

# def dataset importation
@st.cache_data
def data_load(link):
    data = pd.read_csv(link)
    health_data = data.copy()
    return health_data


    col1, col2, col3 = st.columns((1,5,1))
    col2.title("🧪 Metriques du Model")
    st.expander("info").info(""" Cette partie concerne plus ceux qui ont des connaissances en data science ou ML.""") 
    tabs = st.tabs(["Confusion Matrix🌫️","Classification report🎀","AUC ROC🎖️","Calibration Curve📈","Learning Curve📇","error📊", "Precision Recall curve📉", "Threshold🗠", "Lift chart🗳️", "Gain chart❄️", "KS statistic❇️"])
    
    
    with tabs[0]:
            
            st.image("MyApps/img metrics/Confusion Matrix.png")
    with tabs[1]:
            
            st.image("MyApps/img metrics/Class Report.png")
    with tabs[2]:
            
            st.image("MyApps/img metrics/AUC.png")
    with tabs[3]:
            
            st.image("MyApps/img metrics/Calibration Curve.png")
    with tabs[4]:
            
            st.image("MyApps/img metrics/Learning Curve.png")
    with tabs[5]:
            
            st.image("MyApps/img metrics/Prediction Error.png")
    with tabs[6]:
           
            st.image("MyApps/img metrics/Precision Recall.png")
    with tabs[7]:
            
            st.image("MyApps/img metrics/Threshold.png")
    with tabs[8]:
            
            st.image("MyApps/img metrics/Lift Chart.png")
    with tabs[9]:
            
            st.image("MyApps/img metrics/Gain Chart.png")
    with tabs[10]:
           
            st.image("MyApps/img metrics/KS Statistic Plot.png")






