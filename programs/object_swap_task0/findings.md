# Findings: libero-pro/libero_object_swap/task_0

## Root causes observed

- Execution timeout on the initial pre-grasp approach: v00 produced program errors on all 15 development seeds. A retry from the current state let v01 complete on all 15.
- Object identification: `alphabet soup can` selected the red can in the observed scene. v02 placed that can visibly inside the basket on seed 51 without satisfying the task. The red-can program scored 0/15.
- Placement geometry and settling were uncertain: v01 released near the basket edge and stopped before the falling can settled. v02 used footprint quantiles and 30 hold ticks; its red-can success remained 0/15, so their individual effects cannot be measured from task success.

## What fixed them

- Retry a timed-out pose from the measured current state: v00 had 15 program errors; v01 completed all 15 programs, though none achieved the task.
- Use the visually identified `blue soup can` prompt: v03 scored 15/15, versus v02's 0/15 with the red can. This comparison also retains v02's basket center and settling changes.
- Midpoint of the 5th and 95th percentiles of basket footprint and post-release hold ticks were retained in the successful program; no controlled ablation establishes their separate contribution.

## Development vs unseen

15/15 development; 15/15 unseen check. The selected program generalized to the assigned unseen scenes.

## Generalizable patterns

None proposed: object identity is task-specific, and placement and retry changes were not independently isolated across the full sweep.

## Skill report

The machine-readable skill report grades all consulted sections. The staged pick, early detection, gripper conventions, above-rim release and explicit settling were used in the successful program; individual contribution was not ablated. Other consulted sections were not applicable as distinct procedures.

## Blocked modes

None observed in the selected development sweep.

## Non-privileged API audit

PASS. Programs use public perception, robot state, motion, gripper, and step interfaces only. Object and basket positions and height are derived at runtime; tuned quantiles, offsets and tolerances are generic. No simulator internals, assets, rewards, seed-dependent branches, hardcoded observed poses or external baseline code were used.
