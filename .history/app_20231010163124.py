import streamlit as st
import preprocessing

st.sidebar.title("Whatsapp Chat Analyzer")
f = open("_chat.txt", "r", encoding="utf-8")
df = preprocessing.preprocessing(f.read())
st.dataframe(df)
