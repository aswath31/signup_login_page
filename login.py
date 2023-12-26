import streamlit as st
from signup import sign_up, fetch_users

def login():
    try:
        users = fetch_users()

        # Extracting usernames and passwords from the fetched users
        usernames = [user['username'] for user in users]
        passwords = [user['password'] for user in users]

        email, authentication_status, entered_username = st.session_state.login_authenticator.login(':green[Login]', 'main')

        info, _ = st.columns(2)

        if not authentication_status:
            sign_up()

        if entered_username:
            print("Usernames in database:", usernames)  # Add this line

            # Convert entered username to lowercase for case-insensitive comparison
            entered_username_lower = entered_username.lower()

            # Convert stored usernames to lowercase for case-insensitive comparison
            usernames_lower = [user.lower() for user in usernames]

            if entered_username_lower in usernames_lower:
                print("Username found:", entered_username)  # Add this line

                index = usernames_lower.index(entered_username_lower)
                stored_password = passwords[index]

                if authentication_status:
                    st.session_state.page = "home"
                else:
                    entered_password = st.session_state.login_authenticator.get_password()

                    print("Entered password:", entered_password)  # Add this line
                    print("Stored password:", stored_password)  # Add this line

                    if entered_password == stored_password:
                        st.session_state.page = "home"
                    else:
                        with info:
                            st.error('Incorrect password. Check your credentials.')
            else:
                with info:
                    st.warning(f'Username {entered_username} does not exist, please sign up!!')  # Add this line

    except Exception as e:
        st.exception(e)
        st.success('Refresh Page')

def on_logout_button_click():
    st.session_state.page = "login"

if __name__ == '__main__':
    st.set_page_config(page_title='TestApp', initial_sidebar_state='collapsed')
    login()
