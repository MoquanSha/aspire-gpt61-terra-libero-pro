v00 — initial program from scene analysis → 0/15
modes: execution/contact 51,52,53,55,56,58,59,60,61,62,63,64 (12) | perception 54,57,65 (3)
v01 — execution/contact: approach the handle horizontally from its front and pull outward.
v01 → 0/15; no success, same perception failures, horizontal reach largely converges but does not pull handle.
v02 — execution/contact: move deeper onto the handle before closing and pull farther.
v02 → 0/15; deeper approach does not capture handle.
v03 — execution/contact: rotate jaws around approach axis to close across the horizontal handle.
v03 → 0/15. Execution/contact blocked after 3 targeted versions.
v04 — perception: accept lower-score handle masks with a bounded height filter to recover missing candidates.
v04 → 0/15; 14/15 programs completed, seed 65 still lacks three accepted handles.
v05 — perception: broaden accepted handle scores while retaining height filtering.
v05 → 0/15, 15 program_ok. Absolute height bound in v04/v05 is scene-specific and quarantined by provenance audit.
v06 — perception: accept lower-scored masks without world-coordinate bounds, preserving permitted provenance.
