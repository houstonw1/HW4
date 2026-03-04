import streamlit as st
st.set_page_config(page_title= "EPL Data Story", layout="wide")
st.title("What teams performed better and how in the 2 Seasons of the EPL")
st.markdown(
    """ A look at team performance over the 2023-24 and 2024-25 EPL seasons
    and their data surrounding certain metrics. The layout on the side should 
    be to explore the data yourself.

    Story = Follow the narrative
    Explore = Interact with the visualizations and data
    Methods = See the data and its limits """
)
st.info("Datasets: PL-season-2324.csv and PL-season-2425.csv")