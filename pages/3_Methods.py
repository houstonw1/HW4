import streamlit as st

st.set_page_config(page_title= "Methods", layout = "wide")
st.title("Methods and Limitations")

st.markdown(
    """ Datasets: **PL-season-2324.csv** , **PL-season-2324.csv**
    Source: Provided by instructor

    Variables: 'HomeTeam', 'AwayTeam', 'FTR', 'HF', 'AF'

    Limitations: 
    - The data only contains 2 seasons which causes short term anaysis rather than long term
    - Fouls could be more specific in the kind. They are generalized in these datasets """
)