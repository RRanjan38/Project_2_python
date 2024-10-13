# Importing necessary libraries
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Set Streamlit page title and layout
st.set_page_config(page_title="Imports and Exports Dashboard", layout="wide")
st.title('Imports and Exports Dataset Dashboard')

# Load the dataset
IE_dataset = pd.read_csv("C:\\Users\\Rajiv Ranjan\\Downloads\\Imports_Exports_Dataset.csv")

# Ensure 'Date' column is in datetime format
IE_dataset['Date'] = pd.to_datetime(IE_dataset['Date'], format='%d-%m-%Y', errors='coerce')

# Sample of 3001 records
IE_dataset = IE_dataset.sample(n=3001, random_state=55038)

# Sidebar for filtering options
st.sidebar.title('Filter Options')

# Date filter
start_date = pd.Timestamp(st.sidebar.date_input("Start Date", value=pd.to_datetime(IE_dataset['Date'].min())))
end_date = pd.Timestamp(st.sidebar.date_input("End Date", value=pd.to_datetime(IE_dataset['Date'].max())))

# Shipping Method filter - include 'All' option
shipping_method_options = ['All'] + list(IE_dataset['Shipping_Method'].unique())
selected_shipping_method = st.sidebar.selectbox('Select Shipping Method:', shipping_method_options)

# Payment Terms filter - include 'All' option
payment_terms_options = ['All'] + list(IE_dataset['Payment_Terms'].unique())
selected_payment_terms = st.sidebar.selectbox('Select Payment Terms:', payment_terms_options)

# Filter the dataset based on the selected filters
filtered_data = IE_dataset[(IE_dataset['Date'] >= start_date) & (IE_dataset['Date'] <= end_date)]

# Apply Shipping Method filter only if a specific shipping method is selected
if selected_shipping_method != 'All':
    filtered_data = filtered_data[filtered_data['Shipping_Method'] == selected_shipping_method]

# Apply Payment Terms filter only if a specific payment term is selected
if selected_payment_terms != 'All':
    filtered_data = filtered_data[filtered_data['Payment_Terms'] == selected_payment_terms]

# ----------------------------------- Graph Section -----------------------------------

# Display a brief description of the dataset
st.markdown("""
### Overview
This dashboard visualizes the Imports and Exports dataset, allowing users to explore transactions based on different filters such as shipping method and payment terms. 
Use the sidebar to select the desired date range, shipping method, and payment terms for your analysis.
""")

# 1. Boxplot for Value based on Shipping Method
st.subheader('Boxplot of Value by Shipping Method')
st.markdown("This boxplot shows the distribution of transaction values across different shipping methods. It helps identify any outliers and trends.")
fig, ax = plt.subplots()
sns.boxplot(x='Shipping_Method', y='Value', data=filtered_data, ax=ax)
plt.title('Boxplot of Value by Shipping Method')
st.pyplot(fig)

# 2. Scatter plot of Quantity vs Value
st.subheader('Scatter Plot of Quantity vs Value')
st.markdown("The scatter plot illustrates the relationship between quantity and value of transactions. Each point represents a transaction.")
fig, ax = plt.subplots()
ax.scatter(filtered_data['Quantity'], filtered_data['Value'])
ax.set_title('Scatter Plot of Quantity vs Value')
ax.set_xlabel('Quantity')
ax.set_ylabel('Value')
st.pyplot(fig)

# 3. Histogram of the 'Value' column
st.subheader('Histogram of Transaction Values')
st.markdown("This histogram displays the frequency distribution of transaction values, providing insights into the most common transaction amounts.")
fig, ax = plt.subplots()
ax.hist(filtered_data['Value'], bins=20, edgecolor='k')
ax.set_title('Histogram of Transaction Values')
ax.set_xlabel('Value')
ax.set_ylabel('Frequency')
st.pyplot(fig)

# 4. Pie chart for Payment Terms
st.subheader('Pie Chart of Payment Terms')
st.markdown("This pie chart represents the distribution of payment terms used in transactions. It helps understand common practices in payment terms.")
payment_terms_counts = filtered_data['Payment_Terms'].value_counts()
fig, ax = plt.subplots()
ax.pie(payment_terms_counts, labels=payment_terms_counts.index, autopct='%.2f%%')
ax.set_title('Pie Chart of Payment Terms')
st.pyplot(fig)

# 5. Bar chart for Shipping Methods Distribution
st.subheader('Distribution of Shipping Methods')
st.markdown("This bar chart shows the number of transactions for each shipping method, highlighting the most frequently used methods.")
shipping_method_counts = filtered_data['Shipping_Method'].value_counts().reset_index()
shipping_method_counts.columns = ['Shipping_Method', 'Number_of_Transactions']
fig, ax = plt.subplots(figsize=(12, 7))
bar_plot = sns.barplot(data=shipping_method_counts, x='Shipping_Method', y='Number_of_Transactions', palette='viridis', ax=ax)
plt.title('Distribution of Shipping Methods', fontsize=16)
plt.xlabel('Shipping Method', fontsize=14)
plt.ylabel('Number of Transactions', fontsize=14)
for p in bar_plot.patches:
    bar_plot.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='bottom', fontsize=12, color='black', xytext=(0, 5), textcoords='offset points')
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(plt)

# NEWLY ADDED GRAPHS:

# 6. Total Value of Imports vs Exports by Country (Bar Chart)
st.subheader('Total Value of Imports vs Exports by Country')
st.markdown("This bar chart compares the total import and export values for each country, providing insights into trade relationships.")
grouped_data = filtered_data.groupby(['Country', 'Import_Export']).agg({'Value': 'sum'}).reset_index()
fig = px.bar(grouped_data, x='Country', y='Value', color='Import_Export', title='Total Value of Imports vs Exports by Country')
st.plotly_chart(fig)

# 7. Line Chart of Transaction Value Over Time
st.subheader('Transaction Value Over Time')
st.markdown("This line chart illustrates the trend of total transaction values over time, revealing seasonal patterns and changes in trading activity.")
time_data = filtered_data.groupby('Date').agg({'Value': 'sum'}).reset_index()
fig = px.line(time_data, x='Date', y='Value', title='Transaction Value Over Time')
st.plotly_chart(fig)

# 8. Stacked Bar Chart: Export vs Import Quantity by Port
st.subheader('Export vs Import Quantity by Port')
st.markdown("This stacked bar chart shows the quantities of imports and exports for each port, helping to visualize trade flow.")
port_data = filtered_data.groupby(['Port', 'Import_Export']).agg({'Quantity': 'sum'}).reset_index()
fig = px.bar(port_data, x='Port', y='Quantity', color='Import_Export', title='Export vs Import Quantity by Port')
st.plotly_chart(fig)

# Option to download filtered dataset
if st.button("Download Filtered Data"):
    filtered_data.to_csv("filtered_data.csv", index=False)  # Save filtered data as CSV
    st.success("Filtered data saved as 'filtered_data.csv'")

# ----------------------------------- Footer Section -----------------------------------
st.markdown("---")
st.markdown("### About")
st.markdown("This dashboard was created to visualize the Imports and Exports dataset. It allows users to explore data based on selected filters and gain insights into trade activities.")
