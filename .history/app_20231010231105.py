import streamlit as st
import preprocessing
import helper
import matplotlib.pyplot as plt

st.sidebar.title("Whatsapp Chat Analyzer")

uploadFile = st.sidebar.file_uploader(
    "Upload your own Chat history to see some insights"
)
df = None
if uploadFile is not None:
    byte_data = uploadFile.getvalue()
    data = byte_data.decode("utf-8")
    df = preprocessing.preprocessing(data)
else:
    f = open("_chat.txt", "r", encoding="utf-8")
    df = preprocessing.preprocessing(f.read())
userList = df["user"].unique().tolist()
userList.sort()
userList.insert(0, "Overall")
selected_user = st.sidebar.selectbox("Show Analysis for ", userList)
col1, col2, col3, col4 = st.columns(4)
num_msg, word_cnt, num_media, links = helper.fetch_stats(selected_user, df)
with col1:
    st.header("Total Messages")
    st.title(num_msg)
with col2:
    st.header("Total Words")
    st.title(word_cnt)
with col3:
    st.header("Media Shared")
    st.title(num_media)
with col4:
    st.header("Links shared")
    st.title(links)
if selected_user == "Overall":
    col1, col2 = st.columns(2)
    top_chatter, top_chatter_per = helper.get_top_chatter(df)
    fig, ax = plt.subplots()
    with col1:
        ax.bar(top_chatter.index, top_chatter.values, color="green")
        plt.xticks(rotation=45)
        plt.xlabel("User Name")
        plt.ylabel("Num of msgs")
        plt.title("Top Five Chatters")
        st.pyplot(fig)
    with col2:
        st.dataframe(top_chatter_per)
st.write("""# Word Cloud for {} """.format(selected_user))
df_wc = helper.wordCloud(selected_user, df)
fig, ax = plt.subplots()
ax.imshow(df_wc)
st.pyplot(fig)
st.write("""# Top 10 used Words by {}""".format(selected_user))
tmp = helper.get_top_words(df, selected_user)
fig, ax = plt.subplots()
ax.bar(tmp[0], tmp[1])
plt.xticks(rotation=90)
st.pyplot(fig)
