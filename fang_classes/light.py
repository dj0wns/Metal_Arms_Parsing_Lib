from construct import (
  Struct, Byte, Padding, CString, Tell, If, PaddedString
)
from .utils import Int32u, Int16u, Int8u, Int8s, Float32, Int64u, IsGC, IsXbox
from .common import (
  sphere, vec3, xfm, mtx43a, mtx43, color_rgb, color_rgba, color_motif, link, link_root
)
from .world import (
  world_key
)

light_init = Struct (
  #TODO fix strings
  "name" / PaddedString(16, "utf-8"),
  #"name" / Byte[16],
  "per_pixel_texture_name" / PaddedString(16, "utf-8"),
  #"per_pixel_texture_name" / Byte[16],
  "corona_texture_name" / PaddedString(16, "utf-8"),
  #"corona_texture_name" / Byte[16],
  "flags" / Int32u,
  "light_id" / Int16u,
  "type" / Int8u,
  Padding(1),
  "intensity" / Float32,
  "motif" / color_motif,
  "light_position_and_radius_in_model_space" / sphere,
  "orientation_in_model_space" / mtx43,
  "spotlight_inner_radians" / Float32,
  "spotlight_outer_radians" / Float32,
  "corona_scale" / Float32
)
