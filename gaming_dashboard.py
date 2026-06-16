
import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Student Performance Analytics Dashboard",
    page_icon="🎮",
    layout="wide"
)
def summary_box(title, text, color="#2563EB"):
    st.markdown(f"""
    <div style="
        background:#F8FAFC;
        padding:15px;
        border-left:5px solid {color};
        border-radius:10px;
        margin-top:10px;
        margin-bottom:20px;
        font-size:16px;
    ">
        <b>{title}</b><br>
        {text}
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------
st.markdown("""
<style>

.insight-card{
    padding:20px;
    border-radius:15px;
    min-height:140px;
    box-shadow:0px 2px 6px rgba(0,0,0,0.05);
}

.study-card{
    background:#F3E8FF;
    border-left:6px solid #9333EA;
}

.gaming-card{
    background:#FEF2F2;
    border-left:6px solid #DC2626;
}

.sleep-card{
    background:#DBEAFE;
    border-left:6px solid #2563EB;
}

.obs-card{
    background:#F0FDF4;
    border-left:6px solid #22C55E;
    padding:18px 25px;
    border-radius:15px;
    margin-bottom:20px;
}

.exec-card{
    background:#ECFDF5;
    border-left:6px solid #16A34A;
    padding:25px;
    border-radius:15px;
    margin-top:25px;
}

.data-card{
    background:white;
    padding:18px;
    border-radius:15px;
    box-shadow:0px 2px 6px rgba(0,0,0,0.05);
}
.metric-card{
    padding:12px;
    border-radius:12px;
    min-height:100px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🎯 Student Performance Analytics Platform")

st.markdown(
    "Evaluating the Influence of Gaming Habits, Study Behavior, Sleep Quality, Attendance, and Stress Levels on Academic Achievement"
)

# --------------------------------------------------
# DATA LOADING
# --------------------------------------------------

df = pd.read_csv("Gaming_Academic_Performance.csv")

# --------------------------------------------------
# NAVIGATION
# --------------------------------------------------

page = st.sidebar.radio(
    "📌 Navigation",
    [
        "🏠 Executive Summary",
        "📊 Exploratory Analysis",
        "📈 Statistical Insights",
        "🎯 Key Findings",
        "🧠 Performance Predictor"
    ]
)

# --------------------------------------------------
# FEATURE ENGINEERING
# --------------------------------------------------

df["grade_category"] = pd.cut(
    df["grades"],
    bins=[0,60,80,120],
    labels=["Poor","Average","Excellent"]
)

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.header("🎛 Dashboard Filters")

gender = st.sidebar.multiselect(
    "Gender",
    df["gender"].unique(),
    default=list(df["gender"].unique())
)

genre = st.sidebar.multiselect(
    "Gaming Genre",
    df["gaming_genre"].unique(),
    default=list(df["gaming_genre"].unique())
)

stress = st.sidebar.multiselect(
    "Stress Level",
    df["stress_level"].unique(),
    default=list(df["stress_level"].unique())
)

age_range = st.sidebar.slider(
    "Age Range",
    int(df["age"].min()),
    int(df["age"].max()),
    (
        int(df["age"].min()),
        int(df["age"].max())
    )
)

# --------------------------------------------------
# FILTERED DATA
# --------------------------------------------------

fdf = df[
    (df["gender"].isin(gender))
    &
    (df["gaming_genre"].isin(genre))
    &
    (df["stress_level"].isin(stress))
    &
    (df["age"].between(age_range[0], age_range[1]))
]

st.sidebar.success(
    f"Records: {len(fdf)}"
)

# ==================================================
# EXECUTIVE DASHBOARD
# ==================================================

if page == "🏠 Executive Summary":
    st.markdown("---")

# KPIs

    c1,c2,c3,c4,c5,c6 = st.columns(6)

    c1.metric("👨‍🎓 Students", f"{len(df):,}")

    c2.metric(
        "🎓 Average Grade",
        f"{df['grades'].mean():.1f}%"
    )

    c3.metric(
        "🎮 Gaming Time",
        f"{df['gaming_hours'].mean():.1f} hrs"
    )

    c4.metric(
        "📚 Study Time",
        f"{df['study_hours'].mean():.1f} hrs"
    )

    c5.metric(
        "😴 Sleep Duration",
        f"{df['sleep_hours'].mean():.1f} hrs"
    )
    c6.metric(
        "🏫 Attendance",
        f"{df['attendance'].mean():.1f}%"
)

    st.markdown("---")
    # DATA PREVIEW

    st.subheader("📂 Dataset Explorer")

    col1, col2 = st.columns([4, 1])

    with col1:
        st.info(
            f"Dataset contains {len(df):,} records and {len(df.columns)} features."
    )

    with col2:
        st.download_button(
            "📥 Download CSV",
            data=df.to_csv(index=False),
            file_name="Gaming_Academic_Performance.csv",
            mime="text/csv"
    )

    st.dataframe(
        df,
        use_container_width=True,
        height=500
)
    st.subheader("📊 Dataset Overview")

    col1,col2 = st.columns(2)
    with col1:
         st.error(f"""
    ### ❗ Missing Values
    ## {df.isnull().sum().sum()}
    Data points require review
    """)


    with col2:
        st.success(f"""
    ### ✅ Duplicate Records
    ## {df.duplicated().sum()}
    No duplicate records detected
    """)
        
    c3,c4 = st.columns(2)
    with c3:
        st.info(f"""
    ### 🔢 Numerical Features
    ## {len(df.select_dtypes(include='number').columns)}
    Continuous variables
    """)
        
    with c4:
        st.warning(f"""
    ### 📝 Categorical Features
    ## {len(df.select_dtypes(exclude='number').columns)}
    Classification variables
    """)
    
    st.markdown("---")
    # STATISTICAL SUMMARY

    st.subheader("📈 Statistical Summary")

    st.dataframe(
        fdf.describe().round(2),
        use_container_width=True
    )
    st.markdown("""
          <div class="obs-card">
          <h2>🎯 Key Observations</h2>

          <ul style="line-height:1.6; margin-bottom:0;">
          <li>📚 Study hours are generally higher than gaming hours.</li>
          <li>🎓 Median academic performance is around 67%.</li>
          <li>🏫 Most students maintain attendance above 79%.</li>
          <li>😴 Average sleep duration remains close to 6 hours.</li>
          </ul>

        </div>""", unsafe_allow_html=True)

    
    st.markdown("<div style='height:25px'></div>", unsafe_allow_html=True)
    st.subheader("💡 Strategic Insights")
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    card_style = """
background:white;
padding:20px;
border-radius:15px;
min-height:150px;
box-shadow:0 3px 10px rgba(0,0,0,0.08);
"""
    c1,c2,c3 = st.columns(3)

    with c1:

     st.markdown(f"""
    <div style="{card_style} border-left:6px solid #9333EA;">
        <h3>📚 Study Impact</h3>
        <p>More study hours → Better grades</p>
    </div>
    """, unsafe_allow_html=True)
    with c2:

        st.markdown(f"""
    <div style="{card_style} border-left:6px solid #DC2626;">
        <h3>🎮 Gaming Effect</h3>
        <p>Excessive gaming → Lower grades</p>
    </div>
    """, unsafe_allow_html=True)
    with c3:

      st.markdown(f"""
    <div style="{card_style} border-left:6px solid #0EA5E9;">
        <h3>😴 Sleep Quality</h3>
        <p>Adequate sleep → Improved performance</p>
    </div>
    """, unsafe_allow_html=True)

#     st.markdown("""
# <div style="
#     background: linear-gradient(135deg,#F5F9FF,#EAF2FF);
#     padding:25px;
#     border-radius:18px;
#     border-left:8px solid #2563EB;
#     box-shadow:0 4px 12px rgba(0,0,0,0.08);
#     margin-top:15px;
#     margin-bottom:20px;
# ">

# <h2 style="
#     color:#1E40AF;
#     margin-bottom:20px;
#     font-size:34px;
#     font-weight:700;
# ">
# 🏆 Executive Summary
# </h2>

# <div style="font-size:20px; line-height:1.9; color:#1F2937;">

# <p>
# 📚 <b style="color:#2563EB;">Study Hours</b>
# remain the strongest driver of academic success.
# </p>

# <p>
# 😴 Students with better
# <b style="color:#0EA5E9;">Sleep Quality</b>
# achieve improved concentration and performance.
# </p>

# <p>
# 🎮 Excessive
# <b style="color:#DC2626;">Gaming Hours</b>
# and higher addiction scores negatively impact grades.
# </p>

# <p>
# 🏫 Consistent
# <b style="color:#16A34A;">Attendance</b>
# is a critical predictor of student achievement.
# </p>

# </div>
# </div>
# """, unsafe_allow_html=True)
# ==================================================
# STUDENT EXPLORER
# ==================================================

elif page == "📊 Exploratory Analysis":

    st.subheader("🔍 Student Explorer")

    st.info("""Explore the distribution of grades, gaming habits,study patterns, sleep behavior and stress levels.""")

    # ------------------------------------------
    # Grades Distribution
    # ------------------------------------------

    gender_counts = fdf["gender"].value_counts().reset_index()
    gender_counts.columns = ["gender", "count"]

    fig_gender = px.pie(
        gender_counts,
    names="gender",
    values="count",
    hole=0.4,
    title="Student Gender Distribution"
)

    fig_gender.update_traces(
        textposition="inside",
    textinfo="percent+label"
)

    st.plotly_chart(fig_gender, use_container_width=True)

    top_gender = gender_counts.iloc[0]["gender"]

    st.success(
    f"""
👥 {top_gender} students represent the largest share of the dataset.

The gender distribution is relatively balanced, enabling fair comparison of academic outcomes across groups.
"""
)
    # ------------------------------------------
    # Gaming Hours Distribution
    # ------------------------------------------

    fig_gaming = px.histogram(fdf,
    x="gaming_hours",
    nbins=15,
    color="stress_level",
    barmode="overlay",
    title="Gaming Hours Distribution"
)

    fig_gaming.update_layout(
    xaxis_title="Gaming Hours",
    yaxis_title="Number of Students"
)

    st.plotly_chart(fig_gaming, use_container_width=True)
    corr = fdf["gaming_hours"].corr(fdf["grades"])

    st.warning(
    f"""
🎮 Correlation with Grades: {corr:.2f}

Most students spend between 2–6 hours gaming daily.

Students with higher gaming hours tend to show slightly lower academic performance.
"""
)
    st.markdown("---")

    # ------------------------------------------
    # Study & Sleep
    # ------------------------------------------

    col3,col4 = st.columns(2)

    with col3:

        fig = px.scatter(
            fdf,
            x="study_hours",
            y="grades",
            color="gender",
            title="Study Hours vs Grades"
        )
        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.success(f"""
📌 Academic Insight

Average Study Hours: {round(fdf['study_hours'].mean(),2)}

Students dedicating more time to study tend to achieve
consistently higher grades.

The upward trend indicates a strong positive relationship
between study effort and academic performance.

Students studying above the average range are more likely
to score in the high-performance category.
""")

    with col4:

        fig = px.box(
                fdf,
                x="stress_level",
                y="sleep_hours",
                color="stress_level",
                title="Sleep Hours by Stress Level"
         )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.info(f"""
📌 Sleep Analysis

Average Sleep Hours: {round(fdf['sleep_hours'].mean(),2)}

Students experiencing high stress typically report
lower sleep duration.

Low and Medium stress groups demonstrate healthier
sleep patterns compared to highly stressed students.

Maintaining adequate sleep can improve concentration,
memory retention and classroom engagement.
""")

    st.markdown("---")

    # ------------------------------------------
    # Stress Distribution
    # ------------------------------------------

    fig = px.histogram(
        fdf,
        x="stress_level",
        color="stress_level",
        title="Stress Level Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.warning(f"""
📌 Stress Distribution Insight

Most students fall within the Medium Stress category.

A smaller proportion experience High Stress levels,
which may negatively influence academic outcomes.

Monitoring stress and promoting wellness initiatives
can help improve student performance and engagement.
""")

# ==================================================
# GAMING INTELLIGENCE
# ==================================================

elif page == "🎮 Gaming Intelligence":

    st.subheader("🎮 Gaming Intelligence")

    st.info("""
Analyze how gaming behaviour,
device usage and addiction influence grades.
""")

    # ------------------------------------------
    # Gaming Hours vs Grades
    # ------------------------------------------

    fig = px.scatter(
        fdf,
        x="gaming_hours",
        y="grades",
        color="stress_level",
        size="addiction_score",
        hover_data=["gaming_genre"],
        title="Gaming Hours vs Grades"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.warning("""
📌 Insight

Students who spend more hours gaming
often achieve lower grades.
               
The downward trend suggests excessive
gaming negatively affects performance.
""")

    # ------------------------------------------
    # Addiction Score vs Grades
    # ------------------------------------------

    fig = px.scatter(
        fdf,
        x="addiction_score",
        y="grades",
        color="gender",
        title="Gaming Addiction vs Academic Performance"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.warning("""
📌 Insight

Higher addiction scores generally
correspond to weaker academic outcomes.
""")

    # ------------------------------------------
    # Device Usage vs Grades
    # ------------------------------------------

    fig = px.scatter(
        fdf,
        x="device_usage",
        y="grades",
        color="stress_level",
        title="Device Usage vs Grades"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.info("""
📌 Insight

Excessive device usage may reduce
focus on academic activities.
""")

    # ------------------------------------------
    # Gaming Hours by Stress Level
    # ------------------------------------------

    fig = px.box(
        fdf,
        x="stress_level",
        y="gaming_hours",
        color="stress_level",
        title="Gaming Hours by Stress Level"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.warning("""
📌 Insight

Students experiencing higher stress
often spend more time gaming.
""")

    # ------------------------------------------
    # Gaming Genre Analysis
    # ------------------------------------------

    st.subheader("🎮 Gaming Genre Analysis")

    genre_df = (
        fdf.groupby("gaming_genre")["grades"]
        .mean()
        .reset_index()
        .sort_values(
            by="grades",
            ascending=False
        )
    )

    fig = px.bar(
        genre_df,
        x="gaming_genre",
        y="grades",
        color="grades",
        title="Average Grades by Gaming Genre"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.success("""
📌 Insight

Different gaming genres show
different relationships with
academic performance.
""")
    st.subheader("🎮 Gaming Impact Analysis")

    fig = px.scatter(
        fdf,
        x="gaming_hours",
        y="grades",
        size="addiction_score",
        color="stress_level",
        hover_data=["gaming_genre"]
     )

    st.plotly_chart(
    fig,
    use_container_width=True
)

    st.warning(""" Higher gaming addiction scores are associated with lower grades.""") 
# ==================================================
# LIFESTYLE INTELLIGENCE
# ==================================================

elif page == "🧠 Lifestyle Intelligence":

    st.subheader("🧠 Lifestyle Intelligence")

    st.info("""
Analyze how study habits, sleep quality,
attendance and stress influence
student academic performance.
""")

    # ------------------------------------------
    # Study Hours vs Grades
    # ------------------------------------------

    col1,col2 = st.columns(2)

    with col1:

        fig = px.scatter(
            fdf,
            x="study_hours",
            y="grades",
            color="stress_level",
            title="Study Hours vs Grades"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.success(""" Students who study more generally achieve higher grades.""")

    # ------------------------------------------
    # Sleep Hours vs Grades
    # ------------------------------------------

    with col2:

        fig = px.scatter(
            fdf,
            x="sleep_hours",
            y="grades",
            color="gender",
            title="Sleep Hours vs Grades"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.info("""
📌 Insight

Adequate sleep improves concentration
and academic performance.
""")

    st.markdown("---")

    # ------------------------------------------
    # Attendance vs Grades
    # ------------------------------------------

    col3,col4 = st.columns(2)

    with col3:

        fig = px.scatter(
            fdf,
            x="attendance",
            y="grades",
            color="stress_level",
            title="Attendance vs Grades"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.success("""
📌 Insight

Students with higher attendance
tend to score better grades.
""")

    # ------------------------------------------
    # Study vs Sleep
    # ------------------------------------------

    with col4:

        fig = px.scatter(
            fdf,
            x="study_hours",
            y="sleep_hours",
            color="stress_level",
            title="Study Hours vs Sleep Hours"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.info("""
📌 Insight

Balanced study and sleep patterns
support better academic outcomes.
""")

    st.markdown("---")

    # ------------------------------------------
    # Sleep vs Stress
    # ------------------------------------------

    fig = px.box(
        fdf,
        x="stress_level",
        y="sleep_hours",
        color="stress_level",
        title="Sleep Hours by Stress Level"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.warning("""
📌 Insight

Students with high stress levels
often report lower sleep duration.
""")

    # ------------------------------------------
    # Lifestyle Summary
    # ------------------------------------------

    st.subheader("🏆 Lifestyle Findings")

    st.success("""
✓ Consistent study habits improve grades
✓ Adequate sleep supports learning
✓ Attendance contributes to success
✓ Balanced lifestyles produce stronger outcomes
""")

# ==================================================
# ADVANCED ANALYTICS
# ==================================================

elif page == "📈 Statistical Insights":

    # st.subheader("🔬 Advanced Analytics & Academic Intelligence")

    st.info("""
Explore advanced statistical analysis,
correlations and grouped insights.
""")

    # ------------------------------------------
    # Correlation Heatmap
    # ------------------------------------------

    st.subheader("🔥 Correlation Analysis")

    corr = fdf.corr(numeric_only=True)

# -----------------------------
# KPI CARDS
# -----------------------------

    c1,c2,c3,c4 = st.columns(4)

    c1.metric(
    "📚 Strongest Positive",
    "Study Hours",
    "+0.73"
)

    c2.metric(
    "🎮 Strongest Negative",
    "Gaming Hours",
    "-0.55"
)

    c3.metric(
    "😴 Sleep Impact",
    "Moderate",
    "+0.25"
)

    c4.metric(
    "🏫 Attendance Impact",
    "Positive",
    "+0.13"
)

    st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------
# HEATMAP FULL WIDTH
# -----------------------------

    fig, ax = plt.subplots(figsize=(8,5))

    sns.heatmap(
    corr,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    linewidths=0.5,
    annot_kws={"size":7,"weight":"normal"},
    ax=ax)

    plt.title(
    "Correlation Matrix of Academic Performance Factors",
    fontsize=12,
    fontweight="normal"
   )
    plt.xticks(
    fontsize=8,
    rotation=45
   )

    plt.yticks(
        fontsize=8
    )

    st.pyplot(fig)

# -----------------------------
# CORRELATION TABLE
# -----------------------------

    st.markdown("### 📊 Correlation Ranking")

    corr_rank = (
    corr["grades"]
    .sort_values(ascending=False)
    .reset_index()
)

    corr_rank.columns = [
    "Feature",
    "Correlation"
]

    st.dataframe(
    corr_rank,
    use_container_width=True,
    height=400
)

    summary_box(
    "📌 Executive Correlation Insight",
    f"""
    Study Hours show the strongest positive relationship
    with grades ({corr.loc['study_hours','grades']:.2f}).

    Gaming Hours ({corr.loc['gaming_hours','grades']:.2f})
    and Addiction Score ({corr.loc['addiction_score','grades']:.2f})
    negatively impact academic outcomes.

    Sleep Hours and Attendance contribute positively,
    highlighting the importance of balanced student lifestyles.

    Overall, academic success appears to be driven more by
    study behaviour and healthy routines than demographic factors.
    """,
    "#2563EB"
)

    st.markdown("---")

    # ------------------------------------------
    # Top Positive Factors
    # ------------------------------------------

    st.subheader("🏆 Top Positive Factors")

    positive_corr = (
        corr["grades"]
        .sort_values(
            ascending=False
        )
        .reset_index()
    )

    top_positive = (
    positive_corr
    .head(5)
    )

    fig = px.bar(
        top_positive,
        x="grades",
        y="index",
        orientation="h",
        # title="Top Positive Academic Drivers",
        color="grades"
    )

    st.plotly_chart(fig,use_container_width=True)

    summary_box(
    "🏆 Key Academic Drivers",
    """
    Study Hours emerge as the strongest academic success factor.

    Students maintaining consistent study routines,
    adequate sleep and strong attendance records
    generally achieve higher academic performance.

    These variables represent actionable areas
    for improving student outcomes.
    """,
    "#22C55E"
)
    # ------------------------------------------
    # Top Negative Factors
    # ------------------------------------------

    st.subheader("⚠ Top Negative Factors")

    negative_corr = (
        corr["grades"]
        .sort_values()
        .reset_index()
    )

    top_negative = (
    negative_corr
    .head(5)
   )

    fig = px.bar(
        top_negative,
        x="grades",
        y="index",
        orientation="h",
         color="grades",
         text_auto=".2f",
          color_continuous_scale="Reds"
) 

    fig.update_layout(
       height=350
)
    st.plotly_chart(fig,use_container_width=True)
    summary_box(
    "⚠ Academic Risk Factors",
    """
    Gaming Hours and Addiction Score demonstrate
    the strongest negative impact on grades.

    Excessive device usage may also contribute to
    reduced academic focus and productivity.

    Addressing these factors can significantly
    improve student performance.
    """,
    "#DC2626"
)

    st.markdown("---")

    # ------------------------------------------
    # GroupBy Analysis
    # ------------------------------------------

    st.subheader("📊 GroupBy Analysis")

    tab1,tab2,tab3 = st.tabs(
        [
            "Gender Analysis",
            "Genre Analysis",
            "Stress Analysis"
        ]
    )

    with tab1:

        gender_df = (
            fdf.groupby("gender")["grades"]
            .mean()
            .reset_index()
        )
        best_gender = gender_df.loc[
           gender_df["grades"].idxmax(),
           "gender"
           ]
        fig_gender = px.bar(
        gender_df,
        x="gender",
        y="grades",
        color="grades",
        text_auto=".1f",
        color_continuous_scale="Blues"
    )
        fig_gender.update_layout(
        height=350,
        showlegend=False
    )

        st.plotly_chart(
        fig_gender,
        use_container_width=True
    )

    #     col1,col2 = st.columns([3,1])

    #     with col1:
    #        st.plotly_chart(
    #         fig_gender,
    #         use_container_width=True,
    #         key="gender_bar"
    #     )


    #     with col2:
    #        st.metric(
    #         "Top Performing Gender",
    #         best_gender
    #     )

    #     fig = px.bar(
    #        gender_df,
    #        x="gender",
    #        y="grades",
    #        color="grades",
    #        text_auto=".1f",
    #        color_continuous_scale="Blues"
    # )
    #     st.plotly_chart(
    #         fig,
    #         use_container_width=True
    #     )
        summary_box(
    "👨 Gender Analysis",
    f"""
    {best_gender} students recorded the highest average grade.

    Performance differences across genders are relatively small,
    suggesting gender has limited influence on academic outcomes.

    Study habits and attendance appear to be stronger predictors.
    """,
    "#2563EB"
)

    with tab2:

        genre_df = (
            fdf.groupby("gaming_genre")["grades"]
            .mean()
            .reset_index()
        )

        st.dataframe(
            genre_df,
            use_container_width=True
        )

        fig = px.bar(
    genre_df,
    x="gaming_genre",
    y="grades",
    color="grades",
    text_auto=".1f",
    color_continuous_scale="Viridis"
)

        st.plotly_chart(
            fig,
            use_container_width=True
        )
        best_genre = genre_df.loc[
            genre_df["grades"].idxmax(),
           "gaming_genre"
         ]

        summary_box(
    "🎮 Genre Analysis",
    f"""
    {best_genre} players achieved the highest average grades.

    However, differences between genres are relatively small.

    Gaming duration and addiction levels appear more influential
    than the specific genre played.
    """,
    "#22C55E"
    )

    with tab3:

        stress_df = (
            fdf.groupby("stress_level")["grades"]
            .mean()
            .reset_index()
        )

        st.dataframe(
            stress_df,
            use_container_width=True
        )

        fig = px.bar(
    stress_df,
    x="stress_level",
    y="grades",
    color="grades",
    text_auto=".1f",
    color_continuous_scale="RdYlGn"
)

        st.plotly_chart(
            fig,
            use_container_width=True
        )
        st.success(
f"Highest grades are observed in {stress_df.loc[stress_df['grades'].idxmax(),'stress_level']} stress group."
)
        best_stress = stress_df.loc[
            stress_df["grades"].idxmax(),
           "stress_level"
]

        summary_box(
    "😌 Stress Analysis",
    f"""
    Students with {best_stress} stress levels achieved
    the highest academic performance.

    High stress groups generally show lower average grades
    and reduced sleep duration.

    Maintaining healthy stress levels can improve learning
    outcomes and concentration.
    """,
    "#DC2626"
)

        st.markdown("---")

    # ------------------------------------------
    # Crosstab Analysis
    # ------------------------------------------
    st.markdown("---")
    st.subheader("📋 Crosstab Analysis")
    col1, col2 = st.columns(2)

    with col1:
        gender_ct = pd.crosstab(
        fdf["gender"],
        fdf["grade_category"]
    ).reset_index()

        fig = px.bar(
        gender_ct,
        x="gender",
        y=["Poor","Average","Excellent"],
        title="Gender vs Performance"
    )

        fig.update_layout(height=350)

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        stress_ct = pd.crosstab(
          fdf["stress_level"],
          fdf["grade_category"]
    ).reset_index()

        fig = px.bar(
          stress_ct,
        x="stress_level",
        y=["Poor","Average","Excellent"],
        title="Stress vs Performance"
    )

        fig.update_layout(height=350)

        st.plotly_chart(fig, use_container_width=True)
    # ------------------------------------------
    # Pivot Table
    # ------------------------------------------
    st.markdown("---")
    st.subheader("📌 Pivot Analysis")

    pivot = pd.pivot_table(
        fdf,
        values="grades",
        index="gaming_genre",
        columns="gender",
        aggfunc="mean"
    )

    fig = px.imshow(
        pivot,
        text_auto=".1f",
        color_continuous_scale="Viridis"
)

    fig.update_layout(
        title="Performance by Gaming Genre & Gender"
    )

    st.plotly_chart(
         fig,
         use_container_width=True
)
    with st.expander("View Pivot Table"):
        st.dataframe(
            pivot,
        use_container_width=True
    )

    summary_box(
    "📌 Pivot Analysis Insight",
    """
    Academic performance remains relatively consistent
    across gaming genres and gender groups.

    Small differences suggest that personal study habits,
    attendance and sleep patterns have a greater impact
    on grades than gaming genre preferences.

    This analysis helps identify interaction effects
    between multiple student characteristics.
    """,
    "#8B5CF6"
)
    # ==================================================
# RECOMMENDATIONS & PREDICTOR
# ==================================================

elif page == "🎯 Key Findings":

    # st.header("🎯 Key Findings & Insights")

    avg_gaming = fdf["gaming_hours"].mean()
    avg_study = fdf["study_hours"].mean()
    avg_sleep = fdf["sleep_hours"].mean()
    avg_attendance = fdf["attendance"].mean()

    # =====================================
    # KPI SUMMARY
    # =====================================
    # st.markdown("---")

    # st.subheader("📊 Student Lifestyle Snapshot")

    # c1,c2,c3,c4 = st.columns(4)

    # c1.metric(
    #     "🎮 Gaming",
    #     f"{avg_gaming:.1f} hrs/day"
    # )

    # c2.metric(
    #     "📚 Study",
    #     f"{avg_study:.1f} hrs/day"
    # )

    # c3.metric(
    #     "😴 Sleep",
    #     f"{avg_sleep:.1f} hrs/day"
    # )

    # c4.metric(
    #     "🏫 Attendance",
    #     f"{avg_attendance:.1f}%"
    # )

    st.markdown("---")

    # =====================================
    # KEY FINDINGS
    # =====================================

    st.subheader("🏆 Executive Insights")

    col1,col2,col3 = st.columns(3)

    with col1:

        st.markdown("""
        <div class='insight-card study-card'>
        <h3>📚 Academic Drivers</h3>

        <ul>
        <li>Study hours strongly improve grades</li>
        <li>Attendance positively impacts performance</li>
        <li>Balanced routines increase success rate</li>
        </ul>

        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown("""
        <div class='insight-card gaming-card'>
        <h3>🎮 Academic Risks</h3>

        <ul>
        <li>High gaming hours reduce grades</li>
        <li>Addiction affects learning outcomes</li>
        <li>Poor sleep impacts concentration</li>
        </ul>

        </div>
        """, unsafe_allow_html=True)

    with col3:

        st.markdown(f"""
        <div class='insight-card sleep-card'>
        <h3>📊 Student Snapshot</h3>

        🎮 Gaming : {avg_gaming:.1f} hrs/day<br>
        📚 Study : {avg_study:.1f} hrs/day<br>
        😴 Sleep : {avg_sleep:.1f} hrs/day<br>
        🏫 Attendance : {avg_attendance:.1f}%<br>

        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # =====================================
    # FINAL CONCLUSION
    # =====================================

    st.markdown("""
<div style="
    background:linear-gradient(135deg,#F5F9FF,#EAF2FF);
    padding:25px;
    border-radius:18px;
    border-left:8px solid #2563EB;
    margin-top:15px;
">

<h2 style="
    color:#1E40AF;
    margin-bottom:20px;
">
🏆 Executive Conclusions
</h2>

<ul style="
    font-size:18px;
    line-height:2;
    color:#1F2937;
">

<li>📚 Study Hours remain the strongest driver of academic success.</li>

<li>😴 Better Sleep Quality improves concentration and academic performance.</li>

<li>🎮 Excessive Gaming Hours and addiction negatively impact grades.</li>

<li>🏫 Attendance is a critical predictor of student achievement.</li>

<li>⚖️ Students maintaining balanced lifestyles consistently perform better academically.</li>

</ul>

</div>
""", unsafe_allow_html=True)
    # ------------------------------------------
    # STUDENT PERFORMANCE SIMULATOR
    # ------------------------------------------

elif page == "🧠 Performance Predictor":

    st.header("🧠 Academic Performance Predictor")

    st.info(
        "Adjust lifestyle factors and observe their impact on expected academic performance."
    )

    col1, col2 = st.columns([1,1])

    with col1:

        gaming = st.slider(
            "🎮 Gaming Hours",
            0, 10, 4
        )

        study = st.slider(
            "📚 Study Hours",
            0, 12, 5
        )

        sleep = st.slider(
            "😴 Sleep Hours",
            4, 10, 7
        )

        attendance = st.slider(
            "🏫 Attendance %",
            0, 100, 80
        )

    # ==========================================
    # PREDICTION MODEL
    # ==========================================

    predicted_score = (
        0.35 * study +
        0.25 * (attendance / 10) +
        0.20 * sleep -
        0.15 * gaming
    )

    predicted_score = max(
        0,
        min(predicted_score * 10, 100)
    )

    if predicted_score >= 85:
        category = "🟢 Excellent"
    elif predicted_score >= 65:
        category = "🔵 Good"
    elif predicted_score >= 50:
        category = "🟡 Average"
    else:
        category = "🔴 Needs Improvement"

    with col2:

        st.metric(
            "🎯 Predicted Score",
            f"{predicted_score:.1f}/100"
        )

        st.metric(
            "Performance Category",
            category
        )

        st.progress(int(predicted_score))

    st.markdown("---")

    # ==========================================
    # FACTOR ANALYSIS
    # ==========================================

    st.subheader("📊 Lifestyle Factor Analysis")

    factor_df = pd.DataFrame({
        "Factor": [
            "Gaming",
            "Study",
            "Sleep",
            "Attendance"
        ],
        "Value": [
            gaming,
            study,
            sleep,
            attendance
        ]
    })

    fig = px.bar(
        factor_df,
        x="Factor",
        y="Value",
        color="Factor",
        text="Value"
    )

    fig.update_layout(
        height=400,
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("---")

    # ==========================================
    # STUDENT PROFILE
    # ==========================================

    st.subheader("👤 Student Profile")

    if predicted_score >= 85:

        st.success(
            "🌟 High Achiever — Strong academic habits and excellent performance potential."
        )

    elif predicted_score >= 65:

        st.info(
            "📘 Consistent Learner — Good performance with room for improvement."
        )

    elif predicted_score >= 50:

        st.warning(
            "⚠ Developing Student — Academic habits need strengthening."
        )

    else:

        st.error(
            "🚨 At-Risk Student — Immediate lifestyle improvements recommended."
        )

    st.markdown("---")

    # ==========================================
    # SMART RECOMMENDATIONS
    # ==========================================

    st.subheader("🎯 Smart Academic Recommendations")

    recommendations = []

    # Gaming

    if gaming <= 3:
        recommendations.append(
            "🎮 Gaming habits are well balanced."
        )

    elif gaming <= 6:
        recommendations.append(
            "🎮 Moderate gaming detected. Maintain a healthy balance."
        )

    else:
        recommendations.append(
            "🎮 Consider reducing gaming hours to improve academic focus."
        )

    # Study

    if study >= 8:
        recommendations.append(
            "📚 Excellent study commitment. Keep it up!"
        )

    elif study >= 5:
        recommendations.append(
            "📚 Study habits are healthy and support good performance."
        )

    else:
        recommendations.append(
            "📚 Increasing study time by 1–2 hours daily may improve results."
        )

    # Sleep

    if sleep >= 8:
        recommendations.append(
            "😴 Sleep quality appears excellent."
        )

    elif sleep >= 7:
        recommendations.append(
            "😴 Sleep duration is within the recommended range."
        )

    else:
        recommendations.append(
            "😴 Aim for at least 7–8 hours of sleep for better concentration."
        )

    # Attendance

    if attendance >= 90:
        recommendations.append(
            "🏫 Outstanding attendance record."
        )

    elif attendance >= 80:
        recommendations.append(
            "🏫 Attendance is satisfactory."
        )

    else:
        recommendations.append(
            "🏫 Improving attendance can significantly enhance performance."
        )

    for rec in recommendations:
        st.info(rec)

    st.markdown("---")

    # ==========================================
    # IMPROVEMENT POTENTIAL
    # ==========================================

    st.subheader("🚀 Improvement Potential")

    potential_score = min(
        100,
        predicted_score + 15
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Current Score",
            f"{predicted_score:.1f}/100"
        )

    with col2:

        st.metric(
            "Potential Score",
            f"{potential_score:.1f}/100"
        )

    st.success(
        "Small improvements in study habits, sleep quality, attendance, and gaming balance can significantly improve academic outcomes."
    )

# ==================================================
# FINAL EXECUTIVE CONCLUSION
# ==================================================

    st.markdown("---")
elif page == "💡 Recommendations":

    st.header("💡 Strategic Insights & Recommendations")

    avg_grade = round(fdf["grades"].mean(),2)
    avg_gaming = round(fdf["gaming_hours"].mean(),2)
    avg_study = round(fdf["study_hours"].mean(),2)
    avg_sleep = round(fdf["sleep_hours"].mean(),2)

    # KPI CARDS

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("🎓 Avg Grade", avg_grade)
    c2.metric("🎮 Avg Gaming", avg_gaming)
    c3.metric("📚 Avg Study", avg_study)
    c4.metric("😴 Avg Sleep", avg_sleep)

    st.markdown("---")

    st.subheader("📌 Executive Observation")

    st.info(f"""
The analysis of {len(fdf):,} students indicates that academic performance is strongly influenced by study habits,
sleep quality, attendance, stress levels, and gaming behavior.

Students with balanced lifestyles consistently achieve better academic outcomes.
""")

    st.subheader("🔍 Key Findings")

    col1,col2 = st.columns(2)

    with col1:

        st.success("""
### Strengths

✔ Healthy average study duration

✔ Strong attendance levels

✔ Majority maintain moderate stress

✔ Balanced sleep patterns
""")

    with col2:

        st.warning("""
### Areas of Concern

⚠ Excessive gaming among some students

⚠ High addiction scores

⚠ Increased stress impacts grades

⚠ Device overuse observed
""")

    st.markdown("---")

    st.subheader("🎯 Priority Recommendations")

    rec1,rec2 = st.columns(2)

    with rec1:

        st.success("""
### Immediate Actions

📚 Increase daily study hours

😴 Maintain 7–8 hours sleep

🏫 Improve attendance consistency

🎮 Limit gaming to healthy levels
""")

    with rec2:

        st.info("""
### Long-Term Strategies

🧠 Mental wellness programs

📖 Structured learning plans

🎯 Goal-based performance tracking

👨‍🏫 Student mentoring initiatives
""")

    st.markdown("---")

    st.subheader("⚖ SWOT Analysis")

    sw1,sw2 = st.columns(2)

    with sw1:

        st.success("""
### Strengths

• Good study habits

• Strong attendance

• Healthy sleep patterns
""")

        st.info("""
### Opportunities

• Personalized learning plans

• Academic counseling

• Gamified learning platforms
""")

    with sw2:

        st.warning("""
### Weaknesses

• Gaming addiction

• Stress imbalance

• Device dependency
""")

        st.error("""
### Threats

• Academic decline

• Reduced concentration

• Sleep deprivation
""")

    st.markdown("---")

    st.subheader("🏆 Final Conclusion")

    if avg_grade >= 75:

        st.success("""
The student population demonstrates strong academic performance.
Current lifestyle habits are generally supportive of educational success.
""")

    elif avg_grade >= 60:

        st.warning("""
Academic performance is moderate.
Targeted improvements in study habits and gaming control can significantly improve outcomes.
""")

    else:

        st.error("""
Academic performance is below expectations.
Immediate interventions in gaming behavior, study schedules, and wellness practices are recommended.
""")
        st.markdown("""
<div style="
    background: linear-gradient(135deg,#F5F9FF,#EAF2FF);
    padding:25px;
    border-radius:18px;
    border-left:8px solid #2563EB;
">

<h2>🏆 Executive Conclusions</h2>

• Study Hours remain the strongest driver of academic success.

• Better Sleep Quality improves concentration and performance.

• Excessive Gaming Hours negatively impact grades.

• Attendance is a critical predictor of achievement.

</div>
""", unsafe_allow_html=True)

# ==================================================
# FOOTER
# ==================================================

