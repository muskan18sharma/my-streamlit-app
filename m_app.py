import streamlit as st
import pandas as pd
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_csv('https://raw.githubusercontent.com/muskan18sharma/my-streamlit-app/refs/heads/main/youth_smoking_drug_data_10000_rows_expanded.csv')

# Introduction
st.title("Youth Smoking & Drug Use: Uncovering Trends and Insights")
st.write("""
This interactive data visualization app offers a thorough examination of data pertaining to drug use and smoking among young people. 
This app provides a dynamic method to examine important patterns in the data by employing a variety of visualization techniques, including line charts, bar charts, pie charts, scatter plots, heatmaps, and box plots. These techniques highlight the connections between various factors, including age, gender, socioeconomic status, mental health, and peer influence.
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
    st.write("""
    We can see how smoking behavior has changed over time by looking at the **line chart**, which shows the prevalence of smoking across a range of years. 
    The years are shown on the x-axis, while the smoking prevalence % is shown on the y-axis. This graphic allows us to examine trends between male and female populations by plotting statistics for each gender. 
    This graphic shows us if smoking rates have gone up, down, or stayed the same, as well as whether gender influences these patterns. The dynamic structure of the graphic provides important insights into the smoking behavior of young people by illustrating how social shifts or public health initiatives may have affected smoking rates over time.
    """)
    line_chart = alt.Chart(filtered_data).mark_line().encode(
        x='Year:O',
        y='Smoking_Prevalence:Q',
        color='Gender:N'
    ).properties(width=700, height=400)
    st.altair_chart(line_chart)

    # Bar Chart
    st.subheader("Bar Chart: Smoking Prevalence by Age Group")
    st.write("""
    The average prevalence of smoking in various age groups is shown in the **bar chart**. 
    Because it clearly compares smoking practices across various age groups, this figure is useful. The y-axis calculates the prevalence of smoking for each group, while the x-axis groups the data by age. We can easily determine which age groups are most prone to smoke by looking at this chart. For instance, smoking rates may be greater among older teenagers than among younger people, or smoking prevalence may noticeably decline among particular age groups, which may be the result of effective anti-smoking initiatives aimed at particular age groups. We can better comprehend age-related trends in smoking behavior thanks to this chart.
    """)
    age_group_bar = filtered_data.groupby('Age_Group')['Smoking_Prevalence'].mean().reset_index()
    bar_chart = alt.Chart(age_group_bar).mark_bar().encode(
        x='Age_Group:O',
        y='Smoking_Prevalence:Q',
        color='Age_Group:N'
    ).properties(width=700, height=400)
    st.altair_chart(bar_chart)

    # Box Plot
    st.subheader("Box Plot: Drug Experimentation Distribution by Age Group")
    st.write("""
    The distribution of drug experimentation among various age groups is displayed using the **box plot**. 
    It shows the minimum, first quartile, median, third quartile, and maximum values, as well as any possible outliers, to give a statistical picture of how drug experimentation differs within each group. 
    We can comprehend the range of drug experimentation behaviors and determine which age groups exhibit greater variability in drug experimentation by looking at the data spread. For instance, some age groups may exhibit wide ranges with notable outliers, indicating that some members of those age groups may be experimenting with drugs at higher or more extreme rates, while other age groups may have a tighter distribution with fewer outliers, indicating more uniform behavior.
    """)
    box_plot = alt.Chart(filtered_data).mark_boxplot().encode(
        x='Age_Group:O',
        y='Drug_Experimentation:Q',
        color='Age_Group:N'
    ).properties(width=700, height=400)
    st.altair_chart(box_plot)

    # Pie Chart
    st.subheader("Pie Chart: Gender Distribution")
    st.write("""
    The distribution of young people across various gender groups is shown simply but effectively in the **pie chart**. 
    We can observe the relative proportions of men, women, and potentially non-binary or other gender identities in the dataset by using the graphic, which divides the data into sections that correspond to each gender. 
    In addition to showing whether there is any notable skew, such as a predominance of one gender over another, this chart is essential for comprehending the gender balance within the dataset. Analyzing smoking and drug use patterns by gender may provide valuable information on gender-specific behaviors or the social influences on these habits.
    """)

    gender_data = filtered_data['Gender'].value_counts().reset_index()
    gender_data.columns = ['Gender', 'Count']
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(gender_data['Count'], labels=gender_data['Gender'], autopct='%1.1f%%', startangle=90, 
           colors=sns.color_palette('Set3', len(gender_data)))
    ax.axis('equal')
    st.pyplot(fig)

    # Heatmap
    st.subheader("Heatmap: Peer Influence vs Smoking Prevalence")
    st.write("""
    The **heatmap** illustrates the correlation between smoking prevalence over time and peer influence. 
    Peer impact levels are shown on the x-axis, while the years are shown on the y-axis. The heatmap's cells each show the average smoking prevalence for a particular year and peer influence combination. Each cell's color intensity indicates how strong this association is; darker or more intense colors signify higher levels of peer influence and smoking prevalence for a particular year. Understanding how peer influence affects smoking behaviors over time and if particular degrees of peer influence are associated with increases or decreases in smoking prevalence may be done visually with the help of this graphic. It can also show patterns, including if peer pressure increases in importance over time or whether other aspects are overshadowing it.
    """)
    heatmap_data = filtered_data.groupby(['Year', 'Peer_Influence'])['Smoking_Prevalence'].mean().reset_index()
    heatmap_pivot = heatmap_data.pivot(index='Year', columns='Peer_Influence', values='Smoking_Prevalence')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(heatmap_pivot, annot=True, cmap="YlGnBu", ax=ax, linewidths=0.5)
    st.pyplot(fig)

    # Histogram
    st.subheader("Histogram: Mental Health vs Drug Experimentation")
    st.write("""
    The distribution of mental health ratings for drug experimentation by gender is displayed in the **histogram**. 
    We plot mental health scores on the x-axis, where higher scores indicate better mental health, and the frequency of drug experimentation at each range of mental health scores is displayed on the y-axis. We may observe how mental health affects drug experimentation behaviors across genders by examining the bars that show the gender-based distribution of drug experimentation at different mental health levels. The stacked bars clearly show the differences in the experimentation habits of males and females at different levels of mental health. This graphic implies that drug experimentation may be more common among those with lower mental health scores, and gender disparities may also be seen in this context.
    """)
    hist = alt.Chart(filtered_data).mark_bar().encode(
        x=alt.X('Mental_Health:Q', bin=True),
        y='count():Q',
        color='Gender:N'
    ).properties(width=700, height=400)
    st.altair_chart(hist)

    # Scatter Plot
    st.subheader("Scatter Plot: Age Group vs Peer Influence")
    st.write("""
    The association between **Age Group** and **Peer Influence** is depicted by a line in the **scatter plot**. 
    With the age group on the x-axis and the degree of peer influence on the y-axis, each point represents a unique record. 
    We can see the overall trend—whether peer influence rises or falls as the age group shifts—by adding the **line** to the graphic.
    This graphic might shed light on how peer pressure or influence changes as young people get older and whether some age groups are more vulnerable to peer pressure than others.
    """)
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

st.write("""
### Conclusion:
Numerous important insights into the intricate links between different elements, including age, gender, peer influence, and mental health, are revealed by the examination of data on youth drug use and smoking. We have seen how smoking prevalence has changed over time, with differences across age and gender categories, thanks to the various visualizations. While the bar charts provided a comparison of smoking rates by age group, the line charts assisted in tracking smoking patterns. Notably, age has a big impact on smoking habits because younger people often have lower prevalence rates than older teenagers. The gender distribution is clarified by the pie charts, which also show if smoking and drug experimenting practices differ by gender. Additionally, the box plots showed the distribution of drug experimentation across various age categories, giving a clear picture of the data's distribution and anomalies. Peer influence can be a major factor in the initiation and maintenance of smoking behaviors, especially in specific years and demographic groups, according to the heatmap of smoking prevalence and peer influence across time, which revealed a high association. Peer influence and age groups were further highlighted by the scatter plot with a regression line, which suggested that peer pressure appears to rise with age. Lastly, the relationship between higher rates of drug usage and worse mental health is highlighted by the histogram that shows drug experimentation and mental health. All things considered, these graphics highlight how critical it is to comprehend the different socioenvironmental elements that influence teen drug and smoking use. The evidence clearly indicates that Mitigating smoking and drug experimenting behaviors may be made possible by focused treatments that concentrate on particular age groups, gender, and the elimination of peer influence. Additionally, addressing mental health issues may be crucial to lowering young people's likelihood of using drugs. These results highlight the necessity of specialized public health approaches to deal with these related problems and lay the groundwork for further studies meant to comprehend and reduce teen drug and smoking experimentation.""")

   
