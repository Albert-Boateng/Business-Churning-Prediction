import streamlit as st
from login_auth.widgets import build_login_ui
from PIL import Image
from streamlit_extras.switch_page_button import switch_page


LOGGED_IN= build_login_ui()

    
if st.session_state['LOGGED_IN']:
    
    def home():
       st.title('Customer Churn Prediction - See Tomorrow Today, Drive Business Forward!')
    
       st.write('This data-driven App Offers predictive insights to help businesses retain customers effectively, ensuring sustained growth and profitability.')

    st.title("ChurnPulse App", anchor="main") 
    st.subheader("Stay ahead of customer churn with real-time predictive analytics.")
    
    img = Image.open("logo.jpg")
    st.image(img, width=None, use_column_width=True)
    if __name__ == '__main__':
         home()
    st.write('Links:')
    st.markdown('[GitHub](https://github.com/dashboard)')
    st.markdown('[LinkedIn](www.linkedin.com/in/isaac-fumey-27b75774)')
                                      