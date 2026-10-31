# Findings: libero-pro/libero_goal_swap/task_0

## Root causes observed
- Execution/contact: all 15 development seeds fail to open the drawer; v00 approach motions time out, v01 horizontal approach converges on the grasp pose on seed 51 but does not open the drawer.
- Perception: v00 fails to find three high-confidence handles on seeds 54, 57, 65. Lowering the score threshold eliminated program exceptions in v06, but did not yield task success.

## What fixed them
- No successful drawer-opening strategy was found. v01–v03, the three versions aimed at contact, each scored 0/15. v04–v06 each scored 0/15; v06 completed without a program exception on all 15 seeds.

## Development vs unseen
0/15 on development; unseen not run because seed 51 has not succeeded, and the coordinator handoff gate requires it. No generalization claim.

## Generalizable patterns
None.

## Skill report
- manipulation.md §Knob / Switch Turning: not applicable; the target is a drawer handle, not a knob.
- manipulation.md §Hinged Door Opening / Closing: not applicable; the drawer translates rather than hinging.
- manipulation.md §Pushing / Sliding: not applicable; no procedure supplied for a drawer pull.
- manipulation.md §General Notes: not applicable; no tested drawer guidance.
- localize.md §Standard Localization Helper: not applicable; selection needed multiple handle candidates rather than the first localization.
- localize.md §Prompt Registry: not applicable; no drawer handle entry.
- localize.md §Disambiguation: Two Similar Objects in Scene: not applicable; the intended middle handle required choosing the middle of three vertically sorted candidates, rather than a smallest box.
- localize.md §Key Signals: useful; low candidate confidence was implicated in three initial exceptions, and accepting lower scores removed those exceptions in v06, although success remained 0/15.
- localize.md §Prompting Strategy: useful; `drawer handle` segmented the three target handles in the initial scene, though no task succeeded.
- localize.md §Placement Z Notes: not applicable; no placement task.

## Blocked modes
Execution/contact: unable to establish a successful grip and pull after three targeted versions. See debug/blocked/execution_contact.md.

## Non-privileged API audit
v00–v03 and v06 PASS: public APIs only; handle position is derived from segmentation and projected point medians, with relative motion offsets. v04 and v05 QUARANTINED because their absolute world-height filter was scene-specific. No result from those versions is eligible for selection.
