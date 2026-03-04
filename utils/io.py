import streamlit as st
import pandas as pd 

@st.cache_data
def load_data() -> pd.DataFrame:
    pl_2324_df = pd.read_csv("PL-season-2324.csv")
    pl_2425_df = pd.read_csv("PL-season-2425.csv")

    pl_2324_df["Season"] = "2023-24"
    pl_2425_df["Season"] = "2024-25"

    matches = pd.concat([pl_2324_df, pl_2425_df], ignore_index = True)
    return matches