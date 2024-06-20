def convert_to_int(value):
    try:
        return int(value.replace(',', ''))
    except ValueError:
        return 0  # Default value if conversion fails

def convert_to_float(value):
    try:
        return float(value.replace(',', ''))
    except ValueError:
        return 0.0  # Default value if conversion fails