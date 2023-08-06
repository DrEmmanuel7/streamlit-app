import streamlit as st
from streamlit_lottie import st_lottie
import json5






st.set_page_config(
    "health insurance prediction",
    page_icon="✨",
    layout="wide",
    menu_items={
        'Get Help': 'https://github.com/DrEmmanuel7/streamlit-app',
        'Report a bug': "https://github.com/DrEmmanuel7/streamlit-app",
        'About': "Application pour faire des prediction basées sur sur le machine learning !"
    }
)

hide_footer = """
<style>
#MainMenu {visibility: hidden; }
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_footer, unsafe_allow_html=True)


def lottie(filepath:str):
    with open(filepath,"r") as f:
        return json5.load(f)
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
col2.title(" :sparkles: Home")


path = lottie("robo2hello.json")
with col2:
    st_lottie(
path,
speed=1,
reverse=False,
loop=True,
quality="low",

height=200,
width=200,
key=None
)
st.markdown("---")
st.markdown(""" 
            _Source du dataset:  [kaggle.com_](https://www.kaggle.com/datasets/anmolkumar/health-insurance-cross-sell-prediction?resource=download&select=train.csv)_
            
            _0bjectif: predire le  plus exactement possible les assurés qui seront favorables à l'assurance santé afin de minimiser le coût de la communication._
            
            _Ojectif statistique du projet: maximiser l'AUC(Area Under the Curve)._
    """)
st.subheader("Context")




context = """Notre client est une compagnie d'assurance qui offre des produits d'assurance automobile. Il veut désormais proposer un produit d'assurance santé à ses assurés automobiles. Mais la question est de savoir ceux qui seront favorables au produit. 
Etant donné que notre client a de nombreux assurés il est donc judicieux de détecter ceux qui seront favorable à l'offre afin d'éviter des coûts de communication inutiles.
Le but donc de cette application est de predire le plus exactement possible les assurés automobiles qui seront probablement favorable au produit d'assurance santé de notre client.

"""
st.markdown(context)
info = """ Dans le menu principale, cliquer sur Predictions afin d'utiliser le model pour des predictions sur de nouvelles données. Vous pouvez aussi cliquer sur Donnée et Metriques pour connaitre les perfomances du model à travers les differentes métriques importantes.  

"""
st.expander("info🫠").info(info)
 
