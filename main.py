import sys
import os
import struct

bSize = 512
eBytVAL = b'4348PRJ3'
headVAL = '>8sQQ'

def create_index(filename):
    if os.path.exists(filename):
        print(f"Error:file already exists.")
        return

    with open(filename, 'wb') as f:
        header = struct.pack(headVAL, eBytVAL, 0, 1)
        padding = b'\x00' * (bSize - len(header))
        f.write(header + padding)

    print(f"Index file '{filename}' created successfully.")
def main():
    if len(sys.argv) < 3:
        print("Usage: project3 <command> <filename> [args...]")
        return

    command = sys.argv[1]
    filename = sys.argv[2]

    try:
        if command == "create":
            create_index(filename)

       #commands go here

        else:
            print(f"Unknown")

    except IndexError:
        print("Error: Missing arg")
    except ValueError:
        print("Error: Integers only")
    except Exception as e:
        print(f"Error: Exception")

if __name__ == "__main__":
    main()