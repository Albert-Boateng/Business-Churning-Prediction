import streamlit as st
import pandas as pd
from pages.Data import df
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title="History",
    layout='wide',
    page_icon='',
)


if st.session_state['LOGGED_IN']==False:
    switch_page("main")

def clearing():
    df.iloc[[],:].to_csv('./pages/history.csv', mode='w', index=False)


def history():
    st.title('Predictions History')
    
    
    # Load previous predictions dataframe
    previous_predictions = pd.read_csv('./pages/history.csv')

    # Display previous predictions
    st.dataframe(previous_predictions)
    
    st.button('Clear History', on_click=clearing)
    # Call the data function directly
if st.session_state['LOGGED_IN']==False:
    switch_page("main")

history()
