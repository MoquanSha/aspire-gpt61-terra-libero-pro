result = []
s = segment_text('agentview', 'drawer handle')
for candidate in s.segmentations:
    cloud = mask_to_point_cloud(candidate, 'agentview', target_frame=get_robot_state().base_frame)
    if len(cloud.points) >= 20:
        geom = estimate_geometry(cloud)
        result.append({'score': candidate.score, 'center': list(geom.pose.position), 'extents': list(geom.extents), 'count': len(cloud.points), 'box': list(candidate.box_xyxy)})
