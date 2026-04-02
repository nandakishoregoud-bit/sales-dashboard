import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
#from openai import OpenAI

#client = OpenAI()

###### client = OpenAI(api key = "api-key value")

st.title("📊 Sales Analytics Dashboard")

st.markdown("### 📌 Overview")

# Load data
try:
    df = pd.read_csv("sales.csv")
except FileNotFoundError:
    st.error("sales.csv file not found!")
    st.stop()

st.write("Dataset Preview")
df = df.drop_duplicates()
st.dataframe(df.head())


# ---- Filters ----

st.sidebar.header("Filters")

# Region filter
selected_region = st.sidebar.multiselect(
    "Select Region",
    options=df['Region'].unique(),
    default=df['Region'].unique()
)

# Category filter
selected_category = st.sidebar.multiselect(
    "Select Category",
    options=df['Category'].unique(),
    default=df['Category'].unique()
)

total_cities = df['City'].nunique()

# Select number of cities
totalcities= st.sidebar.write(f"Total Cities: {total_cities}")
st.markdown(totalcities)
top_n = st.sidebar.slider(
    "Select number of top cities",
    min_value=1,
    max_value=total_cities,
    value=5
)

if not selected_region or not selected_category:
    st.warning("⚠️ Please select at least one option in both filters")
    st.stop()

# Apply filters
filtered_df = df[
    (df['Region'].isin(selected_region)) &
    (df['Category'].isin(selected_category))
]


category_sales = filtered_df.groupby('Category')['Sales'].sum()
category_profit = filtered_df.groupby('Category')['Profit'].sum()
region_sales = filtered_df.groupby('Region')['Sales'].sum()
top_cities = filtered_df.groupby('City')['Sales'].sum().sort_values(ascending=False).head(top_n)


# ---- KPI Metrics ----

total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
total_orders = filtered_df.shape[0]

# Create 3 columns
col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"${total_sales:,.0f}")
profit_color = "red" if total_profit > 0 else "inverse"
col2.metric("Total Profit", f"${total_profit:,.0f}", delta_color=profit_color)
col3.metric("Total Orders", total_orders)

st.markdown("---")

# ---- Charts ----

st.markdown("## 📊 Visual Insights")

# First row (2 charts)
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sales by Category")
    fig1, ax1 = plt.subplots()
    category_sales.plot(kind='bar', ax=ax1)
    st.pyplot(fig1)

with col2:
    st.subheader("Profit by Category")
    fig2, ax2 = plt.subplots()
    category_profit.plot(kind='bar', ax=ax2)
    st.pyplot(fig2)


# Second row (2 charts)
col3, col4 = st.columns(2)

with col3:
    st.subheader("Sales by Region")
    fig3, ax3 = plt.subplots()
    region_sales.plot(kind='bar', ax=ax3)
    st.pyplot(fig3)

with col4:
    st.subheader("Top 5 Cities")
    fig4, ax4 = plt.subplots()
    top_cities.plot(kind='bar', ax=ax4)
    st.pyplot(fig4)

st.markdown("## 📥 Download Data")

csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download Filtered Data as CSV",
    data=csv,
    file_name='filtered_sales_data.csv',
    mime='text/csv'
)

    
st.markdown("## 🤖 AI Insights (Advanced)")

if st.button("Generate AI Insights"):
    
    ##summary = f"""
    ##Category Sales:
   # {category_sales}

   # Category Profit:
   # {category_profit}
   # """

  #  response = client.chat.completions.create(
   #     model="gpt-4.1-mini",
  #      messages=[
  #          {"role": "system", "content": "You are a data analyst."},
  #          {"role": "user", "content": f"Analyze this data and give business insights:\n{summary}"}
    #    ]
  #  )

   # ai_output = response.choices[0].message.content
   # st.write(ai_output)

    insights = []

    # Category insights
    best_category = category_profit.idxmax()
    worst_category = category_profit.idxmin()

    insights.append(f"🚀 {best_category} is the most profitable category.")
    insights.append(f"⚠️ {worst_category} has the lowest profit and needs attention.")

    # Profit condition
    if total_profit < 50000:
        insights.append("❌ Overall profit is low. Consider reducing discounts.")
    else:
        insights.append("✅ Business is generating good profit.")

    # Region insight
    best_region = region_sales.idxmax()
    insights.append(f"🌍 {best_region} region has the highest sales.")

    for i in insights:
        st.write(i)
