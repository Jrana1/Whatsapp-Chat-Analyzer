import streamlit as st
import preprocessing
import helper
import matplotlib.pyplot as plt

st.title("Whatsapp Chat Analyzer")

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
if selected_user == "Overall":
    st.dataframe(df.head())
else:
    st.dataframe(df[df["user"] == selected_user].head())
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
    st.write("""# Five most active users.""")
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
if not df_wc:
    st.write("Not word has been written by {}".selected_user)
else:
    fig, ax = plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)
st.write("""# Top 10 used Words by {}""".format(selected_user))
tmp = helper.get_top_words(df, selected_user, 15)
fig, ax = plt.subplots()
ax.bar(tmp[0], tmp[1], color="green")
plt.xticks(rotation=90)
st.pyplot(fig)

st.write("# Emoji used")
emoji_df = helper.get_emoji(selected_user, df)
col1, col2 = st.columns(2)
if emoji_df.empty:
    st.write("No emojis to show")
else:
    with col1:
        st.dataframe(emoji_df)
    with col2:
        fig, ax = plt.subplots()
        ax.pie(emoji_df["count"], labels=emoji_df["emoji"], autopct="%0.2f")
        st.pyplot(fig)
st.write("# Month-Year Timeline")
fig, ax = plt.subplots()
timeline = helper.get_timeline(selected_user, df)
ax.plot(timeline["month-year"], timeline["msg"])
plt.xticks(rotation=90)
plt.xlabel("Month-Year")
plt.ylabel("Number of Msg sent")
st.pyplot(fig)
st.write("# Daily timeline")
fig, ax = plt.subplots()
daily_timeline = helper.daily_timeline(selected_user, df)
ax.plot(daily_timeline["only-date"], daily_timeline["msg"])
plt.xticks(rotation=90)
plt.xlabel("Day")
plt.ylabel("Number of Msg sent")
st.pyplot(fig)
fig, ax = plt.subplots()
hour_dis = helper.hour_dis(selected_user, df)
plt.figure(figsize=(8, 6))
bin_labels = ["Vormittag", "Nachmittag", "Abend"]

st.title("Hour Distribution by Time of Day")
# st.dataframe(hour_dis)
ax.bar(
    bin_labels,
    hour_dis["time_of_day"].value_counts(),
    color="lightblue",
)
plt.xlabel("Time of Day")
plt.ylabel("Count of Msg sent")
plt.xticks(rotation=60)
st.pyplot(fig)
