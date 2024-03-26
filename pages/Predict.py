import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
import requests
from sklearn.base import BaseEstimator, TransformerMixin
import joblib
import imblearn
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler,MinMaxScaler,RobustScaler
from sklearn.preprocessing import FunctionTransformer,OneHotEncoder,LabelEncoder,OrdinalEncoder
from sklearn.base import TransformerMixin
from sklearn.feature_selection import SelectKBest, mutual_info_classif
from functools import partial
from sklearn.metrics import roc_curve, auc

from imblearn.over_sampling import RandomOverSampler, SMOTE
from imblearn.pipeline import Pipeline as impipeline


from sklearn.model_selection import GridSearchCV
import os
from pages.Data import df
from streamlit_extras.switch_page_button import switch_page



st.set_page_config(
    page_title="Predict",
    layout='wide',
    page_icon='',
)


if st.session_state['LOGGED_IN']==False:
    switch_page("main")


st.title('Predict Churn Status')


column1, column2 = st.columns([.6, .4])
with column1:
    model_option = st.selectbox('Choose which model to use for prediction', 
                                options=['Decision Tree Classifier','Logistic Classifier','K-nearest Classifier',
                                          'SVM Classifier','Naive Bayes Classifier', 'AdaBoost Classifier',
                                          'Random Forest Classifier'])

@st.cache_data
def take_input():
    customerID = st.session_state['customer_id']
    gender = st.session_state['gender']
    SeniorCitizen = st.session_state['senior_citizen']
    Partner = st.session_state['partners']
    Dependents = st.session_state['dependents']
    tenure = st.session_state['tenure']
    PhoneService = st.session_state['phone_service']
    MultipleLines = st.session_state['multiple_lines']
    InternetService = st.session_state['internet_service']
    OnlineSecurity = st.session_state['online_security']
    OnlineBackup = st.session_state['online_backup']
    DeviceProtection = st.session_state['device_protection']
    TechSupport = st.session_state['tech_support']
    StreamingTV = st.session_state['streaming_tv']
    StreamingMovies = st.session_state['streaming_movies']
    Contract = st.session_state['contract']
    PaperlessBilling = st.session_state['paperless_billing']
    PaymentMethod = st.session_state['payment_method']
    MonthlyCharges = st.session_state['monthly_charges']
    TotalCharges = st.session_state['total_charges']
    
    columns = ['customerID','gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure',
                'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup',
                'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies',
                'Contract', 'PaperlessBilling', 'PaymentMethod', 'MonthlyCharges', 'TotalCharges']
    
    values = [[customerID,gender, SeniorCitizen, Partner, Dependents, tenure, PhoneService,
            MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection,
            TechSupport, StreamingTV, StreamingMovies, Contract, PaperlessBilling,
            PaymentMethod, MonthlyCharges, TotalCharges]]
    
    data = pd.DataFrame(values, columns=columns)

    return data

df=df.iloc[:,1:]

df.fillna(method='ffill', inplace=True)

df.fillna(method='bfill', inplace=True)


X = df.drop(['Churn'], axis=1)  # Features
y = df['Churn']  # Target variable




# Convert boolean values to strings
y = y.astype(str)


X_num_cols = X.select_dtypes(include=np.number).columns

X_cat_cols = X.select_dtypes(include=['object']).columns

class LogTransformer:
    def __init__(self, constant=1):
        self.constant = constant

    def transform(self, X):
        return np.log1p(X + self.constant)


# Numerical transformer with LogTransformer
numerical_pipeline = Pipeline(steps=[
    ('num_imputer', SimpleImputer(strategy='median')),
    ('log_transform', FunctionTransformer(LogTransformer().transform)),
    ('scaler', StandardScaler())
])


class BooleanToStringTransformer(TransformerMixin):
    def fit(self, X, y=None):
        # Fit logic here, if needed
        return self

    def transform(self, X):
        # Transformation logic here
        # Ensure to return the transformed data
        return X.astype(str)


# Categorical transformer
categorical_pipeline = Pipeline(steps=[
    ('bool_to_str', BooleanToStringTransformer()),
    ('cat_imputer', SimpleImputer(strategy='most_frequent')),
    ('cat_encoder', OneHotEncoder())
])


# Combine transformers
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_pipeline, X_num_cols),
        ('cat', categorical_pipeline, X_cat_cols)
        ])

label_encoder = LabelEncoder()
y_train_encoded = label_encoder.fit_transform(y)


if 'prediction' not in st.session_state:
    st.session_state['prediction'] = None
if 'prediction_proba' not in st.session_state:
    st.session_state['prediction_proba'] = None
if 'data1' not in st.session_state:
    st.session_state['data1'] = None


