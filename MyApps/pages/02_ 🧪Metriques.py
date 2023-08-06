import streamlit as st 
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit.components.v1
from pycaret.classification import*
import numpy as np


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


data = data_load(r"C:\Users\HP\MachineLearning\Espace_Projet\HEALTH INSURANCE CROSS SELL PREDICTION\healthinsurancecrosssellpred_train.csv")
health_data = data.copy()
# the case selecting description de la dataset

def suppress_unknwn_var(health_data) :
    data = health_data.drop(["id", "Region_Code", "Policy_Sales_Channel"], axis=1)
    return data
health_data1 = suppress_unknwn_var(health_data)




if True:

    health_pred_preprocess = setup(data=health_data1,
                    target="Response",
                    train_size=0.8,
                    # types of variables
                    numeric_features=["Annual_Premium"],
                    categorical_features=['Gender', 'Vehicle_Age', 'Vehicle_Damage'],
                    ordinal_features=None,
                    date_features=None,
                    text_features=None,
                    ignore_features=None,
                    #Imputation. there are no nan
                    imputation_type=None,
                    # don't remove outlier because they presence is normal
                    remove_outliers=False,
                    # resolving imbalanced data
                    fix_imbalance=True,
                    fix_imbalance_method="SMOTE",
                    # Normalisation
                    normalize=True,
                    normalize_method="minmax",
                    # data transformation
                    transformation=False,
                    # to add polynomial feature into the pipeline
                    polynomial_features=False,
                    # group features that linked each other for a specifi analysis
                    group_features=None,
                    # bin numerical features
                    bin_numeric_features=None,
                    # not replacing rare modality
                    rare_to_value=None,
                    # feature selection
                    feature_selection=False,
                    # better to remove multicolinearity
                    remove_multicollinearity=True,
                    multicollinearity_threshold=0.8,
                    # dimenension reduction
                    pca=False,
                    # low variance variable
                    low_variance_threshold=None,
                    # mlflow tracking
                    log_experiment=False,
                    experiment_name="heathpred_ml",
                    log_data=False,
                    # number of fold for cross vamidation
                    fold=5,
                    # equivalent of random_state
                    session_id=0,
                    # EDA reporting
                    profile=True,
                    profile_kwargs={},
                    custom_pipeline=None,
                    use_gpu=False
)
    @st.cache_resource(show_spinner=True)
    def tree():
        tree_model = create_model('dt', max_depth = 8)
        return tree_model
    
    @st.cache_resource(show_spinner=True)
    def final(_tree_model):
        final_model = tune_model(_tree_model,optimize="auc", n_iter=15)
        return final_model

    tree = tree()

    final_model = final(tree)
    @st.cache_resource(show_spinner=True)
    def calibrate(_model):
        return calibrate_model(final_model, return_train_score=True, fold=5)
    
    calibrated_model = calibrate(final_model)

    @st.cache_data(show_spinner=True)
    def predict(_model):
        prediction = predict_model(_model)
        prediction_label = prediction["prediction_label"]
        prediction_score = prediction["prediction_score"]
        y_true = prediction["Response"]
        return y_true, prediction_label, prediction_score
    
    
    y_true, ypred, proba = predict(calibrated_model)




    col1, col2, col3 = st.columns((1,5,1))
    col2.title("🧪 Metriques du Model")
    st.expander("info").info(""" Cette partie concerne plus ceux qui ont des connaissances en data science ou ML.""") 
    tabs = st.tabs(["Confusion Matrix🌫️","Classification report🎀","AUC ROC🎖️","Calibration Curve📈","Learning Curve📇","error📊", "Precision Recall curve📉", "Threshold🗠", "Lift chart🗳️", "Gain chart❄️", "KS statistic❇️"])
    
    
    with tabs[0]:
            
            st.image("img metrics/Confusion Matrix.png")
    with tabs[1]:
            
            st.image("img metrics/Class Report.png")
    with tabs[2]:
            
            st.image("img metrics/AUC.png")
    with tabs[3]:
            
            st.image("img metrics/Calibration Curve.png")
    with tabs[4]:
            
            st.image("img metrics/Learning Curve.png")
    with tabs[5]:
            
            st.image("img metrics/Prediction Error.png")
    with tabs[6]:
           
            st.image("img metrics/Precision Recall.png")
    with tabs[7]:
            
            st.image("img metrics/Threshold.png")
    with tabs[8]:
            
            st.image("img metrics/Lift Chart.png")
    with tabs[9]:
            
            st.image("img metrics/Gain Chart.png")
    with tabs[10]:
           
            st.image("img metrics/KS Statistic Plot.png")






