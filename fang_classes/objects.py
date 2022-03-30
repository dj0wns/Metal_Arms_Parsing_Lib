from construct import (
  Struct, Byte, Array, Padding, Tell, If, Pointer
)
from .utils import Int32u
from .world import (
  world_header, world_mesh_header, world_data_header, world_init_header,
  world_mesh, world_shape_init,
)
from .mesh import (
  mesh
)
from .vis import (
  vis_data,
)


world = Struct(
  "offset" / Tell,
  "header" / world_header,
  "mesh_offset" / Tell,
  "mesh_pointers" / Int32u[lambda ctx: ctx.header.num_meshes],
  "mesh_sizes" / Int32u[lambda ctx: ctx.header.num_meshes],
  "meshes" / Array(lambda ctx: ctx.header.num_meshes,
                   Pointer(lambda ctx: ctx.offset + ctx.mesh_pointers[ctx._index],
                           mesh)),
  #TODO figure out to use these mesh sizes for mesh reading - maybe each mesh knows
  #Skip unknown data
  "offset1" / Tell,
  Padding(lambda ctx: ctx.header.world_offset - ctx.offset1),
  "vis_data" / vis_data,
  #TODO consider splitting this up
  "streaming_data" / If(lambda ctx: ctx.header.streaming_data_bytes > 0, Byte[lambda ctx: ctx.header.streaming_data_bytes]),
  "offset2" / Tell,
  #"data_header" / world_data_header,
  ##Skip unknown data
  #Padding(lambda ctx: ctx.header.init_offset - ctx.offset2),
  "init_header" / world_init_header,
  "inits_offset" / Tell,
  "inits" / world_shape_init[lambda ctx: ctx.init_header.num_init_structs],
)

