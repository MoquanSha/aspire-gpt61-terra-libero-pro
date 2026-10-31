# Findings: libero-pro/libero_object_swap/task_0

## Root causes observed
- Initial transit timed out on development seeds 51–65; lowering transit collided with the basket in the inspected seed 51.
- Visible basket cloud median biased the drop point: v02 failed 51, 55, 59, 62, 65; seed 51 showed a missed basket.

## What fixed them
- Higher clearance and retry improved 0/15 to 10/15. Robust 5th–95th percentile cloud-bound midpoint improved 10/15 to 15/15; this was the sole v02-to-v03 change.

## Development vs unseen
15/15 development, 15/15 unseen. No residual failure regime was observed in these partitions; untested arrangements remain unknown.

## Generalizable patterns
- Target skill file: localize.md. Trigger: visible container wall biases the point-cloud median and releases miss the opening. Exact selected snippet:

```python
def quantile(values, fraction):
    values = sorted(float(v) for v in values)
    return values[int((len(values) - 1) * fraction)]

target = localize_object("wicker basket", camera_name="agentview", target_frame=get_robot_state().base_frame)
if not target.ok or len(target.point_cloud.points) < 20:
    raise ValueError("basket localization failed")
target_center = tuple((quantile((v[axis] for v in target.point_cloud.points), 0.05) + quantile((v[axis] for v in target.point_cloud.points), 0.95)) / 2.0 for axis in range(3))
```
Evidence: seeds 51, 55, 59, 62, 65 flipped; this snippet requires the complete grasp, transit and above-rim release in the selected program to reproduce the task.

## Skill report
- localize.md §Standard Localization Helper: useful — Runtime localization with point-count guard supported 15/15 development runs.
- localize.md §Prompt Registry: not-applicable — Consulted; no independent use or direct test in the selected program.
- localize.md §Disambiguation: Two Similar Objects in Scene: not-applicable — Consulted; no independent use or direct test in the selected program.
- localize.md §Key Signals: not-applicable — Consulted; no independent use or direct test in the selected program.
- localize.md §Prompting Strategy: useful — Blue soup can and wicker basket prompts detected the intended objects before grasp on development runs.
- localize.md §Placement Z Notes: not-applicable — Consulted; no independent use or direct test in the selected program.
- grasp.md §Standard Pick-and-Place Template: useful — Staged downward grasp and lift succeeded as part of 15/15 development runs.
- grasp.md §Cylindrical Side Grasp (bottles, cans): not-applicable — Consulted; no independent use or direct test in the selected program.
- grasp.md §Key Conventions: useful — Close gripper and preserve command during transport worked in 15/15 development runs.
- grasp.md §Object Geometry Utilities: not-applicable — Consulted; no independent use or direct test in the selected program.
- transport.md §Waypoint Sequences: not-applicable — Consulted; no independent use or direct test in the selected program.
- transport.md §Pre-Probe IK Conditioning: not-applicable — Consulted; no independent use or direct test in the selected program.
- transport.md §Safe Transit (Lateral Escape Before Lift): not-applicable — Consulted; no independent use or direct test in the selected program.
- transport.md §Placement Approach: not-applicable — Consulted; no independent use or direct test in the selected program.
- transport.md §Physics Settling After Release: useful — Explicit 20 hold ticks were applied in all successful runs.
- transport.md §Basket / Container Placement: useful — High transit and release above basket permitted successful placement in 15/15 development runs.

## Blocked modes
None observed in selected version.

## Non-privileged API audit
PASS. Object selection uses observed semantic prompts; all object and goal coordinates, extents and height derive from public perception at runtime. Numeric parameters are relative offsets, quantiles, tolerances, or tick counts. No native state, assets, success feedback, or seed-specific logic was used.
