"""LEACE reporting sanity audit (exploratory, non-publication evidence).

Checks only algebraic/reporting consistency of the frozen values already recorded
in the private testing repository. It does not rerun LEACE and must not be used
as a substitute for the confirmatory Colab execution.
"""
from math import isclose


def auc_star(auc: float) -> float:
    return max(auc, 1.0 - auc)


def main() -> None:
    # Existing reported values from LEACE-001/06E.
    raw_auc = 0.2901
    assert isclose(auc_star(raw_auc), 0.7099, rel_tol=0, abs_tol=1e-12)

    # Existing focused held-out preliminary summary.
    raw_protected = 0.8763
    leace_protected = 0.5561
    raw_task = 0.7755
    leace_task = 0.7780

    protected_delta = leace_protected - raw_protected
    task_delta = leace_task - raw_task

    assert protected_delta < 0
    assert task_delta > 0
    assert 0.5 <= leace_protected <= 1.0

    # Geometry report consistency: parallel + orthogonal retention is not
    # expected to sum to 1 because the former is deformation concentration,
    # not retention of the original representation energy.
    bias_energy_retention = 0.0333
    orthogonal_energy_retention = 0.9980
    deformation_parallel_fraction = 0.99664
    assert 0 <= bias_energy_retention <= 1
    assert 0 <= orthogonal_energy_retention <= 1
    assert 0 <= deformation_parallel_fraction <= 1

    print("LEACE reporting audit: PASS")
    print(f"AUC*({raw_auc}) = {auc_star(raw_auc):.4f}")
    print(f"Held-out protected delta = {protected_delta:+.4f}")
    print(f"Held-out task delta = {task_delta:+.4f}")
    print("No publication status is inferred by this audit.")


if __name__ == "__main__":
    main()
