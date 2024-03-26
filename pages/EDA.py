import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")
import pyodbc
from pages.Data import df
from streamlit_extras.switch_page_button import switch_page


st.set_page_config(
    page_title="Dashboard",
    layout='wide',
    page_icon='',
)



# Distribution of numerical values
df.fillna(method='bfill', inplace=True)
df.fillna(method='ffill', inplace=True)

if st.session_state['LOGGED_IN']==False:
    switch_page("main")

st.write(f'# EDA')
st.write(f'### Multivariate Analysis')
data = df[["tenure","MonthlyCharges",'TotalCharges','Churn']]
plt.figure(figsize=(10, 8))
fig=sns.pairplot(data, palette={True:'Firebrick', False:'blue'}, hue = 'Churn')
st.pyplot(fig)

st.write('### Which variable type do you want to visualize (Numerical or Categorical)')

vtp=st.selectbox('Select Variable Type', ['Select Variable Type','Numerical','Categorical'])

n=['Select Variable']
c=['Select Variable']
for i in df.columns:
    if i!="customerID":
        if df[i].dtype=='O' or df[i].dtype=='bool':
            c+=[i]
        else:
            n+=[i]
if vtp=='Numerical':
    vt1=st.selectbox('Variable Name', n)
    if vt1!='Select Variable':
        feature=vt1
        st.write(f'### {feature.capitalize()}')
        fig=plt.figure(figsize=(8, 6))
        sns.histplot(df[feature], kde=True)
        plt.title(f'Distribution of {feature.capitalize()}')
        plt.xlabel(feature.capitalize())
        plt.ylabel('Frequency')
        st.pyplot(fig)

elif vtp=='Categorical':
    vt2=st.selectbox('Variable Name',  c)
    if vt2!='Select Variable':
        feature=vt2
        df[feature].fillna("Unknown", inplace=True)
        fig=plt.figure(figsize=(8, 6))
        sns.countplot(x=feature, data=df.iloc[:,1:], hue='Churn', palette='viridis')
        plt.title(f'Count plot of {feature.capitalize()}')
        plt.xlabel(feature.capitalize())
        plt.ylabel('Count')
        st.pyplot(fig)


#st.subheader('Distribution of numerical features')
