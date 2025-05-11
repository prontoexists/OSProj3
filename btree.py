import os
import struct

bSize = 512
eBytVAL = b'4348PRJ3'
headVAL = '>8sQQ'
nodeVAL = '>QQQ' + 'Q' * 19 + 'Q' * 19 + 'Q' * 20
hSize = struct.calcsize(headVAL)
nSize = struct.calcsize(nodeVAL)
keyVAL = 19
childVAL = 20


def readh(f):

    f.seek(0)
    data = f.read(bSize)
    magic, root_id, next_block_id = struct.unpack(headVAL, data[:hSize])
    if magic != eBytVAL:
        raise Exception("Invalid index file format.")
    return root_id, next_block_id

def writeh(f, root_id, next_block_id):

    f.seek(0)
    header = struct.pack(headVAL, eBytVAL, root_id, next_block_id)
    f.write(header + b'\x00' * (bSize - hSize))

def read_node(f, block_id):

    f.seek(block_id * bSize)
    data = f.read(bSize)
    tempQ = struct.unpack(nodeVAL, data[:nSize])
    return {
        'id': tempQ[0],
        'parent': tempQ[1],
        'num_keys': tempQ[2],
        'keys': list(tempQ[3:3 + keyVAL]),
        'values': list(tempQ[3 + keyVAL:3 + 2 * keyVAL]),
        'children': list(tempQ[3 + 2 * keyVAL:3 + 2 * keyVAL + childVAL])
    }

def write_node(f, node):

    newQ = struct.pack(
        nodeVAL,
        node['id'],
        node['parent'],
        node['num_keys'],
        *node['keys'],
        *node['values'],
        *node['children']
    )
    f.seek(node['id'] * bSize)
    f.write(newQ + b'\x00' * (bSize - nSize))

def insert_key(filename, key, value):

    with open(filename, 'r+b') as f:
        root_id, next_block_id = readh(f)

        if root_id == 0:
            node = {
                'id': 1,
                'parent': 0,
                'num_keys': 1,
                'keys': [key] + [0] * (keyVAL - 1),
                'values': [value] + [0] * (keyVAL - 1),
                'children': [0] * childVAL
            }
            write_node(f, node)
            writeh(f, 1, 2)
        else:
            node = read_node(f, root_id)

            if node['num_keys'] < keyVAL:
                idx = node['num_keys']
                node['keys'][idx] = key
                node['values'][idx] = value
                node['num_keys'] += 1
                write_node(f, node)
            else:
                raise Exception("Node Full")


def search_key(filename, key):

    with open(filename, 'rb') as f:
        root_id, _ = readh(f)
        if root_id == 0:
            print("Key not found.")
            return
        node = read_node(f, root_id)
        for i in range(node['num_keys']):
            if node['keys'][i] == key:
                print(f"Found: {key}, {node['values'][i]}")
                return
        print("Key not found.")


def print_tree(filename):
    with open(filename, 'rb') as f:
        root_id, _ = readh(f)
        if root_id == 0:
            print("Empty tree.")
            return
        node = read_node(f, root_id)
        for i in range(node['num_keys']):

            print(f"{node['keys'][i]} , {node['values'][i]}")


def load_csv(filename, csvfile):

    if not os.path.exists(csvfile):
        print(f"Error: CSV file '{csvfile}' not found.")
        return

    with open(csvfile, 'r') as csv:
        for line in csv:
            try:
                key, value = map(int, line.strip().split(','))
                insert_key(filename, key, value)
            except ValueError:
                print(f"error ")
            except Exception as e:
                print(f"Error inserting  {e}")

    print(f"Data loaded from '{csvfile}' into '{filename}'.")


def extract_csv(filename, output):

    if os.path.exists(output):
        print(f"Error: Output file  already exists.")
        return

    with open(filename, 'rb') as f, open(output, 'w') as out:
        root_id, _ = readh(f)

        if root_id == 0:
            print(f"No data to extract from")
            return

        node = read_node(f, root_id)

        for i in range(node['num_keys']):

            out.write(f"{node['keys'][i]} , {node['values'][i]}\n")

    print(f"Data extracted to '{output}'.")
