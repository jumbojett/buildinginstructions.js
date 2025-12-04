# Isometric LEGO Builder

This is a simple isometric LEGO builder repurposing the `buildinginstructions.js` library.

## How to use

1.  Open `isometric_builder.html` in a browser (served via a web server).
2.  The sidebar lists available parts (from `ldraw_parts` directory).
3.  Click on a part name to add it to the scene.
4.  Move the mouse to position the part on the grid.
5.  Press 'R' to rotate the part 90 degrees.
6.  Click to place the part.
7.  Click another part in the list to add another one.

## Setup

1.  Ensure `parts.json` is generated. If not, run:
    ```bash
    python3 generate_parts_json.py
    ```
2.  Serve the directory:
    ```bash
    python3 -m http.server
    ```
3.  Navigate to `http://localhost:8000/isometric_builder.html`.

## Features

-   Isometric view (Orthographic camera).
-   Part picker with search.
-   Drag and drop placement (snapping to grid).
-   Rotation support.
