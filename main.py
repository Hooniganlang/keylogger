import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.title("Cybersecurity Activity Dashboard")

if os.path.exists("logs.csv"):
    df = pd.read_csv("logs.csv", names=["timestamp","key"])
else:
    df = pd.DataFrame(columns=["timestamp","key"])

st.metric("Total Keystrokes", len(df))
st.metric("Unique Keys", df["key"].nunique())

if not df.empty:
    freq = df["key"].value_counts().reset_index()
    freq.columns = ["key","count"]

    fig = px.bar(freq, x="key", y="count")
    st.plotly_chart(fig)

st.dataframe(df)
