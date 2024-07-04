import pandas as pd
import numpy as np
from faker import Faker
import random

# Initialize Faker for generating random data
fake = Faker()

# Function to generate random Indian phone numbers
def generate_indian_phone_number():
    return f"+91{random.randint(6000000000, 9999999999)}"

# Function to generate random dates within the specified range
def generate_random_dates(start_date, end_date, n):
    start_u = start_date.value // 10**9
    end_u = end_date.value // 10**9
    return pd.to_datetime(np.random.randint(start_u, end_u, n), unit='s')

# Set the number of entries
n = 500

# Generate data
data = {
    "Client Name": [fake.name() for _ in range(n)],
    "Client Number": [generate_indian_phone_number() for _ in range(n)],
    "Org Name": [fake.company() for _ in range(n)],
    "Org Type": [random.choice(['Hospital', 'Interior', 'Restaurant', 'Others']) for _ in range(n)],
    "Location": [random.choice(['India', 'USA', 'UK', 'Japan', 'Singapore', 'Malaysia']) for _ in range(n)],
    "City": [random.choice(['Chennai', 'Madhurai', 'Erodu', 'Namakkal', 'Salam', 'Pudukkottai', 'Paramakudi', 'Karaikudi', 'Thambaram', 'Sengalpattu']) for _ in range(n)],
    "Business type": [random.choice(['One Time', 'Recurring']) for _ in range(n)],
    "Products": [random.choice(['Branding', 'Design', 'SMM', 'Website', 'CRM', 'Google Ads', 'Meta Ads', 'Video Editing', 'Marketing']) for _ in range(n)],
    "Proposal Amount": [random.randint(1000, 100000) for _ in range(n)],
    "Finally Budget": [random.randint(1000, 100000) for _ in range(n)],
    "End of Date": generate_random_dates(pd.to_datetime('2023-01-01'), pd.to_datetime('2024-07-04'), n),
    "Priority": [random.choice(['High', 'Medium', 'Low']) for _ in range(n)],
    "Email": [fake.email() for _ in range(n)],
    "Status": [random.choice(['Fresh', 'Call Back', 'Do Not Disturb', 'Follow up', 'Proposed', 'Hold', 'Closed']) for _ in range(n)],
    "Additional Remarks": [fake.sentence() for _ in range(n)],
    "Call Back Comments": [fake.sentence() for _ in range(n)],
    "Call Back": generate_random_dates(pd.to_datetime('2023-01-01'), pd.to_datetime('2024-07-04'), n),
    "Referral Name": [random.choice(['Arun Kumar', 'Ravi Kumar', 'Vignesh', 'Sathish', 'Prasath']) for _ in range(n)]
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv("dummy_data_updated.csv", index=False)
