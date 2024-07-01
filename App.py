import streamlit as st
import pandas as pd
import openpyxl

# Load or create the Excel file
excel_file = "dictionary.xlsx"

# Try to load the Excel file, create one if it doesn't exist
try:
    df = pd.read_excel(excel_file, engine='openpyxl')
except FileNotFoundError:
    df = pd.DataFrame(columns=["word", "definition"])
    df.to_excel(excel_file, index=False, engine='openpyxl')

# CSS to inject contained in a string
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            body {
                background-color: #f0f2f6;
                font-family: 'Arial', sans-serif;
            }
            .css-1d391kg {padding-top: 2rem;}
            .stButton button {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                transition-duration: 0.4s;
                cursor: pointer;
                border-radius: 8px;
            }
            .stButton button:hover {
                background-color: #45a049;
            }
            .stTextInput>div>div>input {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 12px 20px;
                margin: 8px 0;
                box-sizing: border-box;
            }
            .stTextArea>div>div>textarea {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 12px 20px;
                margin: 8px 0;
                box-sizing: border-box;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("📚 Dictionary App")

# Sidebar to choose the operation
st.sidebar.title("Operations")
operation = st.sidebar.radio("Select an Operation:", ("Search", "Add", "Update", "Delete"))

if operation == "Search":
    st.header("🔍 Search a Word")
    all_words = df['word'].tolist()
    search_word = st.selectbox("Enter a word to search:", options=[""] + all_words)
    
    if st.button("Search"):
        result = df[df['word'].str.lower() == search_word.lower()]
        if not result.empty:
            for index, row in result.iterrows():
                st.write(f"**{row['word']}**: {row['definition']}")
        else:
            st.warning(f"No definition found for '{search_word}'.")

elif operation == "Add":
    st.header("➕ Add a Word")
    new_word = st.text_input("Enter a new word:")
    new_definition = st.text_area("Definition:")
    
    if st.button("Add Word"):
        new_entry = pd.DataFrame({"word": [new_word], "definition": [new_definition]})
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_excel(excel_file, index=False, engine='openpyxl')
        st.success(f"Added '{new_word}' to the dictionary.")

elif operation == "Update":
    st.header("🔄 Update a Word")
    all_words = df['word'].tolist()
    update_word = st.selectbox("Enter a word to update:", options=[""] + all_words)
    updated_definition = st.text_area("Updated Definition:")
    
    if st.button("Update Word"):
        index = df.index[df['word'].str.lower() == update_word.lower()]
        if not index.empty:
            df.loc[index, 'definition'] = updated_definition
            df.to_excel(excel_file, index=False, engine='openpyxl')
            st.success(f"Updated definition for '{update_word}'.")
        else:
            st.warning(f"Word '{update_word}' not found.")

elif operation == "Delete":
    st.header("❌ Delete a Word")
    all_words = df['word'].tolist()
    delete_word = st.selectbox("Enter a word to delete:", options=[""] + all_words)
    
    if st.button("Delete Word"):
        index = df.index[df['word'].str.lower() == delete_word.lower()]
        if not index.empty:
            df = df.drop(index)
            df.to_excel(excel_file, index=False, engine='openpyxl')
            st.success(f"Deleted '{delete_word}' from the dictionary.")
        else:
            st.warning(f"Word '{delete_word}' not found.")

with st.container():
    st.markdown("---")
    st.write("Created by [Aftab Hussain Shar](https://www.linkedin.com/in/aftab-hussain-912853245/) with :heart:")
    st.write("7-July-2024")
    st.markdown("---")