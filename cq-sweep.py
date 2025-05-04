#!/usr/bin/env python
# Initially based on https://github.com/CadQuery/cadquery/blob/master/examples/Ex023_Sweep.py
import cadquery as cq
from cadquery.vis import show

#pts = [(0, 0, 0), (0, 0, 1)] # path 2 points on Z axis
pts = [(0, 0, 0), (1, 1, 1)] # path 2 points 45 degrees diaginal to (1,1,1)
path = cq.Workplane("XY").spline(pts)

# Create a cylinder with a radius of 0.5 along the path
cylinder = cq.Workplane("XY").circle(0.5).sweep(path)
show(cylinder)
