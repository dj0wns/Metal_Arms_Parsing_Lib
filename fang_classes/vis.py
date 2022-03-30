from construct import (
  Struct, Byte, Padding, CString, Tell, If
)
from .utils import Int32u, Int16u, Int8u, Int8s, Float32, Int64u, IsGC, IsXbox
from .common import (
  sphere, vec3, vec3a, xfm, mtx43a, color_rgb, color_rgba, color_motif, link, link_root
)
from .world import (
  world_key
)
from .light import (
  light_init
)

vis_axis_aligned_bounding_box = Struct (
  "min_xyz" / vec3,
  "max_xyz" / vec3
)

vis_cell_tree_node = Struct (
  "axis_aligned_bounding_box" / vis_axis_aligned_bounding_box,
  "parent_node_index" / Int16u,
  "child_node_index_1" / Int16u,
  "child_node_index_2" / Int16u,
  "containing_cell_index" / Int16u,

)

vis_cell_tree = Struct (
  "first_node_index" / Int16u,
  "node_count" / Int16u,
  "node_array_pointer" / Int32u
)

vis_cell = Struct (
  "bounding_sphere_in_world_space" / sphere,
  "parent_volume_idx" / Int16u,
  "plane_count" / Int8u,
  Padding(1),
  "bounding_planes_offset" / Int32u,
)

vis_plane = Struct (
  "normal" / vec3a,
  "point" / vec3a,
)

vis_portal = Struct (
  "flags" / Int16u,
  "portal_id" / Int16u,
  "adjacent_volume_ids" / Int16u[2],
  "portals_portal_index_in_adjacent_volume" / Int8u[2],
  "vertex_count" / Int16u,
  "coplanar_vertices_that_form_the_portal" / vec3[4],
  "normal" / vec3,
  "bounding_sphere_in_world_space" / sphere,
  "square_of_bounding_sphere_radius" / Float32,
)

def aggregate_volume_portal_pointers(volumes) :
  aggregate = 0
  for volume in volumes:
    aggregate += volume.portal_count
  return aggregate

#TODO Verify correctness of this structure - whats in source doesnt match, this is the closest guess without digging
vis_volume = Struct (
  "volume_id" / Int16u,
  "flags" / Int8u,
  Padding(1),
  "world_key" / world_key,
  "bounding_sphere_in_world_space" / sphere,
  "portal_count" / Int8u,
  "cell_count" / Int8u,
  "first_cell_index" / Int16u,
  "crosses_planes_mask" / Int8s,
  "active_adjacent_steps" / Int8u,
  "active_step_decrement" / Int8u,
  Padding(1),
  #This may have been removed due to the count being stored in the links
  #"number_of_trackers_intersecting_this_volume" / Int16u[3],
  #Padding(2),
  "tracker_intersects" / link_root[3],
  "portal_indices_pointer" / Int32u,
  "world_geo_associated_with_this_volume_pointer" / Int32u,
  "user_data_pointer" / Int32u,
)

vis_data = Struct (
  "portal_count" / Int16u,
  "cell_count" / Int16u,
  "volume_count" / Int16u,
  "light_count" / Int16u,
  "vis_cell_tree" / vis_cell_tree,
  "ambient_light_color" / color_rgb,
  "ambient_light_intensity" / Float32,
  "fog_start_z" / Float32,
  "fog_end_z" / Float32,
  "fog_motif" / color_motif,
  "portal_array_pointer" / Int32u,
  "volume_array_pointer" / Int32u,
  "cell_array_pointer" / Int32u,
  "light_init_array_pointer" / Int32u,
  "vis_cell_tree_nodes" / vis_cell_tree_node[lambda ctx: ctx.vis_cell_tree.node_count],
  "vis_portals" / vis_portal[lambda ctx: ctx.portal_count],
  "vis_volumes" / vis_volume[lambda ctx: ctx.volume_count],
  "portal_indices" / Int16u[lambda ctx: aggregate_volume_portal_pointers(ctx.vis_volumes)],
  Padding(32), # Unknown probably null bytes
  "vis_cells" / vis_cell[lambda ctx: ctx.cell_count],
  Padding(12), #unknown null bytes
  "vis_cell_bounding_planes" / vis_plane[lambda ctx: sum(cell.plane_count for cell in ctx.vis_cells)],
  "vis_lights" / light_init[lambda ctx: ctx.light_count],
  Padding(4), #unknown - probably alignment related
)
