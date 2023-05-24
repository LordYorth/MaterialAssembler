import unreal


# References
AssetMatTools = unreal.AssetToolsHelpers.get_asset_tools()
MaterialEditingLibrary = unreal.MaterialEditingLibrary
EditorAssetLibrary = unreal.EditorAssetLibrary
editor_util = unreal.EditorUtilityLibrary
content_browser = unreal.EditorUtilityLibrary.get_current_content_browser_path()
asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
selected_assets = asset_registry.get_assets_by_path(content_browser)


# Texture Handlers
def handle_base_color(rc_master_mat, t_basecolor):
    ts_node_basecolor = MaterialEditingLibrary.create_material_expression(rc_master_mat, unreal.MaterialExpressionTextureSample, -500, (node_spot * 300) - 450)
    ts_node_basecolor.set_editor_property('Texture', t_basecolor)
    MaterialEditingLibrary.connect_material_property(ts_node_basecolor, "RGB", unreal.MaterialProperty.MP_BASE_COLOR)


def handle_orm(rc_master_mat, t_metallic):
    #Occlusion
    ts_node_orm = MaterialEditingLibrary.create_material_expression(rc_master_mat, unreal.MaterialExpressionTextureSample, -500, (node_spot * 300) - 450)
    ts_node_orm.set_editor_property('Texture', t_metallic)
    MaterialEditingLibrary.connect_material_property(ts_node_orm, "R", unreal.MaterialProperty.MP_AMBIENT_OCCLUSION)

    #Roughness
    ts_node_orm.set_editor_property('Texture', t_metallic)
    MaterialEditingLibrary.connect_material_property(ts_node_orm, "G", unreal.MaterialProperty.MP_ROUGHNESS)

    #Metallic
    ts_node_orm.set_editor_property('Texture', t_metallic)
    MaterialEditingLibrary.connect_material_property(ts_node_orm, "B", unreal.MaterialProperty.MP_METALLIC)


def handle_normal(rc_master_mat, t_normal):
    ts_node_normal = MaterialEditingLibrary.create_material_expression(rc_master_mat,unreal.MaterialExpressionTextureSample, -500, (node_spot * 300) - 450)
    ts_node_normal.set_editor_property('Texture', t_normal)
    MaterialEditingLibrary.connect_material_property(ts_node_normal, "RGB", unreal.MaterialProperty.MP_NORMAL)


# create a dictionary that maps substrings to functions
handlers = {
    'BaseColor': handle_base_color,
    'OcclusionRoughnessMetallic': handle_orm,
    'Normal': handle_normal
}


# Create Dictionary [Material] = [Array of Textures]
materials = {}
#for asset in selected_assets:
for asset in selected_assets:
    asset = asset.get_asset()
    # Get name
    texture_name = asset.get_name()
    # Clean up name
    if texture_name.startswith("T_"):
        texture_name = texture_name[2:]

    texture_name = texture_name.split('_')[0]

    #Add to dictionary
    if texture_name in materials:
        materials[texture_name].append(asset.get_name())
    else:
        materials[texture_name] = [asset.get_name()]


# Assemble Materials from dictionary
for material_name, textures in materials.items():
    print(content_browser + "/" + material_name + ": " + ", ".join(textures))
    node_spot = 0

    rc_master_mat = AssetMatTools.create_asset("M_" +material_name, content_browser, unreal.Material, unreal.MaterialFactoryNew())

    # loop through the strings and call the appropriate function for each substring
    for texture in textures:
        for substr, handler in handlers.items():
            if substr in texture:
                node_spot += 1
                print(texture)
                t_node = unreal.EditorAssetLibrary.load_asset(content_browser + "/" + texture)
                handler(rc_master_mat, t_node)
    
    # Recompile Material
    unreal.MaterialEditingLibrary.recompile_material(rc_master_mat)
