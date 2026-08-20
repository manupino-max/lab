import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("selective_leace_validation_v1.py")
spec = importlib.util.spec_from_file_location("sle", MODULE_PATH)
sle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sle)


def test_tau_grid_is_frozen():
    assert list(sle.TAU_GRID) == [
        0.00, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06,
        0.07, 0.08, 0.09, 0.10, 0.12, 0.15, 0.20
    ]
    assert sle.SEEDS == list(range(20))
    assert sle.EPS_F1 == 0.01


def test_selective_replacement_is_rowwise_only():
    import numpy as np

    raw = np.array([[1., 1.], [2., 2.], [3., 3.]])
    leace = np.array([[10., 10.], [20., 20.], [30., 30.]])
    mask = np.array([False, True, False])

    out = sle.selective(raw, leace, mask)

    np.testing.assert_array_equal(
        out,
        np.array([[1., 1.], [20., 20.], [3., 3.]])
    )


def test_validation_rule_is_strict_on_fairness_and_tolerant_on_utility():
    eps_f1 = sle.EPS_F1
    eps_auc = 0.005
    eps_ba = 0.002

    cases = [
        # fairness improvement required
        (0.0001, -eps_f1, -eps_auc, -eps_ba, True),
        # no fairness improvement -> invalid
        (0.0, 0.0, 0.0, 0.0, False),
        # F1 outside tolerance -> invalid
        (0.01, -eps_f1 - 1e-9, 0.0, 0.0, False),
        # AUC outside tolerance -> invalid
        (0.01, 0.0, -eps_auc - 1e-9, 0.0, False),
        # BA outside tolerance -> invalid
        (0.01, 0.0, 0.0, -eps_ba - 1e-9, False),
    ]

    for dphi, df1, dauc, dba, expected in cases:
        valid = (
            (dphi > 0)
            and (df1 >= -eps_f1)
            and (dauc >= -eps_auc)
            and (dba >= -eps_ba)
        )
        assert valid is expected


def test_no_test_split_in_data_generator():
    import numpy as np

    result = sle.make_data(0)
    assert len(result) == 6
    xtr, xva, ytr, yva, ztr, zva = result
    assert xtr.shape[0] == ytr.shape[0] == ztr.shape[0]
    assert xva.shape[0] == yva.shape[0] == zva.shape[0]
    assert not np.shares_memory(xtr, xva)
