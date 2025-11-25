import pandas as pd
import numpy as np


def run_etl(input_path: str = "data/bank_marketing.csv") -> None:
    """
    Run the ETL pipeline:
    - Read raw bank marketing data
    - Build client, campaign, and economics tables
    - Export them as CSV files in the current directory
    """
    # Read raw data
    df = pd.read_csv(input_path)

    # ===========================
    # CLIENT TABLE
    # ===========================
    client = df[['client_id', 'age', 'job', 'marital', 'education',
                 'credit_default', 'mortgage']].copy()

    # Clean job: replace "." with "_"
    client['job'] = client['job'].replace(r'\.', '_', regex=True)

    # Clean education: replace "." with "_" and "unknown" -> NaN
    client['education'] = (
        client['education']
        .replace(r'\.', '_', regex=True)
        .replace('unknown', np.nan)
    )

    # Convert credit_default and mortgage to boolean
    client['credit_default'] = client['credit_default'] \
        .apply(lambda x: 1 if x == 'yes' else 0).astype(bool)
    client['mortgage'] = client['mortgage'] \
        .apply(lambda x: 1 if x == 'yes' else 0).astype(bool)

    # ===========================
    # CAMPAIGN TABLE
    # ===========================
    campaign = df[['client_id', 'number_contacts', 'contact_duration',
                   'previous_campaign_contacts', 'previous_outcome',
                   'campaign_outcome', 'month', 'day']].copy()

    # Build last_contact_date as datetime (year fixed at 2022)
    campaign['last_contact_date'] = pd.to_datetime(
        campaign['month'] + campaign['day'].astype(str).str.zfill(2) + '2022',
        format='%b%d%Y',
        errors='coerce'
    )

    # Drop month and day
    campaign = campaign.drop(['month', 'day'], axis=1)

    # previous_outcome: True if "success", else False
    campaign['previous_outcome'] = campaign['previous_outcome'] \
        .apply(lambda x: 1 if x == 'success' else 0).astype(bool)

    # campaign_outcome: True if "yes", else False
    campaign['campaign_outcome'] = campaign['campaign_outcome'] \
        .apply(lambda x: 1 if x == 'yes' else 0).astype(bool)

    # ===========================
    # ECONOMICS TABLE
    # ===========================
    economics = df[['client_id', 'cons_price_idx',
                    'euribor_three_months']].copy()

    # ===========================
    # EXPORT FILES
    # ===========================
    client.to_csv("client.csv", index=False)
    campaign.to_csv("campaign.csv", index=False, date_format="%Y-%m-%d")
    economics.to_csv("economics.csv", index=False)


if __name__ == "__main__":
    run_etl()
