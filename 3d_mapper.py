import cv2
import numpy as np
import open3d as o3d

# 3d visualizer
vis = o3d.visualization.Visualizer()
vis.create_window(window_name="SLAM", width=800, height=600)

# makes background black
opt = vis.get_render_option()
opt.background_color = np.asarray([0, 0, 0])
# point size
opt.point_size = 1.0

# cloud object
point_cloud = o3d.geometry.PointCloud()

points = [[0.0, 0.0, 0.0]]
# green starting point
colors = [[0.0, 1.0, 0.0]] 
# needed so open3d will not crash, dumpy data
point_cloud.points = o3d.utility.Vector3dVector(np.array(points))
point_cloud.colors = o3d.utility.Vector3dVector(np.array(colors))
vis.add_geometry(point_cloud)


print(np.array(point_cloud.points))
print(np.array(point_cloud.colors))
print(vis)
