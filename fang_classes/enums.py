import enum

class ShapeType(enum.IntEnum):
  Point = 0
  Line = 1
  Spline = 2
  Box = 3
  Sphere = 4
  Cylinder = 5
  Mesh = 6

class CSVFieldType(enum.IntEnum):
  String = 0
  Float = 1
  Widestring = 2
