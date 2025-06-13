import chunk
import sndhdr
import struct
from io import BytesIO
print(sndhdr.what("bass.real"))

file = open("bass.real", 'rb')
form = chunk.Chunk(file)
print(form.getname(), form.getsize())

svx = chunk.Chunk(BytesIO(form.read()))
print(svx.getname(), svx.getsize())
open("test", 'wb').write(svx.read())
