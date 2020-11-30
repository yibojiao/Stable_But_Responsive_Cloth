# %%
import pythreejs as THREE
import numpy as np
import dhutils as dhu
import math

# %%
from cloth import cloth
from particle import particle

# %%
N = 10
x0, faces = dhu.standard_rectangle(N, N, N, N)
normals = np.zeros(faces.shape)
normals += np.array([0,1,0])
geometry = THREE.BufferGeometry(
        attributes={
            'position': THREE.BufferAttribute(np.array(x0, dtype=np.float32), normalized=False),
            'normal': THREE.BufferAttribute(np.array(normals, dtype=np.float32), normalized=False),
            'index': THREE.BufferAttribute(np.array(faces.ravel(), dtype=np.uint16)),
        }
)
mesh = THREE.Mesh(geometry, THREE.MeshStandardMaterial(sice='DoubleSide', wireframe=True))

# %%
def viewer_cloth(cloth):
    view_width = 400
    view_height = 400
    camera = THREE.PerspectiveCamera(
        position=[30, 15, 15], aspect=view_width/view_height)
    key_light = THREE.DirectionalLight(position=[10, 10, 10])
    ambient_light = THREE.AmbientLight()
    axes_helper = THREE.AxesHelper(0.5)

    scene = THREE.Scene()
    controller = THREE.OrbitControls(controlling=camera)
    renderer = THREE.Renderer(camera=camera, scene=scene, controls=[controller],
                        width=view_width, height=view_height)
    scene.children = [cloth, axes_helper,
                     camera, key_light, ambient_light]
    return renderer

viewer = viewer_cloth(mesh)
viewer

# %%
cloth = cloth(x0, N)
cloth.add_springs()
cloth.cuff_cloth()
t = 0
while t < 500:
    delta = cloth.time_step()
    mesh.geometry.attributes['position'].array = mesh.geometry.attributes['position'].array + delta
    t += 1
# %%
