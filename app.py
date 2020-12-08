# %%
import pythreejs as THREE
import numpy as np
import dhutils as dhu
import math

# %%
from cloth import cloth
from particle import particle

# %%
N = 15
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
mesh = THREE.Mesh(geometry, THREE.MeshBasicMaterial(sice='DoubleSide', wireframe=True, color='red'))

# %%
def viewer_cloth(cloth):
    view_width = 800
    view_height = 600
    camera = THREE.PerspectiveCamera(
        position=[20, 5, 30], aspect=view_width/view_height)
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

# # %%
# cloth1 = cloth(x0, N, t2=False, d=True)
# cloth1.add_springs()
# cloth1.cuff_cloth()
# t = 0
# while t < 500:
#     delta = cloth1.time_step()
#     mesh.geometry.attributes['position'].array = mesh.geometry.attributes['position'].array + delta
#     t += 1
# %%
# mesh.geometry.attributes['position'].array = x0
# cloth2 = cloth(x0, N, t2=True, d=False)
# cloth2.add_springs()
# cloth2.cuff_cloth()
# t = 0
# while t < 500:
#     delta = cloth2.time_step()
#     mesh.geometry.attributes['position'].array = mesh.geometry.attributes['position'].array + delta
#     t += 1
# %%
mesh.geometry.attributes['position'].array = x0
cloth3 = cloth(x0, N, t2=True, d=True)
cloth3.add_springs()
cloth3.cuff_cloth()
cloth3.add_ball()
t = 0
sphere_geo = THREE.SphereGeometry(cloth3.r-0.5, 8, 8)
sphere = THREE.Mesh(sphere_geo, THREE.MeshBasicMaterial(wireframe=True))
sphere.position = (5,-5,5)
viewer.scene.add(sphere)
while t < 300:
    delta = cloth3.time_step()
    mesh.geometry.attributes['position'].array = mesh.geometry.attributes['position'].array + delta
    t += 1
# %%
