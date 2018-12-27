# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import pytest
import papermill as pm
from tests.notebooks_common import OUTPUT_NOTEBOOK, KERNEL_NAME


TOL = 0.05


@pytest.mark.smoke
def test_sar_single_node_smoke(notebooks):
    notebook_path = notebooks["sar_single_node"]
    pm.execute_notebook(notebook_path, OUTPUT_NOTEBOOK, kernel_name=KERNEL_NAME)
    pm.execute_notebook(
        notebook_path,
        OUTPUT_NOTEBOOK,
        kernel_name=KERNEL_NAME,
        parameters=dict(TOP_K=10, MOVIELENS_DATA_SIZE="100k"),
    )
    results = pm.read_notebook(OUTPUT_NOTEBOOK).dataframe.set_index("name")["value"]

    assert results["map"] == pytest.approx(0.105815262, TOL)
    assert results["ndcg"] == pytest.approx(0.373197255, TOL)
    assert results["precision"] == pytest.approx(0.326617179, TOL)
    assert results["recall"] == pytest.approx(0.175956743, TOL)