"""Simple Utilities for Digital Humans

    >>> import dhutils as dhu
    >>> human = dhu.load_SkinnedMesh (glTF_file_path)
    >>> viewer = dhu.viewer(human)
    >>> viewer
    """

# %%
import math
import numpy as np
from pathlib import Path
from scipy.spatial.transform import Rotation
from IPython.display import display
import ipywidgets
import pythreejs as THREE
from gltflib import GLTF

# %%


def standard_rectangle(Lx, Ly, Nx, Ny):
    ''' Conveniece function to construct a rectangle in the XY plane, extending from the X axis downards (along -Y)

    Args:
        Lx (float): length of rectangle in X
        Ly (float): length of rectangle in Y
        Nx (int): number of segments in X
        Ny (int): number of segments in Y

    Returns:
        positions: array of vertex positions
        faces: array of faces (consistently oriented vertex loop for each face)
    '''

    dx = Lx / Nx
    dy = Ly / Ny

    # vertex positions

    positions = np.zeros(((Nx + 1) * (Ny + 1), 3), dtype=np.float32)
    j = 0  # vertex index
    #  with x to right and y up, j's look like this
    #  0 - 3 - 6
    #  | \ | \ |
    #  1 - 4 - 7
    #  | \ | \ |
    #  2 - 5 - 8

    for jx in range(Nx+1):
        for jy in range(Ny + 1):
            positions[j, 0] = jx * dx
            positions[j, 2] = jy *  dy  # negative sign to make it hang down
            j += 1

    # faces (elements)
    faces = np.zeros((Nx * Ny * 2, 3), dtype=np.uint16)
    i = 0  # face index
    j = 0  # vertex index
    for jx in range(Nx):
        for jy in range(Ny):
            faces[i] = [j, j + 1, j + Ny + 2]
            faces[i + 1] = [j, j + Ny + 2, j + Ny + 1]
            i += 2
            j += 1
        j += 1

    return positions, faces


# %%

def mesh_animation(times, xt, faces):
    """ Animate a mesh from a sequence of mesh vertex positions

        Args:
        times   - a list of time values t_i at which the configuration x is specified
        xt      -   i.e., x(t). A list of arrays representing mesh vertex positions at times t_i.
                    Dimensions of each array should be the same as that of mesh.geometry.array
        TODO nt - n(t) vertex normals
        faces    - array of faces, with vertex loop for each face

        Side effects:
            displays rendering of mesh, with animation action

        Returns: None
        TODO renderer - THREE.Render to show the default scene
        TODO position_action - THREE.AnimationAction IPython widget
    """

    position_morph_attrs = []
    for pos in xt[1:]:  # xt[0] uses as the Mesh's default/initial vertex position
        position_morph_attrs.append(
            THREE.BufferAttribute(pos, normalized=False))

    # Testing mesh.geometry.morphAttributes = {'position': position_morph_attrs}
    geom = THREE.BufferGeometry(
        attributes={
            'position': THREE.BufferAttribute(xt[0], normalized=False),
            'index': THREE.BufferAttribute(faces.ravel())
        },
        morphAttributes={
            'position': position_morph_attrs
        }
    )
    matl = THREE.MeshStandardMaterial(
        side='DoubleSide', color='red', wireframe=True, morphTargets=True)

    mesh = THREE.Mesh(geom, matl)

    # create key frames
    position_track = THREE.NumberKeyframeTrack(
        name='.morphTargetInfluences[0]', times=times, values=list(range(0, len(times))))
    # create animation clip from the morph targets
    position_clip = THREE.AnimationClip(tracks=[position_track])
    # create animation action
    position_action = THREE.AnimationAction(
        THREE.AnimationMixer(mesh), position_clip, mesh)

    # TESTING
    camera = THREE.PerspectiveCamera(position=[2, 1, 2], aspect=600/400)
    scene = THREE.Scene(children=[mesh,
                                  camera,
                                  THREE.AxesHelper(0.2),
                                  THREE.DirectionalLight(
                                      position=[3, 5, 1], intensity=0.6),
                                  THREE.AmbientLight(intensity=0.5)])
    renderer = THREE.Renderer(camera=camera, scene=scene,
                              controls=[THREE.OrbitControls(
                                  controlling=camera)],
                              width=600, height=400)

    display(renderer, position_action)

    # return renderer, position_action
