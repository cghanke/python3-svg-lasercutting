"""
Special edges as used in lasercutting
"""

import math

from svgwrite_laser.utils import TransformMixin, MarginsMixin
from svgwrite_laser.generators import rectangle
from svgwrite_laser.utils import TransGroup
from svgwrite.extensions.shapes import rotate, scale, translate

class edge(TransformMixin, MarginsMixin):
    """
    Base class for edges
    """
    def __init__(self):
        self.points = []
        return

    def transform(self, new_start, new_end):
        """
        transform this edge to different start and end points.
        The features keep their shape
        """
        # set new length
        x = new_end[0] - new_start[0]
        y = new_end[1] - new_start[1]
        self.length = math.hypot(x, y)

        self.calculate_margins(self.original_num_features)
        self.reset(restore_length=False)
        angle = math.atan2(y, x)
        self.rotate(angle)
        self.translate(new_start[0], new_start[1])
        return


class fingered(edge):

    def __init__(self, dwg, length, feature_width, feature_height, inter_feature_distance=None, margin_left=0, margin_right=0, num_features=-1):
        """
        create a rectangular fingerjoint as polyline 
        """
        edge.__init__(self)
        self.dwg = dwg
        self.feature_height = feature_height
        self.feature_width = feature_width
        if inter_feature_distance:
            self.inter_feature_distance = inter_feature_distance
        else:
            self.inter_feature_distance = feature_width
        self.margin_left = margin_left 
        self.margin_right = margin_right 
        self.length = length
        # this survives transform()
        self.__original_length = length
        # this is required for transform()
        self.original_num_features = num_features

        self.reset()

    def reset(self, restore_length=True):
        """
        Reset all transformations done on this object
        """
        if restore_length:
            self.length = self.__original_length
        self.calculate_margins()
        self.points = [(0, 0)]
        self.points += list(translate(rectangle(self.feature_width, self.feature_height, self.inter_feature_distance, self.num_features), self.margin_left, 0))

        self.points += [(self.length, 0)]
        return 

    def generate_svg(self, **style):
        obj = self.dwg.polyline(self.points, **style)
        return  obj

class plain(edge):
    """ 
    straight line
    """
    def __init__(self, dwg, length):
        edge.__init__(self)
        self.dwg = dwg
        self.length = length
        # this survives transform()
        self.__original_length = length
        # this is required for transform()
        self.original_num_features = 0
        self.num_features = 0
        self.feature_width = 0
        self.feature_height = 0
        self.inter_feature_distance = 0
        self.margin_left = self.margin_right = 0
        self.reset()
        return

    def generate_svg(self, **style):
        obj = self.dwg.polyline(self.points, **style)
        return  obj

    def transform(self, new_start, new_end):
        return 

    def reset(self, restore_length=True):
        """
        Reset all transformations done on this object
        """
        if restore_length:
            self.length = self.__original_length
        self.points = [(0,0), (self.length,0)]


class hole(TransformMixin):
    """
    A simple transformable hole
    """

    def __init__(self, dwg, feature_width, feature_height):
        self.dwg = dwg
        self.feature_width = feature_width
        self.feature_height = feature_height
        return

    def reset(self, restore_length=True):
        self.points = list(rectangle(self.feature_width, self.feature_height, 0, 1))
        return

    def generate_svg(self, **style):
        obj = self.dwg.polygon(self.points, **style)
        return  obj

class holed(TransGroup, MarginsMixin):
    """
    create a plain edge with holes beside
    """
    def __init__(self, dwg, length, feature_width, feature_height, inter_feature_distance=None, margin_left=0, margin_right=0, num_features=-1 , feature_edge_distance=None):
        TransGroup.__init__(self, dwg)
        self.length = length
        self.feature_width = feature_width
        self.feature_height = feature_height
        if inter_feature_distance:
            self.inter_feature_distance = inter_feature_distance
        else:
            self.inter_feature_distance = feature_width
        self.margin_left = margin_left
        self.margin_right = margin_right
        self.hole_type = hole(self.dwg, self.feature_width, self.feature_height)
        self.edge_type = plain(self.dwg, self.length)
        self.__original_length = length
        self.original_num_features = num_features
        if feature_edge_distance:
            self.hole_edge_distance = 30
        else:
            self.hole_edge_distance = feature_height 
        self.calculate_margins(self.original_num_features)
        self.reset()
        return 

    def reset(self, restore_length=True):
        """
        reset all transformations on this group
        """
        if restore_length:
            self.length = self.__original_length
        self.calculate_margins(self.original_num_features)
        self.members = []
        self.add_member(self.edge_type)
        for hon in range(self.num_features):
            self.hole_type.reset()
            self.hole_type.translate(self.margin_left + hon * (self.feature_width + self.inter_feature_distance), self.hole_edge_distance)
            self.add_member(self.hole_type)
        return

    def transform(self, new_start, new_end):
        """
        transform this edge to different start and end points.
        The features keep their shape
        """
        # set new length
        x = new_end[0] - new_start[0]
        y = new_end[1] - new_start[1]
        self.length = math.hypot(x, y)

        self.reset(restore_length=False)
        angle = math.atan2(y, x)
        # this rotate, translate comes from TransGroup
        self.rotate(angle)
        self.translate(new_start[0], new_start[1])
        return


#
# not implemented yet
#

def ellipitic_finger_joint(dwg, identifier, origin, axis_x, axis_y, hole_distance, num_features,  margin=0, **extra):
    """
    create one part of a fingerjoint as a group of objects, the fingers are half-ellipses.
    """
    o_x = origin[0] + margin
    o_y = origin[1]
    clip_path = dwg.clipPath(id="%s_clippath" % identifier, clipPathUnits="objectBoundingBox")
    clip_path.add(dwg.rect((-0.1, -0.1), (1.2, 0.6)))
    dwg.defs.add(clip_path)
    group_obj = dwg.g(**extra)
    _line = dwg.line((origin[0], origin[1]), (origin[0] + margin, origin[1]))
    group_obj.add(_line)

    for hon in range(num_features):
        delta_x = hon * (hole_distance + 2*axis_x)
        _elli = dwg.ellipse(center=(o_x + axis_x +  delta_x, o_y), r=(axis_x, axis_y), clip_path="url(#%s_clippath)" % identifier)
        group_obj.add(_elli)
        if hon == num_features - 1:
            break
        _line = dwg.line((o_x + 2*axis_x + delta_x, o_y), (o_x + 2*axis_x + hole_distance + delta_x, origin[1]))
        group_obj.add(_line)
    _line = dwg.line((o_x + 2*axis_x + delta_x, o_y), ( o_x + 2*axis_x + margin + delta_x, o_y))
    group_obj.add(_line)
    return group_obj

class elliptic_fingered(edge):
    """
    Fingered line, where finger-holes are half-ellipses
    """

    def __init__(self, dwg, length):
        edge.__init__(self)
        return 

    def generate_svg(self, **style):
        obj = self.dwg.polyline(self.points)
        return  obj
