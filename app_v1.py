import streamlit as st
import pandas as pd

# Set page configuration to wide mode
st.set_page_config(page_title="Doctor Performance Analyzer", layout="wide")

# Load the dataset (replace 'your_dataset.csv' with the actual path)
df = pd.read_csv('cleaned_data.csv')

# Convert column to numeric, coercing errors to NaN
df['ACLC (Average Claimant Cost Doctor Clinic)'] = pd.to_numeric(df['ACLC (Average Claimant Cost Doctor Clinic)'], errors='coerce')

# Streamlit app title
st.title("Doctor Performance Analyzer")

# Dropdown for Clinic selection
clinic_selected = st.selectbox("Select a Clinic:", df['Clinic'].unique())

# Sections to select
sections = ['Consultation', 'Lab', 'Medications', 'Procedures', 'Radiology', 'Total']

# Create columns for horizontal checkboxes
cols = st.columns(len(sections))

# Iterate over sections and place checkboxes in the columns
sections_selected = []
for i, section in enumerate(sections):
    if cols[i].checkbox(section, value=True):
        sections_selected.append(section)

# Filter the dataset based on the Clinic and Sections selected
filtered_df = df[(df['Clinic'] == clinic_selected) & (df['Section'].isin(sections_selected))]

# Calculate the average ACLC for the filtered data
average_aclc = filtered_df['ACLC (Average Claimant Cost Doctor Clinic)'].mean()

# Display the calculated average ACLC
st.write(f"Average ACLC for selected filters: **{average_aclc:.2f}**")

# Add 10% to the average ACLC
threshold = average_aclc * 1.10
st.write(f"Threshold (Average ACLC + 10%): **{threshold:.2f}**")

# Filter doctors with ACLC greater than the threshold
high_aclc_doctors = filtered_df[filtered_df['ACLC (Average Claimant Cost Doctor Clinic)'] > threshold]

# Display the doctors with high ACLC and make their names clickable
st.subheader("Doctors with ACLC greater than the threshold")

# Get the base URL of the app (assuming it runs at a certain domain or localhost)
# If the app is hosted on Streamlit Cloud or similar, the base URL is automatically handled
base_url = st.experimental_get_query_params().get("url", [""])[0]

# Create a markdown string with clickable links
for index, row in high_aclc_doctors.iterrows():
    doctor_name = row['Doctor Name']
    # Construct the app-specific URL
    link = f"{base_url}/app/{doctor_name.replace(' ', '%20')}"
    st.markdown(f"[{doctor_name}]({link}) - ACLC: **{row['ACLC (Average Claimant Cost Doctor Clinic)']:.2f}**")
