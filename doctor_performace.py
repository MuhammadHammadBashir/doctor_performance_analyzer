import streamlit as st
import pandas as pd

# Load the dataset (replace 'your_dataset.csv' with the actual path)
df = pd.read_csv('cleaned_data.csv')

# Convert column to numeric, coercing errors to NaN
df['ACLC (Average Claimant Cost Doctor Clinic)'] = pd.to_numeric(df['ACLC (Average Claimant Cost Doctor Clinic)'], errors='coerce')

# Streamlit app title
st.title("Doctor Performance Analyzer")

# Dropdown for Clinic selection
clinic_selected = st.selectbox("Select a Clinic:", df['Clinic'].unique())

sections = ['Consultation', 'Lab', 'Others', 'PHR', 'Radiology', 'Total']
sections_selected = [section for section in sections if st.checkbox(section, value=True)]

# Filter the dataset based on the Clinic and Sections selected
filtered_df = df[(df['Clinic'] == clinic_selected) & (df['Section'].isin(sections_selected))]

# Calculate the average ACLC for the filtered data
average_aclc = filtered_df['ACLC (Average Claimant Cost Doctor Clinic)'].mean()

# Display the calculated average ACLC
st.write(f"Average ACLC for selected filters: {average_aclc}")

# Add 10% to the average ACLC
threshold = average_aclc * 1.10
st.write(f"Threshold (Average ACLC + 10%): {threshold}")

# Filter doctors with ACLC greater than the threshold
high_aclc_doctors = filtered_df[filtered_df['ACLC (Average Claimant Cost Doctor Clinic)'] > threshold]

# Display the doctors with high ACLC and make the doctor name clickable
st.subheader("Doctors with ACLC greater than the threshold")
for index, row in high_aclc_doctors.iterrows():
    doctor_name = row['Doctor Name']
    link = f"http://localhost:8501/?doctor={doctor_name}"  # Update with your Streamlit app URL
    st.markdown(f"[{doctor_name}]({link}) - ACLC: {row['ACLC (Average Claimant Cost Doctor Clinic)']:.2f}")
