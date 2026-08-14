# ERIZO CI fixture audit — 2026-08-14

The latest fixture run generated **64** rows and failed only because the workflow verification asserted **32** rows.

The runner dimensions are:
- 4 surfaces
- 2 N values
- 2 noise levels
- 2 seeds
- 2 k values

Therefore the expected count is `4 × 2 × 2 × 2 × 2 = 64`.

The synthetic experiment itself completed successfully on both Python 3.10 and 3.11; the failure is a CI assertion mismatch, not a scientific experiment failure.

This audit is kept separate from private research evidence. The correction is limited to the public lab fixture workflow and does not alter any frozen research result.
