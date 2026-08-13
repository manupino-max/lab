"""Clean-room smoke test for the three-paper reproducibility suite."""
import numpy as np

from experiments.reproducible_three_papers import p01, p02, p03


def main():
    seed = 123

    r01 = p01(seed)
    assert len(r01) == 44
    assert all(np.isfinite(r[k]) for r in r01 for k in ("Dc", "Dg", "Ds"))

    r02 = p02(seed)
    assert set(r02) == {"seed", "linear_auc", "nonlinear_auc", "utility_auc"}
    assert all(0.0 <= r02[k] <= 1.0 for k in ("linear_auc", "nonlinear_auc", "utility_auc"))

    r03 = p03(seed)
    assert len(r03) == 6
    required = {"lambda_", "distortion", "DP_gap", "EO_gap", "accuracy"}
    assert required.issubset(r03[0])
    assert all(np.isfinite(r[k]) for r in r03 for k in required)
    assert all(0.0 <= r["DP_gap"] <= 1.0 for r in r03)
    assert all(0.0 <= r["EO_gap"] <= 1.0 for r in r03)
    assert all(0.0 <= r["accuracy"] <= 1.0 for r in r03)

    print("SMOKE TEST PASSED: P01, P02 and P03 execute and return finite, bounded outputs.")


if __name__ == "__main__":
    main()
