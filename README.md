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
