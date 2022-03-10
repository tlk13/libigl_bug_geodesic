import igl
import openmesh as om
import numpy as np


mesh = om.read_trimesh("50009_standing_tall.obj")
polyline_pts = np.load("polylines_points.npy", allow_pickle=True)
works = polyline_pts[4]
does_not_work = polyline_pts[9]

_, closest_faces, closest_points = igl.point_mesh_squared_distance(works, mesh.points(), mesh.fv_indices())
added_vhs = []
for j in range(closest_faces.shape[0]):
    vh = mesh.add_vertex(closest_points[j])
    mesh.split(om.FaceHandle(closest_faces[j]), vh)
    added_vhs.append(vh.idx())
added_vhs = np.array(added_vhs, dtype=np.int32)
dists = np.empty((len(mesh.points()), 1))
dists[:, 0] = igl.heat_geodesic(mesh.points(), mesh.fv_indices(), 0.01, added_vhs)
print("it worked")

mesh = om.read_trimesh("50009_standing_tall.obj")
_, closest_faces, closest_points = igl.point_mesh_squared_distance(does_not_work, mesh.points(), mesh.fv_indices())
added_vhs = []
for j in range(closest_faces.shape[0]):
    vh = mesh.add_vertex(closest_points[j])
    mesh.split(om.FaceHandle(closest_faces[j]), vh)
    added_vhs.append(vh.idx())
added_vhs = np.array(added_vhs, dtype=np.int32)
dists = np.empty((len(mesh.points()), 1))
dists[:, 0] = igl.heat_geodesic(mesh.points(), mesh.fv_indices(), 0.01, added_vhs)
print("did not work")