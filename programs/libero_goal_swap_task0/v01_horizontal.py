s = segment_text('agentview', 'drawer handle')
handles = []
for candidate in s.segmentations:
    if candidate.score < 0.4:
        continue
    cloud = mask_to_point_cloud(candidate, 'agentview', target_frame=get_robot_state().base_frame)
    if len(cloud.points) < 20:
        continue
    coords = []
    for axis in range(3):
        vals = sorted([float(p[axis]) for p in cloud.points])
        coords.append(vals[len(vals)//2])
    handles.append(coords)
if len(handles) < 3:
    raise ValueError('three drawer handles not found')
handles = sorted(handles, key=lambda p: p[2])
h = handles[len(handles)//2]
q = [0.70710678, 0.70710678, 0, 0]
frame = get_robot_state().base_frame
open_gripper()
move_to_pose(Pose([h[0], h[1]+0.16, h[2]], q, frame))
move_to_pose(Pose([h[0], h[1]+0.025, h[2]], q, frame))
close_gripper()
move_to_pose(Pose([h[0], h[1]+0.20, h[2]], q, frame))
result = {'handle': h}
