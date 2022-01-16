from docmodel import DocModel
import os
from OCC.Core.AIS import AIS_Shape, AIS_Line, AIS_Circle
from OCC.Display.SimpleGui import init_display

models_dir_path = "C:/Users/Computer/PycharmProjects/graphStepSimilarity/Datasets/DS_4/Models/"
images_dir_path = "C:/Users/Computer/PycharmProjects/graphStepSimilarity/images/models_images/"
files = []
for file in os.listdir(models_dir_path):
    if file.endswith((".step", ".stp")):
        files.append(file)

error_files = []

for file in files:
    doc = DocModel()
    doc.my_load_stp_at_top(models_dir_path + file)
    print(doc.label_dict)
    print(doc.part_dict)

    for uid in doc.part_dict:
        #if uid not in self.hide_list:

        part_data = doc.part_dict[uid]
        shape = part_data["shape"]
        color = part_data["color"]
        name = part_data["name"]

        aisShape = AIS_Shape(shape)
        display, start_display, add_menu, add_function_to_menu = init_display()

        drawer = aisShape.DynamicHilightAttributes()
        zoom_factor = 16.0
        # display.ZoomFactor(zoom_factor)
        display.Context.Display(aisShape, True)
        display.Context.SetColor(aisShape, color, True)
        # Set shape transparency, a float from 0.0 to 1.0
        display.Context.HilightWithColor(aisShape, drawer, True)
        display.FitAll()

        image_name = os.path.splitext(file)[0] + "_" + name + '.jpeg'
        display.View.Dump(images_dir_path + image_name)
        # display.DisplayShape(aisShape)
        # start_display()
