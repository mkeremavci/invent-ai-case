# © 2025 kerem.ai · All rights reserved.

import argparse
import datetime
import gc
from pathlib import Path

import pandas as pd

# Define the root directory
ROOT_DIR = Path(__file__).parent

# Import the source classes
from src import (
    read_data,
    calculate_features,
    write_features,
    calculate_wmape,
    write_wmapes,
)


def main(min_date: str, max_date: str, top: int) -> None:
    """
    Main function to run the program.
    It calculates the product, brand, and store-related features for the given
    time period, and returns the calculated features as a CSV file (features.csv).
    The program also calculates the WMAPE for the same time period, and saves
    the top N products with the highest WMAPE as a CSV file (mapes.csv).

    Parameters
    ----------
    min_date: str
        Start of the date range for the analysis.
    max_date: str
        End of the date range for the analysis.
    top: int
        Number of rows in the WMAPE output.
    """
    # Validate the input arguments
    min_date = datetime.datetime.strptime(min_date, "%Y-%m-%d")
    max_date = datetime.datetime.strptime(max_date, "%Y-%m-%d")
    assert min_date < max_date, "Start date must be before end date."
    assert top > 0, "Number of rows in the WMAPE output must be greater than 0."

    # Read the data files and merge them into a single dataframe
    df = read_data()

    # Filter the data from 7 days before the minimum date, and maximum date
    df = df[df["date"] >= min_date - datetime.timedelta(days=7)]
    df = df[df["date"] <= max_date]

    # Calculate the features
    product_features = calculate_features(
        df, ["product_id", "brand_id", "store_id"], min_date
    )
    brand_features = calculate_features(df, ["brand_id", "store_id"], min_date)
    store_features = calculate_features(df, ["store_id"], min_date)

    # Merge the features into a single dataframe
    features = pd.merge(
        product_features,
        brand_features,
        on=["brand_id", "store_id", "date"],
        how="left",
    )
    features = pd.merge(features, store_features, on=["store_id", "date"], how="left")

    del product_features, brand_features, store_features  # Free up memory
    gc.collect()

    # Write the features to the output directory
    write_features(features)

    # Calculate the WMAPE
    wmapes = calculate_wmape(features)

    # Write the WMAPE to the output directory
    write_wmapes(wmapes, top)


if __name__ == "__main__":
    # Parse the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--min-date",
        type=str,
        default="2021-01-08",
        help="Start of the date range. Format: YYYY-MM-DD",
    )
    parser.add_argument(
        "--max-date",
        type=str,
        default="2021-05-30",
        help="End of the date range. Format: YYYY-MM-DD",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=5,
        help="Number of rows in the WMAPE output.",
    )
    args = vars(parser.parse_args())

    # Run the main function
    main(**args)
