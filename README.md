# 🏦 Bank Marketing ETL Pipeline
A complete ETL pipeline that cleans, reformats, and exports the Bank Marketing dataset into normalized tables for SQL ingestion.

---

## 📌 Project Overview

Personal loans are a major revenue stream for banks. A typical two-year loan in the UK averages around **10% interest**, and UK consumers borrowed **£1.5 billion in September 2022**, generating roughly **£300 million** in interest over two years.

This project processes the raw **bank_marketing.csv** file and transforms it into:

- `client.csv`
- `campaign.csv`
- `economics.csv`

These outputs are fully cleaned and structured for PostgreSQL ingestion.

---

# 📁 Final Output Files & Requirements

---

## 1️⃣ client.csv

| column         | data type | description                 | cleaning rules                                       |
|----------------|-----------|-----------------------------|------------------------------------------------------|
| client_id      | integer   | Client ID                   | —                                                    |
| age            | integer   | Client age                  | —                                                    |
| job            | object    | Job type                    | Replace "." → "_"                                    |
| marital        | object    | Marital status              | —                                                    |
| education      | object    | Education level             | Replace "." → "_" ; "unknown" → NaN                  |
| credit_default | bool      | Credit default flag         | "yes" → True, else False                             |
| mortgage       | bool      | Mortgage / housing loan     | "yes" → True, else False                             |

---

## 2️⃣ campaign.csv

| column                      | data type | description                        | cleaning rules                                       |
|-----------------------------|-----------|------------------------------------|------------------------------------------------------|
| client_id                   | integer   | Client ID                          | —                                                    |
| number_contacts             | integer   | Contacts in this campaign          | —                                                    |
| contact_duration            | integer   | Last contact duration in seconds   | —                                                    |
| previous_campaign_contacts  | integer   | Contacts in previous campaign      | —                                                    |
| previous_outcome            | bool      | Previous campaign outcome          | "success" → True, else False                         |
| campaign_outcome            | bool      | Current campaign outcome           | "yes" → True, else False                             |
| last_contact_date           | datetime  | Date of last contact (YYYY-MM-DD) | Build using month + day + fixed year 2022            |

---

## 3️⃣ economics.csv

| column               | data type | description                              |
|----------------------|-----------|------------------------------------------|
| client_id            | integer   | Client ID                                |
| cons_price_idx       | float     | Consumer price index                     |
| euribor_three_months | float     | Three-month Euribor interest rate        |

---

# ⚙️ ETL Pipeline (bank_marketing_etl.py)

```python
import pandas as pd
import numpy as np

# Read raw data
df = pd.read_csv("bank_marketing.csv")

# ===========================
# CLIENT TABLE
# ===========================
client = df[['client_id', 'age', 'job', 'marital', 'education', 'credit_default', 'mortgage']].copy()
client['job'] = client['job'].replace(r'\.', '_', regex=True)
client['education'] = client['education'].replace(r'\.', '_', regex=True).replace('unknown', np.nan)
client['credit_default'] = client['credit_default'].apply(lambda x: 1 if x == 'yes' else 0).astype(bool)
client['mortgage'] = client['mortgage'].apply(lambda x: 1 if x == 'yes' else 0).astype(bool)

# ===========================
# CAMPAIGN TABLE
# ===========================
campaign = df[['client_id', 'number_contacts', 'contact_duration',
               'previous_campaign_contacts', 'previous_outcome',
               'campaign_outcome', 'month', 'day']].copy()

campaign['last_contact_date'] = pd.to_datetime(
    campaign['month'] + campaign['day'].astype(str).str.zfill(2) + '2022',
    format='%b%d%Y',
    errors='coerce'
)

campaign = campaign.drop(['month', 'day'], axis=1)
campaign['previous_outcome'] = campaign['previous_outcome'].apply(lambda x: 1 if x == 'success' else 0).astype(bool)
campaign['campaign_outcome'] = campaign['campaign_outcome'].apply(lambda x: 1 if x == 'yes' else 0).astype(bool)

# ===========================
# ECONOMICS TABLE
# ===========================
economics = df[['client_id', 'cons_price_idx', 'euribor_three_months']].copy()

# ===========================
# EXPORT FILES
# ===========================
client.to_csv("client.csv", index=False)
campaign.to_csv("campaign.csv", index=False, date_format="%Y-%m-%d")
economics.to_csv("economics.csv", index=False)
```
🧪 Optional Pytest Tests
```python
def test_job_cleaning(client):
    assert not client['job'].str.contains(r'\.').any()

def test_education_cleaning(client):
    assert 'unknown' not in client['education'].dropna().unique()

def test_credit_default_boolean(client):
    assert client['credit_default'].dtype == bool

def test_campaign_date(campaign):
    assert str(campaign['last_contact_date'].dtype).startswith("datetime64")
```
🚀 How to Run

Place `bank_marketing.csv` in your project root

Run the ETL script:

`python etl.py`


The following files will be generated:

- `client.csv`
- `campaign.csv`
- `economics.csv`
