import pandas as pd
from src.analysis.prepare import build_metrics


def test_build_metrics():
    df = pd.DataFrame(
        {
            "date": pd.to_datetime(["2024-01-01", "2024-01-15", "2024-02-01"]),
            "value": [10, 20, 30],
        }
    )
    out = build_metrics(df)
    assert {
        "year",
        "month",
        "value_sum",
        "value_mean",
        "value_median",
        "value_count",
    } <= set(out.columns)
    jan = out[(out["year"] == 2024) & (out["month"] == 1)].iloc[0]
    feb = out[(out["year"] == 2024) & (out["month"] == 2)].iloc[0]
    assert jan["value_sum"] == 30
    assert feb["value_sum"] == 30
