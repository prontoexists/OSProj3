import sys
import os
import struct

bSize = 512
eBytVal = b'4348PRJ3'
headVAL = '>8sQQ'

def create_index(filename):

    if os.path.exists(filename):

        print(f"Error: file already exists.")
        return

    try:
        with open(filename, 'wb') as f:

            header = struct.pack(headVAL, eBytVal, 0, 1)
            padding = b'\x00' * (bSize - len(header))
            f.write(header + padding)

        print(f"file created successfully.")

    except Exception as e:

        print(f"Error creating file ")

def insert_key(filename, key, value):

    from btree import insert_key

    try:

        insert_key(filename, key, value)
        print(f"Inserted key={key}, value={value} into {filename}.")

    except Exception as e:

        print(f"Error inserting into '{filename}': {e}")

def search_key(filename, key):

    from btree import search_key
    try:

        search_key(filename, key)

    except Exception as e:

        print(f"Error searching")

def print_tree(filename):

    from btree import print_tree
    try:
        print_tree(filename)

    except Exception as e:

        print(f"Error printing ")

def load_csv(filename, csvfile):

    from btree import load_csv
    try:

        load_csv(filename, csvfile)
        print(f"Data successfully loaded")

    except Exception as e:

        print(f"Error loading CSV file ")

def extract_csv(filename, output):

    from btree import extract_csv
    try:

        extract_csv(filename, output)
        print(f"Data extracted")

    except Exception as e:
        print(f"Error extracting data ")

def handle_command(command_args):


    command = command_args[0]
    filename = command_args[1]

    try:
        if command == "create":

            create_index(filename)

        elif command == "insert":

            if len(command_args) < 4:
                print("Error insert needs a key and a value.")
                return

            key = int(command_args[2])
            value = int(command_args[3])
            insert_key(filename, key, value)

        elif command == "search":

            if len(command_args) < 3:
                print("Error: search needs a key.")
                return

            key = int(command_args[2])
            search_key(filename, key)

        elif command == "print":
            print_tree(filename)

        elif command == "load":

            if len(command_args) < 3:
                print("Error load requires csv")
                return

            csvfile = command_args[2]
            load_csv(filename, csvfile)

        elif command == "extract":

            if len(command_args) < 3:
                print("Error: 'extract' requires output")
                return

            output = command_args[2]
            extract_csv(filename, output)

        else:
            print(f" error Unknown command")

    except ValueError:
        print("Error: Key and value must be integers.")
    except Exception as e:
        print(f"Error: {e}")

def main():

    print("Format: create file | search (file) ____ | insert (file) ____ | load (file) ___ | print (file) | extract (file) (other file)" )
    print("Type 'm' to exit.\n")

    while True:

        user_input = input("Enter command: ").strip()

        if user_input.lower() == "m":

            print("Exit")
            break

        command_args = user_input.split()
        handle_command(command_args)

if __name__ == "__main__":
    main()
