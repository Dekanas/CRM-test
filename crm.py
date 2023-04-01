import streamlit as st
import pandas as pd
from google.cloud import bigquery

# Authenticate and connect to BigQuery
client = bigquery.Client.from_service_account_json('keys.json')

# Define the BigQuery dataset and table for storing sales leads
dataset_id = 'crm'
table_id = 'crm_leads'

# Define a function to add new sales leads to the BigQuery table
def add_lead(name, email, phone, company, status):
    # Define the SQL query to insert the new lead into the table
    sql = f"""
    INSERT INTO `{dataset_id}.{table_id}` (name, email, phone, company, status)
    VALUES ('{name}', '{email}', '{phone}', '{company}', '{status}')
    """

    # Execute the SQL query
    job = client.query(sql)
    job.result()

# Define a function to retrieve all sales leads from the BigQuery table
def get_leads():
    # Define the SQL query to retrieve all leads from the table
    sql = f"""
    SELECT * FROM `{dataset_id}.{table_id}`
    """

    # Execute the SQL query
    job = client.query(sql)
    rows = job.result()

    # Convert the query results to a Pandas DataFrame
    df = rows.to_dataframe()

    return df

# Define the layout of the CRM application using Streamlit widgets
st.title("Sales Leads CRM")

name = st.text_input("Name")
email = st.text_input("Email")
phone = st.text_input("Phone")
company = st.text_input("Company")
status = st.selectbox("Status", ["New", "Contacted", "Qualified", "Lost"])

if st.button("Add Lead"):
    add_lead(name, email, phone, company, status)
    st.success("Lead added successfully!")

leads = get_leads()

# Display the sales leads in a table
st.dataframe(leads)
