import streamlit as st

default = "default"

# Initialize session state for text area
if "text_area_content" not in st.session_state:
    st.session_state.text_area_content = ""

with st.form("myform"):
    placeholder_for_radio = st.empty()
    placeholder_for_textarea = st.empty()
    submit_button = st.form_submit_button("Submit!")

# Create radio and selectbox outside the form
with placeholder_for_radio:
    defaultbutton = 0
    if st.session_state.text_area_content:
        defaultbutton = 2
    radio_option = st.radio("radio",
                            ["Plants", "Animals", "Custom"],
                            index = defaultbutton,
                            horizontal=True)

with placeholder_for_textarea:
    st.text_area("Enter a sequence to analyze:",
                 st.session_state.text_area_content,
                 height=150,
                 key="text_area_content",
                 placeholder=default)
