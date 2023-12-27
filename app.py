import streamlit as st
import login
import signup

def welcome():
    st.title("Welcome to Your App")
    st.write("Please choose a page from the sidebar.")

def main():
    st.set_page_config(page_title='TestApp', initial_sidebar_state='collapsed')

    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", ["Login", "Signup"])

    if page == "Login":
        login.login()
    elif page == "Signup":
        signup.sign_up()
    else:  # Default to the Welcome page
        welcome()

if __name__ == '__main__':
    main()
