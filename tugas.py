import bpy
import math
import os
from random import randint
from bpy_extras.image_utils import load_image



def add_plane(size):
    bpy.ops.mesh.primitive_plane_add(size=size, enter_editmode=False, align='WORLD', 
    location=(0, 0, 0), scale=(1, 1, 10))

def clear_scene():
    for obj in bpy.data.objects:
        if(obj.name != "Light" and obj.name != "Camera" and obj.name != "Light.001"):
            bpy.data.objects.remove(obj)
    for mtr in bpy.data.materials:
        bpy.data.materials.remove(mtr)
               

###########################################################
# Fungsi untuk memuat gambar sebagai tekstur
###########################################################
def load_texture(image_path):
    image_name = os.path.basename(image_path)
    
    # Cek apakah gambar sudah ada di Blender
    bImg = bpy.data.images.get(image_name)
    if not bImg:
        bImg = load_image(image_path)

    return bImg

# Fungsi untuk menambahkan objek dan menerapkan tekstur ke material
def add_textured_object(obj, image_path):
    # Tambahkan material baru
    material = bpy.data.materials.new("TexturedMaterial")
    obj.data.materials.append(material)

    # Dapatkan material dan node tree
    material = obj.data.materials[0]
    material.use_nodes = True
    nodes = material.node_tree.nodes

    # Hapus semua node yang ada
    for node in nodes:
        nodes.remove(node)

    # Tambahkan shader principled BSDF
    shader_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    shader_node.location = (0, 0)

    # Tambahkan texture node
    texture_node = nodes.new(type='ShaderNodeTexImage')
    texture_node.image = load_texture(image_path)
    texture_node.location = (-300, 0)

    # Tambahkan output shader
    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    output_node.location = (300, 0)

    # Hubungkan node secara otomatis
    links = material.node_tree.links
    links.new(shader_node.outputs["BSDF"], output_node.inputs["Surface"])
    links.new(texture_node.outputs["Color"], shader_node.inputs["Base Color"])




#######################################################################
# Membuat Cylinder
#######################################################################
def add_cylinder(radius, depth, locX_cy, locY_cy, locZ_cy):
    for x in [1, 2, 3, 4]:    
        if x == 1:
            locX_cy = locX_cy
            locY_cy = locY_cy
            locZ_cy = locZ_cy 
            
        elif x == 2:
            locX_cy = (-locX_cy)
            locY_cy = (locY_cy)
            locZ_cy = locZ_cy 
            
        elif x == 3:
            locX_cy = (locX_cy)
            locY_cy = (-locY_cy)
            locZ_cy = locZ_cy
            
        elif x == 4: 
            locX_cy = (-locX_cy)
            locY_cy = locY_cy
            locZ_cy = locZ_cy
            
        
        bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, 
        enter_editmode=False, align='WORLD', location=(locX_cy, locY_cy, locZ_cy), scale=(1, 1, 1))
 
        # Dapatkan referensi objek yang baru saja dibuat
        cylinder_obj = bpy.context.active_object
        
#        # Tambahkan tekstur
#        image_path_cube = 'D:/Kuliah/Semester 3/Komputer Grafik/Praktek/Pertemuan 13/Textures/tembok2.jpg'
#        add_textured_object(cylinder_obj, image_path_cube)  

#        #  Pilih objek dan aktifkan mode edit
#        bpy.context.view_layer.objects.active = cylinder_obj
#        bpy.ops.object.mode_set(mode='EDIT')
#        bpy.ops.mesh.select_all(action='SELECT')

#        # Unwrap UV
#        bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.001)

#        # Kembali ke mode objek
#        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.object.rotation_euler[1] = 1.5708
        
        #MEMBERIKAN WARNA PADA OBJEK     
        mat = bpy.data.materials.new(name="EmissionMaterial")
        mat.use_nodes = True
        node_tree = mat.node_tree
        emission_shader = node_tree.nodes.new(type='ShaderNodeEmission')
        emission_shader.location = (0, 0)
        output_shader = node_tree.nodes["Material Output"]
        node_tree.links.new(emission_shader.outputs["Emission"], output_shader.inputs["Surface"])

        # Set emission color to red
        emission_shader.inputs["Color"].default_value = (1, 0.01, 0.01, 1)

        # Set emission strength to 5
        emission_shader.inputs["Strength"].default_value = 5

        # Assign the material to the object
        cylinder_obj.data.materials.append(mat)

        # Enable bloom and screen space reflection in Eevee
        bpy.context.scene.eevee.use_bloom = True
        bpy.context.scene.eevee.use_ssr = True
        

