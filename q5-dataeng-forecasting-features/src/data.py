# © 2025 kerem.ai · All rights reserved.

import warnings
from pathlib import Path

import pandas as pd

# Define the root directory
ROOT_DIR = Path(__file__).parents[1]
DATA_DIR = ROOT_DIR / "input_data" / "data"
OUTPUT_DIR = ROOT_DIR / "output_data"


def read_data() -> pd.DataFrame:
    """
    Read the data from the input directory.
    It loads not only the sales data, but also the auxilary data
    such as product, brand, and store information.
    All dataframes are merged into a single dataframe that
    will be returned.

    Returns
    -------
    df: pd.DataFrame
        The dataframe with the sales data and the auxilary data.
    """
    # Load the sales data and rename the columns
    df = pd.read_csv(DATA_DIR / "sales.csv")
    df.columns = df.columns.to_series().replace(
        {"store": "store_id", "product": "product_id"}
    )

    # Convert the date column to datetime
    df["date"] = pd.to_datetime(df["date"])

    # Read the auxilary data
    product_df, store_df = read_auxilary_data()

    # Merge the sales data with the auxilary data
    df = pd.merge(df, product_df, on="product_id", how="left")
    df = pd.merge(df, store_df, on="store_id", how="left")

    # Sort by product, store, and date
    df = df.sort_values(by=["product_id", "store_id", "date"])

    return df


def read_auxilary_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Read the auxilary data from the input directory.
    Brand information is merged with the product data.
    Store information is loaded separately.

    Returns
    -------
    product_df: pd.DataFrame
        The product data with brand information.
    store_df: pd.DataFrame
        The store data including the store name and city information.
    """
    # Load the product data and rename the columns
    product_df = pd.read_csv(DATA_DIR / "product.csv")
    product_df.columns = product_df.columns.to_series().replace(
        {"id": "product_id", "name": "product"}
    )

    # Load the brand data and merge it with the product data
    brand_df = pd.read_csv(DATA_DIR / "brand.csv")
    brand_df.columns = brand_df.columns.to_series().replace(
        {"id": "brand_id", "name": "brand"}
    )
    product_df = pd.merge(product_df, brand_df, on="brand", how="left")

    # Load the store data and rename the columns
    store_df = pd.read_csv(DATA_DIR / "store.csv")
    store_df.columns = store_df.columns.to_series().replace(
        {"id": "store_id", "name": "store"}
    )

    return product_df, store_df


def write_features(features: pd.DataFrame) -> None:
    """
    Write the features to the output directory.

    Parameters
    ----------
    features: pd.DataFrame
        The dataframe with the features.
    """
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")  # Suppress all warnings

        # Sort the columns in the order of the output
        columns_sorted = [
            "product_id",
            "store_id",
            "brand_id",
            "date",
            "sales_product",
            "MA7_P",
            "LAG7_P",
            "sales_brand",
            "MA7_B",
            "LAG7_B",
            "sales_store",
            "MA7_S",
            "LAG7_S",
        ]
        features: pd.DataFrame = features[columns_sorted]

        # Fill the NaN values with 0
        features.fillna(0, inplace=True)

        # Convert LAG columns to integer
        lag_columns = ["LAG7_P", "LAG7_B", "LAG7_S"]
        for col in lag_columns:
            features[col] = features[col].astype(int)

        # Sort features before writing to file
        features.sort_values(
            by=["product_id", "brand_id", "store_id", "date"], inplace=True
        )

        # Write the features to the output directory
        if not OUTPUT_DIR.exists():
            OUTPUT_DIR.mkdir(parents=True)
        features.to_csv(
            OUTPUT_DIR / "features.csv",
            float_format="%.8f",
            index=False,
        )


def write_wmapes(wmapes: pd.DataFrame, top: int) -> None:
    """
    Write the WMAPE to the output directory after sorting by
    WMAPE in descending order.
    The top N products are written to the output directory.

    Parameters
    ----------
    wmapes: pd.DataFrame
        The dataframe with the WMAPE.
    top: int
        The number of top products to write to the output directory.
    """
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")  # Suppress all warnings

        # Sort the WMAPE in descending order
        wmapes.sort_values(by="WMAPE", ascending=False, inplace=True)

        # Get the top N products
        wmapes = wmapes.head(top)

        # Write the top N products to the output directory
        if not OUTPUT_DIR.exists():
            OUTPUT_DIR.mkdir(parents=True)
        wmapes.to_csv(
            OUTPUT_DIR / "mapes.csv",
            float_format="%.6f",
            index=False,
        )
