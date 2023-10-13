def fetch_stats(user, df):
    if user != "Overall":
        df = df[df["user"] == user]
    cnt = 0
    for ms in df["msg"]:
        cnt += len(ms.split())
    num_media = df[df["msg"].str.contains("weggelassen")].shape[0]

    return df.shape[0], cnt, num_media
