import bpy
import math

r0 = 2
r1 = 2
r2 = 5
r3 = 2
r = 18
phi0 = 30
phi1 = 60
phi0 = math.radians(phi0)
phi1 = math.radians(phi1)
h = 4
gapx = 3
gapy = 0.5

def print(data):
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'CONSOLE':
                override = {'window': window, 'screen': screen, 'area': area}
                bpy.ops.console.scrollback_append(override, text=str(data), type="OUTPUT")

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
length = r1 - r0

def return_y(hyp, phi, r):
    y = (r * math.sin(phi)) + (hyp * math.sin(phi))
    return y
def x(r, phi):
    return r * math.cos(phi)
def y(r, phi):
    return r * math.sin(phi)

def build_prism(r0, r1, phi0, phi1, h, offset=0, front=False, back=False):
    lower = [x(r0, phi0), y(r0, phi0), 0 + offset], [x(r0, phi1), y(r0, phi1), 0 + offset], [x(r1, phi0), y(r1, phi0), 0 + offset], [x(r1, phi1), y(r1, phi1), 0 + offset] # 0, 1, 2, 3
    upper = [x(r0, phi0), y(r0, phi0), h + offset], [x(r0, phi1), y(r0, phi1), h + offset], [x(r1, phi0), y(r1, phi0), h + offset], [x(r1, phi1), y(r1, phi1), h + offset] # 4, 5, 6, 7

    
    vertices = lower + upper
    if front:
        faces = [[2, 3, 7, 6]]
    elif back:
        faces = [[0, 1, 5, 4]]
    else:
        faces = [[0, 1, 5, 4], [2, 3, 7, 6], [1, 5, 7, 3], [0, 2, 6, 4]]
        #faces = [[0, 1, 3, 2], [0, 1, 5, 4], [2, 3, 7, 6], [4, 5, 7, 6], [1, 5, 7, 3], [0, 2, 6, 4]]
    edges = []
    mesh = bpy.data.meshes.new('new_mesh')

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    object = bpy.data.objects.new("Object", mesh)

    collection = bpy.data.collections.new("Collection")
    bpy.context.scene.collection.children.link(collection)

    collection.objects.link(object)
    
    
    vertices = lower + upper

    edges = []
    mesh = bpy.data.meshes.new('new_mesh')

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    object = bpy.data.objects.new("Object", mesh)

    collection = bpy.data.collections.new("Collection")
    bpy.context.scene.collection.children.link(collection)

    collection.objects.link(object)

def curve_end_faces(r0):
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
    
    
    vertices = []
    for i in range(0, 20):
        angle = (phi1 - phi0) * i / 19
        vertices.append([x(r0, phi0 + angle), y(r0, phi0 + angle), 0])
        
    for i in range(0, 20):
        angle = (phi1 - phi0) * i / 19
        vertices.append([x(r0, phi0 + angle), y(r0, phi0 + angle), h])
    faces = []
    
    for i in range(19):
        faces.append([i, i+1, i+21, i+20])
    edges = []
    mesh = bpy.data.meshes.new('new_mesh')

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    object = bpy.data.objects.new("Object", mesh)

    collection = bpy.data.collections.new("Collection")
    bpy.context.scene.collection.children.link(collection)

    collection.objects.link(object)

def curve_top_faces(h, r0, r1):
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
    
    
    vertices = []
    for i in range(20):
        angle = (phi1 - phi0) * i / 19
        vertices.append([x(r1, phi0 + angle), y(r1, phi0 + angle), h])
        
    for i in range(20):
        angle = (phi1 - phi0) * i / 19
        vertices.append([x(r0, phi0 + angle), y(r0, phi0 + angle), h])
    faces = []
    
    for i in range(19):
        faces.append([i, i+1, i+21, i+20])
    edges = []
    mesh = bpy.data.meshes.new('new_mesh')

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    object = bpy.data.objects.new("Object", mesh)

    collection = bpy.data.collections.new("Collection")
    bpy.context.scene.collection.children.link(collection)

    collection.objects.link(object)
    return vertices

def camera():
    camera_data = bpy.data.cameras.new(name='Camera')
    camera_object = bpy.data.objects.new('Camera', camera_data)
    bpy.context.scene.collection.objects.link(camera_object)

def curve_sides(r0, r1, phi0, c):
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
    
    
    vertices = []
    for i in range(20):
        current = r0 + ((r1 - r0) * i / 19)
        phi = phi0 - math.tan(math.radians(c)) * math.log(current/r0)
        x = current * math.cos(phi)
        y = current * math.sin(phi)
        #print(str(x) + " " + str(y) + " " + str(current))
        vertices.append([x, y, 0])
        
    
    for i in range(20):
        current = r0 + ((r1 - r0) * i / 19)
        phi = phi0 - math.tan(math.radians(c)) * math.log(current/r0)
        x = current * math.cos(phi)
        y = current* math.sin(phi)
        #print(x**2 + y**2)
        vertices.append([x, y, h])
        
    faces = []
    
    for i in range(19):
        faces.append([i, i+1, i+21, i+20])
    edges = []
    mesh = bpy.data.meshes.new('new_mesh')

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    object = bpy.data.objects.new("Object", mesh)

    collection = bpy.data.collections.new("Collection")
    bpy.context.scene.collection.children.link(collection)

    collection.objects.link(object)
    return vertices

def curves(c, r0, r1):
    a = curve_sides(r0, r0+r1, phi0, c)
    b = curve_sides(r0, r0+r1, phi1, c)
    vertices = a + b
    edges = []
    faces = []
    mesh = bpy.data.meshes.new('new_mesh')

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    object = bpy.data.objects.new("Object", mesh)

    collection = bpy.data.collections.new("Collection")
    bpy.context.scene.collection.children.link(collection)

    collection.objects.link(object)
    
    faces = []
    
    for i in range(19):
        faces.append([i, i+1, i+41, i+40])
    
    for i in range(20, 39):
        faces.append([i, i+1, i+41, i+40])
    edges = []
    mesh = bpy.data.meshes.new('new_mesh')

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    object = bpy.data.objects.new("Object", mesh)

    collection = bpy.data.collections.new("Collection")
    bpy.context.scene.collection.children.link(collection)

    collection.objects.link(object)
    
    
try:
    camera()
    #build_prism(r0, r1+r0, phi0, phi1, h, front=True)
    #build_prism(r1+r0, r1+r0+r2, phi0, phi1, h/3)
    #build_prism(r0+r1, r0+r1+r2, phi0, phi1, h/3, 2*h/3)
    #build_prism(r0+r1+r2, r0+r1+r2+r3, phi0, phi1, h, back=True)
    curve_end_faces(r0)
    #curve_end_faces(r0+r1+r2+r3)
    
    #curve_top_faces(h, r0, r0+r1)
    #curve_top_faces(0, r0, r0+r1)
    
    #curve_top_faces(h, r0+r1+r2, r0+r1+r2+r3)
    #curve_top_faces(0, r0+r1+r2, r0+r1+r2+r3)
    
    #curve_top_faces(h, r0+r1, r0+r1+r2)
    #curve_top_faces(0, r0+r1, r0+r1+r2)
    curves(10, r0, r1)
    curves(10, r0+r1, r0+r1+r2)
except Exception as e:
    print(e)
