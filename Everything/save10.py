import bpy
import math


r0 = 3
r1 = 0.8
r2 = 0.8
r3 = 0.2
r = 18
phi0f = 0.3*22.5
phi1f = 0.5*22.5
phi0d = 0.6*22.5
phi1d = 0.7*22.5
phi0f = math.radians(phi0f)
phi1f = math.radians(phi1f)
phi0d = math.radians(phi0d)
phi1d = math.radians(phi1d)
h = 4
gapx = 3
gapy = 0.5
radius = r0 + r1 + ((r2) / 2)
speed = 4
particle_radius = 0.3
velocity = 25
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()



def print(data):
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'CONSOLE':
                override = {'window': window, 'screen': screen, 'area': area}
                bpy.ops.console.scrollback_append(override, text=str(data), type="OUTPUT")
                
                
def animation(trace):
    vertices =  []
    faces = []
    edges = []
    mesh = bpy.data.meshes.new('new_mesh')

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    object = bpy.data.objects.new("Object", mesh)

    collection = bpy.data.collections.new("Collection")
    bpy.context.scene.collection.children.link(collection)

    collection.objects.link(object)
    
    bpy.ops.mesh.primitive_uv_sphere_add()
    sphere = bpy.context.active_object 
    sphere.scale[0] = particle_radius
    sphere.scale[1] = particle_radius
    sphere.scale[2] = particle_radius

    edges = [[]]
    sphere.keyframe_insert("location", frame=0)
    print(len(trace))
    for i in range(len(trace) - 16 ): ## THIS FOR LAST FRAME!
        vertices.append(trace[i])
#        edges[-1].append(i)
        sphere.keyframe_insert("location", frame=i)
        sphere.location.x = trace[i][0]
        sphere.location.y = trace[i][1]
        sphere.location.z = h/2
    
#    vertices = [[0, 0, 0], [1, 1, 1], [2, 2, 2], [3, 3, 3]]
    for i in range(len(vertices) - 5):
        faces.append([i, i+1, i+5, i+4])
#    faces = [[0, 1, 2, 3]]
    mesh = bpy.data.meshes.new('new_mesh')

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    object = bpy.data.objects.new("Object", mesh)

    collection = bpy.data.collections.new("Collection")
    bpy.context.scene.collection.children.link(collection)

    collection.objects.link(object)
    
    
def grab_co(file):
    data = open(file, "r").read().strip()
    data = data.split("\n")
    trace = []
    for i in range(0, len(data), velocity):
        data[i] = data[i].split()
        if i >= 2:
            trace.append([float(data[i][1]), float(data[i][3]), h/2])
    return trace

def colour_sphere():
    template_object = bpy.data.objects.get('Sphere')
    matr = bpy.data.materials.new("Red")
    matr.diffuse_color = (1,0,0,0.8)

    ob = template_object.copy()
    ob.active_material = matr
    print('red')
    bpy.context.collection.objects.link(ob)
    

try:
    file = "fets_ffa-trackOrbit_1.dat"
    trace = grab_co(file)
    animation(trace)
    colour_sphere()
except Exception as e:
    print(e)
