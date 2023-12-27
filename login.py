import streamlit as st
from signup import sign_up, fetch_users
import hashlib

def hash_password(password):
    # Hash the password using SHA-256
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

def login():
    try:
        users = fetch_users()

        # Extracting usernames and hashed passwords from the fetched users
        usernames = [user['username'] for user in users]
        hashed_passwords = [user['password'] for user in users]

        with st.form(key='login_form'):
            # Get the entered username
            entered_username = st.text_input('Username')

            # Get the entered password
            entered_password = st.text_input('Password', type='password')

            # Submit button
            submit_button = st.form_submit_button('Login')

        info, _ = st.columns(2)

        if submit_button:
            print("Usernames in database:", usernames)  # Add this line

            # Convert entered username to lowercase for case-insensitive comparison
            entered_username_lower = entered_username.lower()

            # Convert stored usernames to lowercase for case-insensitive comparison
            usernames_lower = [user.lower() for user in usernames]

            if entered_username_lower in usernames_lower:
                print("Username found:", entered_username)  # Add this line

                index = usernames_lower.index(entered_username_lower)
                stored_hashed_password = hashed_passwords[index]

                # Hash the entered password for comparison
                entered_hashed_password = hash_password(entered_password)

                # Check if the entered hashed password matches the stored hashed password
                if entered_hashed_password == stored_hashed_password:
                    st.success('Login successful!')
                else:
                    with info:
                        st.error('Incorrect password. Check your credentials.')
            else:
                with info:
                    st.warning(f'Username {entered_username} does not exist. Please sign up.')  # Add this line

        # Display the signup form
        if st.button("Go to Signup"):
            st.experimental_set_query_params(page="signup")

    except Exception as e:
        st.exception(e)
        st.success('Refresh Page')

def on_logout_button_click():
    st.session_state.page = "login"
