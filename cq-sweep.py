#!/usr/bin/env python
# Initially based on https://github.com/CadQuery/cadquery/blob/master/examples/Ex023_Sweep.py
import cadquery as cq
from cadquery.vis import show
import sys
import argparse

argparse = argparse.ArgumentParser(description="Sweep a cylinder along a path defined by points and optional tangents.")
argparse.add_argument(
    "-p","--pts",
    type=str,
    help="List of points defining the path. Example: --pts='[(0,0,0),(10,0,10)]'",
)
argparse.add_argument(
    "-t","--tangents",
    type=str,
    default=None,
    help="List of tangents for the path. Example: --tangents='[(0,0,1),(10,0,20)]'",
)
args = argparse.parse_args()

# Check if the script is run with the correct number of arguments
if args.pts is None:
    print("No points provided.")
    sys.exit(1)

pts = eval(args.pts)
if args.tangents is not None:
    tangents = eval(args.tangents)
else:
    tangents = None

path = cq.Workplane("XY").spline(pts, tangents)

# Create a cylinder with a radius of 0.5 along the path
cylinder = cq.Workplane("XY").circle(0.5).sweep(path)
show(cylinder, title=f"pts: {pts}, tangents: {tangents}")
