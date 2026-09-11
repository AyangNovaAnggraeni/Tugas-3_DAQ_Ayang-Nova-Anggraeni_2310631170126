import requests
import pandas as pd

from .config import (
    BASE_URL,
    COUNTRIES,
    INDICATORS,
    START_YEAR,
    END_YEAR
)


def fetch_indicator_data(
    countries,
    indicator_code,
    start_year,
    end_year,
    per_page=100
):
    """
    Retrieve World Bank indicator data using REST API.
    Handles pagination automatically.
    """

    country_codes = ";".join(countries)

    url = (
        f"{BASE_URL}/country/"
        f"{country_codes}/indicator/"
        f"{indicator_code}"
    )

    params = {
        "date": f"{start_year}:{end_year}",
        "format": "json",
        "per_page": per_page,
        "page": 1
    }

    all_records = []

    while True:

        try:
            response = requests.get(
                url,
                params=params,
                timeout=30
            )

            response.raise_for_status()

        except requests.exceptions.Timeout:
            raise RuntimeError(
                "Request ke World Bank API mengalami timeout."
            )

        except requests.exceptions.HTTPError as e:
            raise RuntimeError(
                f"HTTP error dari World Bank API: {e}"
            )

        except requests.exceptions.RequestException as e:
            raise RuntimeError(
                f"Request error: {e}"
            )

        try:
            result = response.json()

        except ValueError:
            raise RuntimeError(
                "Response API bukan JSON yang valid."
            )

        if not isinstance(result, list) or len(result) < 2:
            raise RuntimeError(
                "Format response World Bank API tidak sesuai."
            )

        metadata = result[0]
        records = result[1]

        if records:
            all_records.extend(records)

        current_page = int(metadata["page"])
        total_pages = int(metadata["pages"])

        print(
            f"Indicator {indicator_code}: "
            f"page {current_page}/{total_pages}"
        )

        if current_page >= total_pages:
            break

        params["page"] = current_page + 1

    return pd.DataFrame(all_records)


def acquire_worldbank_data():
    """
    Acquire GDP growth and unemployment data
    from World Bank API.
    """

    datasets = []

    for variable_name, indicator_code in INDICATORS.items():

        df = fetch_indicator_data(
            countries=COUNTRIES,
            indicator_code=indicator_code,
            start_year=START_YEAR,
            end_year=END_YEAR
        )

        df["indicator_variable"] = variable_name

        datasets.append(df)

    combined_df = pd.concat(
        datasets,
        ignore_index=True
    )

    return combined_df