def make_prediction():

    data1 = take_input()
    
    models = [
        ('Decision Tree Classifier', DecisionTreeClassifier(random_state=42)),
        ('Logistic Classifier', LogisticRegression(random_state=42)),
        ('K-nearest Classifier', KNeighborsClassifier()),
        ('SVM Classifier', SVC(random_state=42, probability=True)),
        ('Naive Bayes Classifier', GaussianNB()),
        ('Random Forest Classifier', RandomForestClassifier(random_state=42)),
        ('AdaBoost Classifier',AdaBoostClassifier(n_estimators=50, learning_rate=1))
        ]
    for model_name, classifier in models:
        if model_name==model_option:
            pipeline = Pipeline(steps=[
                ('preprocessor', preprocessor),
                ('classifier', classifier)
                ])
            pipeline.fit(X, y_train_encoded)


            data= data1.drop('customerID',axis=1)

            prediction = pipeline.predict(data)

            prediction = label_encoder.inverse_transform(prediction)

            prediction_proba = pipeline.predict_proba(data)

            st.session_state['prediction'] = prediction

            st.session_state['prediction_proba'] = prediction_proba

            data1['Model'] = model_name
            data1['Churn'] = prediction
            

            #st.write(f'### Your Inputs')
            #st.write(data1)  
    db= pd.read_csv('./pages/history.csv')
    dt=pd.concat([db.iloc[:,:-1],data1], axis=0, ignore_index=True)

    st.session_state['data1']=data1

    dt.to_csv('./pages/history.csv', mode='w', index=False)


    
    return prediction, prediction_proba, data1




def input_features():

    with st.form('features'):
        col1, col2 = st.columns(2)

        # ------ Collect customer information
        with col1:
            st.subheader('Demographics')
            st.text_input('Customer ID', value="", placeholder='eg. 1234-ABCDE', key='customer_id')
            st.radio('Gender', options=['Male', 'Female'],horizontal=True, key='gender',)
            st.radio('Partners', options=['Yes', 'No'],horizontal=True, key='partners')
            st.radio('Dependents', options=['Yes', 'No'],horizontal=True, key='dependents')
            st.radio("Senior Citizen ('Yes-1, No-0')", options=[1, 0],horizontal=True, key='senior_citizen')
        
        # ------ Collect customer account information
        with col1:
            st.subheader('Customer Account Info.')
            st.number_input('Tenure', min_value=0, max_value=70, key='tenure')
            st.selectbox('Contract', options=['Month-to-month', 'One year', 'Two year'], key='contract')
            st.selectbox('Payment Method',
                                        options=['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'],
                                        key='payment_method')
            st.radio('Paperless Billing', ['Yes', 'No'], horizontal=True, key='paperless_billing')
            st.number_input('Monthly Charges', placeholder='Enter amount...', key='monthly_charges')
            st.number_input('Total Charges', placeholder='Enter amount...', key='total_charges')
            
        # ------ Collect customer subscription information
        with col2:
            st.subheader('Subscriptions')
            st.radio('Phone Service', ['Yes', 'No'], horizontal=True, key='phone_service')
            st.selectbox('Multiple Lines', ['Yes', 'No', 'No internet servie'], key='multiple_lines')
            st.selectbox('Internet Service', ['DSL','Fiber optic', 'No'], key='internet_service')
            st.selectbox('Online Security', ['Yes', 'No', 'No internet servie'], key='online_security')
            st.selectbox('Online Backup', ['Yes', 'No', 'No internet servie'], key='online_backup')
            st.selectbox('Device Protection', ['Yes', 'No', 'No internet servie'], key='device_protection')
            st.selectbox('Tech Support', ['Yes', 'No', 'No internet servie'], key='tech_support')
            st.selectbox('Streaming TV', ['Yes', 'No', 'No internet servie'], key='streaming_tv')
            st.selectbox('Streaming Movies', ['Yes', 'No', 'No internet servie'], key='streaming_movies')
        
        st.form_submit_button('Predict', on_click=make_prediction)
    # return input_data

input_features()

prediction = st.session_state['prediction']
probability = st.session_state['prediction_proba'] 
dta1=st.session_state['data1']   

if st.session_state['prediction'] == None:
    col1, col2, col3 = st.columns([.225,.55,.225])
    with col2:
        st.markdown('#### Predictions will show here ⤵️')
    col1, col2, col3 = st.columns([.225,.55,.225])
    with col2:
        st.markdown('##### No predictions made yet. Make prediction')
else:
    if prediction == "True":
        st.write(f'### Your Inputs & Output')
        st.write(dta1)
        col1, col2, col3 = st.columns([.1,.8,.1])
        with col2:
            st.markdown(f'### The customer will churn with a {round(probability[0][1],2)}% probability.')
        col1, col2, col3 = st.columns([.3,.4,.3])
        with col2:
            st.success('Churn status predicted successfullly🎉')
    else:
        st.write(f'### Your Inputs & Output')
        st.write(dta1)
        col1, col2, col3 = st.columns([.1,.8,.1])
        with col2:
            st.markdown(f'### The customer will not churn with a {round(probability[0][0],2)}% probability.')
        col1, col2, col3 = st.columns([.3,.4,.3])
        with col2:
            st.success('Churn status predicted successfullly🎉')