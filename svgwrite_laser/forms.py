#!/usr/bin/env python
# coding:utf-8
# Author:  ya-induhvidual
# Modified
# Copyright (C) 2019, Christof Hanke
# License: MIT License
from __future__ import unicode_literals
import math

from svgwrite.extensions.shapes import ngon
import svgwrite_laser.generators as generators
from svgwrite_laser.utils import TransGroup, TransformMixin, MarginsMixin

class ext_polygon(TransGroup):

    def __init__(self, dwg, num_corners, edge):
        """
        class for creating regular polygons with 
        a decorated edge.
        """
        TransGroup.__init__(self, dwg)
        self.edge_type = edge
        self.corners = list(ngon(num_corners, self.edge_type.length))
        self.edges = list(generators.edges(self.corners))
       
        for ed in self.edges:
            self.edge_type.reset()
            self.edge_type.transform(ed[0], ed[1])
            self.add_member(self.edge_type)
        return

