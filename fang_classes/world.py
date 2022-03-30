from construct import (
  Struct, Byte, Padding, CString, Tell, If, Pointer, Enum, Switch, Pass
)
from .utils import Int32u, Int32s, Int16u, Int8u, Int8s, Float32, Int64u, IsGC, IsXbox
from .common import (
  sphere, vec3, xfm, mtx43, mtx43a, color_rgb, color_rgba, color_motif,
  link, link_root
)
from .csv import csv_header
from .enums import ShapeType

world_header = Struct (
  "num_bytes" / Int32u,
  "num_meshes" / Int32u,
  "offset_to_mesh_inits" / Int32u,
  "offset_to_mesh_sizes" / Int32u,
  "mesh_bytes" / Int32u,
  "world_offset" / Int32u,
  "world_bytes" / Int32u,
  "streaming_data_offset" / Int32u,
  "streaming_data_bytes" / Int32u,
  "init_offset" / Int32u,
  "init_bytes" / Int32u,
)

world_mesh_header = Struct (
  "offset_to_fixup_table" / Int32u,
  "num_fixups" / Int32u,
  Padding(8)
)

world_data_header = Struct (
  "offset_to_fixup_table" / Int32u,
  "num_fixups" / Int32u,
  Padding(8)
)

world_init_header = Struct (
  "num_init_structs" / Int32u,
  Padding(12)
)

world_key = Struct (
  "visited_key" / Int32u[3]
)

world_mesh_directional_light = Struct (
  "light_color_motif" / color_motif,
  "intensity" / Float32,
  "light_direction" / vec3,
)

world_tracker = Struct (
  "offset" / Tell,
  "visited_key" / world_key,
  "user_pointer" / Int32u,
  "user_data" / Int32u,
  "last_frame_moved" / Int32u,
  "user_type_bits" / Int64u,
  "tracker_type" / Int8u,
  "tracker_flags" / Int8u,
  "intersect_list" / link_root,
  "bound_sphere" / sphere,
  "tracker_link" / link,
  "tracker_auto_delete_link" / link
)

world_mesh_instance = Struct (
  "offset" / Tell,
  "pointer_to_mesh" / Int32u,
  "flags" / Int32u,
  "cull_distance" / Float32,
  "kdop_buffer_start_index" / Int16u,
  "cull_direction" / Int8u,
  "current_lod" / Int8u,
  "transformation_matrix" / xfm,
  "bounding_sphere" / sphere,
  "final_ambient_rgb" / color_rgb,
  "procedural_textures_offset" / Int32u,
  "frame_last_drawn" / Int32u,
  "bone_matrix_palette" / mtx43a,
  "created_parts_mask" / Int32u,
  "drawn_parts_mask" / Int32u,
  "collision_parts_mask" / Int32u,
  "created_bones_count" / Int8u,
  "drawn_bones_count" / Int8u,
  "color_stream_count" / Int8u,
  "render_light_count" / Int8u,
  "lowest_weighted_light" / Int8s,
  Padding(1),
  "pixel_radius_last_render" / Int16u,
  "render_lights_pointer" / Int32u,
  "color_streams_pointer" / Int32u,
  "mesh_instance_texture_layer_id_pointer" / Int32u,
  "mesh_animation_tc_pointer" / Int32u,
  "mesh_texture_flip_pointer" / Int32u,
  "mesh_tint" / color_rgba,
  "shadow_intensity" / Float32,
  "frame_of_last_animate_layer" / Int32u,
  "last_animate_layer_ticks" / Int64u,
  "mesh_instance_pre_draw_callback_pointer" / Int32u,
  "mesh_instance_post_draw_callback_pointer" / Int32u,
)

world_mesh = Struct (
  "world_tracker" / world_tracker,
  "world_mesh_instance" / world_mesh_instance,
  "ambient_rgb" / color_rgb,
  "directional_light" / world_mesh_directional_light,
  "light_root" / link_root,
  "id" / Int32u,
  "world_collision_prep_callback_pointer" / Int32u,
  "drawn_key" / Int32u
)

world_line = Struct (
  "length" / Float32
)

world_spline = Struct (
  "point_count" / Int32u,
  "closed_spline" / Int32u,
  "point_array_pointer" / Int32u,
  "point_array" / vec3[lambda ctx: ctx.point_count],
)

world_box = Struct (
  "dimensions" / vec3
)

world_sphere = Struct (
  "radius" / Float32
)

world_cylinder = Struct (
  "radius" / Float32,
  "length" / Float32
)

world_mesh = Struct (
  "name_offset" / Int32u,
  "name" / Pointer(lambda ctx: ctx._._.inits_offset + ctx.name_offset,
                   CString("ascii")),
  "lightmap_name_offsets" / Int32u[4],
  "lightmap_motifs" / Int16u[4],
  "flags" / Int32u,
  "cull_distance" / Float32,
  "tint" / color_rgb,
  "color_stream_count" / Int8u,
  Padding(3),
  "color_stream_offset" / Int32u
)

world_shape_init = Struct (
  "shape_type" / Enum(Int32u, ShapeType),
  "data_pointer" / Int32u,
  "data" / Pointer(lambda ctx: ctx._.inits_offset + ctx.data_pointer,
                   Switch(lambda ctx: int(ctx.shape_type), {
                       ShapeType.Point : Pass,
                       ShapeType.Line : world_line,
                       ShapeType.Spline : world_spline,
                       ShapeType.Box : world_box,
                       ShapeType.Sphere : world_sphere,
                       ShapeType.Cylinder : world_cylinder,
                       ShapeType.Mesh : world_mesh,
                   })),
  "orientation" / mtx43,
  "parent_shape_index" / Int32s,
  "game_data_pointer" / Int32s,
  "game_data" / If(lambda ctx: ctx.game_data_pointer > 0,
                   Pointer(lambda ctx: ctx.game_data_pointer + ctx._.inits_offset,
                           csv_header))
)
