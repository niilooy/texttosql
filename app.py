import streamlit as st
import sqlite3

import google.generativeai as genAi

## Configure api key
genAi.configure(api_key=st.secrets["api_key"])

#Function to load google gemini model and provide an sql query as response
def get_response(question, prompt):
    model = genAi.GenerativeModel("gemini-pro")
    response = model.generate_content([prompt[0], question])
    return response.text

#Function to retrieve google gemini model and provide an sql query as response
def read_sql_query(sql, db):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    connection.commit()
    connection.close()
    for row in result:
        print(row)
    return result

## Define your prompt
prompt = [
    st.secrets["prompt"]
]

## Streamlit app
st.set_page_config(page_title="SQL Data Retriever")
st.header("Retrieve SQL Data")
st.write("Check out the Chinook Database [here](https://www.sqlitetutorial.net/sqlite-sample-database/)")

question = st.text_input("Input: ",key="input")

submit = st.button("Find out!")

if submit:
    response = get_response(question,prompt)
    print(response)
    sql_query = response  # Save the SQL query
    response = read_sql_query(response,"chinook.db")
    if response:
        for row in response:
            # Convert the row to a string and remove parentheses and quotation marks
            row_str = str(row).translate(str.maketrans('', '', '()\'"'))
            # If the string ends with a comma, remove it
            if row_str.endswith(','):
                row_str = row_str[:-1]
            print(row_str)
            st.header(row_str)
        with st.expander("See query"):
            st.write(sql_query)  # Display the SQL query
    else:
        st.header("The query didn't return any result")
