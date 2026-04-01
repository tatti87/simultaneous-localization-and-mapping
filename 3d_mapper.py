import cv2
import numpy as np
import open3d as o3d

vis = o3d.visualization.Visualizer()
vis.create_window(window_name="SLAM", width=800, height=600)

pcd = o3d.geometry.PointCloud()

# needed to prevent runtime error
map_points = [[0.0, 0.0, 0.0]]
map_colors = [[0.0, 1.0, 0.0]]  # green starting point
pcd.points = o3d.utility.Vector3dVector(np.array(map_points))
pcd.colors = o3d.utility.Vector3dVector(np.array(map_colors))
vis.add_geometry(pcd)

# geometry_added = True
centered = False

opt = vis.get_render_option()
opt.background_color = np.asarray([0, 0, 0])
opt.point_size = 2.0

video = cv2.VideoCapture("sample.mp4")
orb = cv2.ORB_create(nfeatures=1500)
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
K = np.array([[w, 0, w/2], [0, w, h/2], [0, 0, 1]], dtype=np.float32)

v_pose = np.eye(4)
ret, frame1 = video.read()
gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
kp1, des1 = orb.detectAndCompute(gray1, None)


while True:
    ret, frame2 = video.read()
    if not ret:
        break

    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    kp2, des2 = orb.detectAndCompute(gray2, None)
    if des1 is None or des2 is None:
        kp1, des1 = kp2, des2
        continue

    matches = bf.knnMatch(des1, des2, k=2)
    t = [j for j, i in matches if j.distance < 0.75 * i.distance]

    if len(t) > 12:
        pts1 = np.float32([kp1[m.queryIdx].pt for m in t]).reshape(-1, 1, 2)
        pts2 = np.float32([kp2[m.trainIdx].pt for m in t]).reshape(-1, 1, 2)

        E, _ = cv2.findEssentialMat(
            pts2, pts1, K, method=cv2.RANSAC, prob=0.999, threshold=1.0)
        if E is not None and E.shape == (3, 3):
            _, R, t_vec, _ = cv2.recoverPose(E, pts2, pts1, K)

            P1 = K @ np.hstack((np.eye(3), np.zeros((3, 1))))
            P2 = K @ np.hstack((R, t_vec))
            pts4d = cv2.triangulatePoints(
                P1, P2, pts1.reshape(-1, 2).T, pts2.reshape(-1, 2).T)
            pts3d = (pts4d[:3, :] / pts4d[3, :]).T

            new_count = 0
            for i, p in enumerate(pts3d):
                if 0.1 < p[2] < 40.0 and abs(p[0]) < 30 and abs(p[1]) < 30:
                    p_world = (v_pose @ np.array([p[0], p[1], p[2], 1.0]))[:3]
                    map_points.append(p_world)

                    # Grab color from the image
                    u, v_coord = int(pts2[i][0][0]), int(pts2[i][0][1])
                    if 0 <= u < w and 0 <= v_coord < h:
                        c = frame2[v_coord, u] / 255.0
                        map_colors.append([c[2], c[1], c[0]])
                    else:
                        map_colors.append([1, 1, 1])
                    new_count += 1

            v_pose = v_pose @ np.vstack((np.hstack((R, t_vec)), [0, 0, 0, 1]))

            if new_count > 0:
                pcd.points = o3d.utility.Vector3dVector(np.array(map_points))
                pcd.colors = o3d.utility.Vector3dVector(np.array(map_colors))
                vis.update_geometry(pcd)

            if not centered and len(map_points) > 200:
                vis.reset_view_point(True)
                centered = True

    vis.poll_events()
    vis.update_renderer()

    cv2.imshow("Video Feed", frame2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    kp1, des1 = kp2, des2

video.release()
cv2.destroyAllWindows()
print("completed: generated", len(map_points), "points")
vis.run()
vis.destroy_window()
