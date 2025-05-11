# OSProj3
Repository for OS Project 3 

Format: create file | search (file) ____ | insert (file) ____ | load (file) ___ | print (file) | extract (file) (other file)
Click m to exit when you run

an interactive program that creates and manages index files. The index files will contain a b-tree. The user can create, insert, and search such index files. The program will be a command-line program that allows the user to give various commands as command-line arguments. These commands will perform various operations on an index file.

Commands: create search insert load print extract 

The index file will be divided into blocks of 512 bytes. Each node of the btree will fit in one 512 byte block, and the file header will use the entire first block. New nodes will be appended to the end of the file. Since, we do not have a delete operation, we do not need to worry about deleting nodes.

The header can be maintained in memory, but needs to be in sync with the file. The header will have the following fields, in the order presented.

The b-tree should have minimal degree 10. This will give 19 key/value pairs, and 20 child pointers. Each node will be stored in a single block with some header information. Below is the node block f ields in order.
