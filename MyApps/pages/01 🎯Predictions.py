import streamlit as st 
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

from pycaret.classification import*
import json5
from streamlit_lottie import st_lottie
#from Model_building_steps import data_load

st.set_page_config(
    page_title="Prédiction",
    page_icon="🎯",
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

data = pd.read_csv(r"C:\Users\HP\MachineLearning\Espace_Projet\HEALTH INSURANCE CROSS SELL PREDICTION\healthinsurancecrosssellpred_train.csv")
data = data.drop(["Region_Code","Policy_Sales_Channel","id"], axis=1)
data = data.drop("Response", axis=1)
data_columns = data.columns.to_list()

def lottie(filepath:str):
    with open(filepath,"r") as f:
        return json5.load(f)
path = lottie("./animation_lky5ete7.json")

num_vars = data.select_dtypes(np.number).columns.to_list()
cat_vars =data.select_dtypes("object").columns.to_list()

div = int(round(len(data_columns)/3, 0))

st.title(" :dart: Predictions avec le model")



variables1 = data_columns[0:div]
variables2 = data_columns[div: len(data_columns)-div]
#variables3 = data_columns[len(data_columns)-div: ]
vars_extra = ["Driving_License", "Previously_Insured"]


@st.cache_data()
def loading_model():
    return load_model(model_name="calibrated_tree_ insurance_model")

model = loading_model()
def predict(model,input_data):
    prediction = predict_model(model, input_data)
    prediction_label = prediction["prediction_label"]
    prediction_score = prediction["prediction_score"]
    return prediction_label, prediction_score

with st.form("form_prediction", clear_on_submit=False):
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        var = cat_vars[0]
        var1 = st.radio(var, 
                 options=data[var].unique().tolist(),
                   horizontal=True)
    
    with col2:
        var = cat_vars[1]
        var2 = st.radio(var, 
                 options=data[var].unique().tolist(),
                   horizontal=True)

    with col3:
        var = cat_vars[2]
        var3 = st.radio(var, 
                 options=data[var].unique().tolist(),
                   horizontal=True)

    with col4:
        var = vars_extra[0]
        var4 = st.radio(var,
                 options=["Yes", "No"],
                  horizontal=True)

    with col5:
      var = vars_extra[1]
      var5 = st.radio(var,
                 options=["Yes", "No"],
                  horizontal=True)  




    col1, col2 = st.columns(2)
    with col1:
        values_list = []
        variables_list = []
        for variable in num_vars:
           if variable not in vars_extra:
                
                variables_list.append(variable)
                variable_value = st.number_input(variable, min_value=0)
                values_list.append(variable_value)

    soumettre = st.form_submit_button("predire", type="primary")

    with col2:

        dict_vars = {cat_vars[0]:var1,
            cat_vars[1]: var2,
            cat_vars[2]: var3,
            vars_extra[0]: [1 if var4=="Yes" else 0][0] ,
            vars_extra[1]: [1 if var5 == "Yes" else 0][0],
            variables_list[0]: values_list[0],
            variables_list[1]: values_list[1],
            variables_list[2]: values_list[2]
            }

        explain_vars = pd.DataFrame([dict_vars]) 

        with st.empty():
            st.info("Entrer les données puis cliquer sur predire. Le resultat s'affichera juste ici.")
            if soumettre:
                st.info("patientez quelques instants...")
                label, score = predict(model, explain_vars)
                if label[0]==0:
                    st.warning(f'''
                       cet(te) assuré(e) ne sera pas favorable à l'offre 
                       de l'assurance santé. la certitude est à {round(score[0]*100,1)}%''')
                else:
                    st.success(f'''
                       cet(te) assuré(e) sera favorable à
                    l'offre de l'assurance santé. la certitude est à {round(score[0]*100,1)}%''')
        col21, col22, col23 = st.columns((2,5,1))
        with col22:
            st_lottie(
            path,
            speed=1,
            reverse=False,
            quality="medium",
            loop=True,
            width=250,
            height=250
        )




