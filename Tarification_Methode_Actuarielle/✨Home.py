import streamlit as st
import pandas as pd
import mitosheet

st.set_page_config(
    page_title="Tarification vie",
    page_icon=":sparkles:",
    layout="wide",

)



   

hide_footer = """
<style>
#MainMenu {visibility: hidden; }
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_footer, unsafe_allow_html=True)

st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
col2.title(" :sparkles: Home")


st.subheader("Objectif de l'application")

st.write("Cette application  peut être utilisée par les professionnels d'assurance, les étudiants en assurance, les actuaires, ainsi que par tout autre personne désireuse de découvrire des produits d'assurance. C'est une application de tarification des produits d'assurances de base ou courants. Le calcul des primes est basé sur des méthodes ou techniques acturielles. Pour ce faire, des connaissances en mathematiques financières, en probabilité sont essentielles dans la création de ces produits. Le calcul des produits vie est basé sur la table de mortalité CIMA F et celui des produits décès est basé sur la table CIMA H.")

st.subheader(" Ce qu'il y a dans l'application")

st.write("Dans le menu principal il y a en plus de la page Home, deux autres pages dont Produits et Table de mortalité. Dans le menu Produits sont présentés differents produits assuranciels de base tels que la rente viagère, le temporaire décès, le produit vie entière etc. Pour calculer la prime de chaque produit il suffira d'entrer les coordonnées du client et d'appuyer sur le bouton 'tarifer'. Pour voir la description de chaque produit il suffira de cliquer sur 'à propos du produit'. " )
st.write("Dans le menu Table de mortalité est présentée les differentes tables de mortalité en zone CIMA dont la table CIMA H(homme) et la table CIMA F(femme)")
