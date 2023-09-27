import pandas as pd
import streamlit as st
from mitosheet.streamlit.v1 import spreadsheet

st.set_page_config(
    "Données",
    "💾",
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

@st.cache_data
def data_load(link):
    data = pd.read_csv(link)
    health_data = data.copy()
    return health_data


data = data_load("MyApps/healthinsurancecrosssellpred_train.csv")
health_data = data.copy()
# the case selecting description de la dataset
@st.cache_data()
def suppress_unknwn_var(health_data) :
    data = health_data.drop(["id", "Region_Code", "Policy_Sales_Channel"], axis=1)
    return data
health_data1 = suppress_unknwn_var(health_data)

col1, col2, col3 = st.columns(3)
col2.title(" 💾Données")
new_dfs, code = spreadsheet(health_data1)
#st.write(new_dfs)
#st.code(code)
