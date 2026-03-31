import cv2
import open3d


# create sphere
s = open3d.geometry.TriangleMesh.create_sphere(radius=1.0)
s.compute_vertex_normals()
# red green blue
s.paint_uniform_color([0.3, 0.7, 0.3])


# visualizer
vis = open3d.visualization.VisualizerWithKeyCallback()
vis.create_window(window_name="sphere test", width=800, height=600)
vis.add_geometry(s)

# # background black, just in case
# opt = vis.get_render_option()
# opt.background_color = np.asarray([0, 0, 0])

while vis.poll_events():
    vis.update_renderer()

def quit(vis):
    vis.close()
    return False


vis.register_key_callback(ord("q"), quit)


vis.destroy_window()


# video = cv2.VideoCapture("sample.mp4")
# while True:
#    ret, frame = video.read()
#    if not ret:
#        print("video ended")
#        break
#
#    cv2.imshow("dog", frame)
#
#    # simulate normal video speed
#    if cv2.waitKey(30) & 0xFF == ord('q'):
#        break
#
# video.release()
# cv2.destroyAllWindows()
