import streamlit as st
import preprocessing

st.sidebar.title("Whatsapp Chat Analyzer")

uploadFile = st.sidebar.file_uploader("Upload your own Chat history to see insights")

f = open("_chat.txt", "r", encoding="utf-8")
df = preprocessing.preprocessing(f.read())
st.dataframe(df)
userList = df["user"].unique().tolist()
userList.sort()
userList.insert(0, "Overall")
st.sidebar.selectbox("Show Analysis for ", userList)
