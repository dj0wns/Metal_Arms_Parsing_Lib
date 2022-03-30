from construct import (
  Struct, Byte, Padding, CString, Tell, If, PaddedString, Pointer
)
from .utils import Int32u, Int16u, Int8u, Int8s, Float32, Int64u, IsGC, IsXbox
from .common import sphere, vec3, xfm, mtx43a, color_rgb, color_rgba

mesh_segment = Struct (
  "bounding_sphere_in_model_space" / sphere,
  "bone_matrix_count" / Int8u,
  #TODO check this padding
  "bone_matrix_indexes" / Int8u[4],
  Padding(3),

)

mesh_material = Struct (
  "shader_light_register_array_pointer" / Int32u,
  "shader_surface_register_array_pointer" / Int32u,
  "light_shader_index" / Int8u,
  "specular_shader_index" / Int8u,
  "surface_shader_index" / Int16u,
  "mesh_part_id_mask" / Int32u,
  "platform_specific_data_pointer" / Int32u,
  "lod_mask" / Int8u,
  "depth_bias_level" / Int8u,
  "base_st_sets" / Int8u,
  "light_map_st_sets" / Int8u,
  "texture_layer_id_index" / Int8u[4],
  "affect_angle" / Float32,
  "compressed_affect_normal" / Int8s[3],
  "affect_bone_id" / Int8s,
  "compressed_radius" / Int8u,
  Padding(1),
  "material_flags" / Int16u,
  #TODO move material_flags to an enum type
  "draw_key" / Int32u,
  "material_tint" / color_rgb,
  "average_vertex_position" / vec3,
  "display_list_hash_key" / Int32u
)

mesh = Struct (
  "offset" / Tell,
  "name" / PaddedString(12, "ascii"),
  "bounding_sphere" / sphere,
  "bounding_box_minimum" / vec3,
  "bounding_box_maximum" / vec3,
  #TODO This padding seems correct, double check later
  Padding(4),
  "flags" / Int16u,
  "mesh_collision_mask" / Int16u,
  "used_bone_count" / Int8u,
  "root_bone_index" / Int8u,
  "bone_count" / Int8u,
  "segment_count" / Int8u,
  "texture_layer_id_count" / Int8u,
  "texture_layer_id_count_with_ST_INFO" / Int8u,
  "texture_layer_id_count_with_FLIP_INFO" / Int8u,
  "light_count" / Int8u,
  "material_count" / Int8u,
  "collision_tree_count" / Int8u,
  "lod_count" / Int8u,
  "shadow_lod_bias" / Int8u,
  "lod_distance" / Float32[8],
  "mesh_segment_array_pointer" / Int32u,
  "mesh_segments" / If(lambda ctx: ctx.segment_count > 0,
                       Pointer(lambda ctx: ctx.offset + ctx.mesh_segment_array_pointer,
                               mesh_segment[lambda ctx: ctx.segment_count])),
  "mesh_bone_array_pointer" / Int32u,
  #TODO parse mesh bones
  "light_array_pointer" / Int32u,
  #TODO parse lights
  "skeleton_index_array_pointer" / Int32u,
  #TODO parse seleton indexes
  "material_array_pointer" / Int32u,
  "materials" / If(lambda ctx: ctx.material_count > 0,
                       Pointer(lambda ctx: ctx.offset + ctx.material_array_pointer,
                               mesh_material[lambda ctx: ctx.material_count])),

  "collision_tree_array_pointer" / Int32u,
  "texture_layer_id_array_pointer" / Int32u,
  "implementation_specific_object_data_pointer" / Int32u,
)
