# Findings: libero-pro/libero_spatial_swap/task_0

## Root causes observed
- Grasp execution: all development seeds failed. In v00, descent timed out on 14 seeds, consistent with a center grasp contacting the wide bowl; v01 reached its target but lifted empty in inspected seed 51. v02 also failed all 15. v03 encountered program errors in 14 seeds.

## What fixed them
- None. v00 through v03 each scored 0/15; the grasp mode exhausted its three corrective versions.

## Development vs unseen
- 0/15 development; unseen not run because first development seed has not passed and no policy qualifies for handoff.

## Generalizable patterns
None.

## Skill report
- Localization sections: reference localization and candidate selection gave runnable inputs but did not establish successful task completion; other sections were not applicable to this outcome.
- Grasp sections: top-down skeleton ran but did not establish a grasp of this bowl; other sections not applicable.
- Transport sections: no confirmed grasp made transport patterns testable.

## Blocked modes
- Grasp execution: wide bowl grasp remains unsolved after three corrective versions.

## Non-privileged API audit
PASS for all versions: object choices and coordinates derive from public observations and point-cloud geometry; no simulator internals or asset geometry used. No policy selected.

Correction: v02 was accidentally identical to v01 because the intended source replacement did not match. It was charged against the mode budget; the alternate-axis approach was not tested.
