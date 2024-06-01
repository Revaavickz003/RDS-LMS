import pandas as pd
from datetime import datetime

# Define the columns based on the required headings
data = {
    'Client Name': ['John Doe'],
    'Client Number': ['1234567890'],
    'Company Name': ['Example Corp'],
    'Company Type': ['Technology'],
    'Country': ['USA'],
    'City': ['New York'],
    'Refarrel Name': ['Referral1'],
    'Business type': ['One Time'],
    'Budget': [50000],
    'Products': ['Product1, Product2'],
    'End of Date': [datetime.now().strftime('%Y-%m-%d')],
    'Follow up': [datetime.now().strftime('%Y-%m-%d')],
    'Priority': ['High'],
    'Email': ['johndoe@example.com'],
    'Status': ['Fresh'],
    'Additional Remarks': ['Initial contact made'],
    'Call Back Comments': ['Follow up next week'],
}

# Create a DataFrame
df = pd.DataFrame(data)

# Save to Excel file
file_name = 'sample_leads_import.xlsx'
df.to_excel(file_name, index=False)

print(f"Sample file '{file_name}' created.")
