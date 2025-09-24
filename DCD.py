import plotly.express as px
import streamlit as st
import pandas as pd
import pycountry

st.set_page_config(
    page_title="The Global Death Report",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

df = pd.read_csv("Global Disease Deaths.csv")

st.markdown("""
    <style>
        .title {
            font-size: 45px;
            font-weight: bold;
            color: #FF4C4C;
            text-align: center;
            text-shadow: 2px 2px 8px rgba(255, 76, 76, 0.4);
        }
        .subtitle {
            font-size: 18px;
            color: #666;
            text-align: center;
        }
    </style>
    <div class="title">📊 The Global Death Report</div>
    <div class="subtitle">Uncovering trends and causes of global mortality (1990 - 2019)</div>
    <br>
""", unsafe_allow_html=True)

st.image(
    "https://images.unsplash.com/photo-1584036561566-baf8f5f1b144",
    use_container_width=True,
    caption="Global Health & Mortality Trends"
)

st.sidebar.markdown("""
    <style>
        .sidebar-title {
            font-size: 20px;
            font-weight: bold;
            color: #FF4C4C;
        }
    </style>
    <div class="sidebar-title">🌍 Country Selection</div>
""", unsafe_allow_html=True)

unique_countries = df["Country/Territory"].unique()
selected_country = st.sidebar.selectbox("Select Country", sorted(unique_countries))

filter_df = df[df["Country/Territory"] == selected_country]

def get_country_code(country_name):
    try:
        return pycountry.countries.lookup(country_name).alpha_2.lower()
    except LookupError:
        return None  

country_code = get_country_code(selected_country)
if country_code:
    st.sidebar.image(f"https://flagcdn.com/w320/{country_code}.png", width=150)
else:
    st.sidebar.write("⚠️ Flag not available")

st.sidebar.markdown('<div class="sidebar-title">⚰️ Causes of Death</div>', unsafe_allow_html=True)
remaining_column_names = df.columns[3:-3]
selected_cause = st.sidebar.selectbox("Choose Cause", remaining_column_names)

st.sidebar.markdown('<div class="sidebar-title">📊 Graphs</div>', unsafe_allow_html=True)

# Death Trend Over Years
with st.expander("📉 Death Trend Over Years", expanded=False):
    if st.checkbox("Show Trend Graph", key="trend"):
        fig = px.scatter(
            filter_df, x="Year", y="Total_Deaths",
            title=f"Death Trend in {selected_country}",
            color_discrete_sequence=["#1f77b4"],
            template="plotly_white"
        )
        fig.add_scatter(x=filter_df["Year"], y=filter_df["Total_Deaths"], 
                        mode='lines', line=dict(color="#FF4C4C"))
        st.plotly_chart(fig, use_container_width=True)

# Deaths by Cause
with st.expander("📊 Deaths by Cause", expanded=False):
    if st.checkbox("Show Deaths by Cause", key="cause"):
        if selected_cause in df.columns:
            filter_cause_df = filter_df[["Year", selected_cause]]
            fig_bar = px.bar(
                filter_cause_df, x="Year", y=selected_cause,
                title=f"Total Deaths due to {selected_cause} in {selected_country}",
                color=selected_cause,
                template="plotly_white"
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.warning(f"No data available for {selected_cause}")

#Gender-Based Deaths
with st.expander("👫 Gender-Based Deaths", expanded=False):
    if st.checkbox("Show Gender Comparison", key="gender"):
        option = st.radio("Select Gender:", ["Female Deaths", "Male Deaths"], horizontal=True)
        if option == "Female Deaths":
            filter_df["Female_Deaths_Cause"] = (filter_df["Estimated_Female_Deaths"] / filter_df["Total_Deaths"]) * filter_df[selected_cause]
            fig_F = px.bar(
                filter_df, x="Year", y="Female_Deaths_Cause",
                title=f"Female Deaths in {selected_country} due to {selected_cause}",
                color="Female_Deaths_Cause",
                template="plotly_dark"
            )
            st.plotly_chart(fig_F, use_container_width=True)
        else:
            if selected_cause.strip() == "Maternal_Disorders":
                st.error("🚨 Oops! Maternal Disorders only affect women 🤰❌😂")
            else:
                filter_df["Male_Deaths_Cause"] = (filter_df["Estimated_Male_Deaths"] / filter_df["Total_Deaths"]) * filter_df[selected_cause]
                fig_M = px.bar(
                    filter_df, x="Year", y="Male_Deaths_Cause",
                    title=f"Male Deaths in {selected_country} due to {selected_cause}",
                    color="Male_Deaths_Cause",
                    template="seaborn"
                )
                st.plotly_chart(fig_M, use_container_width=True)

# Global Death Distribution
with st.expander("🌍 Global Death Distribution", expanded=False):
    if st.checkbox("Show Global Distribution", key="global"):
        cause_deaths = df.iloc[:, 3:-3].sum().reset_index()
        cause_deaths.columns = ["Cause", "Total_Deaths"]
        fig_total = px.pie(
            cause_deaths, names="Cause", values="Total_Deaths",
            title="🌍 Global Distribution of Deaths by Cause",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_total, use_container_width=True)

st.markdown("""
    <hr style="border:1px solid #FF4C4C">
    <div style="text-align:center; color:#666;">
        <b>Made with ❤️ by Haris</b><br>
        🔗 <a href="https://github.com/yourusername" target="_blank">GitHub</a> | 
        💼 <a href="https://linkedin.com/in/yourprofile" target="_blank">LinkedIn</a>
    </div>
""", unsafe_allow_html=True)
