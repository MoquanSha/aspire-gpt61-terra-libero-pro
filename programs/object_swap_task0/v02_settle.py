def quantile(values, q):
    s = sorted(float(v) for v in values)
    return s[int((len(s)-1)*q)]

def center(points):
    return [quantile([p[i] for p in points], 0.5) for i in range(3)]

def move(pos, quat, frame):
    r = move_to_pose(Pose(pos, quat, frame), tolerance=0.02, max_steps=250)
    if not r.ok:
        r = move_to_pose(Pose(pos, quat, frame), tolerance=0.03, max_steps=250)
    if not r.ok:
        raise ValueError('motion failed: ' + str(r.status))
    return r

state = get_robot_state()
frame = state.base_frame
quat = state.end_effector_poses['primary'].quaternion_wxyz
obj = localize_object('alphabet soup can', camera_name='agentview', target_frame=frame)
basket = localize_object('basket', camera_name='agentview', target_frame=frame)
if not obj.ok or not basket.ok:
    raise ValueError('localization failed')
p = center(obj.point_cloud.points)
b = center(basket.point_cloud.points)
for i in (0, 1):
    values = [p[i] for p in basket.point_cloud.points]
    b[i] = (quantile(values, 0.05) + quantile(values, 0.95)) / 2.0
rim = quantile([v[2] for v in basket.point_cloud.points], 0.95)
z = quantile([v[2] for v in obj.point_cloud.points], 0.35)
report = {'object': p, 'basket': b, 'rim': rim, 'grasp_z': z}
open_gripper()
move([p[0],p[1],z+0.15],quat,frame)
move([p[0],p[1],z],quat,frame)
close_gripper()
move([p[0],p[1],max(z+0.20,rim+0.20)],quat,frame)
move([b[0],b[1],max(z+0.20,rim+0.20)],quat,frame)
move([b[0],b[1],rim+0.10],quat,frame)
open_gripper()
state = get_robot_state()
for tick in range(30):
    step(RobotAction(arms={"primary": ArmCommand("joint_position", state.joint_positions["primary"], gripper_position=1.0)}))
result = report
