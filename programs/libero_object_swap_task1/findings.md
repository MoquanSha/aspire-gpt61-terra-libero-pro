# Findings: libero-pro/libero_object_swap/task_1

## Root causes observed

- Grasp execution: initial visible-surface grasp left the package on the table after lifting (seed 51 keyframes; all 15 trials failed). Descending 0.025 m led to a motion timeout across all 15 seeds.

## What fixed them

- Descending 0.01 m relative to the observed package surface produced 15/15 successful development trials, versus 0/15 for v00 and v01. The source is `code/v02_shallow_grasp.py`.

## Development vs unseen

15/15 development and 15/15 unseen-check; the selected source generalized on the assigned unseen partition.

## Generalizable patterns

None proposed: the shallow offset is evidenced on this package and task but has not been independently reproduced from a standalone procedure.

## Skill report

- localize.md §Prompting Strategy: useful; a color/shape description localized the package in seed 51 and the policy succeeded across development seeds.
- grasp.md §Standard Pick-and-Place Template: useful; staged top-down approach and close succeeded after tuning the relative grasp depth.
- transport.md §Basket / Container Placement: not applicable; the program did not follow the stated heights.

## Blocked modes

None.

## Non-privileged API audit

PASS. Task-dependent object and basket coordinates come from public perception at runtime. The program uses only documented public APIs, generic relative offsets, and no seed branching, privileged state, asset geometry, or hardcoded scene poses. v02 and fix_code.py share SHA256 2c068ca5c5f5fd22221d4c0d9c491e49c24af2bff672a4912f6bcd681a4eddfa.
