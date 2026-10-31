def quantile(values, fraction):
    values = sorted(float(v) for v in values)
    return values[int((len(values) - 1) * fraction)]

def locate(prompt):
    found = localize_object(prompt, camera_name="agentview", target_frame=get_robot_state().base_frame)
    if not found.ok or len(found.point_cloud.points) < 20:
        raise ValueError("localization failed: " + prompt)
    return found

def xyz(cloud):
    return tuple(quantile((p[axis] for p in cloud.points), 0.5) for axis in range(3))

def move(pos, quat, frame, label):
    r = move_to_pose(Pose(pos, quat, frame), tolerance=0.03, max_steps=250)
    report[label] = {"ok": r.ok, "status": r.status, "steps": r.steps_executed}
    if not r.ok:
        raise ValueError("motion failed: " + label)

frame = get_robot_state().base_frame
quat = get_robot_state().end_effector_poses["primary"].quaternion_wxyz
report = {"task": get_task_context().language}
pick = locate("blue soup can")
target = locate("wicker basket")
p = xyz(pick.point_cloud)
t = xyz(target.point_cloud)
zlo = quantile((v[2] for v in pick.point_cloud.points), 0.1)
zhi = quantile((v[2] for v in pick.point_cloud.points), 0.9)
rim = quantile((v[2] for v in target.point_cloud.points), 0.95)
graspz = zlo + 0.5 * (zhi - zlo)
report["geometry"] = {"pick": p, "target": t, "zlo": zlo, "zhi": zhi, "rim": rim}
open_gripper()
move((p[0], p[1], graspz + 0.15), quat, frame, "pregrasp")
move((p[0], p[1], graspz), quat, frame, "grasp")
close_gripper()
move((p[0], p[1], max(graspz + 0.15, rim + 0.10)), quat, frame, "lift")
move((t[0], t[1], rim + 0.10), quat, frame, "transit")
move((t[0], t[1], rim + 0.08), quat, frame, "release")
open_gripper()
state = get_robot_state()
for tick in range(20):
    step(RobotAction(arms={"primary": ArmCommand("joint_position", state.joint_positions["primary"], gripper_position=1.0)}))
result = report
