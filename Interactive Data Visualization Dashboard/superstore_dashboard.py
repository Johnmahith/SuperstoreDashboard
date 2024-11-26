import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
# Function to load the dataset
@st.cache_data
def load_data():
    try:
        data = pd.read_csv(
            "https://github.com/Johnmahith/SuperstoreDashboard/blob/main/Interactive%20Data%20Visualization%20Dashboard/Dataset/Superstore.csv",
            encoding="latin1"  # Adjust encoding if needed
        )
        # Preprocess date columns
        data["Order Date"] = pd.to_datetime(data["Order Date"])
        data["Ship Date"] = pd.to_datetime(data["Ship Date"])
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return pd.DataFrame()
    return data

# Load the data
data = load_data()
if not data.empty:
    # App Title
    st.title("Superstore Sales Analysis Dashboard")
    st.markdown("Explore sales trends, categories, and regions in the Superstore dataset.")

    # Dataset Overview
    if st.checkbox("Show Dataset Preview"):
        st.write(data.head())
else:
    st.error("Dataset could not be loaded. Please check the file path or format.")
# Sidebar Filters
st.sidebar.header("Filter Options")
regions = data["Region"].unique()
selected_regions = st.sidebar.multiselect("Select Regions:", regions, default=regions)

categories = data["Category"].unique()
selected_categories = st.sidebar.multiselect("Select Categories:", categories, default=categories)

# Filter the data
filtered_data = data[
    (data["Region"].isin(selected_regions)) &
    (data["Category"].isin(selected_categories))
]
# Key Metrics
st.header("Key Metrics")
total_sales = filtered_data["Sales"].sum()
total_profit = filtered_data["Profit"].sum()
total_orders = filtered_data["Order ID"].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Total Orders", total_orders)
# Sales by Category
st.subheader("Sales by Category")
sales_by_category = filtered_data.groupby("Category")["Sales"].sum().reset_index()
fig, ax = plt.subplots()
sns.barplot(data=sales_by_category, x="Category", y="Sales", ax=ax)
ax.set_title("Sales by Category")
st.pyplot(fig)
# Sales Over Time
st.subheader("Sales Over Time")
sales_over_time = filtered_data.groupby("Order Date")["Sales"].sum().reset_index()
fig, ax = plt.subplots()
ax.plot(sales_over_time["Order Date"], sales_over_time["Sales"], marker="o")
ax.set_title("Sales Over Time")
ax.set_xlabel("Date")
ax.set_ylabel("Sales")
st.pyplot(fig)
# Profit by Region
st.subheader("Profit by Region")
profit_by_region = filtered_data.groupby("Region")["Profit"].sum().reset_index()
fig, ax = plt.subplots()
sns.barplot(data=profit_by_region, x="Region", y="Profit", ax=ax, palette="viridis")
ax.set_title("Profit by Region")
st.pyplot(fig)
# Heatmap for Correlations
st.subheader("Correlation Heatmap")
numeric_data = filtered_data.select_dtypes(include=np.number)
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(numeric_data.corr(), annot=True, cmap="coolwarm", ax=ax)
ax.set_title("Correlation Heatmap")
st.pyplot(fig)
# Option to download filtered data
st.sidebar.download_button(
    label="Download Filtered Data as CSV",
    data=filtered_data.to_csv(index=False),
    file_name="filtered_superstore_data.csv",
    mime="text/csv"
)
