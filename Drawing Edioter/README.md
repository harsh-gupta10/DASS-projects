README.txt

Drawing Editor
==============

This is a simple drawing editor implemented in Python using the Tkinter library. It allows you to create and manipulate basic shapes such as lines and rectangles.



How to Run
----------

1. Run the code file(DrawingEditor.py) to start the drawing editor:



2. The drawing editor window will open, and you can start creating and editing shapes.

Usage
-----
- Select the desired shape (line or rectangle) from the toolbar.
- Choose the color for the shape (black, red, green, or blue).
- For rectangles, you can choose the corner style (square or rounded).
- Click and drag on the canvas to create a shape.
- To select a shape, hold the Shift key and click on it. Selected shapes will have a thicker outline.
- Use the toolbar buttons to perform actions on selected shapes:
- Edit: Modify the color and corner style (for rectangles) of the selected shape.
- If multiple Objects then they cont be edited or moved or coppied so domnt do that 
- Delete: Remove the selected shape from the canvas.
- Copy: Copy the selected shape to the clipboard.
- Paste: Paste the copied shape onto the canvas at the Right mouse click position.
- Move: Move the selected shape by specifying horizontal and vertical displacements.
- To save the drawing, click the "Save" button and choose a file location.
- To open a saved drawing, click the "Open" button and select the file.
- To export the drawing as an XML file, click the "Export XML" button and choose a file 
- For Grouping Select few Objects and click Group 
- For Ungrouping Select a Group and click UNgroup 
- After ungrouping Deselect all (Deselect - similar to select)
location.


Limitations
- Group of Groups cant be made 
- Colour of Groups cant be changed 
- On opening Groups cant be loaded
- Groups can be only exported to XML not imported


Assumption 
- Rounded means Dashed (as no drawing method of Rounded directly on tkinter) 

Note
- The file DrawingEditor.py is an attempt at refactoring the original code that can be found in OriginalEditor.py. If in case the DrawingEditor.py doesn't work, kindly run the OriginalEditor.py file

Happy drawing!

The IIIT Paint Team
