# © 2025 kerem.ai · All rights reserved.

import datetime

import numpy as np
import pandas as pd


def calculate_features(
    df: pd.DataFrame, group_by: list[str], min_date: datetime.datetime
) -> pd.DataFrame:
    """
    Calculate the total number of sales, moving average of sales over
    the past 7 days, and the lag of sales over the past 7 days for the
    given group columns.

    Parameters
    ----------
    df: pd.DataFrame
        The dataframe to calculate the features for.
    group_by: list[str]
        The columns to group by.
    min_date: datetime.datetime
        The minimum date to calculate the features for.

    Returns
    -------
    features: pd.DataFrame
        The dataframe with the features.
    """
    # Calculate the total number of sales for the given group columns
    total_sales, column_name = calculate_total_sales(df, group_by)

    # Calculate the moving average of sales over the past 7 days
    ma7 = calculate_ma7(total_sales, group_by, column_name)

    # Get the sales of 7 days before each date for the desired group columns
    lag7 = get_sales_lag7(total_sales, group_by, column_name)

    # Merge the dataframes
    features = pd.merge(total_sales, ma7, on=[*group_by, "date"], how="left")
    features = pd.merge(features, lag7, on=[*group_by, "date"], how="left")

    # Filter the data from the minimum date
    features = features[features["date"] >= min_date]

    return features


def calculate_total_sales(
    df: pd.DataFrame, group_by: list[str]
) -> tuple[pd.DataFrame, str]:
    """
    Calculate the total number of sales for the given group columns.

    Parameters
    ----------
    df: pd.DataFrame
        The dataframe to calculate the total number of sales for.
    group_by: list[str]
        The columns to group by.

    Returns
    -------
    total_sales: pd.DataFrame
        The dataframe with the total number of sales for the given group columns.
    column_name: str
        The name of the column that contains the total number of sales.
    """
    total_sales = df.groupby(by=[*group_by, "date"])["quantity"].sum()
    total_sales = total_sales.reset_index()

    # Rename the quantity column to sales_XXX
    column_name = f"sales_{group_by[0].split('_')[0]}"
    total_sales.columns = total_sales.columns.to_series().replace(
        {"quantity": column_name}
    )

    return total_sales, column_name


def calculate_ma7(
    df: pd.DataFrame, group_by: list[str], column_name: str
) -> pd.DataFrame:
    """
    Calculate the moving average of sales over the past 7 days for
    the given group columns.

    Parameters
    ----------
    df: pd.DataFrame
        The dataframe to calculate the moving average of sales for.
    group_by: list[str]
        The columns to group by.
    column_name: str
        The name of the column that contains the total number of sales.

    Returns
    -------
    ma7: pd.DataFrame
        The dataframe with the moving average of sales for the given group columns.
    """

    def rolling_mean(grouped_df: pd.DataFrame) -> pd.Series:
        grouped_df = grouped_df.set_index("date")[column_name]
        rolling_mean = grouped_df.rolling(window="8D", min_periods=1).sum()
        rolling_mean = (rolling_mean - grouped_df) / 7.0
        return rolling_mean.reset_index()

    # Calculate the moving average of sales over the past 7 days
    ma7 = df.groupby(by=[*group_by]).apply(lambda x: rolling_mean(x)).reset_index()

    # Drop the unnecessary columns - generated while grouping
    ma7.drop(columns=[f"level_{len(group_by)}"], inplace=True)

    # Rename the columns
    ma7_column_name = f"MA7_{group_by[0][0].upper()}"
    ma7.columns = ma7.columns.to_series().replace({column_name: ma7_column_name})

    return ma7


def get_sales_lag7(
    df: pd.DataFrame, group_by: list[str], column_name: str
) -> pd.DataFrame:
    """
    Get the sales of 7 days before each date for the desired group columns.

    Parameters
    ----------
    df: pd.DataFrame
        The dataframe to calculate the lag of sales for.
    group_by: list[str]
        The columns to group by.
    column_name: str
        The name of the column that contains the total number of sales.

    Returns
    -------
    lag7: pd.DataFrame
        The dataframe with the lag of sales for the given group columns.
    """

    def get_lag7(grouped_df: pd.DataFrame) -> pd.Series:
        grouped_df = grouped_df.set_index("date")[column_name]
        lag7 = grouped_df.shift(7, freq="D", fill_value=0)
        return lag7.reset_index()

    # Get the sales of 7 days before each date for the desired group columns
    lag7 = df.groupby(by=[*group_by]).apply(lambda x: get_lag7(x)).reset_index()

    # Drop the unnecessary columns - generated while grouping
    lag7.drop(columns=[f"level_{len(group_by)}"], inplace=True)

    # Rename the columns
    lag7_column_name = f"LAG7_{group_by[0][0].upper()}"
    lag7.columns = lag7.columns.to_series().replace({column_name: lag7_column_name})

    return lag7


def calculate_wmape(features: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the WMAPE for the given features.

    Parameters
    ----------
    features: pd.DataFrame
        The dataframe with the features.
    """

    def calculate_wmape_per_group(grouped_df: pd.DataFrame) -> float:
        error = np.abs(grouped_df["sales_product"] - grouped_df["MA7_P"])
        error = np.sum(error) / np.sum(grouped_df["sales_product"])

        return pd.Series({"WMAPE": error})

    # Calculate the WMAPE for the given features
    features = (
        features.groupby(by=["product_id", "brand_id", "store_id"])
        .apply(lambda x: calculate_wmape_per_group(x))
        .reset_index()
    )

    return features
