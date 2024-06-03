import requests
import os
import pandas as pd

# Step 1: Create the dictionary
user_data = {
    'gender': [],
    'first name': [],
    'last name': [],
    'age': [],
    'city': [],
    'state': [],
    'country': []
}

# Step 2: Define the function to fetch data
def fetch_and_append_user_data():
    url = 'https://randomuser.me/api/?results=10'
    response = requests.get(url)
    
    if response.status_code == 200:
        results = response.json()['results']
        for user in results:
            user_data['gender'].append(user['gender'])
            user_data['first name'].append(user['name']['first'])
            user_data['last name'].append(user['name']['last'])
            user_data['age'].append(user['dob']['age'])
            user_data['city'].append(user['location']['city'])
            user_data['state'].append(user['location']['state'])
            user_data['country'].append(user['location']['country'])
    else:
        print(f"Failed to fetch data: {response.status_code}")

# Step 3: Check for the existence of the CSV file and append or create
def save_to_csv():
    fetch_and_append_user_data()
    file_path = 'data/person_data.csv'
    
    # Convert the dictionary to a DataFrame
    df = pd.DataFrame(user_data)
    
    # Check if the file exists
    if os.path.exists(file_path):
        # If file exists, append the data
        df.to_csv(file_path, mode='a', header=False, index=False)
    else:
        # If file does not exist, create it and add the data with header
        df.to_csv(file_path, mode='w', header=True, index=False)
        
    # Read the data back from the CSV file to ensure all data is written and remove duplicates
    final_df = pd.read_csv(file_path)
    final_df.drop_duplicates(inplace=True)
    final_df.to_csv(file_path, index=False)

# Ensure the data folder exists
os.makedirs('data', exist_ok=True)

# Save the data to CSV
save_to_csv()

print("Data written to file")
