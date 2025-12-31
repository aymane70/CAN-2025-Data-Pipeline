
import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from google.cloud import bigquery
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()


PROJECT_ID = os.getenv("PROJECT_ID")
DATASET_ID = os.getenv("TRANSFORMED_DATA")
CREDENTIALS_PATH = os.getenv("SERVICE_ACCOUNT_FILE")

if not PROJECT_ID or not DATASET_ID or not CREDENTIALS_PATH:
    st.error("❌ Missing required environment variables")
    st.stop()

credentials = service_account.Credentials.from_service_account_file(
    CREDENTIALS_PATH,
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

client = bigquery.Client(credentials=credentials, project=PROJECT_ID)


st.set_page_config(
    page_title="CAN 2025 | Tournament Intelligence",
    layout="wide"
)

st.markdown(
    """
    <style>
    .block-container { padding-top: 2rem; }
    </style>
    """,
    unsafe_allow_html=True
)


@st.cache_data(show_spinner=False)
def load_data(query):
    return client.query(query).to_dataframe()


def team_standings():
    return load_data(f"SELECT * FROM `{PROJECT_ID}.{DATASET_ID}.mart_team_standings`")

def top_scorers():
    return load_data(f"SELECT * FROM `{PROJECT_ID}.{DATASET_ID}.mart_top_scorers`")

def stadium_perf():
    return load_data(f"SELECT * FROM `{PROJECT_ID}.{DATASET_ID}.mart_stadium_performance`")

def financials():
    return load_data(f"SELECT * FROM `{PROJECT_ID}.{DATASET_ID}.mart_financial_summary`")


st.sidebar.title("⚽ CAN 2025")
page = st.sidebar.radio(
    "Explore",
    [
        "🏆 Executive Overview",
        "📈 Team Performance",
        "🥇 Players Impact",
        "🏟 Stadium Insights",
        "💰 Revenue Intelligence"
    ]
)


if page == "🏆 Executive Overview":
    st.title("🏆 CAN 2025 — Tournament Intelligence Overview")

    fin = financials()
    stad = stadium_perf()

    total_rev = fin["total_revenue"].sum()
    total_tickets = fin["total_tickets_sold"].sum()
    avg_ticket = total_rev / total_tickets if total_tickets else 0

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("💰 Revenue", f"${total_rev/1e6:.2f}M")
    k2.metric("🎫 Tickets Sold", f"{total_tickets/1e6:.2f}M")
    k3.metric("💵 Avg Ticket", f"${avg_ticket:.2f}")
    k4.metric("🏟 Avg Occupancy", f"{stad['occupancy_rate'].mean()*100:.1f}%")

    st.divider()

    phase_rev = (
        fin.groupby("tournament_phase", as_index=False)
           .agg(revenue=("total_revenue", "sum"))
           .sort_values("revenue", ascending=False)
    )

    fig = px.bar(
        phase_rev,
        x="tournament_phase",
        y="revenue",
        text_auto=".2s",
        title="Revenue by Tournament Phase"
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


elif page == "📈 Team Performance":
    st.title("📈 Team Performance & Group Dynamics")

    df = team_standings()
    group = st.selectbox("Select Group", sorted(df["group_name"].unique()))

    gdf = df[df["group_name"] == group]

    fig = px.bar(
        gdf,
        x="team_name",
        y="points",
        color="goal_difference",
        title=f"Group {group} — Points & Goal Difference",
        text="points"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        gdf.sort_values("group_position"),
        use_container_width=True
    )


elif page == "🥇 Players Impact":
    st.title("🥇 Player Impact — Goals Decide Tournaments")

    df = top_scorers()

    fig = px.scatter(
        df,
        x="matches_with_events",
        y="total_goals",
        size="total_goals",
        color="team_name",
        hover_name="player_name",
        title="Goal Impact vs Match Presence"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top 10 Goal Scorers")
    st.dataframe(df.head(10), use_container_width=True)


elif page == "🏟 Stadium Insights":
    st.title("🏟 Stadium Utilization & Fan Engagement")

    df = stadium_perf()

    fig = px.scatter(
        df,
        x="capacity",
        y="avg_attendance",
        size="matches_hosted",
        color="city",
        hover_name="stadium_name",
        title="Capacity vs Attendance"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df.sort_values("total_attendance", ascending=False), use_container_width=True)


elif page == "💰 Revenue Intelligence":
    st.title("💰 Revenue Intelligence — Where the Money Is")

    df = financials()

    vip_share = df["vip_revenue"].sum() / df["total_revenue"].sum()

    c1, c2 = st.columns(2)
    c1.metric("💎 VIP Share", f"{vip_share*100:.1f}%")
    c2.metric("📊 Matches Analysed", len(df))

    rev_match = df.groupby("match_date", as_index=False).agg(
        revenue=("total_revenue", "sum")
    )

    fig = px.line(
        rev_match,
        x="match_date",
        y="revenue",
        title="Revenue Trend Over Tournament"
    )
    st.plotly_chart(fig, use_container_width=True)
