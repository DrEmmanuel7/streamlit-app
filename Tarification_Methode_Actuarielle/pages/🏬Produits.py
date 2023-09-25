import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime


st.set_page_config(
    "Produits",
    "🏬",
    layout="wide"
)


hide_footer = """
<style>
#MainMenu {visibility: hidden; }
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_footer, unsafe_allow_html=True)

@st.cache_data()
def cima_df():
    cimah = pd.read_excel("Tarification_Methode_Actuarielle/Table_mortalite_cima.xlsx", sheet_name="CIMA H")
    cimah = pd.DataFrame(cimah)
    cimaf = pd.read_excel("Tarification_Methode_Actuarielle/Table_mortalite_cima.xlsx", sheet_name="CIMA F")
    cimaf = pd.DataFrame(cimaf)
    return cimah, cimaf

cimah, cimaf = cima_df()

with st.sidebar:
    products = st.radio("selectionner le produit souhaité",
                        options=["Rente viagère", "Capital différé", "Temporaire décès","Vie entière","produit mixte"])
########################---------------Capitale différé--------------------###########################
if products =="Capital différé":
        
        st.markdown(hide_footer, unsafe_allow_html=True)


        st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)
        col1, col2, col3 = st.columns((1,3,1))
        col2.title("Tarification -Capital différé")


        with st.expander("A propos du produit"):
              st.info("""

Le capital différé est un produit proposé par les compagnies d’assurance vie. Son principe de fonctionnement est le suivant : le souscripteur paie une prime à l'assureur vie et le bénéficiaire perçoit en contrepartie un capital déterminé lors de la conclusion du contrat à condition que l'assuré survive.""")

        col1, col2, col3 = st.columns((1,2,1))
        with col2:
              col1, col2   = st.columns(2)
              birth = col1.date_input("Choisir la date de naissance", min_value=pd.to_datetime("1960/08/07"))
              birth_dict = {"birth":[pd.to_datetime(birth)]}
              df_birth = pd.DataFrame(birth_dict)
              aujourd = datetime.now()
              age = int((aujourd - df_birth["birth"]).astype('<m8[Y]'))
              ageput = col2.number_input("Age(l'age apparait automatique)", min_value=age, max_value=age, value=age)
        

      
        col1, col2, col3 = st.columns((2,1,1.5))
        col2.subheader("Prime Unique")
        with st.form(key="capital différé unique", clear_on_submit=True):
              col1, col2, col3 = st.columns(3)
              
              annee_differe = col1.number_input("Nombre d'années différé", min_value=1, value=1)
              
              ## calcul de la prime
              df_age = cimaf[cimaf["x"]==age]
              df_age_differe = cimaf[cimaf["x"]==age+annee_differe]
              ppure_differee  = float(df_age_differe["Dx"])/float(df_age["Dx"])
              
        
              ### Chargement
              gestion = col2.text_input("frais de gestion", value=f"{2}%")
              acquisition = col3.text_input("frais d'acquisition", value=f"{7}%")
              capital_differe = col1.number_input("Capital espéré", min_value=1, value=1)

             # prime pure
              ppure_differee = round(ppure_differee*capital_differe,3)
              ppure_differee = col2.number_input("Prime pure",min_value=ppure_differee, value=ppure_differee, max_value=ppure_differee)
            # prime inventaire
              pinventaire = round(float(ppure_differee) + (int(gestion[0])/100)*capital_differe,3)
              pinventaire = col3.number_input("Prime d'inventaire",min_value=pinventaire,max_value=pinventaire, value=pinventaire)
            # Prime commerciale
              pcommercial = round((ppure_differee-(int(gestion[0])/100)*capital_differe)/(1-(int(acquisition[0])/100)),3)
              pcommercial = col1.number_input("Prime commerciale",min_value=pcommercial,max_value=pcommercial, value=pcommercial)

              st.form_submit_button("tarifer", type="primary")
    # Prime annuelle
        col1, col2, col3 = st.columns((2,1,1.5))
        col2.subheader("Prime Annuelle")
        with st.form(key="capital différé annuel", clear_on_submit=True):
             col1, col2 = st.columns(2)
             annee = col1.number_input("nombre d'année", min_value=1, value=1)
             Nx = float(df_age["Nx"])
             Nxplusn = float(cimaf[cimaf["x"]==age+annee]["Nx"])
             Dx = float(df_age["Dx"])
             tauxannuel = (Nx-Nxplusn)/Dx
             pannuelle = pcommercial/tauxannuel
             pannuelle = col2.number_input("Prime annuelle", value=pannuelle, min_value=pannuelle, max_value=pannuelle)
             
             st.form_submit_button(label="tarifer", type="primary")


########################---------------Rente viagère--------------------###########################
if products =="Rente viagère":
        st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)
        col1, col2, col3 = st.columns((1,3,1))
        col2.title("Tarification - Rente viagère")
   
        with st.expander("A propos du produit"):
              st.info("""

