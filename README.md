# cq-sweep

Explore using cadquery workplane.sweep which sweeps along a spline.
Using https://github.com/CadQuery/cadquery/blob/v2.5.2/examples/Ex023_Sweep.py as a base.


## Install

### Prerequisites

- Python 3.12 or later
- [direnv](https://direnv.net/) (optional but recommended)
- pip

### Installing

This repo has a dependency on cadquery with a patch and thus it's added to this
repo as a submodule. I've configured this repo so that it's easy to install
and test if you have `direnv` installed.


You can clone this repo with our without using --recursive. Below
is an example of using --recursive:

```bash
wink@3900x 25-05-15T00:15:24.577Z:~/data/prgs/3dprinting
$ git clone git@github.com:winksaville/cq-sweep --recursive cq-sweep-2
Cloning into 'cq-sweep-2'...
remote: Enumerating objects: 61, done.
remote: Counting objects: 100% (61/61), done.
remote: Compressing objects: 100% (37/37), done.
remote: Total 61 (delta 22), reused 60 (delta 21), pack-reused 0 (from 0)
Receiving objects: 100% (61/61), 1.49 MiB | 4.66 MiB/s, done.
Resolving deltas: 100% (22/22), done.
Submodule 'deps/cadquery' (https://github.com/winksaville/cadquery) registered for path 'deps/cadquery'
Cloning into '/home/wink/data/prgs/3dprinting/cq-sweep-2/deps/cadquery'...
remote: Enumerating objects: 11019, done.        
remote: Counting objects: 100% (40/40), done.        
remote: Compressing objects: 100% (35/35), done.        
remote: Total 11019 (delta 22), reused 6 (delta 5), pack-reused 10979 (from 2)        
Receiving objects: 100% (11019/11019), 10.00 MiB | 13.90 MiB/s, done.
Resolving deltas: 100% (7968/7968), done.
Submodule path 'deps/cadquery': checked out '1527bf7c878b67413ac0bace0e728d2fca64df1e'
wink@3900x 25-05-15T00:15:49.954Z:~/data/prgs/3dprinting
$ cd cq-sweep-2/
direnv: error /home/wink/data/prgs/3dprinting/cq-sweep-2/.envrc is blocked. Run `direnv allow` to approve its contentwink@3900x 25-05-15T00:15:55.547Z:~/data/prgs/3dprinting/cq-sweep-2 (main)
$ direnv allow
direnv: loading ~/data/prgs/3dprinting/cq-sweep-2/.envrc
Installing cadquery immutably from deps/cadquery
direnv: ([/usr/bin/direnv export bash]) is taking a while to execute. Use CTRL-C to give up.

[notice] A new release of pip is available: 25.0.1 -> 25.1.1
[notice] To update, run: pip install --upgrade pip
direnv: export +VIRTUAL_ENV ~PATH
wink@3900x 25-05-15T00:16:26.452Z:~/data/prgs/3dprinting/cq-sweep-2 (main)
$ ./cq-sweep.py --pts="[(0,0,0),(10,0,10)]"
Top face angles: {'XY': 44.99999999999991, 'XZ': 89.9999999999999, 'YZ': 45.00000000000009}
Bottom face angles: {'XY': 134.99999999999997, 'XZ': 89.99999999999999, 'YZ': 135.00000000000003}
wink@3900x 25-05-15T00:16:41.104Z:~/data/prgs/3dprinting/cq-sweep-2 (main)
```

And here is an example of using `git clone` without the --recursive option:

```bash
wink@3900x 25-05-15T00:16:41.104Z:~/data/prgs/3dprinting/cq-sweep-2 (main)
$ cd ..
direnv: unloading
wink@3900x 25-05-15T00:16:50.042Z:~/data/prgs/3dprinting
$ git clone git@github.com:winksaville/cq-sweep cq-sweep-3
Cloning into 'cq-sweep-3'...
remote: Enumerating objects: 61, done.
remote: Counting objects: 100% (61/61), done.
remote: Compressing objects: 100% (37/37), done.
remote: Total 61 (delta 22), reused 60 (delta 21), pack-reused 0 (from 0)
Receiving objects: 100% (61/61), 1.49 MiB | 4.45 MiB/s, done.
Resolving deltas: 100% (22/22), done.
wink@3900x 25-05-15T00:17:02.133Z:~/data/prgs/3dprinting
$ cd cq-sweep-3
direnv: error /home/wink/data/prgs/3dprinting/cq-sweep-3/.envrc is blocked. Run `direnv allow` to approve its contentwink@3900x 25-05-15T00:17:14.227Z:~/data/prgs/3dprinting/cq-sweep-3 (main)
$ direnv allow
direnv: loading ~/data/prgs/3dprinting/cq-sweep-3/.envrc
Initializing cq-sweep/deps/cadquery
Submodule 'deps/cadquery' (https://github.com/winksaville/cadquery) registered for path 'deps/cadquery'
Cloning into '/home/wink/data/prgs/3dprinting/cq-sweep-3/deps/cadquery'...
Submodule path 'deps/cadquery': checked out '1527bf7c878b67413ac0bace0e728d2fca64df1e'
Installing cadquery immutably from deps/cadquery
direnv: ([/usr/bin/direnv export bash]) is taking a while to execute. Use CTRL-C to give up.

[notice] A new release of pip is available: 25.0.1 -> 25.1.1
[notice] To update, run: pip install --upgrade pip
direnv: export +VIRTUAL_ENV ~PATH
wink@3900x 25-05-15T00:17:30.894Z:~/data/prgs/3dprinting/cq-sweep-3 (main)
$ ./cq-sweep.py --pts="[(0,0,0),(10,0,10)]"
Top face angles: {'XY': 44.99999999999991, 'XZ': 89.9999999999999, 'YZ': 45.00000000000009}
Bottom face angles: {'XY': 134.99999999999997, 'XZ': 89.99999999999999, 'YZ': 135.00000000000003}
wink@3900x 25-05-15T00:17:54.629Z:~/data/prgs/3dprinting/cq-sweep-3 (main)
```

## Usage

```bash
$ ./cq-sweep.py -h
usage: cq-sweep.py [-h] [-br BASE_RADIUS] [-tr TOP_RADIUS] [-ml MID_LOCATION] [-p PTS] [-t TANGENTS] [-r ROLL] [-oas OUTPUT_ASCII_STL]
                   [-opng OUTPUT_PNG]

Sweep a cylinder along a path defined by points and optional tangents.

options:
  -h, --help            show this help message and exit
  -br, --base_radius BASE_RADIUS
                        Base radius of the cylinder. Example: --base_radius=0.5
  -tr, --top_radius TOP_RADIUS
                        Top radius of the cylinder. Example: --top_radius=0.15
  -ml, --mid_location MID_LOCATION
                        Location of mid section where transition begins to top_radius. value between 0..1. Example: --mid_location=0.5
  -p, --pts PTS         List of points defining the path. Example: --pts='[(0,0,0),(10,0,10)]'
  -t, --tangents TANGENTS
                        List of tangents for the path. Example: --tangents='[(0,0,1),(10,0,20)]'
  -r, --roll ROLL       Roll angle. Example: --roll=90
  -oas, --output-ascii-stl OUTPUT_ASCII_STL
                        Output an ASCII stl file. Example: --output-ascii-stl=filename' result is 'filename.stl'
  -opng, --output-png OUTPUT_PNG
                        Output as `.png` screenshot. Example: --output-png=filename' result is 'filename.png'
```

## Examples

Straight tapered cylinder along a 45 degree spline with no tangents.

Result:
 - Top face is 45 degrees to the XY and YZ planes and perpendicular to XZ plane.
 - bottom face is parallel to XY and about 45 degrees to the XZ and YZ planes.
```bash
$ ./cq-sweep.py --pts="[(0,0,0),(10,0,10)]" -opng=s1
Top face angles: {'XY': 44.99999999999991, 'XZ': 89.9999999999999, 'YZ': 45.00000000000009}
Bottom face angles: {'XY': 134.99999999999997, 'XZ': 89.99999999999999, 'YZ': 135.00000000000003}
```
![straight cylinder at an angle](./s1.png)

---
Partial-S shaped tapered cylinder along a 45 degree spline with 1 unit long vertical tangents for the bottom and top faces.

Result:
 - Top face is about 45 degrees to the XY and YZ planes and perpendicular to XZ plane.
 - bottom face is parallel to XY and perpendicular to XZ and YZ planes.
```bash
$ ./cq-sweep.py --pts="[(0,0,0),(10,0,10)]" --tangents="[(0,0,1),(10,0,11)]" -opng=s2
Top face angles: {'XY': 42.273689006093655, 'XZ': 89.9999999999999, 'YZ': 47.72631099390635}
Bottom face angles: {'XY': 179.99999999999997, 'XZ': 89.99999999999999, 'YZ': 89.99999999999999}
```
![curved cylinder at an angle](./s2.png)

---
Partial-S shaped tapered cylinder along a 45 degree spline with 1 unit long vertical tangents for the bottom face
and a 1 unit horizontal tangent for the top face.

Result:
 - Top face is about 45 degrees to the XY and YZ planes and perpendicular to XZ plane.
 - bottom face is parallel to XY and perpendicular to XZ and YZ planes.
```bash
$ ./cq-sweep.py --pts="[(0,0,0),(10,0,10)]" --tangents="[(0,0,1),(9,0,10)]" -opng=s3
Top face angles: {'XY': 41.987212495816685, 'XZ': 90.00000000000017, 'YZ': 48.01278750418332}
Bottom face angles: {'XY': 179.99999999999997, 'XZ': 90.0, 'YZ': 90.00000000000004}
Bottom face angles: {'XY': 180.0, 'XZ': 90.0, 'YZ': 90.0}
```
![curved cylinder at an angle](./s3.png)

---
Partial-S shaped tapered cylinder along a 45 degree spline with 1 unit long vertical tangents for the bottom face
and a 0 unit tangent for the top face.

Result:
 - Top face is 45 degrees to the XY and YZ planes and perpendicular to XZ plane.
 - bottom face is parallel to XY and perpendicular to XZ and YZ planes.
```bash
$ ./cq-sweep.py -p="[(0,0,0),(10,0,10)]" -t="[(0,0,1),(10,0,10)]" -opng=s4
Top face angles: {'XY': 44.99999999999977, 'XZ': 89.99999999999991, 'YZ': 45.00000000000023}
Bottom face angles: {'XY': 179.99999999999991, 'XZ': 90.00000000000003, 'YZ': 89.99999999999993}
```
![curved cylinder at an angle](./s4.png)

---
Semi-S shaped cylinder along a 45 degree spline with 1 unit long vertical tangents for the bottom face
and a 10 unit horizontal tangent for the top face.

Result:
 - Top face is parallel to XY and perpendicular to XZ and XZ plane.
 - bottom face is parallel to XY and perpendicular to XZ and YZ planes.
```bash
$ ./cq-sweep.py -p="[(0,0,0),(10,0,10)]" -t="[(0,0,1),(0,0,10)]" -opng=s5
Top face angles: {'XY': 2.0524441350911866e-13, 'XZ': 90.00000000000006, 'YZ': 89.99999999999982}
Bottom face angles: {'XY': 179.99999999999997, 'XZ': 90.00000000000003, 'YZ': 90.0}
```
![curved cylinder at an angle](./s5.png)

---
An arc tapered cylinder along a 45 degree spline with 1 unit long vertical tangents for the bottom face
and a 10 unit long vertical tangent for the bottom face.

Result:
 - Top face is perpendicular to XY and XZ planes and parallelto YZ plane.
 - bottom face is parallel to XY and perpendicular to XZ and YZ planes.
```bash
$ ./cq-sweep.py -p="[(0,0,0),(10,0,10)]" -t="[(0,0,1),(10,0,0)]" --zoom=0.6 -opng=s6
Top face angles: {'XY': 90.0000000000001, 'XZ': 90.0, 'YZ': 1.0438743197066534e-13}
Bottom face angles: {'XY': 179.99999999999997, 'XZ': 90.00000000000003, 'YZ': 90.00000000000003}
```
![arc cylinder at an angle](./s6.png)

---

Semi-S shaped cylinder along a 45 degree spline with 1 unit long vertical tangents for the bottom face
and a 10 unit horizontal tangent for the top face.

Here pasing more parameters, more info in the future.

Result:
 - Top face is parallel to XY and perpendicular to XZ and XZ plane.
 - bottom face is parallel to XY and perpendicular to XZ and YZ planes.
```bash
$ ./cq-sweep.py -p="[(0,0,0),(10,0,10)]" -t="[(0,0,1),(0,0,10)]" -s=False --roll=0 --elevation=0 --azimuth=35 -pos="(5,-20,5)" -vu="(0,0,1)" -fp="(5,0,5)" -cr="(1,1000)" -z=0.75 -opng=s7
Top face angles: {'XY': 2.0524441350911866e-13, 'XZ': 90.00000000000006, 'YZ': 89.99999999999982}
Bottom face angles: {'XY': 179.99999999999997, 'XZ': 90.00000000000003, 'YZ': 90.0}
vis show:+                                                  camera orientation: pos=(   0.00,    0.00,    1.00) fp=(   0.00,    0.00,    0.00) vu=(   0.00,    1.00,    0.00) dis=1.00    va=30.00   cr=(   0.01, 1000.01)      o=(   0.00,   -0.00,    0.00) owxyz=(   0.00,    0.00,    0.00,    1.00)
vis show: get camera                                        camera orientation: pos=(   0.00,    0.00,    1.00) fp=(   0.00,    0.00,    0.00) vu=(   0.00,    1.00,    0.00) dis=1.00    va=30.00   cr=(   0.01, 1000.01)      o=(   0.00,   -0.00,    0.00) owxyz=(   0.00,    0.00,    0.00,    1.00)
vis show: before camera.ResetCamera()                       camera orientation: pos=(   0.00,    0.00,    1.00) fp=(   0.00,    0.00,    0.00) vu=(   0.00,    1.00,    0.00) dis=1.00    va=30.00   cr=(   0.01, 1000.01)      o=(   0.00,   -0.00,    0.00) owxyz=(   0.00,    0.00,    0.00,    1.00)
vis show: after camera.ResetCamera()                        camera orientation: pos=(   4.83,    0.00,   33.31) fp=(   4.83,    0.00,    5.00) vu=(   0.00,    1.00,    0.00) dis=28.31   va=30.00   cr=(  18.08,   41.26)      o=(   0.00,   -0.00,    0.00) owxyz=(   0.00,    0.00,    0.00,    1.00)
vis show: camera.SetViewUp((0.00, 0.00, 1.00))              camera orientation: pos=(   4.83,    0.00,   33.31) fp=(   4.83,    0.00,    5.00) vu=(   0.00,    0.00,    1.00) dis=28.31   va=30.00   cr=(  18.08,   41.26)      o=(   0.00,   -0.00,    0.00) owxyz=( 180.00,    0.00,    0.00,    1.00)
vis show: camera.SetPosition((5.00, -20.00, 5.00))          camera orientation: pos=(   5.00,  -20.00,    5.00) fp=(   4.83,    0.00,    5.00) vu=(   0.00,    0.00,    1.00) dis=20.00   va=30.00   cr=(  18.08,   41.26)      o=( -89.51,  -90.00,  -90.00) owxyz=( 270.00,    1.00,    0.00,    0.00)
vis show: camera.SetFocalPoint((5.00, 0.00, 5.00))          camera orientation: pos=(   5.00,  -20.00,    5.00) fp=(   5.00,    0.00,    5.00) vu=(   0.00,    0.00,    1.00) dis=20.00   va=30.00   cr=(  18.08,   41.26)      o=( -90.00,   -0.00,    0.00) owxyz=(  90.00,   -1.00,    0.00,    0.00)
vis show: camera.SetClippingRange((1.00, 1000.00))          camera orientation: pos=(   5.00,  -20.00,    5.00) fp=(   5.00,    0.00,    5.00) vu=(   0.00,    0.00,    1.00) dis=20.00   va=30.00   cr=(   1.00, 1000.00)      o=( -90.00,   -0.00,    0.00) owxyz=(  90.00,   -1.00,    0.00,    0.00)
vis show: camera.Roll(0.0)                                  camera orientation: pos=(   5.00,  -20.00,    5.00) fp=(   5.00,    0.00,    5.00) vu=(   0.00,    0.00,    1.00) dis=20.00   va=30.00   cr=(   1.00, 1000.00)      o=( -90.00,   -0.00,    0.00) owxyz=(  90.00,   -1.00,    0.00,    0.00)
vis show: camera.Elevation(0.0)                             camera orientation: pos=(   5.00,  -20.00,    5.00) fp=(   5.00,    0.00,    5.00) vu=(   0.00,    0.00,    1.00) dis=20.00   va=30.00   cr=(   1.00, 1000.00)      o=( -90.00,   -0.00,    0.00) owxyz=(  90.00,   -1.00,    0.00,    0.00)
vis show: camera.Elevation(0.0)                             camera orientation: pos=(  16.47,  -16.38,    5.00) fp=(   5.00,    0.00,    5.00) vu=(   0.00,    0.00,    1.00) dis=20.00   va=30.00   cr=(   1.00, 1000.00)      o=( -55.00,  -90.00,  -90.00) owxyz=( 264.81,    0.91,    0.29,    0.29)
vis show: camera.Zoom(0.75)                                 camera orientation: pos=(  16.47,  -16.38,    5.00) fp=(   5.00,    0.00,    5.00) vu=(   0.00,    0.00,    1.00) dis=20.00   va=40.00   cr=(   1.00, 1000.00)      o=( -55.00,  -90.00,  -90.00) owxyz=( 264.81,    0.91,    0.29,    0.29)
vis show: before inter.Start                                camera orientation: pos=(  16.47,  -16.38,    5.00) fp=(   5.00,    0.00,    5.00) vu=(   0.00,    0.00,    1.00) dis=20.00   va=40.00   cr=(   1.00, 1000.00)      o=( -55.00,  -90.00,  -90.00) owxyz=( 264.81,    0.91,    0.29,    0.29)
vis show:-                                                  camera orientation: pos=(  16.47,  -16.38,    5.00) fp=(   5.00,    0.00,    5.00) vu=(   0.00,    0.00,    1.00) dis=20.00   va=40.00   cr=(   1.00, 1000.00)      o=( -55.00,  -90.00,  -90.00) owxyz=( 264.81,    0.91,    0.29,    0.29)
```

![curved cylinder at an angle](./s7.png)]

## License

Licensed under either of

- Apache License, Version 2.0 ([LICENSE-APACHE](LICENSE-APACHE) or http://apache.org/licenses/LICENSE-2.0)
- MIT license ([LICENSE-MIT](LICENSE-MIT) or http://opensource.org/licenses/MIT)

### Contribution

Unless you explicitly state otherwise, any contribution intentionally submitted
for inclusion in the work by you, as defined in the Apache-2.0 license, shall
be dual licensed as above, without any additional terms or conditions.
