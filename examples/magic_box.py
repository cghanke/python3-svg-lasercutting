#!/usr/bin/python3

import argparse
import os
import sys
import svgwrite
from svgwrite import cm, mm
from svgwrite.extensions.shapes import *
from svgwrite_laser import forms

CANVAS_SIZE = (600, 600)
STROKE_WIDTH = 0.0001*mm
STROKE_WIDTH = "1"
STROKE = "black"
TOOTH_WIDTH=50
TOOTH_DEPTH=30
MARGIN=100

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="generate toothed")
    parser.add_argument("--canvas", default="%s, %s" % (CANVAS_SIZE), help="canvas size as x,y in mm. Defaults to %s, %s" % (CANVAS_SIZE))
    parser.add_argument("--stroke-width", dest="stroke_width", default="%s" % (STROKE_WIDTH), help="stroke-width in mm. Defaults to %s" % (STROKE_WIDTH))
    parser.add_argument("filename", default="-", help="filename for output.  \"-\" writes to stdout.")
    
    cmd_opt = parser.parse_args()
    canvas_size = [ x.strip() for x in cmd_opt.canvas.split(",")]
    stroke_width = cmd_opt.stroke_width*mm

    #dwg = svgwrite.Drawing(cmd_opt.filename, CANVAS_SIZE,  profile='full', debug=True)
    dwg = svgwrite.Drawing(cmd_opt.filename, CANVAS_SIZE, debug=True)

    # columns 15 x 15 mmm
    # 4 toothed egde with tooth_depth = 5mm 
    # length = 400
    edge_1 = forms.ext_polygon(dwg, 0, 100,0)
    dwg.add(edge_1)
