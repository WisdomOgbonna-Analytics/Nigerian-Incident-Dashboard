import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Nigeria Incident Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# =========================
# HEADER
# =========================
st.title("📊 Nigeria Incident Analytics Dashboard")


st.info("Project Introduction: This project analyzes incidents, accidents, and " \
"violence-related deaths across Nigeria.")


st.info("""
Objective

To identify:

- States with the highest number of incidents.
- States with the highest number of deaths.
- Incident categories that lead to the most deaths.
- How incidents trend over a given period.
""")

# =========================
st.info("""
🎯 **Research Questions**
1. Which top ten(10) states recorded the highest number of incidents?
2. Which top ten(10) states recorded the highest number of deaths?
3. Which incident categories accounted for the highest number of deaths?
4. How did incident occurrences change between June 2023 and June 2024?
""")

# LOAD DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_incidents.csv")
    df.columns = df.columns.str.strip()

    df["Start date"] = pd.to_datetime(df["Start date"])
    df["End date"] = pd.to_datetime(df["End date"])

    # recreate if needed
    if "Year" not in df.columns:
        df["Year"] = df["Start date"].dt.year
    if "Month" not in df.columns:
        df["Month"] = df["Start date"].dt.month
    if "Month Name" not in df.columns:
        df["Month Name"] = df["Start date"].dt.month_name()

    return df


df = load_data()

# =========================
# SIDEBAR
# =========================
st.sidebar.image("C:/Users/HP/Nigeria_incidents_project/profile image .jpg.jpeg", width=80)

st.sidebar.markdown("""
Name: Ogbonna Wisdom
                     
Role:  Data Analyst
""")
st.sidebar.header("🔎Dashboard Filters")

state_options = sorted(df["State"].dropna().unique())

states = st.sidebar.multiselect(
    "Select State",
    options=state_options,
    default=state_options,
    key="state_filter"
)

years = st.sidebar.multiselect(
    "Select Year(s)",
    options=sorted(df["Year"].unique()),
    default=sorted(df["Year"].unique())
)

# START DATE
start_date = st.sidebar.date_input(
    "Start Date",
    df["Start date"].min().date()
)

end_date = st.sidebar.date_input(
    "End Date",
    df["End date"].max().date()
)

# MONTH NAME
month_names = st.sidebar.multiselect(
    "Select Month Name",
    options=sorted(df["Month Name"].dropna().unique()),
    default=sorted(df["Month Name"].dropna().unique())
)

filtered_df = df[
    (df["State"].isin(states)) &
    (df["Start date"].dt.date >= start_date) &
    (df["End date"].dt.date <= end_date) &
    (df["Month Name"].isin(month_names))
]

# CONTACT BUTTON
st.sidebar.link_button(
    "💬 Chat on WhatsApp",
    "https://wa.me/2348035118372?text=Hello%20👋%20I%20need%20support%20regarding%20the%20incident%20dashboard."
)


st.sidebar.link_button(
    "📧 Send Email",
    "mailto:donwiz200@gmail.com"
)
# CLIENT FEEDBACK BUTTON

st.sidebar.markdown("### 💬 Feedback")

with st.sidebar.form("feedback_form"):
    name = st.text_input("Your Name")
    rating = st.selectbox("Rate this dashboard", [1, 2, 3, 4, 5])
    feedback = st.text_area("Your Feedback")

    submit = st.form_submit_button("Submit")

    if submit:
        st.success("✅ Feedback submitted successfully!")

# =========================
# KPI CARDS
# =========================

col1, col2, col3 = st.columns(3)

col1.metric("Total Incidents", f"{len(filtered_df):,}")
col2.metric("Total Deaths", f"{filtered_df['Number of deaths'].sum():,}")
col3.metric(
    "Average Deaths",
    f"{filtered_df['Number of deaths'].mean():.2f}"
)

# =========================
# CHART 1: TOP STATES INCIDENTS
# =========================
top_states = (
    filtered_df["State"]
    .value_counts()
    .head(10)
    .reset_index()
)
top_states.columns = ["State", "Incident Count"]

fig1, ax1 = plt.subplots(figsize=(8, 4))
sns.set_theme(style="whitegrid")
palette = sns.color_palette("Set2", n_colors=len(top_states))

sns.barplot(
    data=top_states,
    x="State",
    y="Incident Count",
    hue="State",
    palette=palette,
    legend=False,
    ax=ax1
)
sns.despine(left=True, bottom=True)
# DATA LABELS
for container in ax1.containers:
    ax1.bar_label(container, fmt='%d',padding=3,fontsize=8)

ax1.set_title("RQ1: Top 10 States by Incident Count")
ax1.tick_params(axis="x", rotation=45)
plt.tight_layout()

st.pyplot(fig1,use_container_width=True)
if not filtered_df.empty:
    top_state = filtered_df["State"].value_counts().idxmax()
    top_value = filtered_df["State"].value_counts().max()

    st.info(f"""
    Insight:
    
    - {top_state} recorded the highest number of incidents ({top_value}).
    - Other states follow based on the current selection.
    - This indicates that incident distribution varies depending on selected filters.
    """)
else:
    st.info("No data available for selected filters.")

