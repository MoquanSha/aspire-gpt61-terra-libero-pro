import math

frame = get_robot_state().base_frame
orientation = get_robot_state().end_effector_poses["primary"].quaternion_wxyz
plate = localize_object("plate", camera_name="agentview", target_frame=frame)
ramekin = localize_object("ramekin", camera_name="agentview", target_frame=frame)
if not plate.ok or not ramekin.ok:
    raise ValueError("reference localization failed")
p = plate.geometry.pose.position
r = ramekin.geometry.pose.position
seg = segment_text("agentview", "black bowl")
if not seg.ok:
    raise ValueError("bowl localization failed")
best = None
best_distance = None
vx = float(r[0] - p[0])
vy = float(r[1] - p[1])
length2 = vx * vx + vy * vy
for candidate in seg.segmentations:
    if candidate.score < 0.25:
        continue
    cloud = mask_to_point_cloud(candidate, "agentview", target_frame=frame)
    if len(cloud.points) < 20:
        continue
    geometry = estimate_geometry(cloud)
    center = geometry.pose.position
    t = ((center[0] - p[0]) * vx + (center[1] - p[1]) * vy) / max(length2, 0.000001)
    t = max(0.0, min(1.0, t))
    distance = (center[0] - p[0] - t * vx) ** 2 + (center[1] - p[1] - t * vy) ** 2
    if best_distance is None or distance < best_distance:
        best = geometry
        best_distance = distance
if best is None:
    raise ValueError("no bowl candidate")
c = best.pose.position
# Grasp near the rim, with a downward jaw pose.
x = float(c[0])
y = float(c[1])
z = float(c[2])
pose = Pose((x, y, z + 0.01), orientation, frame)
open_gripper()
move_to_pose(Pose((x, y, z + 0.16), orientation, frame), tolerance=0.02, max_steps=250)
move_to_pose(pose, tolerance=0.015, max_steps=250)
close_gripper()
move_to_pose(Pose((x, y, z + 0.18), orientation, frame), tolerance=0.02, max_steps=250)
move_to_pose(Pose((float(p[0]), float(p[1]), z + 0.18), orientation, frame), tolerance=0.02, max_steps=250)
move_to_pose(Pose((float(p[0]), float(p[1]), float(p[2]) + 0.07), orientation, frame), tolerance=0.02, max_steps=250)
open_gripper()
result = {"bowl_center": list(c), "plate_center": list(p), "ramekin_center": list(r)}
