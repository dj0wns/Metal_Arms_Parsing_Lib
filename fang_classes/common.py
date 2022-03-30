from construct import (
  Struct, Padding, If
)
from .utils import Int32u, Int32s, Int16u, Float32, IsXbox, IsGC

vec2 = Struct (
  "x" / Float32,
  "y" / Float32,
)

vec3 = Struct (
  "x" / Float32,
  "y" / Float32,
  "z" / Float32,
)

vec3a = Struct (
  "x" / Float32,
  "y" / Float32,
  "z" / Float32,
  If(lambda ctx: IsXbox(), Padding(112)), # TODO check this for xbox
  If(lambda ctx: IsGC(), Padding(4)) # TODO check this for gc
)

vec4 = Struct (
  "x" / Float32,
  "y" / Float32,
  "z" / Float32,
  "w" / Float32,
)

vec4a = Struct (
  "x" / Float32,
  "y" / Float32,
  "z" / Float32,
  "w" / Float32,
  If(lambda ctx: IsXbox(), Padding(112)), # TODO check this
)

sphere = Struct (
  "radius" / Float32,
  "position" / vec3,
)

mtx33 = Struct (
  "v_x" / vec3,
  "v_y" / vec3,
  "v_z" / vec3,
)

mtx43 = Struct (
  "v_right" / vec3,
  "v_up" / vec3,
  "v_front" / vec3,
  "v_pos" / vec3,
)

mtx43a = Struct (
  "v_right" / vec3a,
  "v_up" / vec3a,
  "v_front" / vec3a,
  "v_pos" / vec3a,
)

mtx44 = Struct (
  "v_right" / vec4,
  "v_up" / vec4,
  "v_front" / vec4,
  "v_pos" / vec4,
)

mtx44a = Struct (
  "v_right" / vec4a,
  "v_up" / vec4a,
  "v_front" / vec4a,
  "v_pos" / vec4a,
)

color_rgb = Struct (
  "red" / Float32,
  "green" / Float32,
  "blue" / Float32
)

color_rgba = Struct (
  "red" / Float32,
  "green" / Float32,
  "blue" / Float32,
  "alpha" / Float32
)

color_motif = Struct (
  "color" / color_rgba,
  "motif_index" / Int32u
)

#Fang transformation matrix
xfm = Struct (
  "forward_matrix" / mtx43a,
  "reverse_matrix" / mtx43a,
  "forward_scale" / Float32,
  "reverse_scale" / Float32,
)

#Fang Doubly Linked List
link = Struct (
  "prev_link_pointer" / Int32u,
  "next_link_pointer" / Int32u,
)

link_root = Struct (
  "head" / link,
  "tail" / link,
  "struct_offset" / Int32s,
  "count" / Int32u,
)
