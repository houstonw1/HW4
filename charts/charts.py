import altair as alt 
import pandas as pd 

def make_selec():
    team_select = alt.selection_point(fields = ["Team"], on = "click", toggle = True)
    season_param = alt.param(name = "season_filter", value = "All", 
        bind = alt.binding_select(options = ["All", "2023-24", "2024-25"], name = "Filter by Season:"))
    return team_select, season_param

def ch_points(matches) -> alt.Chart:
    team_select, season_param = make_selec()

    def stats_calculator(x):
        """ This function goes through each match to assigns points to home and away teams using the FTR variable. H = Home win = 3 points
        for home team, A = Away win = 3 points for away team, D = Draw = 1 point for each. At thend end it is all put in a DataFrame with 
        columns for Team, Points, Wins, Draws, Losses, and Season """
        rows = []
        for i, row in x.iterrows():
            season = row["Season"] 
            home, away, result = row["HomeTeam"], row["AwayTeam"], row["FTR"]
            if result == "H":
                rows.append({"Team": home, "Season": season, "Points": 3, "Wins": 1, "Draws": 0, "Losses": 0})
                rows.append({"Team": away, "Season": season, "Points": 0, "Wins": 0, "Draws": 0, "Losses": 1})
            elif result == "A":
                rows.append({"Team": home, "Season": season, "Points": 0, "Wins": 0, "Draws": 0, "Losses": 1})
                rows.append({"Team": away, "Season": season, "Points": 3, "Wins": 1, "Draws": 0, "Losses": 0})
            else:
                rows.append({"Team": home, "Season": season, "Points": 1, "Wins": 0, "Draws": 1, "Losses": 0})
                rows.append({"Team": away, "Season": season, "Points": 1, "Wins": 0, "Draws": 1, "Losses": 0})
        rowsdf = pd.DataFrame(rows)
        summary = rowsdf.groupby(["Team", "Season"], as_index = False).sum()
        return summary

    stats_team = stats_calculator(matches)
    colorscale = alt.Color("Season:N", scale = alt.Scale(domain = ["2023-24", "2024-25"], range = ["blue", "red"]))
    teamorder = (stats_team.groupby("Team")["Points"].sum().sort_values(ascending = False).index.tolist())
    base1 = alt.Chart(stats_team).transform_filter("(season_filter === 'All') || (datum.Season === season_filter)")

    pchart = base1.mark_circle().encode(y = alt.Y('Team:N', sort = teamorder, title='Team'), 
        x = alt.X('Points:Q', title='Total Points'), color = alt.condition(team_select, colorscale, alt.value("lightgray")), 
        opacity = alt.condition(team_select, alt.value(1.0), alt.value(0.5)), tooltip = [alt.Tooltip('Team:N'),
        alt.Tooltip('Season:N'), alt.Tooltip('Points:Q'), alt.Tooltip('Wins:Q'), alt.Tooltip('Draws:Q'), alt.Tooltip('Losses:Q'),]
    ).add_params(team_select, season_param).properties(height = 500)
    return pchart

def ch_home_away(matches) -> alt.Chart:
    team_select, season_param = make_selec()
    rows = []
    for i, row in matches.iterrows():
        home, away, result, season = row["HomeTeam"], row["AwayTeam"], row["FTR"], row["Season"]
        if result == "H":
            rows.append({"Team": home, "Season": season, "Home Points": 3, "Away Points": 0})
            rows.append({"Team": away, "Season": season, "Home Points": 0, "Away Points": 0})
        elif result == "A":
            rows.append({"Team": home, "Season": season, "Home Points": 0, "Away Points": 0})
            rows.append({"Team": away, "Season": season, "Home Points": 0, "Away Points": 3})
        else:
            rows.append({"Team": home, "Season": season, "Home Points": 1, "Away Points": 0})
            rows.append({"Team": away, "Season": season, "Home Points": 0, "Away Points": 1})
    teamsdf = pd.DataFrame(rows).groupby(["Team", "Season"], as_index = False).sum()
    point_diff = (teamsdf.groupby("Team").apply(lambda x: (x["Home Points"] - x["Away Points"])
        .mean()).sort_values(ascending = False).index.tolist())
    base2 = alt.Chart(teamsdf).transform_filter("(season_filter === 'All') || (datum.Season === season_filter)")

    home_chart = base2.mark_bar().encode(x = alt.X("Home Points:Q", title= "Home Points"), y = alt.Y("Team:N", sort= point_diff, title = "Team"),
        color = alt.condition(team_select, alt.value("orange"), alt.value("lightgray")), opacity = alt.condition(
        team_select, alt.value(1.0), alt.value(0.5)), tooltip = [alt.Tooltip("Team:N"), alt.Tooltip("Season:N"), 
        alt.Tooltip("Home Points:Q")]).add_params(team_select, season_param).properties(height = 400)

    away_chart = base2.mark_bar().encode(x = alt.X("Away Points:Q", title= "Away Points"), y = alt.Y("Team:N", sort= point_diff, title = "Team"),
        color = alt.condition(team_select, alt.value("green"), alt.value("lightgray")), opacity = alt.condition(
        team_select, alt.value(1.0), alt.value(0.5)), tooltip = [alt.Tooltip("Team:N"), alt.Tooltip("Season:N"), 
        alt.Tooltip("Away Points:Q")]).add_params(team_select, season_param).properties(height = 400)
    return home_chart | away_chart

def ch_fouls(matches) -> alt.Chart:
    team_select, season_param = make_selec()
    
    hfouls = matches.groupby(["HomeTeam", "Season"])["HF"].mean().reset_index()
    hfouls.columns = ["Team", "Season", "AvgHomeFouls"]
    afouls = matches.groupby(["AwayTeam", "Season"])["AF"].mean().reset_index()
    afouls.columns = ["Team", "Season", "AvgAwayFouls"]

    teamfouls = hfouls.merge(afouls, on = ["Team", "Season"])
    order = (teamfouls.groupby("Team")["AvgHomeFouls"].mean().sort_values(ascending = False).index.tolist())
    base3 = alt.Chart(teamfouls).transform_filter("(season_filter === 'All') || (datum.Season === season_filter)")

    hfouls_chart = base3.mark_circle().encode(
        x = alt.X("AvgHomeFouls:Q", title = "Average Home Fouls per Match"), y = alt.Y("Team:N", sort = order, title = "Team"), 
        color = alt.condition(team_select, alt.value("orange"), alt.value("lightgray")), 
        opacity = alt.condition(team_select, alt.value(1.0), alt.value(0.5)), tooltip = [alt.Tooltip("Team:N"), alt.Tooltip("Season:N"), 
        alt.Tooltip("AvgHomeFouls:Q", title ="Average Home Fouls"),]
    ).add_params(team_select, season_param).properties(height = 400)

    afouls_chart = base3.mark_circle().encode(
        x = alt.X("AvgAwayFouls:Q", title = "Average Away Fouls per Match"), y = alt.Y("Team:N", sort = order, title = "Team"), 
        color = alt.condition(team_select, alt.value("green"), alt.value("lightgray")),
        opacity = alt.condition(team_select, alt.value(1.0), alt.value(0.5)), tooltip = [alt.Tooltip("Team:N"), alt.Tooltip("Season:N"), 
        alt.Tooltip("AvgAwayFouls:Q"),]).properties(height = 400)
    return hfouls_chart | afouls_chart