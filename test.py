from fang_classes.objects import world
from fang_classes.utils import SetBigEndian, SetSmallEndian
import sys

if __name__ == "__main__":
  SetBigEndian()
  world_obj = world.parse_file(sys.argv[1])
  print(world_obj)

  # ENDIAN SWAPPING
  #SetSmallEndian()
  #world_obj = world.parse_file(sys.argv[1])
  #print(world_obj)
  #SetBigEndian()
  #world_data = world.build(world_obj)
  #endian_swapped = world.parse(world_data)
  #print(endian_swapped)
