import bpy
import mathutils
import math

MEDIA_DIR = '/Users/rostislavnikolaev/Desktop/Sites/ecommerce/backend/media/'
image_name = 'wood-chips.png'
imgpath = MEDIA_DIR + 'wood-chips.png'
cube = bpy.data.materials['cube']


def delete_useless_nodes(base_name):
    if base_name in ['', None]:
        return
    for node in cube.node_tree.nodes:
        if base_name in node.name and node.name != base_name:
            cube.node_tree.nodes.remove(node)

    for node in cube.node_tree.nodes:
        print(node)


try:
    bsdf = cube.node_tree.nodes["Principled BSDF"]
except:
    bsdf = cube.node_tree.nodes.new('ShaderNodeBsdfPrincipled')


def color_texture(material, color=(.1, .7, .1, 1)):
    material.use_nodes = True
    try:
        rgb = material.node_tree.nodes["RGB"]
    except:
        rgb = material.node_tree.nodes.new('ShaderNodeRGB')
    rgb.outputs[0].default_value = color
    material.node_tree.links.new(bsdf.inputs['Base Color'], rgb.outputs['Color'])


def image_texture(material, path=imgpath):
    material.use_nodes = True

    print(bpy.data.images)

    image = bpy.data.images.get(image_name)
    if not image:
        image = bpy.data.images.load(MEDIA_DIR + image_name)

    imageTexture = material.node_tree.nodes.get('Image Texture', None)
    if not imageTexture:
        imageTexture = material.node_tree.nodes.new('ShaderNodeTexImage')

    print('bsdf', bsdf, 'imageTexture', imageTexture)

    imageTexture.image = image
    material.node_tree.links.new(bsdf.inputs['Base Color'], imageTexture.outputs['Color'])


def set_light(light_name, energy=1000, location=(-1.5, -3, 1)):
    light_data_name = light_name + '_data'
    light_data = bpy.data.lights.get(light_data_name)
    if not light_data:
        light_data = bpy.data.lights.new(name=light_data_name, type='POINT')

    # Set light energy
    light_data.energy = 1000

    # Create new object, pass the light data
    light_object = bpy.data.objects.get(light_name)
    if not light_object:
        light_object = bpy.data.objects.new(name=light_name, object_data=light_data)

    # Link object to collection in context
    colection_obj = bpy.context.collection.objects.get(light_name)
    if not colection_obj:
        bpy.context.collection.objects.link(light_object)

    # Change light position
    light_object.location = location


lights = [
    ['main_light'],
    ['second_light', 500, (2, -2, 1.5)],
]

for l in lights:
    set_light(*l)

camera = bpy.data.objects["Camera"]


def get_rotation_coordiantes(steps=12, radius=4, z=3):
    result = []
    if steps > 360:
        steps = 360
    step = 360 / steps

    for i in range(steps):
        angle = i * step
        x = radius * math.sin(math.radians(angle))
        y = radius * math.cos(math.radians(angle))

        rotation = math.pi
        if angle > 0:
            rotation -= math.pi * 2 * angle / 360

        result.append({
            'location': (x, y, z),
            'angle': (math.pi * 0.25, 0, rotation)
        })
    return result


coordinates = get_rotation_coordiantes(36)

# index = 4
# camera.location = mathutils.Vector(coordinates[index]['location'])
# camera.rotation_euler = coordinates[index]['angle']

scene = bpy.context.scene

for i, coordinate in enumerate(coordinates):
    if i % 2:
        color_texture(cube)
    else:
        image_texture(cube)
    # set camera
    camera.location = mathutils.Vector(coordinate['location'])
    camera.rotation_euler = coordinate['angle']
    scene.camera = camera

    # render
    scene.render.image_settings.file_format = 'JPEG'
    scene.render.filepath = MEDIA_DIR + f'blender/image_{i}.jpeg'
    bpy.ops.render.render(write_still=1)