#######################################################################
# Membuat Cylinder Tiang
#######################################################################
def add_cylinder2(radius, depth, locX_cyt, locY_cyt, locZ_cyt):
    for x in [1, 2]:
        if x == 2:
            locX_cyt = (-locX_cyt)
        bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, enter_editmode=False, 
        align='WORLD', location=(locX_cyt, locY_cyt, locZ_cyt), scale=(1, 1, 1))   
        
        # Dapatkan objek yang baru ditambahkan
        cylinder_obj = bpy.context.active_object

        # Buat material baru
        material = bpy.data.materials.new(name="GlossyRed")
        material.use_nodes = True
        node_tree = material.node_tree

        # Hapus semua node material default
        for node in node_tree.nodes:
            node_tree.nodes.remove(node)

        # Tambahkan shader Glossy BSDF
        glossy_shader = node_tree.nodes.new(type='ShaderNodeBsdfGlossy')
        glossy_shader.location = (0, 0)

        # Setel warna Glossy BSDF menjadi merah
        glossy_shader.inputs["Color"].default_value = (1, 0.16, 0.13, 1)

        # Tambahkan shader Output
        output_shader = node_tree.nodes.new(type='ShaderNodeOutputMaterial')
        output_shader.location = (200, 0)

        # Hubungkan Glossy BSDF ke Output
        node_tree.links.new(glossy_shader.outputs["BSDF"], output_shader.inputs["Surface"])

        # Assign material ke objek
        if cylinder_obj.data.materials:
            # Jika objek sudah memiliki material, gunakan material tersebut
            cylinder_obj.data.materials[0] = material
        else:
            # Jika objek belum memiliki material, tambahkan material baru
            cylinder_obj.data.materials.append(material)


        
#######################################################################
# Membuat balok 
#######################################################################
def add_balok(sisi, locX_bl, locY_bl, locZ_bl, ket):
#    sisi = 15
    if ket == "papan":
        p = 2*sisi #panjang
        l = sisi / 3 #tinggi 
        t = 0.2 #lebar
        d = 0 #default
    else:
        p = 4*sisi #panjang
        t = 4*sisi  #tinggi 
        l = sisi / 8 #lebar
        d = 0 #default
        locY_bl = -p
        
    verts = [
        (-p, l, d),
        (-p, -l, d),
        (p, -l, d),
        (p, l, d),
        (-p, l, t),
        (-p, -l, t),
        (p, -l, t),
        (p, l, t),
    ]
    # define faces using the indexes of the vertices
    faces = [
        (0, 1, 2, 3),
        (7, 6, 5, 4),
        (4, 5, 1, 0),
        (7, 4, 0, 3),
        (6, 7, 3, 2),
        (5, 6, 2, 1),
    ]
    edges = []
    # create a mesh from the vert, edge, and face data
    mesh_data = bpy.data.meshes.new("cube_data")
    mesh_data.from_pydata(verts, edges, faces)
    # create a object using the mesh data
    mesh_obj = bpy.data.objects.new("cube_object", mesh_data)
    bpy.context.collection.objects.link(mesh_obj)
    mesh_obj.location.x = locX_bl
    mesh_obj.location.y = locY_bl
    mesh_obj.location.z = locZ_bl     
    
    mesh_obj.rotation_euler[0] = -1.5708
    if ket == "papan":
        # Buat material baru
        material = bpy.data.materials.new(name="GlossyRed")
        material.use_nodes = True
        node_tree = material.node_tree

        # Hapus semua node material default
        for node in node_tree.nodes:
            node_tree.nodes.remove(node)

        # Tambahkan shader Glossy BSDF
        glossy_shader = node_tree.nodes.new(type='ShaderNodeBsdfGlossy')
        glossy_shader.location = (0, 0)

        # Setel warna Glossy BSDF menjadi merah
        glossy_shader.inputs["Color"].default_value = (1, 0.16, 0.13, 1)

        # Tambahkan shader Output
        output_shader = node_tree.nodes.new(type='ShaderNodeOutputMaterial')
        output_shader.location = (200, 0)

        # Hubungkan Glossy BSDF ke Output
        node_tree.links.new(glossy_shader.outputs["BSDF"], output_shader.inputs["Surface"])

        # Assign material ke objek
        if mesh_obj.data.materials:
            # Jika objek sudah memiliki material, gunakan material tersebut
            mesh_obj.data.materials[0] = material
        else:
            # Jika objek belum memiliki material, tambahkan material baru
            mesh_obj.data.materials.append(material)
            
    else:
        image_path_cube = 'D:/Kuliah/Semester 3/Komputer Grafik/Praktek/Pertemuan 13/Textures/tembok1.jpg'
        add_textured_object(mesh_obj, image_path_cube)  
        
        #  Pilih objek dan aktifkan mode edit
        bpy.context.view_layer.objects.active = mesh_obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')

        # Unwrap UV
        bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.001)

        # Kembali ke mode objek
        bpy.ops.object.mode_set(mode='OBJECT')
          
