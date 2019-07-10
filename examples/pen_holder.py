
def main(name):
    """
    laser-cutting plan for a square box standing on a brim, useful for
    storing pens etc.
    """
    canvas_x = 1000
    canvas_y = 1000
    style = {"fill": "none", "stroke": "black", "stroke-width": "1"}
    edge_length = 100
    long_edge = 100
    short_edge = 50
    brim_width = 50
    finger_width = 5
    finger_distance = 5
    # thickness of the plywood to cut
    material_thickness = 3
    margins = [(10, 0), 
               (10, 10), 
               (0, 10), 
               (0, 10) 
            ]
    origins = [(10, 10),
               (120, 10),
               (10, 70),
               (120, 70),
            ]
    origin_brim = (90,200)
    dwg = svgwrite.Drawing(name + ".svg", (canvas_x, canvas_y), debug=True)

    # brim
    dwg.add(dwg.polygon(translate(ngon(4, edge_length=edge_length + brim_width, rotation=math.pi/4), origin_brim[0], origin_brim[1]), **style))
    for corner, next_corner in edges(translate(ngon(4, edge_length=edge_length, rotation=math.pi/4), origin_brim[0], origin_brim[1])):
        num_holes = 10
        points = []
        for num, vertix in enumerate(translate(holes(finger_width, material_thickness, num_holes=num_holes), origin_brim[0], origin_brim[1]), start=1):
            print("num, vertix: ", num, vertix)
            points.append(vertix)
            if num % 4 == 0:
                dwg.add(dwg.polygon(points, **style))
                print("points: ", points)
                points = []
    dwg.save(pretty=True)

if __name__ == '__main__':
    name = "finger_joint_example"
    main(name)
