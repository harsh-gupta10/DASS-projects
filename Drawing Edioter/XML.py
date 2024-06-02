import xml.etree.ElementTree as ET
from tkinter import filedialog, simpledialog , colorchooser, messagebox


 

class XML:
    def __init__(self, dr_ed):
        self.dr_ed = dr_ed
        self.canvas = dr_ed.canvas
    def export_as_xml(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xml")
        if file_path:
            self.dr_ed.isLastSaved = True
            root = ET.Element("drawing")
            objects = self.canvas.find_all()
            for object_id in objects:
                object_type = self.canvas.type(object_id)
                coords = self.canvas.coords(object_id)
                
                if object_type == "line":
                    color = self.canvas.itemcget(object_id, "fill")
                    line_element = ET.SubElement(root, "line")
                    begin_element = ET.SubElement(line_element, "begin")
                    x1_element = ET.SubElement(begin_element, "x")
                    x1_element.text = str(coords[0])
                    y1_element = ET.SubElement(begin_element, "y")
                    y1_element.text = str(coords[1])
                    end_element = ET.SubElement(line_element, "end")
                    x2_element = ET.SubElement(end_element, "x")
                    x2_element.text = str(coords[2])
                    y2_element = ET.SubElement(end_element, "y")
                    y2_element.text = str(coords[3])
                    color_element = ET.SubElement(line_element, "color")
                    color_element.text = color
                elif object_type == "rectangle":
                    color = self.canvas.itemcget(object_id, "outline")
                    corner_style = self.canvas.itemcget(object_id, "dash")
                    rectangle_element = ET.SubElement(root, "rectangle")
                    upper_left_element = ET.SubElement(rectangle_element, "upper-left")
                    x1_element = ET.SubElement(upper_left_element, "x")
                    x1_element.text = str(coords[0])
                    y1_element = ET.SubElement(upper_left_element, "y")
                    y1_element.text = str(coords[1])
                    lower_right_element = ET.SubElement(rectangle_element, "lower-right")
                    x2_element = ET.SubElement(lower_right_element, "x")
                    x2_element.text = str(coords[2])
                    y2_element = ET.SubElement(lower_right_element, "y")
                    y2_element.text = str(coords[3])
                    color_element = ET.SubElement(rectangle_element, "color")
                    color_element.text = color
                    corner_element = ET.SubElement(rectangle_element, "corner")
                    corner_element.text = "rounded" if corner_style else "square"
            
            # Handle grouped objects
            for group_id in self.canvas.find_withtag("group"):
                group_element = ET.SubElement(root, "group")
                group_objects = self.canvas.find_withtag(group_id)
                for obj_id in group_objects:
                    obj_type = self.canvas.type(obj_id)
                    coords = self.canvas.coords(obj_id)
                    color = self.canvas.itemcget(obj_id, "fill") if obj_type == "line" else self.canvas.itemcget(obj_id, "outline")
                    corner_style = self.canvas.itemcget(obj_id, "dash") if obj_type == "rectangle" else ""
                    obj_element = ET.SubElement(group_element, obj_type)
                    if obj_type == "line":
                        begin_element = ET.SubElement(obj_element, "begin")
                        x1_element = ET.SubElement(begin_element, "x")
                        x1_element.text = str(coords[0])
                        y1_element = ET.SubElement(begin_element, "y")
                        y1_element.text = str(coords[1])
                        end_element = ET.SubElement(obj_element, "end")
                        x2_element = ET.SubElement(end_element, "x")
                        x2_element.text = str(coords[2])
                        y2_element = ET.SubElement(end_element, "y")
                        y2_element.text = str(coords[3])
                    elif obj_type == "rectangle":
                        upper_left_element = ET.SubElement(obj_element, "upper-left")
                        x1_element = ET.SubElement(upper_left_element, "x")
                        x1_element.text = str(coords[0])
                        y1_element = ET.SubElement(upper_left_element, "y")
                        y1_element.text = str(coords[1])
                        lower_right_element = ET.SubElement(obj_element, "lower-right")
                        x2_element = ET.SubElement(lower_right_element, "x")
                        x2_element.text = str(coords[2])
                        y2_element = ET.SubElement(lower_right_element, "y")
                        y2_element.text = str(coords[3])
                        corner_element = ET.SubElement(obj_element, "corner")
                        corner_element.text = "rounded" if corner_style else "square"
                    color_element = ET.SubElement(obj_element, "color")
                    color_element.text = color
            tree = ET.ElementTree(root)
            tree.write(file_path, encoding="utf-8", xml_declaration=True)

    def import_from_xml(self, file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()

        for element in root:
            if element.tag == "rectangle":
                upper_left = element.find("upper-left")
                lower_right = element.find("lower-right")
                x1 = float(upper_left.find("x").text)
                y1 = float(upper_left.find("y").text)
                x2 = float(lower_right.find("x").text)
                y2 = float(lower_right.find("y").text)
                color = element.find("color").text
                corner = element.find("corner").text if element.find("corner") is not None else "square"
                dash = (5, 5) if corner == "rounded" else ()
                self.canvas.create_rectangle(x1, y1, x2, y2, outline=color, width=1, dash=dash)

            elif element.tag == "line":
                begin = element.find("begin")
                end = element.find("end")
                x1 = float(begin.find("x").text)
                y1 = float(begin.find("y").text)
                x2 = float(end.find("x").text)
                y2 = float(end.find("y").text)
                color = element.find("color").text
                self.canvas.create_line(x1, y1, x2, y2, fill=color)

            elif element.tag == "group":
                group_objects = []
                for obj in element:
                    if obj.tag == "rectangle":
                        upper_left = obj.find("upper-left")
                        lower_right = obj.find("lower-right")
                        x1 = float(upper_left.find("x").text)
                        y1 = float(upper_left.find("y").text)
                        x2 = float(lower_right.find("x").text)
                        y2 = float(lower_right.find("y").text)
                        color = obj.find("color").text
                        corner = obj.find("corner").text if obj.find("corner") is not None else "square"
                        dash = (5, 5) if corner == "rounded" else ()
                        rect_id = self.canvas.create_rectangle(x1, y1, x2, y2, outline=color, width=1, dash=dash)
                        group_objects.append(rect_id)

                    elif obj.tag == "line":
                        begin = obj.find("begin")
                        end = obj.find("end")
                        x1 = float(begin.find("x").text)
                        y1 = float(begin.find("y").text)
                        x2 = float(end.find("x").text)
                        y2 = float(end.find("y").text)
                        color = obj.find("color").text
                        line_id = self.canvas.create_line(x1, y1, x2, y2, fill=color)
                        group_objects.append(line_id)

                # Create a group tag for the grouped objects
                group_tag = "group_" + str(len(self.groups))
                for obj_id in group_objects:
                    self.canvas.addtag_withtag(group_tag, obj_id)
                self.groups.append(group_tag)
