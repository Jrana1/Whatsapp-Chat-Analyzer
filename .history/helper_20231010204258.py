def fetch_stats(user, df):
    if user != "Overall":
        df = df[df["user"] == user]
    cnt = 0
    for ms in df["msg"]:
        cnt += len(ms.split())

    return df.shape[0], cnt
