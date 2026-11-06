#!/usr/bin/env python
# coding: utf-8

# In[6]:


#%pip install requests pandas matplotlib networkx


# In[7]:


import requests
import pandas as pd

url = "https://remotive.com/api/remote-jobs"

response = requests.get(url, timeout=30)
response.raise_for_status()

jobs = response.json()["jobs"]

df = pd.DataFrame([{
    "job_id": job.get("id"),
    "company": job.get("company_name"),
    "job_title": job.get("title"),
    "category": job.get("category"),
    "location": job.get("candidate_required_location"),
    "job_type": job.get("job_type"),
    "publication_date": job.get("publication_date"),
    "job_url": job.get("url")
} for job in jobs])

print("Total jobs:", len(df))
#display(df.head(10))

#df.to_csv("osint_jobs.csv", index=False, encoding="utf-8-sig")


# In[8]:


#%pip install requests pandas pyodbc


# In[9]:


import pyodbc

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=LAPTOP-11JL5C8P\SQLEXPRESS;"
    "DATABASE=jobs;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

cursor = conn.cursor()

#print("Connected successfully!")


# In[10]:


cursor.execute("""
IF OBJECT_ID('dbo.remotive_jobs', 'U') IS NULL
CREATE TABLE dbo.remotive_jobs (
    job_id BIGINT PRIMARY KEY,
    company NVARCHAR(255),
    job_title NVARCHAR(500),
    category NVARCHAR(255),
    location NVARCHAR(500),
    job_type NVARCHAR(100),
    publication_date DATETIME2,
    job_url NVARCHAR(1000),
    collected_at DATETIME2 DEFAULT SYSUTCDATETIME()
)
""")

conn.commit()

print("Table ready!")


# In[11]:


insert_sql = """
INSERT INTO dbo.remotive_jobs (
    job_id, company, job_title, category,
    location, job_type, publication_date, job_url
)
SELECT ?, ?, ?, ?, ?, ?, ?, ?
WHERE NOT EXISTS (
    SELECT 1
    FROM dbo.remotive_jobs
    WHERE job_id = ?
)
"""

inserted = 0

for _, row in df.iterrows():

    job_id = int(row["job_id"])

    published = pd.to_datetime(
        row["publication_date"],
        errors="coerce",
        utc=True
    )

    published = (
        None if pd.isna(published)
        else published.to_pydatetime().replace(tzinfo=None)
    )

    cursor.execute(insert_sql, (
        job_id,
        row["company"],
        row["job_title"],
        row["category"],
        row["location"],
        row["job_type"],
        published,
        row["job_url"],
        job_id
    ))

    inserted += max(cursor.rowcount, 0)

conn.commit()

#print("New jobs inserted:", inserted)


# In[ ]:





# In[ ]:




