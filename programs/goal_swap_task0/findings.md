# Findings: libero-pro/libero_goal_swap/task_0

## Root causes observed
- v00: 12 seeds stalled on descent toward middle handle; seeds 54, 57, 64 lacked three masks above the arbitrary confidence threshold.
- v06: seeds 53, 55, 59, 60, 63 failed pre-approach; seeds 57, 64, 65 failed high approach.

## What fixed them
- Sort the top three segmented handles by projected median height instead of thresholding at 0.4. Seed 54 became successful in v06.
- A collision-aware high transit, followed by side-facing approach and pull, produced 7/15 on v06 versus 0/15 in v00–v05. The short stand-off in v07 failed high planning on all 15.

## Development vs unseen
7/15 development; 6/15 unseen-check. Comparable rates, but substantial failures remain.

## Generalizable patterns
None proposed: the existing grasp skill already describes collision-aware transit, and the drawer-specific method is not sufficiently reliable.

## Skill report
The grasp Key Conventions section's planned transit was useful; localize's multi-candidate projection and height sorting was useful. Other opened sections did not prescribe the needed drawer interaction.

## Blocked modes
Pre-approach descent contact and high-planning failures remain unresolved; the eight-version development budget is exhausted.

## Non-privileged API audit
PASS. Program uses public APIs; handle positions and ordering derive from runtime segmentation and point clouds. Constants specify relative offsets, orientation and planning tolerances; no seed-specific coordinates, native state, hidden predicates or external baseline code were used.
