#!/usr/bin/env python
# Initially based on https://github.com/CadQuery/cadquery/blob/master/examples/Ex023_Sweep.py
import cadquery as cq
from cadquery.vis import show
import sys

if len(sys.argv) <= 1 or len(sys.argv) > 3:
    print("Usage: cq-sweep.py pts=<list> tangents=<list>")
    print('Example: cq-sweep.py pts="[(0,0,0),(10,0,10)]" tangents="[(0,0,1),(10,0,10)]"')
    print(" Note: Order doesn't matter and tangents are optional.")

    sys.exit(1)

# Parse the arguments
for arg in sys.argv[1:]:
    if "=" not in arg:
        print(f"Invalid argument: {arg}")
        sys.exit(1)
    key, value = arg.split("=")
    if key == "pts":
        pts = eval(value)
    elif key == "tangents":
        tangents = eval(value)
    else:
        print(f"Unknown argument: {key}")
        sys.exit(1)

print(f"pts: {pts}")
print(f"tangents: {tangents}")

path = cq.Workplane("XY").spline(pts, tangents)

# Create a cylinder with a radius of 0.5 along the path
cylinder = cq.Workplane("XY").circle(0.5).sweep(path)
show(cylinder)
