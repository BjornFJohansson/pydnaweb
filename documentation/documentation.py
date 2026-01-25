import streamlit as st
from pathlib import Path

# Define the file path
file_path = Path('docs.md')

# Read the content of the file
text = file_path.read_text()

st.write(text)

