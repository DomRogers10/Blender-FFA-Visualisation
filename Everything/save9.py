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
velocity = 15
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

def print(data):
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'CONSOLE': 
                override = {'window': window, 'screen': screen, 'area': area}
                bpy.ops.console.scrollback_append(override, text=str(data), type="OUTPUT")

def camera():
    bpy.ops.object.camera_add(location=(0, 0, 30), rotation=(0,0,90))
    
def x(r, phi):
    return r * math.cos(phi)
def y(r, phi):
    return r * math.sin(phi)


def curve_end_faces(r0, phi0, phi1, points):
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
    
    print(points)
    gradient = (points[0][1] - points[1][1]) / (points[0][0] - points[1][0])
    length = points[1][0] - points[0][0]
    for i in range(20):
        x0 = points[0][0] + (i * length / 19)
        y0 = (x0 - points[0][0]) * gradient + points[0][1]
        vertices.append([x0, y0, 0])
    for i in range(20):
        x0 = points[0][0] + (i * length / 19)
        y0 = (x0 - points[0][0]) * gradient + points[0][1]
        vertices.append([x0, y0, h])
    
        
    faces = []
    
    for i in range(19):
        faces.append([i, i+1, i+21, i+20])
    
    for i in range(19):
        faces.append([i, i+1, i+41, i+40])
        faces.append([i+20, i+21, i+61, i+60])
    edges = []
    mesh = bpy.data.meshes.new('new_mesh')

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    object = bpy.data.objects.new("Object", mesh)

    collection = bpy.data.collections.new("Collection")
    bpy.context.scene.collection.children.link(collection)

    collection.objects.link(object)
    
    
def curve_sides(r0, r1, phi0, c, h, offset, r00, phi1):
    vertices =  []
    faces = []
    edges = []
    mesh = bpy.data.meshes.new('new_mesh')

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()
    #mesh.materials.append(mat("steel", 255, 0, 0))

    object = bpy.data.objects.new("Object", mesh)

    collection = bpy.data.collections.new("Collection")
    bpy.context.scene.collection.children.link(collection)

    collection.objects.link(object)
    
    
    vertices = []
    for i in range(20):
        current = r0 + ((r1 - r0) * i / 19)
        phi = phi0 - math.tan(math.radians(c)) * math.log(current/r00)
        x = current * math.cos(phi)
        y = current * math.sin(phi)
        vertices.append([x, y, offset])
        
    
    for i in range(20):
        current = r0 + ((r1 - r0) * i / 19)
        phi = phi0 - math.tan(math.radians(c)) * math.log(current/r00)
        x = current * math.cos(phi)
        y = current* math.sin(phi)
        vertices.append([x, y, h+offset])
        
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


def curves(c, r0, r1, r00, h, offset, phi0, phi1, front=False):
    a = curve_sides(r0, r0+r1, phi0, c, h, offset, r00, phi1)
    b = curve_sides(r0, r0+r1, phi1, c, h, offset, r00, phi1)
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
    if front:
        pass
    
    else:
        for i in range(19):
            faces.append([i, i+1, i+41, i+40])
        
        for i in range(20, 39):
            faces.append([i, i+1, i+41, i+40])
        
    faces.append([19, 39, 79, 59])
    points = [vertices[19], vertices[59]]
    edges = []
    mesh = bpy.data.meshes.new('new_mesh')

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    object = bpy.data.objects.new("Object", mesh)

    collection = bpy.data.collections.new("Collection")
    bpy.context.scene.collection.children.link(collection)

    collection.objects.link(object)
    return points
    
def make_wedge(r0, r1, h, phi0, phi1):
    points = curves(10, r0, r1, r0, h, 0, phi0, phi1, front=True)
    curves(10, r0+r1, r2, r0, h/3, 0, phi0, phi1)
    curves(10, r0+r1, r2, r0, h/3, 2*h/3, phi0, phi1)
    curves(10, r0+r1+r2, r3, r0, h, 0, phi0, phi1) 
    curve_end_faces(r0, phi0, phi1, points)

def animation(trace):
    bpy.ops.mesh.primitive_uv_sphere_add()
    sphere = bpy.context.active_object 
    sphere.scale[0] = particle_radius
    sphere.scale[1] = particle_radius
    sphere.scale[2] = particle_radius


    sphere.keyframe_insert("location", frame=0)
    for i in range(len(trace) - 24): ## THIS FOR LAST FRAME!
        sphere.keyframe_insert("location", frame=i)
        sphere.location.x = trace[i][0]
        sphere.location.y = trace[i][1]
        sphere.location.z = trace[i][2]

def grab_co(file):
    data = open(file, "r").read().strip()
    data = data.split("\n")
    trace = []
    for i in range(0, len(data), velocity):
        data[i] = data[i].split()
        if i >= 2:
            trace.append([float(data[i][1]), float(data[i][3]), h/2])
    return trace

def colour(id, r, g, b):
    all = bpy.ops.object.select_all(action='SELECT')
    col = bpy.data.materials.new(id)
    col.diffuse_color = (r,g,b,0.8)
    for ob in all:
        ob.active_material = col
        bpy.context.collection.objects.link(ob)
def colour_sphere():
    template_object = bpy.data.objects.get('Sphere')
    matr = bpy.data.materials.new("Red")
    matr.diffuse_color = (1,0,0,0.8)

    ob = template_object.copy()
    ob.active_material = matr
    print('red')
    bpy.context.collection.objects.link(ob)
try:
    camera()
    file = "fets_ffa-trackOrbit_1.dat"
    trace = grab_co(file)
    animation(trace)
    colour_sphere()
#    for i in range(0, 12, 3):
#        make_wedge(r0, r1, h, phi0 + i * (phi1 - phi0), phi1 + (i+1) * (phi1 - phi0))
    
    for i in range(16):     
        increase = math.radians(22.5*i)
        make_wedge(r0, r1, h, increase + phi0f, increase + phi1f)
        make_wedge(r0, r1, h, increase + phi0d, increase + phi1d)

    

except Exception as e:
    print(e)
