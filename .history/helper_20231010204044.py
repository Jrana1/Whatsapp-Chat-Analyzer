def fetch_stats(user, df):
    if user != "Overall":
        df = df[df["user"] == user]
    return df.shape[0]
