def save_data(df):
    """
    Save final dataset into CSV and Parquet.
    """

    csv_path = "data/hasil_data.csv"
    parquet_path = "data/hasil_data.parquet"

    df.to_csv(
        csv_path,
        index=False
    )

    df.to_parquet(
        parquet_path,
        index=False,
        engine="pyarrow"
    )

    print("\nFiles successfully saved:")
    print(csv_path)
    print(parquet_path)