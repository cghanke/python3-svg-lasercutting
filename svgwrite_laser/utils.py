from svgwrite.extensions.shapes import rotate, scale, translate
import math

class TransformMixin:
    """
    Apply transformations to self.points
    """

    def rotate(self, delta):
        """
        rotate this
        """
        self.points = list(rotate(self.points, delta))
        return

    def scale(self, scale_x, scale_y):
        """
        scale this
        """
        self.points = list(scale(self.points, scale_x, scale_y))
        return

    def translate(self, delta_x, delta_y):
        """
        translate this
        """
        self.points = list(translate(self.points, delta_x, delta_y))
        return

class TransGroup:
    """
    container for special edges
    """
    def __init__(self, dwg):
        self.members = []
        self.dwg = dwg

    def generate_svg(self, **extra):
        group_obj = self.dwg.g(**extra)
        for mem in self.members:
            group_obj.add(mem.generate_svg())
        return group_obj

    def add_member(self, member):
        from copy import deepcopy
        self.members.append(deepcopy(member))
        return len(self.members)

    def rotate(self, delta):
        """
        rotate all members
        """
        for mem in self.members:
            mem.rotate(delta)

    def scale(self, scale_x, scale_y):
        """
        scale all members
        """
        for mem in self.members:
            mem.scale(scale_x, scale_y)

    def translate(self, delta_x, delta_y):
        """
        translate all members
        """
        for mem in self.members:
            mem.translate(delta_x, delta_y)
        return

class MarginsMixin:

    def calculate_margins(self, num_features=-1):
        if num_features == -1:
            self.num_features = math.floor((self.length - self.margin_left - self.margin_right + self.inter_feature_distance)/(self.feature_width + self.inter_feature_distance))
            extra_margin = 0.5 * (self.length - self.margin_left - self.margin_right + self.inter_feature_distance - self.num_features * (self.feature_width + self.inter_feature_distance))
            self.margin_left += extra_margin
            self.margin_right += extra_margin
        elif num_features == 0:
            self.num_features = self.margin_left = self.margin_right = 0
        else:
            self.num_features = num_features
            self.margin_left = self.margin_right = 0.5 * (self.length + self.inter_feature_distance - self.num_features * (self.feature_width + self.inter_feature_distance))
        return 

