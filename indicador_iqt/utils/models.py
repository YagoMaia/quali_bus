import pandas as pd

REQUIRED_COLUMNS = {
    'Name': str,
    'Latitude': float,
    'Longitude': float
}

def validate_dataframe(df: pd.DataFrame) -> bool:
    # Verifica se as colunas esperadas estão presentes
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError(f"DataFrame está faltando colunas: {missing_columns}")

    # Verifica se os tipos das colunas estão corretos
    for col, col_type in REQUIRED_COLUMNS.items():
        if not pd.api.types.is_dtype_equal(df[col].dtype, pd.Series(dtype=col_type).dtype):
            raise ValueError(f"Coluna '{col}' deve ser do tipo {col_type}")

    return True
