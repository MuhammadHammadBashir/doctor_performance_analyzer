import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration
st.set_page_config(page_title="Doctor Performance Analyzer", layout="wide")

# Function to load the dataset for the main page
@st.cache_data
def load_main_data():
    # Load the dataset (replace 'cleaned_data.csv' with the actual path)
    df = pd.read_csv('cleaned_data.csv')

    # Convert column to numeric, coercing errors to NaN
    df['ACLC (Average Claimant Cost Doctor Clinic)'] = pd.to_numeric(df['ACLC (Average Claimant Cost Doctor Clinic)'], errors='coerce')
    return df

# Function to load the dataset for the doctor summary page
@st.cache_data
def load_doctor_data():
    # Load the dataset for doctor summary
    data = pd.read_csv('cleaned_doctor_details_2.csv')  # Replace with your actual data source

    # Parse the Appointment Date column as a datetime object
    data['Appointment Date'] = pd.to_datetime(data['Appointment Date'])

    # Clean up data if necessary, e.g., removing unwanted spaces
    data['Chief Complaint'] = data['Chief Complaint'].str.strip()
    data['Diagnosis code (ICD 10)'] = data['Diagnosis code (ICD 10)'].str.strip()
    data['Diagnosis Name'] = data['Diagnosis Name'].str.strip()

    return data

# Load the main data
main_data = load_main_data()

# Load the doctor-specific data for the summary page
doctor_data_full = load_doctor_data()

# Function to display the doctor summary page
def show_doctor_summary(selected_doctor):
    # Filter the doctor-specific data based on the selected doctor
    doctor_data = doctor_data_full[doctor_data_full['Doctor'] == selected_doctor]

    if doctor_data.empty:
        st.warning(f"Data for Doctor {selected_doctor} is not available.")
        return

    st.title(f'Doctor Dashboard: {selected_doctor}')
    st.write(f"Total Appointments: {doctor_data.shape[0]}")
    st.write(f"Clinics: {', '.join(doctor_data['Clinic'].unique())}")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader('Diagnosis Codes')
        diag_code_counts = doctor_data['Diagnosis code (ICD 10)'].value_counts()
        plt.figure(figsize=(15, 8))
        sns.barplot(x=diag_code_counts.index, y=diag_code_counts.values)
        plt.xlabel('Diagnosis Code (ICD 10)')
        plt.ylabel('Number of Cases')
        plt.title('Diagnosis Codes Distribution')
        plt.xticks(rotation=90)
        st.pyplot(plt)

    with col2:
        st.subheader('Diagnosis Names')
        diag_name_counts = doctor_data['Diagnosis Name'].value_counts()
        plt.figure(figsize=(15, 8))
        sns.barplot(x=diag_name_counts.index, y=diag_name_counts.values)
        plt.xlabel('Diagnosis Name')
        plt.ylabel('Number of Cases')
        plt.title('Diagnosis Names Distribution')
        plt.xticks(rotation=90)
        st.pyplot(plt)

    col3, col4 = st.columns(2)

    with col3:
        st.subheader('Clinics Distribution (Pie Chart)')
        clinic_counts = doctor_data['Clinic'].value_counts()
        plt.figure(figsize=(12, 12))
        plt.pie(clinic_counts, labels=clinic_counts.index, autopct='%1.1f%%', startangle=140)
        plt.title('Clinics Distribution')
        st.pyplot(plt)

    with col4:
        st.subheader('Diagnosis Names Distribution (Pie Chart)')
        diag_name_counts = doctor_data['Diagnosis Name'].value_counts()
        plt.figure(figsize=(12, 12))
        plt.pie(diag_name_counts, labels=diag_name_counts.index, autopct='%1.1f%%', startangle=140)
        plt.title('Diagnosis Names Distribution')
        st.pyplot(plt)

    st.subheader(f'Detailed Appointments Data for {selected_doctor}')
    st.write(doctor_data)

# Main app logic
def main():
    # Get the base URL of the app
    base_url = st.experimental_get_query_params().get("url", [""])[0]

    # If a doctor is selected in the query params, show their summary page
    query_params = st.experimental_get_query_params()
    if "doctor" in query_params:
        selected_doctor = query_params["doctor"][0]
        show_doctor_summary(selected_doctor)
        return

    # Otherwise, show the main page with a list of doctors
    st.title("Doctor Performance Analyzer")

    clinic_selected = st.selectbox("Select a Clinic:", main_data['Clinic'].unique())
    sections = ['Consultation', 'Lab', 'Medications', 'Procedures', 'Radiology', 'Total']
    cols = st.columns(len(sections))
    sections_selected = [sections[i] for i in range(len(sections)) if cols[i].checkbox(sections[i], value=True)]

    filtered_df = main_data[(main_data['Clinic'] == clinic_selected) & (main_data['Section'].isin(sections_selected))]
    average_aclc = filtered_df['ACLC (Average Claimant Cost Doctor Clinic)'].mean()
    threshold = average_aclc * 1.10

    high_aclc_doctors = filtered_df[filtered_df['ACLC (Average Claimant Cost Doctor Clinic)'] > threshold]

    st.subheader("Doctors with ACLC greater than the threshold")

    # Centering the content
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)

    # Create a markdown string with clickable links and enhanced formatting
    for index, row in high_aclc_doctors.iterrows():
        doctor_name = row['Doctor Name']
        link = f"{base_url}/?doctor={doctor_name.replace(' ', '%20')}"
        st.markdown(f"""
        <div style="margin: 20px 0;">
            <a href="{link}" style="font-size: 18px; color: #1f77b4; text-decoration: none;">
                <strong>{doctor_name}</strong> - ACLC: <span style="font-weight:bold; color:#ff6347;">{row['ACLC (Average Claimant Cost Doctor Clinic)']:.2f}</span>
            </a>
        </div>
        """, unsafe_allow_html=True)

    # End the centering div
    st.markdown("</div>", unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()
