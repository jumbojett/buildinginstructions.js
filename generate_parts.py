
def generate_header(filename, description):
    return f"0 {description}\n0 Name: {filename}\n0 Author: Generated\n0 !LICENSE Redistributable under CCAL version 2.0 : see CAlicense.txt\n\n"

def generate_stud(x, y, z, matrix="1 0 0 0 1 0 0 0 1"):
    return f"1 16 {x} {y} {z} {matrix} stud.dat\n"

def generate_box(x1, y1, z1, x2, y2, z2, color=16):
    # Generate quads for a box
    # Top
    s = f"4 {color} {x1} {y1} {z1} {x2} {y1} {z1} {x2} {y1} {z2} {x1} {y1} {z2}\n"
    # Bottom
    s += f"4 {color} {x1} {y2} {z2} {x2} {y2} {z2} {x2} {y2} {z1} {x1} {y2} {z1}\n"
    # Front
    s += f"4 {color} {x1} {y1} {z2} {x2} {y1} {z2} {x2} {y2} {z2} {x1} {y2} {z2}\n"
    # Back
    s += f"4 {color} {x2} {y1} {z1} {x1} {y1} {z1} {x1} {y2} {z1} {x2} {y2} {z1}\n"
    # Left
    s += f"4 {color} {x1} {y1} {z1} {x1} {y1} {z2} {x1} {y2} {z2} {x1} {y2} {z1}\n"
    # Right
    s += f"4 {color} {x2} {y1} {z2} {x2} {y1} {z1} {x2} {y2} {z1} {x2} {y2} {z2}\n"
    return s

def generate_slope(width_studs, length_studs, flat_studs=1):
    w = width_studs * 20
    l = length_studs * 20
    flat = flat_studs * 20
    h = 24
    
    x1 = -w/2
    x2 = w/2
    y_top = 0
    y_bot = 24
    z_back = -10
    z_flat_front = 10
    z_front = -10 + l
    
    s = ""
    
    # Top Flat
    s += f"4 16 {x1} {y_top} {z_back} {x2} {y_top} {z_back} {x2} {y_top} {z_flat_front} {x1} {y_top} {z_flat_front}\n"
    
    # Slope Face
    s += f"4 16 {x1} {y_top} {z_flat_front} {x2} {y_top} {z_flat_front} {x2} {y_bot} {z_front} {x1} {y_bot} {z_front}\n"
    
    # Back Face
    s += f"4 16 {x2} {y_top} {z_back} {x1} {y_top} {z_back} {x1} {y_bot} {z_back} {x2} {y_bot} {z_back}\n"
    
    # Bottom Face
    s += f"4 16 {x1} {y_bot} {z_back} {x2} {y_bot} {z_back} {x2} {y_bot} {z_front} {x1} {y_bot} {z_front}\n"
    
    # Side Left
    s += f"4 16 {x1} {y_top} {z_back} {x1} {y_top} {z_flat_front} {x1} {y_bot} {z_flat_front} {x1} {y_bot} {z_back}\n"
    s += f"3 16 {x1} {y_top} {z_flat_front} {x1} {y_bot} {z_front} {x1} {y_bot} {z_flat_front}\n"

    # Side Right
    s += f"4 16 {x2} {y_top} {z_flat_front} {x2} {y_top} {z_back} {x2} {y_bot} {z_back} {x2} {y_bot} {z_flat_front}\n"
    s += f"3 16 {x2} {y_top} {z_flat_front} {x2} {y_bot} {z_flat_front} {x2} {y_bot} {z_front}\n"
    
    stud_z = 0
    if width_studs == 1:
        s += generate_stud(0, 0, stud_z)
    elif width_studs == 2:
        s += generate_stud(-10, 0, stud_z)
        s += generate_stud(10, 0, stud_z)
    elif width_studs == 3:
        s += generate_stud(-20, 0, stud_z)
        s += generate_stud(0, 0, stud_z)
        s += generate_stud(20, 0, stud_z)
    elif width_studs == 4:
        s += generate_stud(-30, 0, stud_z)
        s += generate_stud(-10, 0, stud_z)
        s += generate_stud(10, 0, stud_z)
        s += generate_stud(30, 0, stud_z)
        
    return s