#    image_path_cube = 'D:/Kuliah/Semester 3/Komputer Grafik/Praktek/Pertemuan 13/Textures/bricks_normal.png'
#    add_textured_object(mesh_obj, image_path_cube)



#######################################################################
# Membuat trapesium
#######################################################################
def add_trapesium(sisi, locx_tp, locy_tp, locz_tp):
    p = 2*sisi #panjang
    l = sisi #lebar
    t = 2*sisi #tinggi
    d = 0 #default 
    sisi2 = sisi
    for x in [1,2,3,4]:
#        sisi = sisi2
        verts = [
            (d, l, d),
            (d, d, d),
            (p, d, d),
            (p, l, d),
            (d, l, t),
            (d, d, t),
            (p/2, d, t),
            (p/2, l, t),
        ]
        # define faces using the indexes of the vertices
        faces = [
            (0, 1, 2, 3),
            (7, 6, 5, 4),
            (4, 5, 1, 0),
            (7, 4, 0, 3),
            (6, 7, 3, 2),
            (5, 6, 2, 1),
        ]
        edges = []

        mesh_data = bpy.data.meshes.new("cube_data")
        mesh_data.from_pydata(verts, edges, faces)

        mesh_obj = bpy.data.objects.new("cube_object", mesh_data)
        bpy.context.collection.objects.link(mesh_obj)
        
        if x == 1:
            mesh_obj.location.x = locx_tp
            mesh_obj.location.y = locy_tp
            mesh_obj.location.z = locz_tp
            mesh_obj.rotation_euler[2] = 1.5708
        if x == 2:
            mesh_obj.location.x =  (-locx_tp) + sisi
            mesh_obj.location.y = locy_tp
            mesh_obj.location.z = locz_tp
            mesh_obj.rotation_euler[2] = 1.5708
        if x == 3:
            mesh_obj.location.x = locx_tp - sisi
            mesh_obj.location.y = -locy_tp
            mesh_obj.location.z = locz_tp
            mesh_obj.rotation_euler[2] = -1.5708
        if x == 4:
            mesh_obj.location.x =  (-locx_tp) 
            mesh_obj.location.y = -locy_tp
            mesh_obj.location.z = locz_tp
            mesh_obj.rotation_euler[2] = -1.5708

        # Tambahkan tekstur
        image_path_cube = 'D:/Kuliah/Semester 3/Komputer Grafik/Praktek/Pertemuan 13/Textures/tembok1.jpg'
        add_textured_object(mesh_obj, image_path_cube)
        
       

        #  Pilih objek dan aktifkan mode edit
        bpy.context.view_layer.objects.active = mesh_obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')

        # Unwrap UV
        bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.001)

        # Kembali ke mode objek
        bpy.ops.object.mode_set(mode='OBJECT')


        


