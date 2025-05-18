#!/usr/bin/env python
# Initially based on https://github.com/CadQuery/cadquery/blob/master/examples/Ex023_Sweep.py
try:
    import cadquery as cq
    from cadquery import show
except ImportError:
    print("Err: CadQuery is not available, it is a submodule")
    print("     run `git submodule init` and `direnv allow` and")
    print("     try to execute cq-sweep again")
    exit(1)

import sys
import argparse
import math
#print(f"cadquery.__file__={cq.__file__} version={cq.__version__}")

default_mid_location = 0.5
default_base_radius = 0.5
default_top_radius = 0.15

argparse = argparse.ArgumentParser(description="Sweep a cylinder along a path defined by points and optional tangents.")
argparse.add_argument(
    "-br","--base_radius",
    type=float,
    default=default_base_radius,
    help=f"Base radius of the cylinder. Example: --base_radius={default_base_radius}",
)
argparse.add_argument(
    "-tr","--top_radius",
    type=float,
    default=default_top_radius,
    help=f"Top radius of the cylinder. Example: --top_radius={default_top_radius}",
)
argparse.add_argument(
    "-ml","--mid_location",
    type=float,
    default=default_mid_location,
    help=f"Location of mid section where transition begins to top_radius. value between 0..1. Example: --mid_location={default_mid_location}",
)
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
argparse.add_argument(
    "-vu","--view-up",
    type=str,
    default=None,
    help="ViewUp XYZ tuple. Example: --view-up='(0, 0, 1)'",
)
argparse.add_argument(
    "-pos","--position",
    type=str,
    default=None,
    help="Position XYZ tuple. Example: --position='(5.0, -20.0, 5.0)'",
)
argparse.add_argument(
    "-fp","--focal-point",
    type=str,
    default=None,
    help="Focal point XYZ tuple. Example: --focal-point='(5.0, 0.0, 5.0)'",
)
argparse.add_argument(
    "-cr","--clipping-range",
    type=str,
    default=None,
    help="Clipping range (near,far) tuple. Example: --clipping-range='(-0.1, 1000.01)'",
)
argparse.add_argument(
    "-z","--zoom",
    type=float,
    default=1,
    help="Camera Zoom for png. Example: --zoom=1",
)
argparse.add_argument(
    "-r","--roll",
    type=float,
    default=-35,
    help="Camera Roll angle for png. Example: --roll=-35",
)
argparse.add_argument(
    "-e","--elevation",
    type=float,
    default=-45,
    help="Camera Elevation for png. Example: --elevation=-45",
)
argparse.add_argument(
    "-a","--azimuth",
    type=float,
    default=0,
    help="Camera azimuth for png. Example: --azimuth=0",
)
argparse.add_argument(
    "-oas","--output-ascii-stl",
    type=str,
    default=None,
    help="Output an ASCII stl file. Example: --output-ascii-stl=filename' result is 'filename.stl'",
)
argparse.add_argument(
    "-s","--show",
    type=str,
    default="True",
    help="Show in with defaults",
)
argparse.add_argument(
    "-opng","--output-png",
    type=str,
    default=None,
    help="Output as `.png` screenshot. Example: --output-png=filename' result is 'filename.png'",
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

bottom_loc = [path.val().locationAt(0)]
middle_loc = [path.val().locationAt(args.mid_location)]
top_loc = [path.val().locationAt(1)]
#print(f"Bottom location: {bottom_loc[0].toTuple()}")
#print(f"middle location: {middle_loc[0].toTuple()}")
#print(f"top location: {top_loc[0].toTuple()}")

base_radius = 0.5
middle_radius = 0.5
top_radius = 0.15

wp = cq.Workplane("XY").pushPoints(bottom_loc).circle(base_radius)
wp = wp.pushPoints(middle_loc).circle(middle_radius)
wp = wp.pushPoints(top_loc).circle(top_radius)
#wp = wp.consolidateWires()
shape = wp.sweep(path, multisection=True)

# Define the normal vectors for the XY, XZ, and YZ planes
xy_plane_normal = cq.Vector(0, 0, 1)
xz_plane_normal = cq.Vector(0, 1, 0)
yz_plane_normal = cq.Vector(1, 0, 0)

# Function to calculate the angle between the normal face and the plane normal
def angle_of_plane(normal, plane_normal):
    return math.degrees(normal.getAngle(plane_normal))

# Get the normal of the top face of the cylinder
top_face = shape.faces(">Z").first().val()
#print(f"Top face: location={top_face.Center().toTuple()}")
normal_top_face = top_face.normalAt(top_face.Center())

top_face_angles = {
    "XY": angle_of_plane(normal_top_face, xy_plane_normal),
    "XZ": angle_of_plane(normal_top_face, xz_plane_normal),
    "YZ": angle_of_plane(normal_top_face, yz_plane_normal),
}
print(f"Top face angles: {top_face_angles}")

# Get the normal of the bottom face of the cylinder
bottom_face = shape.faces("<Z").first().val()
#print(f"Bottom face: location={bottom_face.Center().toTuple()}")
normal_bottom_face = bottom_face.normalAt(bottom_face.Center())

bottom_face_angles = {
    "XY": angle_of_plane(normal_bottom_face, xy_plane_normal),
    "XZ": angle_of_plane(normal_bottom_face, xz_plane_normal),
    "YZ": angle_of_plane(normal_bottom_face, yz_plane_normal),
}
print(f"Bottom face angles: {bottom_face_angles}")

if args.output_ascii_stl:
    # Export as ASCII STL
    cq.Assembly(shape).export(f"{args.output_ascii_stl}.stl", exportType="STL", ascii=True)

# Show the shape in the viewer
if args.show == "True":
    show(shape, width=800, height=600, title=f"pts: {pts}, tangents: {tangents}, angles XY:{top_face_angles["XY"]:.2f}, XZ:{top_face_angles["XZ"]:.2f}, YZ:{top_face_angles["YZ"]:.2f}")

# Write the shape to a file if output_png is specified
if args.output_png:
    vu = eval(args.view_up) if args.view_up else None
    pos = eval(args.position) if args.position else None
    focus_loc = eval(args.focal_point) if args.focal_point else None
    clipping_range = eval(args.clipping_range) if args.clipping_range else None
    #print(f"vu={vu}, pos={pos}, focus_loc={focus_loc}")
    show(
        shape,
        width=800,
        height=600,
        zoom=args.zoom,
        roll=args.roll,
        elevation=args.elevation,
        azimuth=args.azimuth,
        viewup=vu,
        position=pos,
        focus=focus_loc,
        clipping_range=clipping_range,
        interact=True,
        screenshot=f"{args.output_png}.png",
    )

