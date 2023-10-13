import re
import pandas as pd


def remove_text_with_security(text):
    #  pattern = r"Deine Sicherheitsnummer für \+[0-9]*\s[0-9]*\s[0-9]* hat sich geändert. Tippe, um mehr zu erfahren."
    pattern = "Tippe, um mehr zu erfahren."
    match = re.search(pattern, text)
    return bool(match)


def remove_text_with_invitation(text):
    return bool(re.search("ist der Gruppe mit dem Einladungslink beigetreten.", text))


def remove_text_with_group_builder(text):
    return bool(re.search("hat die Gruppe erstellt.", text)) or bool(
        re.search("hat die Gruppenbeschreibung geändert.", text)
    )


def preprocessing(data):
    # extract msg
    pattern = r"\[\d{1,2}.\d{1,2}.\d{1,2},\s\d{1,2}:\d{1,2}:\d{1,2}\]\s"
    msg = re.split(pattern, data)
    msg = msg[1:]
    # extract date
    pattern1 = "\d{1,2}.\d{1,2}.\d{1,2},\s\d{1,2}:\d{1,2}:\d{1,2}"
    dates = re.findall(pattern1, data)
    # create dataFrame
    df = pd.DataFrame({"user_msg": msg, "msg_date": dates})
    # convert type to datetime
    df["msg_date"] = pd.to_datetime(df["msg_date"])
    users = []
    msgs = []
    for ms in df["user_msg"]:
        entry = re.split("([\w\W]+?):\s", ms)
        if entry[1:]:
            users.append(entry[1])
            msgs.append(entry[2])
    df["user"] = users
    df["msg"] = msgs
    # remove unwanted texts
    df = df[~df["msg"].apply(remove_text_with_security)]
    # remove unwanted texts
    df = df[~df["msg"].apply(remove_text_with_invitation)]
    # remove unwanted texts
    df = df[~df["msg"].apply(remove_text_with_group_builder)]
    # drop unwanted col
    df.drop(columns="user_msg", axis="column", inplace=True)
    # add new cos
    df["month"] = df["msg_date"].dt.month_name()
    df["day"] = df["msg_date"].dt.day
    df["year"] = df["msg_date"].dt.year
    df["hour"] = df["msg_date"].dt.hour
    df["minute"] = df["msg_date"].dt.minute

    return df
