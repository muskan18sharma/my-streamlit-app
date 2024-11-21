import streamlit as st
import pandas as pd
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_csv('data/youth_smoking_drug_data_10000_rows_expanded.csv')

# Introduction
st.title("Youth Smoking & Drug Use: Uncovering Trends and Insights")
st.write("""
This interactive data visualization app examines patterns in youth smoking and drug use.
Explore relationships between various factors like age, gender, socioeconomic status, mental health, and peer influence.
""")

# Sidebar Controls
st.sidebar.subheader("Select Chart Type")
chart_type = st.sidebar.selectbox("Select Chart", 
                                  ("Line Chart", "Bar Chart", "Pie Chart", "Box Plot", "Heatmap", "Histogram", "Scatter Plot"))
show_all_charts = st.sidebar.checkbox("Show All Charts")
year_slider = st.slider("Select Year Range", 
                        min_value=int(data['Year'].min()), 
                        max_value=int(data['Year'].max()), 
                        value=(int(data['Year'].min()), int(data['Year'].max())))

# Filter the data based on the selected year range
filtered_data = data[(data['Year'] >= year_slider[0]) & (data['Year'] <= year_slider[1])]

# Function to display all charts
def display_all_charts():
    # Line Chart
    st.subheader("Line Chart: Smoking Prevalence Over Time")
    line_chart = alt.Chart(filtered_data).mark_line().encode(
        x='Year:O',
        y='Smoking_Prevalence:Q',
        color='Gender:N'
    ).properties(width=700, height=400)
    st.altair_chart(line_chart)

    # Bar Chart
    st.subheader("Bar Chart: Smoking Prevalence by Age Group")
    age_group_bar = filtered_data.groupby('Age_Group')['Smoking_Prevalence'].mean().reset_index()
    bar_chart = alt.Chart(age_group_bar).mark_bar().encode(
        x='Age_Group:O',
        y='Smoking_Prevalence:Q',
        color='Age_Group:N'
    ).properties(width=700, height=400)
    st.altair_chart(bar_chart)

    # Box Plot
    st.subheader("Box Plot: Drug Experimentation Distribution by Age Group")
    box_plot = alt.Chart(filtered_data).mark_boxplot().encode(
        x='Age_Group:O',
        y='Drug_Experimentation:Q',
        color='Age_Group:N'
    ).properties(width=700, height=400)
    st.altair_chart(box_plot)

    # Pie Chart
    st.subheader("Pie Chart: Gender Distribution")
    gender_data = filtered_data['Gender'].value_counts().reset_index()
    gender_data.columns = ['Gender', 'Count']
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(gender_data['Count'], labels=gender_data['Gender'], autopct='%1.1f%%', startangle=90, 
           colors=sns.color_palette('Set3', len(gender_data)))
    ax.axis('equal')
    st.pyplot(fig)

    # Heatmap
    st.subheader("Heatmap: Peer Influence vs Smoking Prevalence")
    heatmap_data = filtered_data.groupby(['Year', 'Peer_Influence'])['Smoking_Prevalence'].mean().reset_index()
    heatmap_pivot = heatmap_data.pivot(index='Year', columns='Peer_Influence', values='Smoking_Prevalence')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(heatmap_pivot, annot=True, cmap="YlGnBu", ax=ax, linewidths=0.5)
    st.pyplot(fig)

    # Histogram
    st.subheader("Histogram: Mental Health vs Drug Experimentation")
    hist = alt.Chart(filtered_data).mark_bar().encode(
        x=alt.X('Mental_Health:Q', bin=True),
        y='count():Q',
        color='Gender:N'
    ).properties(width=700, height=400)
    st.altair_chart(hist)

    # Scatter Plot
    st.subheader("Scatter Plot: Age Group vs Peer Influence")
    scatter_plot = alt.Chart(filtered_data).mark_point().encode(
        x='Age_Group:O',
        y='Peer_Influence:Q',
        color='Gender:N',
        tooltip=['Age_Group', 'Peer_Influence', 'Gender']
    ).properties(width=700, height=400)
    st.altair_chart(scatter_plot)

# Show charts based on user selection
if show_all_charts:
    display_all_charts()
else:
    if chart_type == "Line Chart":
        st.subheader("Line Chart: Smoking Prevalence Over Time")
        line_chart = alt.Chart(filtered_data).mark_line().encode(
            x='Year:O',
            y='Smoking_Prevalence:Q',
            color='Gender:N'
        ).properties(width=700, height=400)
        st.altair_chart(line_chart)

    elif chart_type == "Bar Chart":
        st.subheader("Bar Chart: Smoking Prevalence by Age Group")
        age_group_bar = filtered_data.groupby('Age_Group')['Smoking_Prevalence'].mean().reset_index()
        bar_chart = alt.Chart(age_group_bar).mark_bar().encode(
            x='Age_Group:O',
            y='Smoking_Prevalence:Q',
            color='Age_Group:N'
        ).properties(width=700, height=400)
        st.altair_chart(bar_chart)

    elif chart_type == "Pie Chart":
        st.subheader("Pie Chart: Gender Distribution")
        gender_data = filtered_data['Gender'].value_counts().reset_index()
        gender_data.columns = ['Gender', 'Count']
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie(gender_data['Count'], labels=gender_data['Gender'], autopct='%1.1f%%', startangle=90, 
               colors=sns.color_palette('Set3', len(gender_data)))
        ax.axis('equal')
        st.pyplot(fig)

    elif chart_type == "Box Plot":
        st.subheader("Box Plot: Drug Experimentation Distribution by Age Group")
        box_plot = alt.Chart(filtered_data).mark_boxplot().encode(
            x='Age_Group:O',
            y='Drug_Experimentation:Q',
            color='Age_Group:N'
        ).properties(width=700, height=400)
        st.altair_chart(box_plot)

    elif chart_type == "Heatmap":
        st.subheader("Heatmap: Peer Influence vs Smoking Prevalence")
        heatmap_data = filtered_data.groupby(['Year', 'Peer_Influence'])['Smoking_Prevalence'].mean().reset_index()
        heatmap_pivot = heatmap_data.pivot(index='Year', columns='Peer_Influence', values='Smoking_Prevalence')
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(heatmap_pivot, annot=True, cmap="YlGnBu", ax=ax, linewidths=0.5)
        st.pyplot(fig)

    elif chart_type == "Histogram":
        st.subheader("Histogram: Mental Health vs Drug Experimentation")
        hist = alt.Chart(filtered_data).mark_bar().encode(
            x=alt.X('Mental_Health:Q', bin=True),
            y='count():Q',
            color='Gender:N'
        ).properties(width=700, height=400)
        st.altair_chart(hist)

    elif chart_type == "Scatter Plot":
        st.subheader("Scatter Plot: Age Group vs Peer Influence")
        scatter_plot = alt.Chart(filtered_data).mark_point().encode(
            x='Age_Group:O',
            y='Peer_Influence:Q',
            color='Gender:N',
            tooltip=['Age_Group', 'Peer_Influence', 'Gender']
        ).properties(width=700, height=400)
        st.altair_chart(scatter_plot)

# Conclusion
st.write("""
### Conclusion:
Insights from this analysis reveal patterns in youth smoking and drug use, highlighting key influences such as age, gender, peer pressure, and mental health.
""")

   
