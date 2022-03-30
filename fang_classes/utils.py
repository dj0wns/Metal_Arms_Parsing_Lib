from construct import (
  Int64ul, Int64ub,
  Int32ul, Int32ub, Int32sl, Int32sb,
  Int16ul, Int16ub,
  Int8ul, Int8ub, Int8sl, Int8sb,
  IfThenElse, Float32l, Float32b
)

ENDIAN = 'small'
PLATFORM = 'gc'

#special classes to deal with endianness
Int64u = IfThenElse(lambda ctx: True if GetEndian() == "small" else False, Int64ul, Int64ub)
Int32u = IfThenElse(lambda ctx: True if GetEndian() == "small" else False, Int32ul, Int32ub)
Int32s = IfThenElse(lambda ctx: True if GetEndian() == "small" else False, Int32sl, Int32sb)
Int16u = IfThenElse(lambda ctx: True if GetEndian() == "small" else False, Int16ul, Int16ub)
Int8u = IfThenElse(lambda ctx: True if GetEndian() == "small" else False, Int8ul, Int8ub)
Int8s = IfThenElse(lambda ctx: True if GetEndian() == "small" else False, Int8sl, Int8sb)
Float32 = IfThenElse(lambda ctx: True if GetEndian() == "small" else False, Float32l, Float32b)

def GetEndian() :
  global ENDIAN
  return ENDIAN

def SetBigEndian() :
  global ENDIAN
  ENDIAN = 'big'

def SetSmallEndian() :
  global ENDIAN
  ENDIAN = 'small'

def SetXbox() :
  global PLATFORM
  PLATFORM = 'xbox'

def SetGC() :
  global PLATFORM
  PLATFORM = 'gc'

def IsGC() :
  global PLATFORM
  return PLATFORM == 'gc'

def IsXbox() :
  global PLATFORM
  return PLATFORM == 'xbox'
