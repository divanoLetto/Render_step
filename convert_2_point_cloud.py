import os
import open3d as o3d
from OCC.Core.AIS import AIS_PointCloud
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.StlAPI import StlAPI_Writer
from OCC.Core.IFSelect import IFSelect_RetDone, IFSelect_ItemsByEntity
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Display.SimpleGui import init_display


def read_step(filename):

    step_reader = STEPControl_Reader()
    status = step_reader.ReadFile(filename)
    if status == IFSelect_RetDone:
        failsonly = False
        step_reader.PrintCheckLoad(failsonly, IFSelect_ItemsByEntity)
        step_reader.PrintCheckTransfer(failsonly, IFSelect_ItemsByEntity)

        ok = step_reader.TransferRoot(1)
        _nbs = step_reader.NbShapes()
        return step_reader.Shape(1)
    else:
        raise ValueError('Cannot read the file')

def write_stl(shape, filename, definition=0.1):


    directory = os.path.split(__name__)[0]
    stl_output_dir = os.path.abspath(directory)
    assert os.path.isdir(stl_output_dir)

    stl_file = os.path.join(stl_output_dir, filename)

    stl_writer = StlAPI_Writer()
    stl_writer.SetASCIIMode(False)

    mesh = BRepMesh_IncrementalMesh(shape, definition)
    mesh.Perform()
    assert mesh.IsDone()

    stl_writer.Write(shape, stl_file)
    assert os.path.isfile(stl_file)
    return stl_file


def gettarget(c_data_dir,c_data_file):
    fileabs=os.path.join(c_data_dir,c_data_file)

    try:
        mesh=o3d.io.read_triangle_mesh(fileabs)
        if mesh.has_triangles() is True:
            triangle_clusters, cluster_n_triangles, cluster_area = (mesh.cluster_connected_triangles())
            area=sum(cluster_area)
            x=num_points#int(area//4) #means points on 2mmx2mm grid #was 4
            target = mesh.sample_points_uniformly(number_of_points=x, use_triangle_normal=True)
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

num_points = 1024
models_dir_path = "C:/Users/mande/Desktop/Render_step/models/"
stl_dir_path = "C:/Users/mande/Desktop/Render_step/stl/"
txt_dir_path = "C:/Users/mande/Desktop/Render_step/txt/"

for class_ in os.listdir(models_dir_path):
    if os.path.isdir(models_dir_path + class_):
        for file in os.listdir(models_dir_path + class_ + "/"):
            if file.endswith(".stp"):

                if not os.path.exists(stl_dir_path + class_ + "/" ):
                    os.mkdir(stl_dir_path + class_ + "/" )
                if not os.path.exists(txt_dir_path + class_ + "/"):
                    os.mkdir(txt_dir_path + class_ + "/")

                stl_name = stl_dir_path + class_ + "/" + file.replace("stp", "stl")
                txt_name = txt_dir_path + class_ + "/" + file.replace("stp", "txt")
                shape = read_step(models_dir_path + "/" + class_ + "/" + file)
                print("File readed")
                write_stl(shape, stl_name)
                print("Written")

                point_cloud = gettarget(stl_dir_path, stl_name)

                # o3d.visualization.draw_geometries([point_cloud])
                points = point_cloud.points
                normals = point_cloud.normals
                with open(txt_name, 'w') as f:
                    for i in range(num_points):
                        point = points[i]
                        normal = normals[i]
                        # label = 1  # TODO What ??
                        line = '{:.6f},{:.6f},{:.6f},{:.6f},{:.6f},{:.6f}\n'.format(point[0], point[1], point[2], normal[0], normal[1], normal[2])
                        f.write(line)




