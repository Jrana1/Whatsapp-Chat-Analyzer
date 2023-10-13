from urlextract import URLExtract


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
    top_chatter_per = round(df["user"].value_counts() / df.shape[0] * 100, 2)
    return top_chatter, top_chatter_per
