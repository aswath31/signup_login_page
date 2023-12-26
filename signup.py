import streamlit as st
import streamlit_authenticator as stauth
import mysql.connector
from mysql.connector import Error
import datetime
import re


def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            database='user_creds',
            user='root',
            password='*****'
        )
        if connection.is_connected():
            print(f"Connected to MySQL Server version {connection.get_server_info()}")
            return connection
        else:
            print("Connection failed.")

    except Error as e:
        print(f"Error: {e}")

    return connection



def insert_user(email, username, password):
    connection = create_connection()
    signup_date = str(datetime.datetime.now())

    try:
        if connection is not None and connection.is_connected():
            cursor = connection.cursor()
            query = "INSERT INTO users (mail, username, password, date_of_signup) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (email, username, password, signup_date))
            connection.commit()
            print("Record inserted successfully")
        else:
            print("Failed to insert record: Database connection not established.")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()



def fetch_users():
    connection = create_connection()
    users = []

    try:
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    return users


def get_user_emails():
    users = fetch_users()
    emails = []
    for user in users:
        emails.append(user['mail'])
    return emails


def get_username():
    username = []
    users = fetch_users()
    for user in users:
        if 'username' in user:
            username.append(user['username'])
    return username


def validate_email(email):
    pattern_to_verify_email = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"

    if re.match(pattern_to_verify_email, email):
        return True
    else:
        return False


def validate_username(username):
    pattern_to_verify_name = "^[a-zA-Z0-9]*$"

    if re.match(pattern_to_verify_name, username):
        return True
    else:
        return False


def sign_up():
    with st.form(key='signup', clear_on_submit=True):
        st.subheader(':green[User Registration]')
        email = st.text_input('Email', placeholder='Enter your Email')
        username = st.text_input('User Name', placeholder='Enter your Name')
        password = st.text_input('Password', placeholder='Enter your Password', type='password')
        confirm_password = st.text_input('Confirm Password', placeholder='Confirm your password', type='password')

        if email:
            if validate_email(email):
                if email not in get_user_emails():
                    if validate_username(username):
                        if username not in get_username():
                            if len(username) >= 2:
                                if len(password) >= 8:
                                    if password == confirm_password:
                                        hashed_pass = stauth.Hasher([confirm_password]).generate()[0]
                                        insert_user(email, username, hashed_pass)
                                        st.success('Account Created!!!')
                                    else:
                                        st.warning('Password not matching')
                                else:
                                    st.warning('Password is too short')
                            else:
                                st.warning('Username is too short')
                        else:
                            st.warning('Username Already Exists')
                    else:
                        st.warning('Invalid Username')
                else:
                    st.warning('Email Already Exists')
            else:
                st.warning('Invalid Email')

        sb1, sb2, sb3, sb4, sb5 = st.columns(5)
        with sb3:
            st.form_submit_button('Submit')


if __name__ == '__main__':
    sign_up()