def generate_arch(width_studs):
    w = width_studs * 20
    h = 24
    d = 20
    leg_w = 10
    top_h = 4
    x1 = -w/2
    x2 = w/2
    
    # Top bar
    s = generate_box(x1, 0, -10, x2, top_h, 10)
    # Left Leg
    s += generate_box(x1, top_h, -10, x1+leg_w, h, 10)
    # Right Leg
    s += generate_box(x2-leg_w, top_h, -10, x2, h, 10)
    
    start_x = -(width_studs-1)*10
    for i in range(width_studs):
        cx = start_x + i*20
        s += generate_stud(cx, 0, 0)
        
    return s

def generate_brick_mod(sides_studs):
    s = generate_box(-10, 0, -10, 10, 24, 10)
    s += generate_stud(0, 0, 0)
    
    if sides_studs == 2:
        # Front
        s += "1 16 0 12 10 1 0 0 0 0 -1 0 1 0 stud.dat\n"
        # Right
        s += "1 16 10 12 0 0 0 -1 0 0 -1 -1 0 0 stud.dat\n"
    elif sides_studs == 4:
        # Front
        s += "1 16 0 12 10 1 0 0 0 0 -1 0 1 0 stud.dat\n"
        # Back
        s += "1 16 0 12 -10 -1 0 0 0 0 -1 0 -1 0 stud.dat\n"
        # Right
        s += "1 16 10 12 0 0 0 -1 0 0 -1 -1 0 0 stud.dat\n"
        # Left
        s += "1 16 -10 12 0 0 0 1 0 0 -1 1 0 0 stud.dat\n"
        
    return s

def generate_inv_slope():
    s = ""
    # Top Face
    s += "4 16 -20 0 -20 20 0 -20 20 0 20 -20 0 20\n"
    
    # Side 1 (Slope Left)
    s += "4 16 -20 0 -20 -20 0 20 0 24 20 0 24 -20\n"
    
    # Side 2 (Slope Right)
    s += "4 16 20 0 20 20 0 -20 0 24 -20 0 24 20\n"
    
    # End 1 (Triangle)
    s += "3 16 -20 0 -20 0 24 -20 20 0 -20\n"
    
    # End 2 (Triangle)
    s += "3 16 20 0 20 0 24 20 -20 0 20\n"
    
    # Studs
    s += generate_stud(-10, 0, -10)
    s += generate_stud(10, 0, -10)
    s += generate_stud(-10, 0, 10)
    s += generate_stud(10, 0, 10)
    
    return s

parts = {
    "3659.dat": generate_header("3659.dat", "Arch 1 x 4") + generate_arch(4),
    "4490.dat": generate_header("4490.dat", "Arch 1 x 3") + generate_arch(3),
    "3298.dat": generate_header("3298.dat", "Slope 33 3 x 2") + generate_slope(2, 3),
    "3297.dat": generate_header("3297.dat", "Slope 33 3 x 4") + generate_slope(4, 3),
    "4286.dat": generate_header("4286.dat", "Slope 33 3 x 1") + generate_slope(1, 3),
    "3676.dat": generate_header("3676.dat", "Slope, Inverted 45 2 x 2 Double Convex") + generate_inv_slope(),
    "26604.dat": generate_header("26604.dat", "Brick Modified 1 x 1 with Studs on 2 Sides") + generate_brick_mod(2),
    "4733.dat": generate_header("4733.dat", "Brick Modified 1 x 1 with Studs on 4 Sides") + generate_brick_mod(4)
}

for name, content in parts.items():
    print(f"--- {name} ---")
    print(content)
    print("--- END ---")
