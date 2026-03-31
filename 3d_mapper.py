import open3d as o3d
import numpy as np


# create sphere
s = o3d.geometry.TriangleMesh.create_sphere(radius=1.0)
s.compute_vertex_normals()
s.paint_uniform_color([0.8, 0.5, 0.4])


# visualizer
vis = o3d.visualization.Visualizer()
vis.create_window(window_name="sphere test", width=800, height=600)


vis.add_geometry(s)


# # background black, just in case
# opt = vis.get_render_option()
# opt.background_color = np.asarray([0, 0, 0])


vis.run()
vis.destroy_window()