#######################################################################
# membuat bingkai papan nama
#######################################################################
def add_frame_board(sisi, locX_fr, locY_fr,locZ_fr):
    add_frame_tebal_board(sisi, locX_fr, locY_fr, locZ_fr)
    p = 5.125*sisi
    s = sisi
    t = 1
    l = sisi/(sisi*5)
    Ttotal = 4*sisi
    for x in [1,2]:
        verts = [
            (p, 0, 0),
            (p-s, 0, 0),
    #        (p, 0, t),
    #        (p-s, 0, t),
            
            (p-1.25*s, 0, t),
            (p-2*s, 0, t),
    #        (p-s, 0, 2*t),
    #        (p-2*s, 0, 2*t),
            
            (p-2.25*s, 0, 2*t),
            (p-3*s, 0, 2*t),
    #        (p-2*s, 0, 3*t),
    #        (p-3*s, 0, 3*t),
            
            (p-3.25*s, 0, 3*t),
            (p-4*s, 0, 3*t),
    #        (p-3*s, 0, 4*t),
    #        (p-4*s, 0, 4*t),

            (p-4.25*s, 0, 4*t),
            (p-5*s, 0, 4*t),
    #        p-4*s, 0, 5*t),
    #        (p-5*s, 0, 5*t),
            
            
            (p-5.125*s, 0, 5*t),
            (p-5.125*s, 0, 6*t),
    #        p-4*s, 0, 5*t),
    #        (p-5*s, 0, 5*t),
            
    #        (p-5*s, 0, 6*t),
            (p, 0, 6*t),
        ]
        # define faces using the indexes of the vertices
        faces = [
            (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,12),
            
        ]
        edges = []
        # create a mesh from the vert, edge, and face data
        mesh_data = bpy.data.meshes.new("cube_data")
        mesh_data.from_pydata(verts, edges, faces)
        # create a object using the mesh data
        mesh_obj = bpy.data.objects.new("cube_object", mesh_data)
        bpy.context.collection.objects.link(mesh_obj)
        mesh_obj.location.x = locX_fr
        mesh_obj.location.y = locY_fr
        mesh_obj.location.z = locZ_fr
    
    
        if x == 2:
            mesh_obj.rotation_euler[2] = 3.14159 
                   
       

        # Buat material baru
        material = bpy.data.materials.new(name="GlossyRed")
        material.use_nodes = True
        node_tree = material.node_tree

        # Hapus semua node material default
        for node in node_tree.nodes:
            node_tree.nodes.remove(node)

        # Tambahkan shader Glossy BSDF
        glossy_shader = node_tree.nodes.new(type='ShaderNodeBsdfGlossy')
        glossy_shader.location = (0, 0)

        # Setel warna Glossy BSDF menjadi merah
        glossy_shader.inputs["Color"].default_value = (0.1423, 0.2733, 0.2287, 1)

        # Tambahkan shader Output
        output_shader = node_tree.nodes.new(type='ShaderNodeOutputMaterial')
        output_shader.location = (200, 0)

        # Hubungkan Glossy BSDF ke Output
        node_tree.links.new(glossy_shader.outputs["BSDF"], output_shader.inputs["Surface"])

        # Assign material ke objek
        if mesh_obj.data.materials:
            # Jika objek sudah memiliki material, gunakan material tersebut
            mesh_obj.data.materials[0] = material
        else:
            # Jika objek belum memiliki material, tambahkan material baru
            mesh_obj.data.materials.append(material)
 
       
        
