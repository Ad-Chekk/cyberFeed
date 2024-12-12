import streamlit as st
import json
import plotly.express as px
import pandas as pd
from datetime import datetime
from collections import Counter

st.set_page_config(page_title="Single Equity analysis", page_icon=":bar_chart:", layout="wide")
import streamlit as st
import json
import plotly.express as px
import pandas as pd
from datetime import datetime
from collections import Counter

# Load your JSON files with explicit utf-8 encoding
with open('big_data.json', 'r', encoding='utf-8') as file:
    big_data = json.load(file)

with open('secData.json', 'r', encoding='utf-8') as file:
    sec_data = json.load(file)

with open('toi.json', 'r', encoding='utf-8') as file:
    timeline_data = json.load(file)


# 1. Vulnerability Threat Distribution Chart
def create_threat_distribution_chart():
    threats = [article['threat type'] for article in big_data]
    threat_counts = Counter(threats)
    threat_distribution = pd.DataFrame(threat_counts.items(), columns=['Threat Type', 'Count'])
    chart = px.bar(threat_distribution, x='Threat Type', y='Count', title="Threat Type Distribution")
    return chart

# 2. Trending Attack Sectors Pie Chart (from secData.json)
def create_sector_distribution_pie_chart():
    # Count occurrences of each sector
    sector_counts = Counter([article['Predicted_Sector'] for article in sec_data])
    
    # Sectors to show as pie chart (considering only 8 main sectors)
    sectors = ['Banking', 'Telecom', 'Defense', 'Energy', 'Transportation', 'Healthcare', 'IT', 'Others']
    sector_data = {sector: sector_counts[sector] for sector in sectors}
    
    # Convert to DataFrame for pie chart
    sector_distribution = pd.DataFrame(list(sector_data.items()), columns=['Sector', 'Count'])
    
    chart = px.pie(sector_distribution, names='Sector', values='Count', title="Trending Attack Sectors", 
                   color='Sector', color_discrete_sequence=px.colors.sequential.Plasma)
    return chart

# 3. Incident Timeline Graph (from timeline data) - Horizontal Line Chart
def create_incident_timeline_chart():
    # Remove the '(IST)' part from the date string
    dates = [
        datetime.strptime(article['date'].replace(' (IST)', ''), "%b %d, %Y, %H:%M") 
        for article in timeline_data
    ]
    timeline_df = pd.DataFrame({'Date': dates, 'Title': [article['title'] for article in timeline_data]})

    # Create a horizontal line chart instead of a scatter plot
    chart = px.line(timeline_df, x='Title', y='Date', title="Incident Timeline", labels={"Date": "Date", "Title": "Title"}, orientation='h')

    # Adjust the size of the chart to make it bigger
    chart.update_layout(
        height=800,  # Increased height for better visibility
        width=1200,  # Increased width for more horizontal space
        xaxis=dict(tickangle=45),  # Rotate x-axis labels to fit better
        yaxis_title="Incident Date",  # Rename y-axis title for clarity
        title_x=0.5,  # Center the title
    )

    return chart

# Streamlit interface
st.title("Cybersecurity Threat Visualizations")

# Sidebar for user interaction
st.sidebar.title("Query Options")
st.sidebar.write("Select the options below to filter the data and explore it.")

# Sidebar Filters (optional)
selected_threat = st.sidebar.selectbox('Select Threat Type', ['All'] + list(set([article['threat type'] for article in big_data])))
selected_sector = st.sidebar.selectbox('Select Sector', ['All'] + list(set([article['Predicted_Sector'] for article in sec_data])))

# Filter data based on selected options
if selected_threat != 'All':
    filtered_big_data = [article for article in big_data if article['threat type'] == selected_threat]
else:
    filtered_big_data = big_data

if selected_sector != 'All':
    filtered_sec_data = [article for article in sec_data if article['Predicted_Sector'] == selected_sector]
else:
    filtered_sec_data = sec_data

# Create charts based on the filtered data
def create_filtered_threat_distribution_chart():
    threats = [article['threat type'] for article in filtered_big_data]
    threat_counts = Counter(threats)
    threat_distribution = pd.DataFrame(threat_counts.items(), columns=['Threat Type', 'Count'])
    chart = px.bar(threat_distribution, x='Threat Type', y='Count', title="Threat Type Distribution")
    return chart

def create_filtered_sector_distribution_chart():
    sectors = [article['Predicted_Sector'] for article in filtered_sec_data]
    sector_counts = Counter(sectors)
    sector_distribution = pd.DataFrame(sector_counts.items(), columns=['Sector', 'Count'])
    chart = px.bar(sector_distribution, x='Sector', y='Count', title="Trending Attack Sectors")
    return chart

# Display the incident timeline chart (horizontal line chart) first and make it larger
st.subheader("Incident Timeline")
st.write("A timeline showcasing when major cyber incidents were reported.")
st.plotly_chart(create_incident_timeline_chart())

# Display the threat distribution chart below the timeline chart
st.subheader("Cybersecurity Threat Distribution")
st.write("Here is a graphical representation of threat types across various articles.")
st.plotly_chart(create_filtered_threat_distribution_chart())

# Display sector-wise analysis pie chart below the threat distribution chart
st.subheader("Trending Attack Sectors")
st.write("A pie chart showing the distribution of incidents across different sectors.")
st.plotly_chart(create_sector_distribution_pie_chart())
