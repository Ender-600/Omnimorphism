import open3d as o3d

def convert_KlamptGeometry_to_open3d(obj):
    vertex_array = obj[1]
    face_array = obj[0]

    mesh = o3d.geometry.TriangleMesh()
    mesh.vertices = o3d.utility.Vector3dVector(vertex_array)
    mesh.triangles = o3d.utility.Vector3iVector(face_array)
    
    return mesh