import pandas as pd
from datetime import datetime

# Define the columns based on the LeadImportView function
data = {
    'Client Name': ['John Doe'],
    'Client Number': ['1234567890'],
    'Company Name': ['Example Corp'],
    'Company Type': ['Technology'],
    'Location': ['USA'],
    'City': ['New York'],
    'Business type': ['One Time'],
    'Products': ['Product1, Product2'],
    'Proposal Amount': [50000],
    'Finally Budget': [45000],
    'End of Date': [datetime.now().strftime('%Y-%m-%d')],
    'Priority': ['High'],
    'Email': ['johndoe@example.com'],
    'Status': ['Fresh'],
    'Additional Remarks': ['Initial contact made'],
    'Call Back Comments': ['Follow up next week'],
    'Call Back': [datetime.now().strftime('%Y-%m-%d')],
    'Referral Name': ['Referral1'],
}

# Create a DataFrame
df = pd.DataFrame(data)

# Save to Excel file
file_name = 'sample_leads_import.xlsx'
df.to_excel(file_name, index=False)

print(f"Sample file '{file_name}' created.")
