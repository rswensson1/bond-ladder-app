from fred import get_treasury_yields

def build_treasury_ladder(investment_amount, ladder_years, reinvest, fred_api_key):
    available_maturities = [
        ('6mo', 0.5), ('1yr', 1), ('2yr', 2), ('3yr', 3), ('5yr', 5),
        ('7yr', 7), ('10yr', 10), ('20yr', 20), ('30yr', 30)
    ]
    series_map = {
        '6mo': 'DGS6MO',
        '1yr': 'DGS1',
        '2yr': 'DGS2',
        '3yr': 'DGS3',
        '5yr': 'DGS5',
        '7yr': 'DGS7',
        '10yr': 'DGS10',
        '20yr': 'DGS20',
        '30yr': 'DGS30'
    }

    selected_maturities = [label for label, years in available_maturities if years <= ladder_years]
    if not selected_maturities:
        selected_maturities = ['6mo']

    yield_data = get_treasury_yields(series_map, fred_api_key)
    allocation_per_bond = investment_amount / len(selected_maturities)

    ladder = []
    total_final_value = 0
    for label in selected_maturities:
        y = yield_data.get(label, 0.0) / 100  # convert to decimal
        years = next((yrs for lbl, yrs in available_maturities if lbl == label), 0.5)
        final_value = allocation_per_bond * ((1 + y) ** years) if reinvest else allocation_per_bond * (1 + y * years)
        total_final_value += final_value

        ladder.append({
            "maturity": label,
            "allocation": round(allocation_per_bond, 2),
            "yield_": round(y * 100, 2),
            "final_value": round(final_value, 2)
        })

    ladder.append({
        "maturity": "TOTAL",
        "allocation": round(investment_amount, 2),
        "yield_": None,
        "final_value": round(total_final_value, 2)
    })

    return ladder, yield_data
