#!/usr/bin/python3

import argparse
import copy
import math
import os
import sys

import svgwrite
from svgwrite import cm, mm
from svgwrite.extensions.shapes import *
from svgwrite_laser import edges, utils, forms

CANVAS_SIZE = (600, 600)
STROKE_WIDTH = 0.0001*mm
STROKE_WIDTH = "1"
STROKE = "black"
TOOTH_WIDTH=50
TOOTH_HEIGHT=30
MARGIN=100
EDGE_LEN = 400
MATERIAL_THICKNESS=10



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="generate toothed")
    parser.add_argument("--canvas", default="%s, %s" % (CANVAS_SIZE), help="canvas size as x,y in mm. Defaults to %s, %s" % (CANVAS_SIZE))
    parser.add_argument("--stroke-width", dest="stroke_width", default="%s" % (STROKE_WIDTH), help="stroke-width in mm. Defaults to %s" % (STROKE_WIDTH))
    parser.add_argument("filename", default="-", help="filename for output.  \"-\" writes to stdout.")
    
    cmd_opt = parser.parse_args()
    canvas_size = [ x.strip() for x in cmd_opt.canvas.split(",")]
    stroke_width = cmd_opt.stroke_width*mm


    dwg = svgwrite.Drawing(cmd_opt.filename, CANVAS_SIZE, debug=True)

    # columns 15 x 15 mmm
    # 4 toothed egde with tooth_depth = 5mm 
    # length = 400
    
    fingered_edge = edges.fingered(dwg, EDGE_LEN, TOOTH_WIDTH, TOOTH_HEIGHT, num_features=3)
    holed_edge = edges.holed(dwg, EDGE_LEN, TOOTH_WIDTH, MATERIAL_THICKNESS, num_features=3)

    base_plate = forms.ext_polygon(dwg, 7, holed_edge)
    base_plate.rotate(math.pi/4)
    base_plate.translate(200, 200)
    dwg.add(base_plate.generate_svg(fill="none", stroke_width=STROKE_WIDTH, stroke=STROKE))

    #side_plate = forms.ext_polygon(dwg, 4, fingered_edge)
    #side_plate.translate(100,100)
    #dwg.add(side_plate.generate_svg(fill="none", stroke_width=STROKE_WIDTH, stroke=STROKE))

    dwg.save()

    import xml.dom.minidom

    dom = xml.dom.minidom.parseString(dwg.tostring())
    pretty_xml_as_string = dom.toprettyxml()
    with open(cmd_opt.filename, "w") as o_file:
        o_file.write(pretty_xml_as_string)