#######################################################################
# membuat border bingkai papan nama
#######################################################################
def add_frame_tebal_board(sisi, locX_fr, locY_fr, locZ_fr):
    p = 5.125*sisi
    s = sisi
    t = 1
    l = sisi/(sisi*5)
    Ttotal = 4*sisi
    for x in [1, 2]:
        verts = [
            (p, l, 0),
            (p-s, l, 0),
            (p, -l, 0),
            (p-s, -l, 0),
            (p, l, -l),
            (p-s, l, -l),
            (p, -l, -l),
            (p-s, -l, -l),
            
            (p-1.25*s, l, t),
            (p-2*s, l, t),
            (p-1.25*s, -l, t),
            (p-2*s, -l, t),
            (p-1.25*s, l, t-l),
            (p-2*s, l, t-l),
            (p-1.25*s, -l, t-l),
            (p-2*s, -l, t-l),
            
            (p-2.25*s, l, 2*t),
            (p-3*s, l, 2*t),
            (p-2.25*s, -l, 2*t),
            (p-3*s, -l, 2*t),
            (p-2.25*s, l, 2*t-l),
            (p-3*s, l, 2*t-l),
            (p-2.25*s, -l, 2*t-l),
            (p-3*s, -l, 2*t-l),
            
            (p-3.25*s, l, 3*t),
            (p-4*s, l, 3*t),
            (p-3.25*s, -l, 3*t),
            (p-4*s, -l, 3*t),
            (p-3.25*s, l, 3*t-l),
            (p-4*s, l, 3*t-l),
            (p-3.25*s, -l, 3*t-l),
            (p-4*s, -l, 3*t-l),

            (p-4.25*s, l, 4*t),
            (p-5*s, l, 4*t),
            (p-4.25*s, -l, 4*t),
            (p-5*s, -l, 4*t),
            (p-4.25*s, l, 4*t-l),
            (p-5*s, l, 4*t-l),
            (p-4.25*s, -l, 4*t-l),
            (p-5*s, -l, 4*t-l),
            
            (p-5.125*s, l, 5*t),
            (p-5.125*s, l, 6*t),
            (p-5.125*s, -l, 5*t),
            (p-5.125*s, -l, 6*t),
            (p-5.125*s, l, 5*t-l),
            (p-5.125*s, l, 6*t-l),
            (p-5.125*s, -l, 5*t-l),
            (p-5.125*s, -l, 6*t-l),
            
            (p, l, 6*t),
            (p, -l, 6*t),
            (p+l, l, 6*t+l),
            (p+l, -l, 6*t+l),
            
            (p+l, l, -l),
            (p+l, -l, -l),
            
            (p-5.125*s, l, 6*t+l),
            (p-5.125*s, -l, 6*t+l),
            
        ]
        # define faces using the indexes of the vertices
        faces = [
            (4, 6, 53, 52),
            (4, 6, 49, 48),
            (52, 53, 51, 50),
            (4, 52, 50, 48),
            (6, 53, 51, 49),
            
            (49, 48, 41, 43),
            (51, 50, 54, 55),
            (41, 54, 50, 48),
            (43, 55, 51, 49),   
           
            (0, 2, 6, 4),
            
            (0, 1, 3, 2),
            (4, 5, 7, 6),
            (0, 1, 5, 4),
            (2, 3, 7, 6),
            
            (1, 3, 10, 8),
            (5, 7, 14, 12),
            (1, 5, 12, 8),
            (3, 7, 14, 10),
            
            (8, 9, 11, 10),
            (12, 13, 15, 14),
            (8, 9, 13, 12),
            (10, 11, 15, 14),
            
            (9, 11, 18, 16),
            (13, 15, 22, 20),
            (9, 13, 20, 16),
            (11, 15, 22, 18),
            
            (16, 17, 19, 18),
            (20, 21, 23, 22),
            (16, 17, 21, 20),
            (18, 19, 23, 22),
            
            (17, 19, 26, 24),
            (21, 23, 30, 28),
            (17, 21, 28, 24),
            (19, 23, 30, 26),
            
            (24, 25, 27, 26),
            (28, 29, 31, 30),
            (24, 25, 29, 28),
            (26, 27, 31, 30),
            
            (25, 27, 34, 32),
            (29, 31, 38, 36),
            (25, 29, 36, 32),
            (27, 31, 38, 34),
            
            (32, 33, 35, 34),
            (36, 37, 39, 38),
            (32, 33, 37, 36),
            (34, 35, 39, 38),
            
            (33, 35, 42, 40),
            (37, 39, 46, 44),
            (33, 37, 44, 40),
            (35, 39, 46, 42),
            
            (40, 42, 46, 44),
#            (44, 45, 47, 46)
            
        ]
        edges = []
        # create a mesh from the vert, edge, and face data
        mesh_data = bpy.data.meshes.new("cube_data")
        mesh_data.from_pydata(verts, edges, faces)
        # create a object using the mesh data
        mesh_obj = bpy.data.objects.new("cube_object", mesh_data)
        bpy.context.collection.objects.link(mesh_obj)
        mesh_obj.location.x = locX_fr
        mesh_obj.location.y = locY_fr
        mesh_obj.location.z = locZ_fr
         
        #MEMBERIKAN WARNA PADA OBJEK     
        mat = bpy.data.materials.new(name="EmissionMaterial")
        mat.use_nodes = True
        node_tree = mat.node_tree
        emission_shader = node_tree.nodes.new(type='ShaderNodeEmission')
        emission_shader.location = (0, 0)
        output_shader = node_tree.nodes["Material Output"]
        node_tree.links.new(emission_shader.outputs["Emission"], output_shader.inputs["Surface"])

        # Set emission color to red
        emission_shader.inputs["Color"].default_value = (1, 0.01, 0.01, 1)

        # Set emission strength to 5
        emission_shader.inputs["Strength"].default_value = 5

        # Assign the material to the object
        mesh_obj.data.materials.append(mat)

        # Enable bloom and screen space reflection in Eevee
        bpy.context.scene.eevee.use_bloom = True
        bpy.context.scene.eevee.use_ssr = True
    
    
        if x == 2:
            mesh_obj.rotation_euler[2] = 3.14159        
    



#######################################################################
                # camera_add 
#######################################################################   