La rente viagère est un produit exclusivement proposé par les compagnies d’assurance vie. Son principe de fonctionnement est le suivant : le souscripteur paie une prime à l'assureur vie et le bénéficiaire perçoit en contrepartie une rente périodique, généralement mensuelle, jusqu’à son décès, quel que soit l’âge auquel il se produit. Ce produit constitue une solution idéale pour les personnes ayant besoin d’un complément de retraite.""")

        col1, col2, col3, col4 = st.columns(4)
        birth = col1.date_input("Choisir la date de naissance", min_value=pd.to_datetime("1960/08/07"))
        birth_dict = {"birth":[pd.to_datetime(birth)]}
        df_birth = pd.DataFrame(birth_dict)
        aujourd = datetime.now()
        age = int((aujourd - df_birth["birth"]).astype('<m8[Y]'))
        ageput = col2.number_input("Age(l'age apparait automatique)", min_value=age, max_value=age, value=age)
        sex = col3.radio("Sex", options=["Homme", "Femme"], horizontal=True)
        type_rente = col4.checkbox("Anticipé ?", help="la prime de la rente viagère est-elle anticipée c'est-à-dire payable au début de l'année? si la case n'est pas coché alors elle est à termes échus ou payable à la fin de l'année")
       
        # Anticipé ou pas
        if type_rente:
              df_age = cimaf[cimaf["x"]==age]
              ppure  = float(df_age["Nx"])/float(df_age["Dx"])
        else:
            df_age = cimaf[cimaf["x"]==age]
            df_ageechu = cimaf[cimaf["x"]==age+1]
            ppure  = float(df_ageechu["Nx"])/float(df_age["Dx"])
            
        
        col1, col2, col3 = st.columns((2,1,1.5))
        col2.subheader("Prime Unique")
        with st.form(key="rente viagère unique", clear_on_submit=True):
              col1, col2, col3 = st.columns(3)
              ### Chargement
              gestion = col1.text_input("frais de gestion", value=f"{2}%")
              acquisition = col2.text_input("frais d'acquisition", value=f"{7}%")
              rente = col3.number_input("Rente espérée", min_value=1, value=1)
             # prime pure
              ppure = round(ppure*rente,3)
              ppure = col1.number_input("Prime pure",min_value=ppure, value=ppure, max_value=ppure)
            # prime inventaire
              pinventaire = round(float(ppure) + (int(gestion[0])/100)*rente,3)
              pinventaire = col2.number_input("Prime d'inventaire",min_value=pinventaire,max_value=pinventaire, value=pinventaire)
            # Prime commerciale
              pcommercial = round((ppure-(int(gestion[0])/100)*rente)/(1-(int(acquisition[0])/100)),3)
              pcommercial = col3.number_input("Prime commerciale",min_value=pcommercial,max_value=pcommercial, value=pcommercial)

              st.form_submit_button("tarifer", type="primary")
    # Prime annuelle
        col1, col2, col3 = st.columns((2,1,1.5))
        col2.subheader("Prime Annuelle")
        with st.form(key="rente viagère annuelle", clear_on_submit=True):
             col1, col2 = st.columns(2)
             annee = col1.number_input("nombre d'année", min_value=1, value=1)
             Nx = float(df_age["Nx"])
             Nxplusn = float(cimaf[cimaf["x"]==age+annee]["Nx"])
             Dx = float(df_age["Dx"])
             tauxannuel = (Nx-Nxplusn)/Dx
             pannuelle = pcommercial/tauxannuel
             pannuelle = col2.number_input("Prime annuelle", value=pannuelle, min_value=pannuelle, max_value=pannuelle)
             
             st.form_submit_button(label="tarifer", type="primary")


