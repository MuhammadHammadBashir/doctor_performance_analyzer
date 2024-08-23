import pandas as pd
df = pd.read_csv('Average Claim Report.csv')
unique_clinics = df['Clinic'].unique()
print(unique_clinics)
# # Create a mapping of unique doctor names to identifiers
# unique_doctors = df['Doctor Name'].unique()
# doctor_mapping = {name: f'Doctor {i+1}' for i, name in enumerate(unique_doctors)}

# # Apply the mapping to the doctor_name column
# df['Doctor Name'] = df['Doctor Name'].map(doctor_mapping)

# df.to_csv("cleaned_data.csv")
