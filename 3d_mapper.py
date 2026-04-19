import cv2
import numpy as np
import open3d as o3d

video = "sample.mp4"
cap = cv2.VideoCapture(video)

# 3d visualizer
vis = o3d.visualization.Visualizer()
vis.create_window(window_name="SLAM", width=800, height=600)

opt = vis.get_render_option()
opt.background_color = np.asarray([0, 0, 0])
opt.point_size = 10.0

point_cloud = o3d.geometry.PointCloud()
points = np.array([[0.0, 0.0, 0.0], [-1.0, -1.0, -1.0], [1.0, 1.0, 1.0]], dtype=np.float64)
colors = np.array([[0.0, 1.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]], dtype=np.float64)

point_cloud.points = o3d.utility.Vector3dVector(points)
point_cloud.colors = o3d.utility.Vector3dVector(colors)
vis.add_geometry(point_cloud)

# points
orb = cv2.ORB_create(nfeatures=500)

# compares points between frames
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# first frame
ret, prev_frame = cap.read()
prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
prev_keypoints, prev_descriptors = orb.detectAndCompute(prev_gray, None)

while True:
    ret, frame = cap.read()
    
    # current frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    keypoints, descriptors = orb.detectAndCompute(gray, None)

    if prev_descriptors is not None and descriptors is not None:
        matches = bf.match(prev_descriptors, descriptors)
        
        # best matches
        matches = sorted(matches, key=lambda x: x.distance)

        # draw top matches 
        m = 100
        match_img = cv2.drawMatches(prev_frame, prev_keypoints, frame, keypoints, matches[:m], None, flags=2)
        cv2.imshow("video", match_img)
    else:
        cv2.imshow("video", frame)

    
    prev_frame = frame.copy()
    prev_keypoints = keypoints
    prev_descriptors = descriptors

    # prevents 3d window from freezing
    vis.update_geometry(point_cloud)
    vis.poll_events()
    vis.update_renderer()

    if cv2.waitKey(30) & 0xFF == ord("q"):
        break

# cleanup
cap.release()
cv2.destroyAllWindows()
vis.destroy_window()