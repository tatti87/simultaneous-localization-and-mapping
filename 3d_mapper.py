import cv2
import numpy as np
import open3d as o3d

video = "sample.mp4"
cap = cv2.VideoCapture(video)

# 3d visualizer
vis = o3d.visualization.Visualizer()
vis.create_window(window_name="SLAM", width=800, height=600)

# makes background black
opt = vis.get_render_option()
opt.background_color = np.asarray([0, 0, 0])
# point size
opt.point_size = 10.0

# cloud object
point_cloud = o3d.geometry.PointCloud()

# dummy points
points = np.array([
    [0.0, 0.0, 0.0],
    [-1.0, -1.0, -1.0],
    [1.0, 1.0, 1.0]
], dtype=np.float64)

colors = np.array([
    [0.0, 1.0, 0.0],
    [0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0]
], dtype=np.float64)
# ---------------------------------------------------------

# needed so open3d will not crash, dumpy data
point_cloud.points = o3d.utility.Vector3dVector(points)
point_cloud.colors = o3d.utility.Vector3dVector(colors)
vis.add_geometry(point_cloud)

vis.reset_view_point(True)

while True:
    ret, frame = cap.read()

    cv2.imshow("video", frame)

    # prevets 3d window from freezing
    vis.update_geometry(point_cloud)
    vis.poll_events()
    vis.update_renderer()

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# cleanup
cap.release()
cv2.destroyAllWindows()
vis.destroy_window()
