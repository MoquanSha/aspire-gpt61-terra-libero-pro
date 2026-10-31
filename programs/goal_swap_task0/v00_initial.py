def quantile(values, q):
    ordered = sorted(float(v) for v in values)
    return ordered[int((len(ordered)-1)*q)]

frame = get_robot_state().base_frame
seg = segment_text('agentview', 'drawer handle')
if not seg.ok:
    raise ValueError('handle segmentation failed')
handles = []
for candidate in seg.segmentations:
    if candidate.score < 0.4:
        continue
    cloud = mask_to_point_cloud(candidate, 'agentview', target_frame=frame)
    if len(cloud.points) < 20:
        continue
    p = cloud.points
    handles.append((quantile((v[2] for v in p), 0.5), quantile((v[0] for v in p), 0.5), quantile((v[1] for v in p), 0.5)))
if len(handles) != 3:
    raise ValueError('expected three handles')
handles = sorted(handles)
z, x, y = handles[1]
q = get_robot_state().end_effector_poses['primary'].quaternion_wxyz
open_gripper()
pre = move_to_pose(Pose((x, y + 0.03, z + 0.14), q, frame), tolerance=0.015, max_steps=250)
if not pre.ok:
    raise ValueError('pre approach failed')
reach = move_to_pose(Pose((x, y, z), q, frame), tolerance=0.01, max_steps=250)
if not reach.ok:
    raise ValueError('handle approach failed')
close_gripper()
pull = move_to_pose(Pose((x, y + 0.20, z), q, frame), tolerance=0.015, max_steps=300)
result = {'handle': [x,y,z], 'pull_ok': pull.ok}
