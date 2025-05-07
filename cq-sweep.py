#!/usr/bin/env python
# Initially based on https://github.com/CadQuery/cadquery/blob/master/examples/Ex023_Sweep.py
import cadquery as cq
from cadquery.vis import show
import sys
import argparse
import math

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

# Define the normal vectors for the XY, XZ, and YZ planes
xy_plane_normal = cq.Vector(0, 0, 1)
xz_plane_normal = cq.Vector(0, 1, 0)
yz_plane_normal = cq.Vector(1, 0, 0)

# Function to calculate the angle between the normal face and the plane normal
def angle_of_plane(normal, plane_normal):
    return math.degrees(normal.getAngle(plane_normal))

# Get the normal of the top face of the cylinder
top_face = cylinder.faces(">Z").first().val()
normal_top_face = top_face.normalAt(top_face.Center())

top_face_angles = {
    "XY": angle_of_plane(normal_top_face, xy_plane_normal),
    "XZ": angle_of_plane(normal_top_face, xz_plane_normal),
    "YZ": angle_of_plane(normal_top_face, yz_plane_normal),
}
print(f"Top face angles: {top_face_angles}")

# Get the normal of the bottom face of the cylinder
bottom_face = cylinder.faces("<Z").first().val()
normal_bottom_face = bottom_face.normalAt(bottom_face.Center())

bottom_face_angles = {
    "XY": angle_of_plane(normal_bottom_face, xy_plane_normal),
    "XZ": angle_of_plane(normal_bottom_face, xz_plane_normal),
    "YZ": angle_of_plane(normal_bottom_face, yz_plane_normal),
}
print(f"Bottom face angles: {bottom_face_angles}")

show(cylinder, title=f"pts: {pts}, tangents: {tangents}, angles XY:{top_face_angles["XY"]:.2f}, XZ:{top_face_angles["XZ"]:.2f}, YZ:{top_face_angles["YZ"]:.2f}")
