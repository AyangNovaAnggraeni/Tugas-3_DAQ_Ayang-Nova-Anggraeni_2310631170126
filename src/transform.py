import pandas as pd


def transform_data(df):
    """
    Perform basic transformation and cleaning.
    """

    result = df[
        [
            "countryiso3code",
            "country",
            "date",
            "indicator",
            "indicator_variable",
            "value"
        ]
    ].copy()

    # Extract country name from World Bank nested JSON object
    result["country"] = result["country"].apply(
        lambda x: x.get("value")
        if isinstance(x, dict)
        else x
    )

    # Extract indicator name from World Bank nested JSON object
    result["indicator"] = result["indicator"].apply(
        lambda x: x.get("value")
        if isinstance(x, dict)
        else x
    )

    result = result.rename(
        columns={
            "countryiso3code": "country_code",
            "date": "year",
            "indicator": "indicator_name"
        }
    )

    result["year"] = pd.to_numeric(
        result["year"],
        errors="coerce"
    ).astype("Int64")

    result["value"] = pd.to_numeric(
        result["value"],
        errors="coerce"
    )

    result = result.sort_values(
        by=[
            "country_code",
            "year",
            "indicator_variable"
        ]
    )

    result = result.reset_index(drop=True)

    return result