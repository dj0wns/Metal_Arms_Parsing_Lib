import enum
from construct import (
  Struct, Padding, If, PaddedString, Tell, Byte, Enum, Pointer, Computed, Switch, Pass
)
from .utils import Int32u, Int32s, Int16u, Float32, IsXbox, IsGC
from .enums import CSVFieldType

csv_field = Struct (
  "data_type" / Enum(Int32u, CSVFieldType),
  "string_pointer" / If(lambda ctx: int(ctx.data_type) != CSVFieldType.Float, Int32u),
  "float" / If(lambda ctx: int(ctx.data_type) == CSVFieldType.Float, Float32),
  "string_length" / Int32u,
  "string" / Switch(lambda ctx: int(ctx.data_type), {
         CSVFieldType.String : Pointer(lambda ctx: ctx._._.offset + ctx.string_pointer,
             PaddedString(lambda ctx: ctx.string_length, 'ascii')),
         CSVFieldType.Float : Pass,
         CSVFieldType.Widestring : Pointer(lambda ctx: ctx._._.offset + ctx.string_pointer,
             PaddedString(lambda ctx: ctx.string_length * 2, 'utf-16-le')),

     }),
)

csv_table = Struct (
  "keystring_pointer" / Int32u,
  "keystring_length" / Int32u,
  "keystring" / Pointer(lambda ctx: ctx._.offset + ctx.keystring_pointer,
                        PaddedString(lambda ctx: ctx.keystring_length, 'ascii')),
  "number_of_fields" / Int16u,
  "table_index" / Int16u,
  "field_pointer" / Int32u,
  "fields" / Pointer(lambda ctx: ctx.field_pointer + ctx._.offset,
                     csv_field[lambda ctx: ctx.number_of_fields])
)

csv_header = Struct (
  "offset" / Tell,
  "size" / Int32u,
  "number_of_tables" / Int32u,
  "table_pointer" / Int32u,
  "flags" / Int32u,
  "table_pointer_value" / Computed(lambda ctx: ctx.offset + ctx.table_pointer),
  "tables" / Pointer(lambda ctx: ctx.offset + ctx.table_pointer,
                     csv_table[lambda ctx: ctx.number_of_tables])
)
