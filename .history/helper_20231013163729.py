from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji


def fetch_stats(user, df):
    if user != "Overall":
        df = df[df["user"] == user]
    # get total words
    cnt = 0
    for ms in df["msg"]:
        cnt += len(ms.split())
    # get total media shared
    num_media = df[df["msg"].str.contains("weggelassen")].shape[0]
    # get total links shared
    urls = []
    urlExtracter = URLExtract()
    for ms in df["msg"]:
        urls += urlExtracter.find_urls(ms)
    links = len(urls)
    return df.shape[0], cnt, num_media, links


def get_top_chatter(df):
    top_chatter = df["user"].value_counts().sort_values(ascending=False).nlargest(5)
    top_chatter_per = (
        round(df["user"].value_counts() / df.shape[0] * 100, 2)
        .reset_index()
        .rename(columns={"user": "Name", "count": "Percent(%)"})
    )

    return top_chatter, top_chatter_per


def wordCloud(user, df):
    if user != "Overall":
        df = df[df["user"] == user]

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color="white")
    df_wc = wc.generate(df["msg"].str.cat(sep=" "))
    return df_wc


def get_top_words(df, user, cnt):
    if user != "Overall":
        df = df[df["user"] == user]
    german_stopwords = [
        "aber",
        "als",
        "an",
        "auch",
        "auf",
        "aus",
        "bei",
        "bin",
        "bis",
        "da",
        "dann",
        "der",
        "des",
        "die",
        "doch",
        "du",
        "ein",
        "eine",
        "einen",
        "einer",
        "den",
        "hat",
        "für",
        "diese",
        "ich",
        "das",
        "ist",
        "und",
        "er",
        "in",
        "mit",
        "zu",
        "wie",
        "oder",
        "zu",
        "jemand",
        "\u200e",
        "ja",
        "man",
        "nicht",
        "kann",
        "was",
        "schon",
        "wenn",
        "war",
        "mir",
        "es",
        "?",
        "so",
        "dir",
        "wir",
        "mal",
        "wird",
        "wurde",
        "hab",
        "the",
        "von",
        "ihr",
        "sein",
        "ob",
        "nur",
        "noch",
        "dass",
        "gelöscht",
        "also",
        "sind",
        "haben",
        "machen",
        "sich",
        "kommt",
        "dem",
        "nachricht",
        "gemacht",
    ]
    tmp = df[~df["msg"].str.contains("weggelassen")]
    words = []
    for ms in tmp["msg"]:
        for word in ms.split():
            if (
                word.lower() not in german_stopwords
                and len(word) > 6
                and "https" not in word
            ):
                words.append(word.lower())
    return pd.DataFrame(Counter(words).most_common(cnt))


def extract_emojis(s):
    return emoji.emoji_list(s)


def get_emoji(user, df):
    if user != "Overall":
        df = df[df["user"] == user]
    emojis = []
    emojis.append(df["msg"].apply(extract_emojis))
    emoji = []
    for e in emojis[0]:
        if len(e) != 0:
            for obj in e:
                emoji.append(obj["emoji"])
    if len(emoji) == 0:
        return pd.DataFrame()
    df_em = (
        pd.DataFrame(Counter(emoji).most_common(len(emoji)))
        .rename(columns={0: "emoji", 1: "count"})
        .nlargest(n=15, columns="count")
    )
    return df_em


def get_timeline(user, df):
    if user != "Overall":
        df = df[df["user"] == user]
    timeline = (
        df.groupby(["year", "month", "monthNumerical"]).count()["msg"].reset_index()
    )
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline["month"].iloc[i] + "-" + str(timeline["year"].iloc[i]))
    timeline["month-year"] = time
    timeline.sort_values(by=["year", "monthNumerical"], inplace=True)
    return timeline


def daily_timeline(user, df):
    if user != "Overall":
        df = df[df["user"] == user]
    df["only-date"] = df["msg_date"].dt.date
    daily_timeline = (
        df.groupby("only-date").count()["msg"].reset_index().sort_values(by="only-date")
    )
    return daily_timeline


def hour_dis(user, df):
    if user != "Overall":
        df = df[df["user"] == user]
    bin_edges = [0, 12, 18, 23]  # Bins for 'before noon', 'after noon', and 'evening'
    bin_labels = ["Vormittag", "Nachmittag", "Am Abend"]

    # Categorize the 'hour' column into bins
    df["time_of_day"] = pd.cut(
        df["hour"].astype(int), bins=bin_edges, labels=bin_labels
    )
    return df


def get_busy_month(user, df):
    if user != "Overall":
        df = df[df["user"] == user]
    return (
        df.groupby("month")
        .count()["msg"]
        .reset_index()
        .sort_values(by="msg", ascending=False)
    )


def get_busy_day(user, df):
    if user != "Overall":
        df = df[df["user"] == user]
    return (
        df.groupby("day-name")
        .count()["msg"]
        .reset_index()
        .sort_values(by="msg", ascending=False)
    )
