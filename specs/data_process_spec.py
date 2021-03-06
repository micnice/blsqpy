"""

"""
import json
import pandas as pd
import blsqpy.data_process as dp
from mamba import description, it


with description("reconciliation") as self:
    with it("sequential reconciliation with prefered source"):
        config = json.loads(open("./specs/fixtures/config/sample_2_sources.json", encoding='utf-8').read())
        input_data = pd.read_csv('./specs/fixtures/reconcile/input.csv', sep=';')
        expected_data = pd.read_csv('./specs/fixtures/reconcile/expected.csv', sep=';')
        serie = dp.measured_serie(input_data, config, 'pills', 'delivered', 'moh')
        serie.reconcile_series()
        reconciled_serie =serie.data
        pd.testing.assert_frame_equal(
            reconciled_serie,
            expected_data.reset_index(drop=True),
            check_dtype=False,
            )
