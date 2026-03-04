import streamlit as st 
from utils.io import load_data
from charts.charts import (ch_points, ch_home_away, ch_fouls)

st.set_page_config(page_title = "Story", layout = "wide")
matches = load_data()

st.title("A Data Story: EPL and Team's Performance")
st.markdown("Central Question: How do we see team performance differ across select metrics?")

st.header("1) Which EPL team(s) had the most points?")
st.write("Points determine final league standings. Click on a team to highlight it. Use the dropdown to see specific seasons.")
st.altair_chart(ch_points(matches), use_container_width = True)
st.caption("Takeaway: A small group of clubs are consistently at the top. There is clear dominance.")

st.header("2) Does home field advantage matter in the EPL?")
st.write("In sports there is a theory that teams play better at home. Click on a team to highlight it. Use the dropdown to see specific seasons.")
st.altair_chart(ch_home_away(matches), use_container_width = True)
st.caption("Takeaway: Home field advantage really depends on the team. The ones who don't perform well away can be picked on by rivals.")

st.header("3) Which team(s) plays more aggressive in terms of fouls?")
st.write("Fouls can change the momentum of a match. Click on a team to highlight it. Use the dropdown to see specific seasons.")
st.altair_chart(ch_fouls(matches), use_container_width = True)
st.caption("Takeaway: Teams typically foul more away than home. This could imply teams are more aggressive away or the officiating differs.")
