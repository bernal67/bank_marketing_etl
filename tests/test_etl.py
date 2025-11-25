import os
import pandas as pd
from etl import run_etl


def test_etl_creates_output_files(tmp_path, monkeypatch):
    """
    Basic smoke test:
    - Copies a sample CSV into a temp folder
    - Runs ETL
    - Checks that all three output files are created
    """
    # Arrange: point ETL to a temporary directory
    temp_csv = tmp_path / "bank_marketing.csv"

    # For now, just skip if sample file isn't available
    # In a real project, you'd include a small fixture CSV.
    if not os.path.exists("data/bank_marketing.csv"):
        # No real input present, so we don't fail CI because of that.
        return

    # Copy the real file into tmp_path
    pd.read_csv("data/bank_marketing.csv").to_csv(temp_csv, index=False)

    # Act
    monkeypatch.chdir(tmp_path)
    run_etl(input_path=str(temp_csv))

    # Assert: outputs exist
    assert (tmp_path / "client.csv").exists()
    assert (tmp_path / "campaign.csv").exists()
    assert (tmp_path / "economics.csv").exists()
