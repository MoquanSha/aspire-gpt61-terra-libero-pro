def quantile(points, axis, q):
    values = sorted(float(p[axis]) for p in points)
    return values[int((len(values)-1)*q)]
def locate(query):
    found = localize_object(query, camera_name="agentview", target_frame=base)
    if not found.ok or len(found.point_cloud.points) < 20:
        raise ValueError("localization failed: " + query)
    return found.point_cloud.points
def move(x,y,z):
    moved = move_to_pose(Pose((x,y,z), down, base), tolerance=0.02, max_steps=220)
    if not moved.ok:
        raise ValueError("motion failed")
base = get_robot_state().base_frame
down = get_robot_state().end_effector_poses["primary"].quaternion_wxyz
obj = locate("blue rectangular package")
basket = locate("basket")
x = (quantile(obj,0,0.05)+quantile(obj,0,0.95))/2
y = (quantile(obj,1,0.05)+quantile(obj,1,0.95))/2
z = quantile(obj,2,0.5)
tx = (quantile(basket,0,0.05)+quantile(basket,0,0.95))/2
ty = (quantile(basket,1,0.05)+quantile(basket,1,0.95))/2
rim = quantile(basket,2,0.95)
open_gripper()
move(x,y,z+0.15)
move(x,y,z)
close_gripper()
move(x,y,max(z+0.18,rim+0.10))
move(tx,ty,max(z+0.18,rim+0.10))
move(tx,ty,rim+0.04)
open_gripper()
result = {"object": [x,y,z], "target": [tx,ty,rim]}
