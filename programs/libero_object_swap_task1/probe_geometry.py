base = get_robot_state().base_frame
report = {}
for query in ("blue rectangular package", "basket"):
    found = localize_object(query, camera_name="agentview", target_frame=base)
    entry = {"ok": found.ok}
    if found.ok:
        points = found.point_cloud.points
        entry["count"] = len(points)
        entry["quantiles"] = [[sorted(float(p[i]) for p in points)[int((len(points)-1)*q)] for q in (0.05, 0.5, 0.95)] for i in (0,1,2)]
    report[query] = entry
result = report