########################---------------Vie entière--------------------###########################
if products =="Vie entière":
        st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)
        col1, col2, col3 = st.columns((1,2,1))
        col2.title("Tarification - Vie entière")
        col1, col2, col3 = st.columns((1,2,1))

        with st.expander("A propos du produit"):
              st.info(""" L' assurance-vie entière est une assurance décès couvrant le risque de décès quelle que soit la date de disparition du souscripteur, car la garantie est viagère. En cas de décès de l'assuré, l'assureur s'engage à verser au (x) bénéficiaire (s) désigné (s) un capital proportionnel au montant des primes versées par le titulaire du contrat. """)


        with col2:
              col1, col2   = st.columns(2)
              birth = col1.date_input("Choisir la date de naissance", min_value=pd.to_datetime("1960/08/07"))
              birth_dict = {"birth":[pd.to_datetime(birth)]}
              df_birth = pd.DataFrame(birth_dict)
              aujourd = datetime.now()
              age = int((aujourd - df_birth["birth"]).astype('<m8[Y]'))
              ageput = col2.number_input("Age(l'age apparait automatique)", min_value=age, max_value=age, value=age)
        

        col1, col2, col3 = st.columns((2,1,1.5))
        col2.subheader("Prime Unique")
        with st.form(key="vie entière unique", clear_on_submit=True):
              col1, col2, col3 = st.columns(3)
              annee_effet_differe = col1.number_input("Nombre d'années différé", min_value=0, value=0)
              
              ## calcul de la prime
              df_age = cimah[cimah["x"]==age]
              df_age_vie_entiere_effet_differe = cimah[cimah["x"]==age+annee_effet_differe]
              ppure_vie_entiere  = float(df_age_vie_entiere_effet_differe["Mx"])/float(df_age["Dx"])
              
        
              ### Chargement
              gestion = col2.text_input("frais de gestion", value=f"{2}%")
              acquisition = col3.text_input("frais d'acquisition", value=f"{7}%")
              capital_vie_entiere = col1.number_input("Capital espéré", min_value=1, value=1)

             # prime pure
              ppure_vie_entiere = round(ppure_vie_entiere*capital_vie_entiere,3)
              ppure_vie_entiere = col2.number_input("Prime pure",min_value=ppure_vie_entiere, value=ppure_vie_entiere, max_value=ppure_vie_entiere)
            # prime inventaire
              pinventaire = round(float(ppure_vie_entiere) + (int(gestion[0])/100)*capital_vie_entiere,3)
              pinventaire = col1.number_input("Prime d'inventaire",min_value=pinventaire,max_value=pinventaire, value=pinventaire)
            # Prime commerciale
              pcommercial = round((ppure_vie_entiere-(int(gestion[0])/100)*capital_vie_entiere)/(1-(int(acquisition[0])/100)),3)
              pcommercial = col2.number_input("Prime commerciale",min_value=pcommercial,max_value=pcommercial, value=pcommercial)

              st.form_submit_button("tarifer", type="primary")
    # Prime annuelle
        col1, col2, col3 = st.columns((2,1,1.5))
        col2.subheader("Prime Annuelle")
        with st.form(key="vie entière annuelle", clear_on_submit=True):
             col1, col2 = st.columns(2)
             annee = col1.number_input("nombre d'année", min_value=1, value=1)
             Nx = float(df_age["Nx"])
             Nxplusn = float(cimah[cimah["x"]==age+annee]["Nx"])
             Dx = float(df_age["Dx"])
             tauxannuel = (Nx-Nxplusn)/Dx
             pannuelle = pcommercial/tauxannuel
             pannuelle = col2.number_input("Prime annuelle", value=pannuelle, min_value=pannuelle, max_value=pannuelle)
             
             st.form_submit_button(label="tarifer", type="primary")


