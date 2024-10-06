# Importing necessary libraries
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set Streamlit page title
st.title('Imports and Exports Dataset Dashboard')

# Load the dataset
IE_dataset = pd.read_csv("Imports_Exports_Dataset.csv")

# Ensure 'Date' column is in datetime format
IE_dataset['Date'] = pd.to_datetime(IE_dataset['Date'], format='%d-%m-%Y', errors='coerce')

# Sample of 3001 records
IE_dataset = IE_dataset.sample(n=3001, random_state=55038)

# Sidebar for filtering options
st.sidebar.title('Filter Options')

# Convert start_date and end_date to pandas timestamps
start_date = pd.Timestamp(st.sidebar.date_input("Start Date", value=pd.to_datetime(IE_dataset['Date'].min())))
end_date = pd.Timestamp(st.sidebar.date_input("End Date", value=pd.to_datetime(IE_dataset['Date'].max())))

shipping_method = st.sidebar.selectbox('Select Shipping Method:', IE_dataset['Shipping_Method'].unique())
payment_terms = st.sidebar.selectbox('Select Payment Terms:', IE_dataset['Payment_Terms'].unique())

# Filter the dataset based on the selected date range
filtered_data = IE_dataset[(IE_dataset['Date'] >= start_date) & (IE_dataset['Date'] <= end_date)]

# 1. Boxplot for Value based on Shipping Method
st.subheader('Boxplot of Value by Shipping Method')
fig, ax = plt.subplots()
sns.boxplot(x='Shipping_Method', y='Value', data=filtered_data, ax=ax)
plt.title('Boxplot of Value by Shipping Method')
st.pyplot(fig)

# 2. Scatter plot of Quantity vs Value
st.subheader('Scatter Plot of Quantity vs Value')
fig, ax = plt.subplots()
ax.scatter(filtered_data['Quantity'], filtered_data['Value'])
ax.set_title('Scatter Plot of Quantity vs Value')
ax.set_xlabel('Quantity')
ax.set_ylabel('Value')
st.pyplot(fig)

# 3. Histogram of the 'Value' column
st.subheader('Histogram of Transaction Values')
fig, ax = plt.subplots()
ax.hist(filtered_data['Value'], bins=20, edgecolor='k')
ax.set_title('Histogram of Transaction Values')
ax.set_xlabel('Value')
ax.set_ylabel('Frequency')
st.pyplot(fig)

# 4. Pie chart for Payment Terms
st.subheader('Pie Chart of Payment Terms')

# Calculating the payment terms frequencies for the filtered data
payment_terms_counts = filtered_data['Payment_Terms'].value_counts()
fig, ax = plt.subplots()
ax.pie(payment_terms_counts, labels=payment_terms_counts.index, autopct='%.2f%%')
ax.set_title('Pie Plot of Payment Terms')
st.pyplot(fig)

# 5. Bar chart for Shipping Methods Distribution
st.subheader('Distribution of Shipping Methods')
shipping_method_counts = filtered_data['Shipping_Method'].value_counts().reset_index()
shipping_method_counts.columns = ['Shipping_Method', 'Number_of_Transactions']

# Create a bar chart
fig, ax = plt.subplots(figsize=(12, 7))
bar_plot = sns.barplot(data=shipping_method_counts, 
                       x='Shipping_Method', 
                       y='Number_of_Transactions', 
                       palette='viridis', 
                       ax=ax)

# Adding titles and labels
plt.title('Distribution of Shipping Methods', fontsize=16)
plt.xlabel('Shipping Method', fontsize=14)
plt.ylabel('Number of Transactions', fontsize=14)

# Add data labels on top of each bar
for p in bar_plot.patches:
    bar_plot.annotate(f'{int(p.get_height())}', 
                      (p.get_x() + p.get_width() / 2., p.get_height()), 
                      ha='center', va='bottom', 
                      fontsize=12, color='black', 
                      xytext=(0, 5),  # Offset text
                      textcoords='offset points')

# Show the plot in Streamlit
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Display the plot
st.pyplot(plt)

# Option to download filtered dataset
if st.button("Download Filtered Data"):
    filtered_data.to_csv("filtered_data.csv", index=False)  # Save filtered data as CSV
    st.success("Filtered data saved as 'filtered_data.csv'")
