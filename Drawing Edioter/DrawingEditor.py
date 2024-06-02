import tkinter as tk
from tkinter import filedialog, simpledialog , colorchooser, messagebox
import sys
from XML import XML


class DrawingEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("Drawing Editor")
        master.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.canvas = tk.Canvas(self.master, width=800, height=600, bg="white")
        self.canvas.pack()
        
        self.selected_objects = []
        self.selected_group = None
        self.objects = []  # Initialize objects attribute
        self.groups = []  # Initialize groups attribute

        self.xml = XML(self)
        
        # Initialize attributes
        self.current_object = None
        self.copied_object = None
        self.copied_object = None
        self.isLastSaved = True

        self.create_toolbar()

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Button-3>", self.paste_object)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Shift-Button-1>", self.on_select)
        
        self.colour = {
            "black": "k",
            "red": "r",
            "green": "g",
            "blue": "b",
        }
        
        self.color2 = {
          "k": "black",
          "r": "red",
          "g": "green",
          "b": "blue",
        }
        if len(sys.argv) > 1:
          file_path = sys.argv[1]
          # print(file_path)
          # file_path = './' + file_path
          self.load_drawing(file_path)
        
    def on_paste_click(self, event):
        self.paste_object(event)

    def create_toolbar(self):
        toolbar = tk.Frame(self.master)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        self.shape_var = tk.StringVar(value="line")
        line_button = tk.Radiobutton(toolbar, text="Line", variable=self.shape_var, value="line")
        line_button.pack(side=tk.LEFT)
        rectangle_button = tk.Radiobutton(toolbar, text="Rectangle", variable=self.shape_var, value="rectangle")
        rectangle_button.pack(side=tk.LEFT)
        
        self.color_var = tk.StringVar(value="black")
        black_button = tk.Radiobutton(toolbar, text="Black", variable=self.color_var, value="black")
        black_button.pack(side=tk.LEFT)
        red_button = tk.Radiobutton(toolbar, text="Red", variable=self.color_var, value="red")
        red_button.pack(side=tk.LEFT)
        green_button = tk.Radiobutton(toolbar, text="Green", variable=self.color_var, value="green")
        green_button.pack(side=tk.LEFT)
        blue_button = tk.Radiobutton(toolbar, text="Blue", variable=self.color_var, value="blue")
        blue_button.pack(side=tk.LEFT)
        
        self.corner_var = tk.StringVar(value="square")
        square_button = tk.Radiobutton(toolbar, text="Square", variable=self.corner_var, value="square")
        square_button.pack(side=tk.LEFT)
        rounded_button = tk.Radiobutton(toolbar, text="Rounded", variable=self.corner_var, value="rounded")
        rounded_button.pack(side=tk.LEFT)
        
        edit_button = tk.Button(toolbar, text="Edit", command=self.edit_object)
        edit_button.pack(side=tk.LEFT)
        delete_button = tk.Button(toolbar, text="Delete", command=self.delete_object)
        delete_button.pack(side=tk.LEFT)
        copy_button = tk.Button(toolbar, text="Copy", command=self.copy_object)
        copy_button.pack(side=tk.LEFT)
        paste_button = tk.Button(toolbar, text="Paste", command=self.paste_object)
        paste_button.pack(side=tk.LEFT)
        move_button = tk.Button(toolbar, text="Move", command=self.move_object)
        move_button.pack(side=tk.LEFT)
        group_button = tk.Button(toolbar, text="Group", command=self.group_objects)
        group_button.pack(side=tk.LEFT)
        ungroup_button = tk.Button(toolbar, text="Ungroup", command=self.ungroup_objects)
        ungroup_button.pack(side=tk.LEFT)
        
        save_button = tk.Button(toolbar, text="Save", command=self.save_drawing)
        save_button.pack(side=tk.LEFT)
        open_button = tk.Button(toolbar, text="Open", command=self.open_drawing)
        open_button.pack(side=tk.LEFT)
        export_button = tk.Button(toolbar, text="Export XML", command=self.xml.export_as_xml)
        export_button.pack(side=tk.LEFT)


    def on_close(self):
        if self.isLastSaved==False:
            save_warning = messagebox.askyesnocancel("Unsaved Changes", "Do you want to save the drawing before exiting?")
            if save_warning is None:
                return
            elif save_warning:
                self.save_drawing()
        self.master.destroy()



        
    def on_click(self, event):
        if not self.selected_objects:
            self.isLastSaved = False
            self.start_x = event.x
            self.start_y = event.y
            
            if self.shape_var.get() == "line":
                self.current_object = self.canvas.create_line(
                    self.start_x, self.start_y, self.start_x, self.start_y,
                    fill=self.color_var.get()
                )
                # ! Why 4 cordinates in line
            elif self.shape_var.get() == "rectangle":
                self.current_object = self.canvas.create_rectangle(
                    self.start_x, self.start_y, self.start_x, self.start_y,
                    outline=self.color_var.get(), width=1,
                    dash=(5, 5) if self.corner_var.get() == "rounded" else ()
                    #! Change here to change from dashed to Rounded
                )

        
    def on_drag(self, event):
        if self.current_object:
            self.canvas.coords(self.current_object, self.start_x, self.start_y, event.x, event.y)
        

        
    def on_release(self, event):
        self.current_object = None
    def on_select(self, event):
        object_id = self.canvas.find_closest(event.x, event.y)[0]
        group_id = self.canvas.gettags(object_id)[0] if self.canvas.gettags(object_id) else None

        if group_id and group_id.startswith("group_"):
            if group_id == self.selected_group:
                self.selected_group = None
                for obj_id in self.canvas.find_withtag(group_id):
                    self.canvas.itemconfig(obj_id, width=1)
            else:
                if self.selected_group:
                    for obj_id in self.canvas.find_withtag(self.selected_group):
                        self.canvas.itemconfig(obj_id, width=1)
                self.selected_group = group_id
                for obj_id in self.canvas.find_withtag(group_id):
                    self.canvas.itemconfig(obj_id, width=4)
        else:
            if object_id in self.selected_objects:
                self.selected_objects.remove(object_id)
                self.canvas.itemconfig(object_id, width=1)
            else:
                self.selected_objects.append(object_id)
                self.canvas.itemconfig(object_id, width=4)

    def edit_object(self):
      
        if len(self.selected_objects) == 1:
            self.isLastSaved = False
            object_id = self.selected_objects[0]
            
            if self.canvas.type(object_id) == "line":
                color = simpledialog.askstring("Edit Line", "Enter new color: Red/Blue/Green/Bleck")
                if color:
                  self.canvas.itemconfig(object_id, fill=color)
                else:
                  ValueError("Incorrect colour typed")
            elif self.canvas.type(object_id) == "rectangle":
                color = simpledialog.askstring("Edit Rectangle", "Enter new color: Red/Blue/Green/Bleck")
                if color:
                  self.canvas.itemconfig(object_id, outline=color)
                else:
                  ValueError("Incorrect colour typed")
                corner_style = simpledialog.askstring("Edit Rectangle", "Enter corner style (square/rounded):")
                if corner_style:
                  corner_style = corner_style.lower()
                  if corner_style == "rounded":
                    self.canvas.itemconfig(object_id, dash=(5, 5))
                  else:
                    self.canvas.itemconfig(object_id, dash=())

        
    def delete_object(self):
        if self.selected_group:
            group_objects = self.canvas.find_withtag(self.selected_group)
            for object_id in group_objects:
                self.canvas.delete(object_id)
            self.groups.remove(self.selected_group)
            self.selected_group = None
        else:
            for object_id in self.selected_objects:
                self.canvas.delete(object_id)
            self.selected_objects.clear()
        
    def copy_object(self):
        if self.selected_group:
            group_objects = self.canvas.find_withtag(self.selected_group)
            self.copied_object = []
            for object_id in group_objects:
                object_type = self.canvas.type(object_id)
                coords = self.canvas.coords(object_id)
                if object_type == "line":
                    color = self.canvas.itemcget(object_id, "fill")
                    self.copied_object.append({"type": "line", "coords": coords, "color": color})
                elif object_type == "rectangle":
                    color = self.canvas.itemcget(object_id, "outline")
                    corner_style = self.canvas.itemcget(object_id, "dash")
                    self.copied_object.append({"type": "rectangle", "coords": coords, "color": color, "corner_style": corner_style})
        if len(self.selected_objects) == 1:
            object_id = self.selected_objects[0]
            object_type = self.canvas.type(object_id)
            coords = self.canvas.coords(object_id)
            
            if object_type == "line":
                color = self.canvas.itemcget(object_id, "fill")
                self.copied_object = {"type": "line", "coords": coords, "color": color}
            elif object_type == "rectangle":
                color = self.canvas.itemcget(object_id, "outline")
                corner_style = self.canvas.itemcget(object_id, "dash")
                self.copied_object = {"type": "rectangle", "coords": coords, "color": color, "corner_style": corner_style}


    def paste_object(self, event=None):
        if self.copied_object:
            if isinstance(self.copied_object, list):
                # Pasting grouped objects
                new_group_id = f"group_{len(self.groups) + 1}"
                for obj_data in self.copied_object:
                    object_type = obj_data["type"]
                    old_coords = obj_data["coords"]
                    color = obj_data["color"]
                    corner_style = obj_data.get("corner_style", ())
                    
                    # Calculate the displacement from the original position to the mouse click position
                    if event:
                        dx = event.x - old_coords[0]
                        dy = event.y - old_coords[1]
                    else:
                        dx, dy = 0, 0
                    
                    # Calculate the new coordinates based on the mouse click position
                    new_coords = [coord + dx if i % 2 == 0 else coord + dy for i, coord in enumerate(old_coords)]
                    
                    if object_type == "line":
                        new_object = self.canvas.create_line(*new_coords, fill=color)
                    elif object_type == "rectangle":
                        new_object = self.canvas.create_rectangle(*new_coords, outline=color, width=2, dash=corner_style)
                    
                    self.canvas.addtag_withtag(new_group_id, new_object)
                
                self.groups.append(new_group_id)
                self.selected_group = new_group_id
            else:
                self.isLastSaved = False
                object_type = self.copied_object["type"]
                old_coords = self.copied_object["coords"]
                color = self.copied_object["color"]
                corner_style = self.copied_object.get("corner_style", ())
                
                # Calculate the displacement from the original position to the mouse click position
                if event:
                    dx = event.x - old_coords[0]
                    dy = event.y - old_coords[1]
                else:
                    dx, dy = 0, 0
                
                # Calculate the new coordinates based on the mouse click position
                new_coords = [coord + dx if i % 2 == 0 else coord + dy for i, coord in enumerate(old_coords)]
                
                if object_type == "line":
                    new_object = self.canvas.create_line(*new_coords, fill=color)
                elif object_type == "rectangle":
                    new_object = self.canvas.create_rectangle(*new_coords, outline=color, width=2, dash=corner_style)
                # ! Made this change not know corrrect or not 
                # self.selected_objects = [new_object]


        
    def move_object(self):
        if self.selected_group:
            dx = simpledialog.askinteger("Move Group", "Enter horizontal displacement:")
            dy = simpledialog.askinteger("Move Group", "Enter vertical displacement:")
            if dx is not None and dy is not None:
                for object_id in self.canvas.find_withtag(self.selected_group):
                    self.canvas.move(object_id, dx, dy)
        elif len(self.selected_objects) == 1:
            self.isLastSaved = False
            object_id = self.selected_objects[0]
            dx = simpledialog.askinteger("Move Object", "Enter horizontal displacement:")
            dy = simpledialog.askinteger("Move Object", "Enter vertical displacement:")
            if dx is not None and dy is not None:
              self.canvas.move(object_id, dx, dy)
        
    def group_objects(self):
        if len(self.selected_objects) > 1:
            group_id = f"group_{len(self.groups) + 1}"
            for object_id in self.selected_objects:
                self.canvas.addtag_withtag(group_id, object_id)
            self.groups.append(group_id)
            self.selected_objects.clear()
            self.selected_group = group_id

    def ungroup_objects(self):
        if self.selected_group:
            group_objects = self.canvas.find_withtag(self.selected_group)
            for object_id in group_objects:
                self.canvas.dtag(object_id, self.selected_group)
            self.groups.remove(self.selected_group)
            self.selected_group = None


        
    def save_drawing(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            self.isLastSaved = True
            with open(file_path, "w") as file:
                objects = self.canvas.find_all()
                for object_id in objects:
                    object_type = self.canvas.type(object_id)
                    coords = self.canvas.coords(object_id)
                    
                    if object_type == "line":
                        color = self.canvas.itemcget(object_id, "fill")
                        file.write(f"line,{coords[0]},{coords[1]},{coords[2]},{coords[3]},{self.colour[color]}\n")
                        # ! Why 4 cordinates in line
                    elif object_type == "rectangle":
                        color = self.canvas.itemcget(object_id, "outline")
                        corner_style = self.canvas.itemcget(object_id, "dash")
                        save_corner_style = None
                        print(type(corner_style))
                        if corner_style=="":
                          save_corner_style = "s"
                        elif corner_style=="5 5":
                          save_corner_style = "r"
                        file.write(f"rectangle,{coords[0]},{coords[1]},{coords[2]},{coords[3]},{self.colour[color]},{save_corner_style}\n")
                for group_id in self.groups:
                    file.write(f"group_start\n")
                    group_objects = self.canvas.find_withtag(group_id)
                    for object_id in group_objects:
                        object_type = self.canvas.type(object_id)
                        coords = self.canvas.coords(object_id)
                        
                        if object_type == "line":
                            color = self.canvas.itemcget(object_id, "fill")
                            file.write(f"line,{coords[0]},{coords[1]},{coords[2]},{coords[3]},{self.colour[color]}\n")
                        elif object_type == "rectangle":
                            color = self.canvas.itemcget(object_id, "outline")
                            corner_style = self.canvas.itemcget(object_id, "dash")
                            save_corner_style = "r" if corner_style else "s"
                            file.write(f"rectangle,{coords[0]},{coords[1]},{coords[2]},{coords[3]},{self.colour[color]},{save_corner_style}\n")
                    file.write(f"group_end\n")



    def load_drawing(self, file_path=None):
        print("File path:", file_path)  # Debugging
        if file_path:
            self.canvas.delete("all")
            if file_path.endswith(".xml"):
                print("Importing XML file")  # Debugging
                self.xml.import_from_xml(file_path)  # This line should call the import_from_xml function
            else:
                # Loading from non-XML file types
                with open(file_path, "r") as file:
                    INgRP=False
                    for line in file:
                        line = line.strip()
                        if line == "group_start":
                            # current_group = f"group_{len(self.groups) + 1}"
                            # group_objects = []
                            INgRP=True
                        elif line == "group_end":
                            INgRP=False
                        elif INgRP==False:
                            data = line.strip().split(",")
                            object_type = data[0]
                            coords = [float(x) for x in data[1:5]]
                            color = data[5]
                            color_open = self.color2[color]
                            if object_type == "line":
                                self.canvas.create_line(*coords, fill=color_open)
                            elif object_type == "rectangle":
                                # corner_style = tuple(map(int, data[6][1:-1].split(", "))) if data[6] else ()
                                if data[6] == "r":
                                    corner_style = "5 5"
                                else:
                                    corner_style = ""
                                self.canvas.create_rectangle(*coords, outline=color_open, width=1, dash=corner_style)

    
    def open_drawing(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.canvas.delete("all")
            self.selected_objects.clear()
            self.selected_group = None
            self.groups.clear()
            self.objects.clear()

            if file_path.endswith(".xml"):
                # self.load_drawing(file_path)
                self.xml.import_from_xml(file_path)
            else:
                with open(file_path, "r") as file:
                    current_group = None
                    group_objects = []
                    INgRP=False
                    for line in file:
                        line = line.strip()
                        if line == "group_start":
                            # current_group = f"group_{len(self.groups) + 1}"
                            # group_objects = []
                            INgRP=True
                        elif line == "group_end":
                            INgRP=False
                        elif INgRP==False:
                            data = line.strip().split(",")
                            object_type = data[0]
                            coords = [float(x) for x in data[1:5]]
                            color = data[5]
                            color_open = self.color2[color]
                            if object_type == "line":
                                self.canvas.create_line(*coords, fill=color_open)
                            elif object_type == "rectangle":
                                if data[6] == "r":
                                    corner_style = "5 5"
                                else:
                                    corner_style = ""
                                self.canvas.create_rectangle(*coords, outline=color_open, width=1, dash=corner_style)


  


# class DrawingCanvas:





if __name__ == "__main__":
    root = tk.Tk()
    editor = DrawingEditor(root)
    root.mainloop()