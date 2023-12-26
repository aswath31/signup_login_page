import streamlit as st
from login import login
from signup import sign_up
import streamlit_authenticator as sauth


def main():
    st.set_page_config(page_title='TestApp', initial_sidebar_state='collapsed')

    # Initialize the authenticator
    creds = {'usernames': {}}  # Replace with your credentials
    login_authenticator = sauth.Authenticate(creds, cookie_name='Streamlit', key='aaaaaa', cookie_expiry_days=3)

    # Add authenticator to session state
    st.session_state.login_authenticator = login_authenticator

    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", ["Login", "Signup"])

    if page == "Login":
        login()
    elif page == "Signup":
        sign_up()


if __name__ == '__main__':
    main()
