import cv2
import numpy

"""https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html"""

"""camera movements (pose estimation)"""

SCALE = 10.0
OFFSET = (300, 500)


video = cv2.VideoCapture("sample.mp4")
# Oriented FAST and Rotated BRIEF
orb = cv2.ORB_create(nfeatures=1000)
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)

# draw path on canvas, trajectory Visualization


def draw(img, v):  # v -> vector (x, y, z)
    global SCALE, OFFSET
    traj = numpy.zeros((600, 600, 3), dtype=numpy.uint8)

    # from top view
    x = int(v[0, 3] * SCALE) + OFFSET[0]
    z = int(v[2, 3] * SCALE) + OFFSET[1]

    cv2.circle(traj, (x, z), 3, (0, 255, 0), -1)
    cv2.line(traj, OFFSET, (x, z), (255, 0, 0), 1)

    return traj


w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

focal = 1.0 * w
cp = [w / 2, h / 2]

K = numpy.array([
    [focal, 0, cp[0]],
    [0, focal, cp[1]],
    [0, 0, 1]
], dtype=numpy.float32)

# camera starting position, nothing is moving
v = numpy.eye(4)

ret, frame1 = video.read()
if not ret:
    print("fail frame1")
    exit()

gray_frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
point1, description1 = orb.detectAndCompute(gray_frame1, None)

while True:
    ret, frame2 = video.read()
    if not ret:
        break

    gray_frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    point2, description2 = orb.detectAndCompute(gray_frame2, None)

    # if there is no descriptions
    if description2 is None or description1 is None:
        point1 = point2
        description1 = description2
        continue

    matches = bf.knnMatch(description1, description2, k=2)

    # good matcches
    t = []
    for j, i in matches:
        if j.distance < 0.75 * i.distance:
            t.append(j)

    # essential matrix needs 8 points
    if len(t) < 8:
        continue

    # matching points
    fr1 = []  # previous points
    fr2 = []  # next pooints

    for i in t:
        # index of point1, .pt is x, y of point1
        fr1.append(point1[i.queryIdx].pt)
    pts1 = numpy.float32(fr1).reshape(-1, 1, 2)

    for j in t:
        fr2.append(point2[j.trainIdx].pt)  # index of point2
    pts2 = numpy.float32(fr2).reshape(-1, 1, 2)

    print(pts1)
    print(pts2)

    # cv2.imshow("pose estimation",)
    # cv2.imshow('trajectory', )

    #  essential matrix and pose
    E, mask = cv2.findEssentialMat(
        pts2, pts1, K, method=cv2.RANSAC, prob=0.999, threshold=1.0)
    _, R, t_mat, mask = cv2.recoverPose(E, pts2, pts1, K)

    # camera moving, updating pose
    T_rel = numpy.hstack((R, t_mat))
    T_rel = numpy.vstack((T_rel, numpy.array([0, 0, 0, 1])))
    v = v @ T_rel

    trajectory = draw(frame2, v)
    cv2.imshow('trajectory', trajectory)

    frame1 = frame2
    point1 = point2
    description1 = description2

    cv2.waitKey(1)

video.release()
cv2.destroyAllWindows()
