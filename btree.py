import os
import struct

bSize = 512
eBytVAL = b'4348PRJ3'
headVAL = '>8sQQ'
nodeVAL = '>QQQ' + 'Q'*19 + 'Q'*19 + 'Q'*20
hSize = struct.calcsize(headVAL)
nSize = struct.calcsize(nodeVAL)
keyVAL = 19
childVAL = 20

def readh(f):
    f.seek(0)
    data = f.read(bSize)
    tempEight = struct.unpack(headVAL, data[:hSize])
    rootID = struct.unpack(headVAL, data[:hSize])
    nextID = struct.unpack(headVAL, data[:hSize])
    if tempEight != eBytVAL:
        raise Exception("Invalid index file format.")
    return rootID, nextID

def writeh(f, rootID, nextID):
    f.seek(0)
    header = struct.pack(headVAL, eBytVAL, rootID, nextID)
    f.write(header + b'\x00' * (bSize - hSize))
