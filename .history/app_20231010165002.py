import streamlit as st
import preprocessing

st.sidebar.title("Whatsapp Chat Analyzer")
f = open("_chat.txt", "r", encoding="utf-8")
df = preprocessing.preprocessing(f.read())
st.dataframe(df)
userList = df["user"].unique().tolist()
st.sidebar.selectbox("Show Analysis for ", userList)