# =========================
# CHART 2: TOP STATES BY DEATHS
# =========================
top_death_states = (
    filtered_df.groupby("State")["Number of deaths"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
sns.despine(left=True, bottom=True)
fig2, ax2 = plt.subplots(figsize=(8, 4))
sns.set_theme(style="whitegrid")
palette = sns.color_palette("Set2", n_colors=len(top_death_states))

sns.barplot(
    data=top_death_states,
    x="State",
    y="Number of deaths",
    hue="State",
    palette=palette,
    legend=False,
    ax=ax2
)
sns.despine(left=True, bottom=True)
# ADD DATA LABELS
for container in ax2.containers:
    ax2.bar_label(container, fmt='%d',padding=3,fontsize=8)

ax2.set_title("RQ2: Top 10 States by Number of Deaths")
ax2.tick_params(axis="x", rotation=45)
plt.tight_layout()

st.pyplot(fig2,use_container_width=True)
if not filtered_df.empty:
    death_state = (
        filtered_df.groupby("State")["Number of deaths"]
        .sum()
        .idxmax()
    )

    death_value = (
        filtered_df.groupby("State")["Number of deaths"]
        .sum()
        .max()
    )

    st.info(f"""
    Insight:
    
    - {death_state} recorded the highest number of deaths ({death_value}).
    - Fatality levels differ significantly across states.
    - High incidents do not always mean high deaths.
    """)

# =========================
# CHART 3: DEADLIEST INCIDENT TYPES
# =========================

top_deadly_incidents = (
    filtered_df.groupby("Incident")["Number of deaths"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig3, ax3 = plt.subplots(figsize=(8, 4))
sns.set_theme(style="whitegrid")

sns.barplot(
    data=top_deadly_incidents,
    x="Number of deaths",
    y="Incident",
    hue="Incident",
    palette="Set2",
    legend=False,
    ax=ax3
)
sns.despine(left=True, bottom=True)
# ADD DATA LABELS
for container in ax3.containers:
    ax3.bar_label(container, fmt='%d',padding=3,fontsize=8)

ax3.set_title("RQ3: Top 10 Deadliest Incident Types")
plt.tight_layout()

st.pyplot(fig3,use_container_width=True)
if not filtered_df.empty:
    deadly_incident = (
        filtered_df.groupby("Incident")["Number of deaths"]
        .sum()
        .idxmax()
    )

    deadly_value = (
        filtered_df.groupby("Incident")["Number of deaths"]
        .sum()
        .max()
    )

    st.info(f"""
    Insight:

    - {deadly_incident} is the deadliest incident type ({deadly_value} deaths).
    - Different incident categories contribute differently to fatalities.
    """)


# =========================
# CHART 4: MONTHLY TREND (JUNE 2023 - JUNE 2024)
# =========================

df_filtered = filtered_df[
    ((filtered_df['Year'] == 2023) & (filtered_df['Month'] >= 6)) |
    ((filtered_df['Year'] == 2024) & (filtered_df['Month'] <= 6))
]

incident_trend = (
    df_filtered.groupby(["Year", "Month", "Month Name"])
    .size()
    .reset_index(name="incident_Count")
)

incident_trend["Month_Year"] = (
    incident_trend["Month Name"] + " " + incident_trend["Year"].astype(str)
)

fig4, ax4 = plt.subplots(figsize=(8, 4))

sns.set_theme(style="whitegrid")
ax = sns.lineplot(
    data=incident_trend,
    x="Month_Year",
    y="incident_Count",
    marker="o",
    linewidth=1.5,
    color="tab:green"
    
)
sns.despine(left=True, bottom=True)

# ADD DATA LABELS
for x, y in zip(incident_trend["Month_Year"], incident_trend["incident_Count"]):
    ax4.text(x, y, str(y), ha='right', va='top', fontsize=11)

ax4.set_title("RQ4: Incident Trend (June 2023 - June 2024)")
ax4.tick_params(axis="x", rotation=45)

plt.tight_layout()

st.pyplot(fig4,use_container_width=True)
if not incident_trend.empty:
    peak_month = incident_trend.loc[
        incident_trend["incident_Count"].idxmax(), "Month_Year"
    ]

    lowest_month = incident_trend.loc[
        incident_trend["incident_Count"].idxmin(), "Month_Year"
    ]

    st.info(f"""
    Insight:

    - Incidents peaked in {peak_month}.
    - The lowest point occurred in {lowest_month}.
    - The trend fluctuates over time based on selected filters.
    """)


st.info("""
Conclusion:
        
This analysis reveals that while Lagos experiences the highest number of incidents, Borno suffers the 
greatest fatalities, highlighting differences in incident severity. 
Road accidents emerge as the single deadliest category, underscoring the importance 
of everyday safety measures alongside conflict resolution. Between June 2023-June 2024,incidents were fairly stable. In mid‑2023,
dipped at the end of the year, hit their lowest in February 2024, then surged to a peak in April before moderating again by June 2024.

Recommendations:

1) Focus safety and prevention programs in Lagos to reduce incident frequency.
Prioritize conflict resolution and humanitarian aid in Borno, Zamfara, and Kaduna to reduce fatalities.


2) Strengthen traffic regulations, road infrastructure, and public awareness campaigns to address the high death toll from road accidents.


3) Establish real-time monitoring systems to detect and respond to spikes in incidents, especially during high-risk months.


4) Combine security measures with public health and disaster management strategies to address both conflict-related and non-conflict incidents.
""")

# =========================
# =========================
# DATA VIEW
# =========================
with st.expander("📂 View Dataset"):
    st.dataframe(filtered_df)

# DOWNLOAD BUTTON
# =========================
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download Dataset",
    data=csv,
    file_name="Nigera_incident_Project.csv",
    mime="text/csv"
)     

# FOOTER
# =========================
 
st.caption("Powered by: Wikode")