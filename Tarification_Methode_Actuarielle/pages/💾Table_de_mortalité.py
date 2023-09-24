import pandas as pd 
import streamlit as st
from  mitosheet.streamlit.v1 import spreadsheet

st.set_page_config(
    "Table de mortalité",
     "💾",
    layout="wide"
)


hide_footer = """
<style>
#MainMenu {visibility: hidden; }
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_footer, unsafe_allow_html=True)

st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)
#ol1, col2, col3 = st.columns((1,9,1))
st.title(" :sparkles: Table de mortalité CIMA, Homme et Femme")

with st.expander("Info"):
              st.info(""" La table CIMA H est aussi appelé table décès car elle est utilisée pour tarifer les produits décès. Alors que la table CIMA F appelé table vie est utilisée pour tarifer les produits décès. """)

cimah = pd.read_excel("Table_mortalite_cima.xlsx", sheet_name="CIMA H", index_col="x")
cimah = pd.DataFrame(cimah)
cimaf = pd.read_excel("Table_mortalite_cima.xlsx", sheet_name="CIMA F", index_col="x")
cimaf = pd.DataFrame(cimaf)
sheet, code = spreadsheet(cimah, cimaf, df_names=["CIMA H", "CIMA F"])
st.write(sheet)
#st.dataframe(cima) 


