from .extract import acquire_worldbank_data
from .transform import transform_data
from .validate import validate_data
from .load import save_data


def run_pipeline():

    print("Starting World Bank data acquisition...")

    raw_data = acquire_worldbank_data()

    print("\nRaw data acquired.")
    print(f"Rows: {len(raw_data)}")

    final_data = transform_data(raw_data)

    validate_data(final_data)

    save_data(final_data)

    print("\nData acquisition pipeline completed.")

    return final_data


if __name__ == "__main__":
    run_pipeline()