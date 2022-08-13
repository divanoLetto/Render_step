from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.StlAPI import StlAPI_Writer
from OCC.Core.IFSelect import IFSelect_RetDone, IFSelect_ItemsByEntity
from OCC.Display.SimpleGui import init_display
from OCC.Display.WebGl import threejs_renderer
import sys
import os

models_dir_path = "C:/Users/mande/Desktop/Render_step/models/"
images_dir_path = "C:/Users/mande/Desktop/Render_step/images/"

files = []
for file in os.listdir(models_dir_path):
    if file.endswith((".step", ".stp")):
        files.append(file)

error_files = []

for file in files:
    step_reader = STEPControl_Reader()
    status = step_reader.ReadFile(models_dir_path + file)

    if status == IFSelect_RetDone: # check status
        failsonly = False
        step_reader.PrintCheckLoad(failsonly, IFSelect_ItemsByEntity)
        step_reader.PrintCheckTransfer(failsonly, IFSelect_ItemsByEntity)

        ok = step_reader.TransferRoot(1)
        _nbs = step_reader.NbShapes()
        aResShape = step_reader.Shape(1)
    else:
        print("Error: can't read file.")
        sys.exit(0)

    display, start_display, add_menu, add_function_to_menu = init_display()
    display.DisplayShape(aResShape, update=True)
    image_name = os.path.splitext(file)[0] + '.jpeg'
    display.View.Dump(images_dir_path + image_name)
    # start_display()

    # my_renderer = threejs_renderer.ThreejsRenderer()
    # my_renderer.DisplayShape(aResShape)

