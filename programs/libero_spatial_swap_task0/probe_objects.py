report = []
for prompt in ("black bowl", "akita black bowl", "plate", "ramekin"):
    seg = segment_text("agentview", prompt)
    entry = {"prompt": prompt, "objects": []}
    if seg.ok:
        for item in seg.segmentations[:10]:
            cloud = mask_to_point_cloud(item, "agentview", target_frame=get_robot_state().base_frame)
            if len(cloud.points) >= 20:
                geom = estimate_geometry(cloud)
                entry["objects"].append({"score": item.score, "box": item.box_xyxy, "center": geom.pose.position, "extents": geom.extents, "count": len(cloud.points)})
    report.append(entry)
result = report
