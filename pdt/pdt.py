import argparse
from pathlib import Path
import os

def filter_hidden_files(f):
    return not f.startswith('.')

def filter_hidden_folders(f):
    return not f.name.startswith('.')

def return_current_structure(this_path, current_depth, max_depth, total_folders, folder_count, current_depth_prefix, filter_hidden=False):
    v_bracket = '│ '
    t_bracket = '├─'
    l_bracket = '└─'

    if current_depth > max_depth:
        return ['']
    
    files_and_folders = list(this_path.glob('*'))

    files = []
    folders = []

    for f in files_and_folders:
        if not f.is_dir():
            files.append(f.name)
        else:
            folders.append(f)

    if filter_hidden:
        files = list(filter(filter_hidden_files, files))
        folders = list(filter(filter_hidden_folders, folders))

    subtree_struct = []

    if current_depth == 0:
        subtree_struct.append(f"{os.path.sep}" + "\n")
    else:
        folder_prefix = t_bracket if folder_count < total_folders else l_bracket
        folder_prefix = current_depth_prefix[:-2] + folder_prefix if folder_count == total_folders else current_depth_prefix[:-3] + folder_prefix
        subtree_struct.append(f"{folder_prefix} {this_path.name}{os.path.sep}" + "\n")


    for i, file in enumerate(sorted(files)):
        if (i+1) < len(files) + len(folders):
            subtree_struct.append(f"{current_depth_prefix}{t_bracket} {file}\n")
        else:
            subtree_struct.append(f"{current_depth_prefix}{l_bracket} {file}\n")

    for i, folder in enumerate(folders):
        if i+1 != len(folders):
            next_prefix = current_depth_prefix + f"{v_bracket}\t"
        else:
            next_prefix = current_depth_prefix + f" \t"

        s_ = return_current_structure(folder, current_depth+1, max_depth, len(folders), i+1, next_prefix, filter_hidden)
        subtree_struct.extend(s_)
    
    return subtree_struct

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Print directory structure for requested folder or pipe it to a folder')

    parser.add_argument('path')
    parser.add_argument('-p', '--path', type=str, nargs=1, default = '.', help='Directory tree will begin at this path (default: current directory')
    parser.add_argument('-o', '--output-file', type=str, nargs=1, default=[None], help='If specified, directory tree will be written to this file')
    parser.add_argument('-d', '--depth', type=int, nargs=1, default=[5], help='Maximum depth to recurse (default: 5). Set to -1 to recurse all the way to the bottom')
    parser.add_argument('-f', '--filter-hidden', action='store_true', help='Filter hidden files and folders (default: False)')
    args = parser.parse_args()

    dirpath = Path(args.path)
    output_path = args.output_file[0]
    max_depth = args.depth[0]
    filter_hidden = args.filter_hidden

    current_depth = 0
    total_folders = 1
    folder_count = 1
    next_prefix = ''
    tree_structure = return_current_structure(dirpath, current_depth, max_depth, total_folders, folder_count, next_prefix, filter_hidden)

    tree_structure = ''.join(tree_structure)

    if output_path is not None:
        with open(output_path[0], 'w') as outf:
            outf.write(tree_structure)
    else:
        print(tree_structure)