# Tambahkan empty
def add_camera():
    bpy.ops.object.add(type='EMPTY', location=(0, 0, 30))
    empty = bpy.context.object
    empty.name = 'MyEmpty'

    # Tambahkan kamera
    bpy.ops.object.camera_add(location=(200, 200, 150), rotation=(math.radians(60), 0, math.radians(45)))
    camera = bpy.context.object
    camera.name = 'MyCamera'

    # Pilih kamera dan empty
    bpy.context.view_layer.objects.active = empty
    empty.select_set(True)
    camera.select_set(True)

    # Pilih empty sebagai parent dari kamera
    bpy.ops.object.parent_set(type='OBJECT')

    # Tambahkan constraint "Track To" pada kamera
    track_to_constraint = camera.constraints.new(type='TRACK_TO')
    track_to_constraint.target = empty  # Set the target to the empty
    track_to_constraint.track_axis = 'TRACK_NEGATIVE_Z'  # Camera tracks to the negative Z-axis of the empty
    track_to_constraint.up_axis = 'UP_Y'  # Y-axis is considered as the up axis

    # Fungsi untuk mengatur rotasi empty
    def rotate_empty(scene):
        empty.rotation_euler.z += math.radians(1)  # Mengubah nilai rotasi sesuai kebutuhan

    # Tambahkan handler untuk memanggil fungsi rotate_empty pada setiap frame
    bpy.app.handlers.frame_change_pre.append(rotate_empty)





#######################################################################
                # light sun
####################################################################### 
def add_sun():
    bpy.ops.object.light_add(type='SUN', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    bpy.context.object.rotation_euler[0] = 0.785398
    bpy.context.object.rotation_euler[1] = 0.523599
    bpy.context.object.rotation_euler[1] = 0.523599
    

#######################################################################
                # light point
####################################################################### 
def add_point():
    bpy.ops.object.light_add(type='POINT', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    bpy.context.object.data.energy = 1000
    bpy.ops.transform.translate(value=(2.41872, 4.51591, 8.03679), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)






#######################################################################
                # MAIN
####################################################################### 
#lokasi titik pusat
locX = 50
locY = 5
locZ = 12


clear_scene()
#lokasi titik pusat trapesium
lebar_alas = locX/4
locX_tp = locX * 3/2
locY_tp = lebar_alas/2
locZ_tp = locZ + 0
add_trapesium(lebar_alas,locX_tp,locY_tp,locZ_tp)

#lokasi titik pusat cylinder di kaki
radius = lebar_alas/4
depth = lebar_alas
locX_cy = locX_tp - (lebar_alas/2)
locY_cy = locY_tp + (lebar_alas)
locZ_cy = locZ + radius



#besar
for locZ_cy, locY_cy in [[locZ_cy, locY_cy + (lebar_alas * 3/4)], 
                  [(locZ_cy * 1.35),(locY_cy + (lebar_alas * 1.2/2))],
                  [(locZ_cy * 1.70),(locY_cy + (lebar_alas * 1.5/4))],
                  [(locZ_cy * 2.05),(locY_cy + (lebar_alas * 1/6))]
                  ]:
    add_cylinder(radius, depth, locX_cy, locY_cy, locZ_cy)


#lokasi titik pusat cylinder di tiang
radius = lebar_alas/2 + 1
depth = lebar_alas * 7 + 1
locX_cy = locX * 3/2 - (lebar_alas/2)
locY_cy = 0
locZ_cy = locZ + (depth/2) 
add_cylinder2(radius, depth, locX_cy, locY_cy, locZ_cy)


#lokasi titik pusat balok papan tulisan
sisi_balok = locX * 3/4
ket = "papan"
locX_bl = 0
locY_bl = 0
locZ_bl = lebar_alas * 6
add_balok(sisi_balok,locX_bl,locY_bl,locZ_bl, ket)


#lokasi titik pusat frame board dan bordernya
lebar_frame = locX / 4.225
#tinggi frame = 1*6
locX_fr = 0
locY_fr = 0
locZ_fr = locZ_bl - sisi_balok/2
add_frame_board(lebar_frame, locX_fr, locY_fr, locZ_fr)


#lokasi titik pusat balok tangga
sisi_balok = 23
ket = "tangga"
locX_bl = 0
locY_bl = 0

for sisi, locZ_bl in [[-23, sisi_balok/8],[23, sisi_balok/8],
                      [-20, sisi_balok*3/8],[20, sisi_balok*3/8],
                      [-15, sisi_balok*4.5/8],[15, sisi_balok*4.5/8]]:
    add_balok(sisi,locX_bl,locY_bl,locZ_bl, ket)


add_plane(500)
add_sun()
add_point()
add_camera()







