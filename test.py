import os
import open3d as o3d
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.StlAPI import StlAPI_Writer


def gettarget(c_data_dir,c_data_file):
    fileabs=os.path.join(c_data_dir,c_data_file)
    try:
        mesh=o3d.io.read_triangle_mesh(fileabs)
        if mesh.has_triangles() is True:
            triangle_clusters, cluster_n_triangles, cluster_area = (mesh.cluster_connected_triangles())
            area=sum(cluster_area)
            x=int(area//4) #means points on 2mmx2mm grid #was 4
            target = mesh.sample_points_uniformly(number_of_points=x)
        else:
            raise ValueError
    except:
        print('Failed to read Mesh')
        try:
            target=o3d.io.read_point_cloud(fileabs)
        except:
            print('Failed to read Point Cloud Data')
            target=False
    return target


models_dir_path = "C:/Users/mande/Desktop/Render_step/models/"
stl_dir_path = "C:/Users/mande/Desktop/Render_step/stl/"

files = []
for file in os.listdir(models_dir_path):
    if file.endswith((".step", ".stp")):
        files.append(file)

for file in files:
    step_reader = STEPControl_Reader()
    step_reader.ReadFile(models_dir_path + file)
    step_reader.TransferRoot()
    myshape = step_reader.Shape()
    print("File readed")

    # Export to STL
    stl_writer = StlAPI_Writer()
    stl_writer.SetASCIIMode(True)
    stl_writer.Write(myshape, stl_dir_path + file.replace("stp", "stl"))
    print("Written")

    gettarget(stl_dir_path, file)


