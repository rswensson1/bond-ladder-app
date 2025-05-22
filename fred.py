import requests

def get_treasury_yields(series_map, api_key):
    yield_curve = {}
    for label, series_id in series_map.items():
        url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={api_key}&file_type=json"
        try:
            response = requests.get(url)
            data = response.json()
            latest = next((obs for obs in reversed(data['observations']) if obs['value'] != '.'), None)
            if latest:
                yield_curve[label] = float(latest['value'])
        except Exception:
            yield_curve[label] = 0.0

    return yield_curve
