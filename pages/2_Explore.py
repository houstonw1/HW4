import streamlit as st 
from utils.io import load_data
from charts.charts import ch_points, ch_home_away, ch_fouls

st.set_page_config(page_title = "Explore", layout="wide")
matches = load_data()

st.title("Explore the Data")
st.markdown("To explore the story without a narrative: Use the dropdown to filter the charts by season and click to highlight a team.")

st.subheader("Points by Team")
st.altair_chart(ch_points(matches), use_container_width= True)

st.subheader("Home vs Away Points")
st.altair_chart(ch_home_away(matches), use_container_width= True)

st.subheader("Average Fouls by Team")
st.altair_chart(ch_fouls(matches), use_container_width= True)