########################---------------Temporaire décès--------------------###########################
if products =="Temporaire décès":
        st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)
        col1, col2, col3 = st.columns((1,3,1))
        col2.title("Tarification - Temporaire décès")
        col1, col2, col3 = st.columns((1,2,1))

        with st.expander("A propos du produit"):
              st.info("""

 il s'agit d'une assurance prévoyance dont le but est de garantir un capital ou une rente aux bénéficiaires du contrat désignés par le souscripteur, dans l’éventualité de son décès durant la période d'effet du contrat. Le contrat n’est valable que pour une période déterminée.""")

        with col2:
              col1, col2   = st.columns(2)
              birth = col1.date_input("Choisir la date de naissance", min_value=pd.to_datetime("1960/08/07"))
              birth_dict = {"birth":[pd.to_datetime(birth)]}
              df_birth = pd.DataFrame(birth_dict)
              aujourd = datetime.now()
              age = int((aujourd - df_birth["birth"]).astype('<m8[Y]'))
              ageput = col2.number_input("Age(l'age apparait automatique)", min_value=age, max_value=age, value=age)
        

      
        col1, col2, col3 = st.columns((2,1,1.5))
        col2.subheader("Prime Unique")
        with st.form(key="temporaire décès unique", clear_on_submit=True):
              col1, col2, col3 = st.columns(3)
              
              
              annee_temporaire = col1.number_input("temporaire décès pour combien d'années", min_value=1, value=1)
              annee_temp_differee = col2.number_input("différé de combien d'années", min_value=0, value=0)

              ## calcul de la prime 
              df_age = cimah[cimah["x"]==age]
              df_age_temp_differe = cimah[cimah["x"]==age+annee_temp_differee]
              df_age_temp_annee_differe = cimah[cimah["x"]==age+annee_temporaire+annee_temp_differee]
              ppure_temporaire_deces  = (float(df_age_temp_differe["Mx"]) - float(df_age_temp_annee_differe["Mx"]))/float(df_age["Dx"])
              
        
              ### Chargement
              gestion = col3.text_input("frais de gestion", value=f"{2}%")
              acquisition = col1.text_input("frais d'acquisition", value=f"{7}%")
              capital_temporaire_deces = col2.number_input("Capital espéré", min_value=1, value=1)

             # prime pure
              ppure_temporaire_deces = round(ppure_temporaire_deces*capital_temporaire_deces,3)
              ppure_temporaire_deces = col3.number_input("Prime pure",min_value=ppure_temporaire_deces, value=ppure_temporaire_deces, max_value=ppure_temporaire_deces)
            # prime inventaire
              pinventaire = round(float(ppure_temporaire_deces) + (int(gestion[0])/100)*capital_temporaire_deces,3)
              pinventaire = col1.number_input("Prime d'inventaire",min_value=pinventaire,max_value=pinventaire, value=pinventaire)
            # Prime commerciale
              pcommercial = round((ppure_temporaire_deces-(int(gestion[0])/100)*capital_temporaire_deces)/(1-(int(acquisition[0])/100)),3)
              pcommercial = col2.number_input("Prime commerciale",min_value=pcommercial,max_value=pcommercial, value=pcommercial)

              st.form_submit_button("tarifer", type="primary")
    # Prime annuelle
        col1, col2, col3 = st.columns((2,1,1.5))
        col2.subheader("Prime Annuelle")
        with st.form(key="temporaire decès annuel", clear_on_submit=True):
             col1, col2 = st.columns(2)
             annee = col1.number_input("nombre d'année", min_value=1, value=1)
             Nx = float(df_age["Nx"])
             Nxplusn = float(cimah[cimah["x"]==age+annee]["Nx"])
             Dx = float(df_age["Dx"])
             tauxannuel = (Nx-Nxplusn)/Dx
             pannuelle = pcommercial/tauxannuel
             pannuelle = col2.number_input("Prime annuelle", value=pannuelle, min_value=pannuelle, max_value=pannuelle)
             
             st.form_submit_button(label="tarifer", type="primary")



