import streamlit as st
import preprocessing

st.write("Hello stream")
f = open("_chat.txt", "r", encoding="utf-8")
df = preprocessing.preprocessing(f.read())
st.dataframe(df)
