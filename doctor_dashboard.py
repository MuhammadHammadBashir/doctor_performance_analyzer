import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load doctor details dataset
data = pd.read_csv('cleaned_doctor_details_2.csv')  # Replace with your actual data source

# Parse the Appointment Date column as a datetime object
data['Appointment Date'] = pd.to_datetime(data['Appointment Date'])

# Clean up data if necessary
data['Chief Complaint'] = data['Chief Complaint'].str.strip()
data['Diagnosis code (ICD 10)'] = data['Diagnosis code (ICD 10)'].str.strip()
data['Diagnosis Name'] = data['Diagnosis Name'].str.strip()

# Get the doctor name from URL parameters
doctor_name = st.experimental_get_query_params().get('doctor', [''])[0]

if doctor_name:
    st.title(f'Doctor Dashboard for {doctor_name}')

    # Filter data by selected doctor
    doctor_data = data[data['Doctor'] == doctor_name]

    # Show summary statistics
    st.header(f"Summary for {doctor_name}")
    st.write(f"Total Appointments: {doctor_data.shape[0]}")
    st.write(f"Clinics: {', '.join(doctor_data['Clinic'].unique())}")

    # Set up layout with two rows for larger graphs
    col1, col2 = st.columns(2)

    # Bar plot for Diagnosis Codes
    with col1:
        st.subheader('Diagnosis Codes')
        diag_code_counts = doctor_data['Diagnosis code (ICD 10)'].value_counts()
        plt.figure(figsize=(15, 8))  # Increase figure size
        sns.barplot(x=diag_code_counts.index, y=diag_code_counts.values)
        plt.xlabel('Diagnosis Code (ICD 10)')
        plt.ylabel('Number of Cases')
        plt.title('Diagnosis Codes Distribution')
        plt.xticks(rotation=90)  # Rotate x-axis labels to vertical
        st.pyplot(plt)

    # Bar plot for Diagnosis Names
    with col2:
        st.subheader('Diagnosis Names')
        diag_name_counts = doctor_data['Diagnosis Name'].value_counts()
        plt.figure(figsize=(15, 8))  # Increase figure size
        sns.barplot(x=diag_name_counts.index, y=diag_name_counts.values)
        plt.xlabel('Diagnosis Name')
        plt.ylabel('Number of Cases')
        plt.title('Diagnosis Names Distribution')
        plt.xticks(rotation=90)  # Rotate x-axis labels to vertical
        st.pyplot(plt)

    # Set up layout with two more columns for pie charts
    col3, col4 = st.columns(2)

    # Pie chart for Clinics Distribution
    with col3:
        st.subheader('Clinics Distribution (Pie Chart)')
        clinic_counts = doctor_data['Clinic'].value_counts()
        plt.figure(figsize=(12, 12))  # Increase figure size
        plt.pie(clinic_counts, labels=clinic_counts.index, autopct='%1.1f%%', startangle=140)
        plt.title('Clinics Distribution')
        st.pyplot(plt)

    # Pie chart for Diagnosis Names Distribution
    with col4:
        st.subheader('Diagnosis Names Distribution (Pie Chart)')
        diag_name_counts = doctor_data['Diagnosis Name'].value_counts()
        plt.figure(figsize=(12, 12))  # Increase figure size
        plt.pie(diag_name_counts, labels=diag_name_counts.index, autopct='%1.1f%%', startangle=140)
        plt.title('Diagnosis Names Distribution')
        st.pyplot(plt)

    # Show detailed data in a table
    st.subheader(f'Detailed Appointments Data for {doctor_name}')
    st.write(doctor_data)
else:
    st.write("No doctor selected. Please return to the previous page and select a doctor.")