########################---------------Produit mixte--------------------###########################
if products =="produit mixte":
        
        st.markdown(hide_footer, unsafe_allow_html=True)


        st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)
        #col1, col2, col3 = st.columns((1,15,1))
        st.title("Tarification -produit mixte(capital différé-temporaire décès)")

        with st.expander("A propos du produit"):
              st.info(""" le versement d’un capital est fait au(x) bénéficaire(s) si à une date déterminée:

* l’assuré est toujours vivant,
* ou au décès de l’assuré si celui-ci survient avant cette date.""")

        col1, col2, col3 = st.columns((1,3,1))
        with col2:
              col1, col2   = st.columns(2)
              birth = col1.date_input("Choisir la date de naissance", min_value=pd.to_datetime("1960/08/07"))
              birth_dict = {"birth":[pd.to_datetime(birth)]}
              df_birth = pd.DataFrame(birth_dict)
              aujourd = datetime.now()
              age = int((aujourd - df_birth["birth"]).astype('<m8[Y]'))
              ageput = col2.number_input("Age(l'age apparait automatique)", min_value=age, max_value=age, value=age)
        

      
        col1, col2, col3 = st.columns((2,1,1.5))
        col2.subheader("Prime Unique")
        with st.form(key="produit mixte unique", clear_on_submit=True):
              col1, col2, col3 = st.columns(3)
              
              annee_differe = col1.number_input("Nombre d'années différé", min_value=1, value=1)
              annee_temporaire = col2.number_input("temporaire décès pour combien d'années", min_value=1, value=1)
              ## calcul de la prime capital différé
              df_age1 = cimaf[cimaf["x"]==age]
              df_age_differe = cimaf[cimaf["x"]==age+annee_differe]
              ppure_differee  = float(df_age_differe["Dx"])/float(df_age1["Dx"])
              
              ## calcul de la prime temporaire décès
              df_age2 = cimah[cimah["x"]==age]
              df_age_annee_temporaire = cimah[cimah["x"]==age+annee_temporaire]
              ppure_temporaire_deces  = (float(df_age2["Mx"]) - float(df_age_annee_temporaire["Mx"]))/float(df_age2["Dx"])
              
        
              ## prime pure mixte

              ppure_mixte = ppure_differee+ppure_temporaire_deces
              ### Chargement
              gestion = col3.text_input("frais de gestion", value=f"{2}%")
              acquisition = col1.text_input("frais d'acquisition", value=f"{7}%")
              capital_mixte = col2.number_input("Capital espéré", min_value=1, value=1)

             # prime pure
              ppure_mixte = round(ppure_mixte*capital_mixte,3)
              ppure_mixte = col3.number_input("Prime pure",min_value=ppure_mixte, value=ppure_mixte, max_value=ppure_mixte)
            # prime inventaire
              pinventaire = round(float(ppure_mixte) + (int(gestion[0])/100)*capital_mixte,3)
              pinventaire = col1.number_input("Prime d'inventaire",min_value=pinventaire,max_value=pinventaire, value=pinventaire)
            # Prime commerciale
              pcommercial = round((ppure_mixte-(int(gestion[0])/100)*capital_mixte)/(1-(int(acquisition[0])/100)),3)
              pcommercial = col2.number_input("Prime commerciale",min_value=pcommercial,max_value=pcommercial, value=pcommercial)

              st.form_submit_button("tarifer", type="primary")
    # Prime annuelle
        col1, col2, col3 = st.columns((2,1,1.5))
        col2.subheader("Prime Annuelle")
        with st.form(key="produit mixte annuel", clear_on_submit=True):
             col1, col2 = st.columns(2)
             annee = col1.number_input("nombre d'année", min_value=1, value=1)
             Nx1 = float(df_age1["Nx"])
             Nx2 = float(df_age2["Nx"])
             Nxplusn1 = float(cimaf[cimaf["x"]==age+annee]["Nx"])
             Nxplusn2 = float(cimah[cimaf["x"]==age+annee]["Nx"])

             Dx1 = float(df_age1["Dx"])
             Dx2 = float(df_age2["Dx"])
            #taux capital différé
             tauxannuel1 = (Nx1-Nxplusn1)/Dx1
             #taux temporaire décès
             tauxannuel2 = (Nx2-Nxplusn2)/Dx2
             
             # prime annuelle
             pannuelle = pcommercial/(tauxannuel2)
             pannuelle = col2.number_input("Prime annuelle", value=pannuelle, min_value=pannuelle, max_value=pannuelle)
             
             st.form_submit_button(label="tarifer", type="primary")

