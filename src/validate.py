def validate_data(df):
    """
    Perform basic data quality checks.
    """

    print("\n=== DATA QUALITY CHECK ===")

    print("\nColumn data types:")
    print(df.dtypes)

    print("\nColumns containing dictionaries:")

    dict_columns = []

    for column in df.columns:
        has_dict = df[column].apply(
            lambda x: isinstance(x, dict)
        ).any()

        if has_dict:
            dict_columns.append(column)

    if dict_columns:
        print(dict_columns)
    else:
        print("No dictionaries found.")

    print(f"\nRows       : {len(df)}")
    print(f"Columns    : {len(df.columns)}")

    print("\nMissing values:")
    print(df.isna().sum())

    duplicate_count = df.duplicated(
        subset=[
            "country_code",
            "year",
            "indicator_variable"
        ]
    ).sum()

    print("\nDuplicate observations:")
    print(duplicate_count)

    print("\nCountries:")
    print(df["country_code"].nunique())

    print("\nIndicators:")
    print(df["indicator_variable"].value_counts())

    print("\nYear range:")
    print(
        df["year"].min(),
        "-",
        df["year"].max()
    )