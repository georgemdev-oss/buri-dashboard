import streamlit as st
import pandas as pd
import plotly.express as px

# Load Excel file
file = "Summary of balances as at 25th Sep2025.xlsx"
data = pd.read_excel(file, sheet_name="06.09.25")

# Drop the first row (extra headers) and reset index
data = data.drop(0).reset_index(drop=True)

# Rename columns for clarity
data = data.rename(columns={
    "Name": "Name",
    "Deficits": "Monthly Deficit",
    "Unnamed: 2": "Annual 2020/2021",
    "Unnamed: 3": "Annual 2023",
    "Unnamed: 4": "Annual 2024",
    "Unnamed: 5": "Annual 2025",
    "Unnamed: 6": "Sub-Total",
    "Total Deficit": "Total Deficit"
})

# Convert numeric columns
numeric_cols = ["Monthly Deficit", "Annual 2020/2021", "Annual 2023", 
                "Annual 2024", "Annual 2025", "Sub-Total", "Total Deficit"]
for col in numeric_cols:
    data[col] = pd.to_numeric(data[col], errors="coerce")

# Streamlit UI
st.title("📊 Members Contribution Dashboard")
st.markdown("Data source: **06.09.25 sheet** from the uploaded Excel file.")

# Show raw data
st.subheader("Raw Data")
st.dataframe(data[["Name"] + numeric_cols])

# Total contributions
st.subheader("Total Contributions by Member")
fig1 = px.bar(data, x="Name", y="Sub-Total", title="Total Contributions (Sub-Total)",
              labels={"Sub-Total": "Total Contribution"}, text="Sub-Total")
st.plotly_chart(fig1)

# Annual contributions
st.subheader("Annual Contributions Trend")
annual_cols = ["Annual 2020/2021", "Annual 2023", "Annual 2024", "Annual 2025"]
annual_data = data.melt(id_vars=["Name"], value_vars=annual_cols,
                        var_name="Year", value_name="Contribution")
fig2 = px.bar(annual_data, x="Name", y="Contribution", color="Year",
              barmode="group", title="Annual Contributions")
st.plotly_chart(fig2)

# Deficits
st.subheader("Deficits by Member")
fig3 = px.bar(data, x="Name", y="Total Deficit", color="Total Deficit",
              title="Deficits per Member")
st.plotly_chart(fig3)

# Contribution share
st.subheader("Contribution Share")
fig4 = px.pie(data, names="Name", values="Sub-Total", title="Contribution Distribution")
st.plotly_chart(fig4)
