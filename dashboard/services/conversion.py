def convert_measurement(value: float, from_unit: str, to_unit: str) -> str:
    conversion_rates = {
        ("yard", "foot"): 3,
        ("foot", "yard"): 1 / 3,
        ("pound", "kilogram"): 0.453592,
        ("kilogram", "pound"): 2.20462,
    }
    converted = value if from_unit == to_unit else value * conversion_rates[(from_unit, to_unit)]
    return f"{value:g} {from_unit} = {converted:g} {to_unit}"
