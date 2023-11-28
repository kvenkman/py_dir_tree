import argparse
from pathlib import Path
import os

def filter_hidden_files(f):
    return not f.startswith('.')

def filter_hidden_folders(f):
    return not f.name.startswith('.')

def return_current_structure(this_path, current_depth, max_depth, filter_hidden=False):
    if current_depth > max_depth:
        return ''
    
    if current_depth > 0:
        current_file_spacing = '│\t'*max(0, (current_depth))
        current_folder_spacing = '│\t'*(max(0, current_depth))
    else:
        current_file_spacing = ''
        current_folder_spacing = ''

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

    if current_depth == 0:
        subtree_struct = [f'{this_path.name}{os.path.sep}\n']
    else:
        subtree_struct = [f'{current_folder_spacing}├─ {this_path.name}{os.path.sep}\n']

    for f in sorted(files):
        subtree_struct.append(f'{current_file_spacing}├─ {f}\n')
    
    if len(folders) > 0:
        for fcount, f in enumerate(sorted(folders)):
            _s = return_current_structure(f, current_depth+1, max_depth, filter_hidden)
            
            if fcount == len(folders):
                _s = _s.split("\n")
                _s[0] = _s[0].replace("├─", "└─")
                _s = '\n'.join(_s)
            subtree_struct.append(_s)
    
    temp_subtree = subtree_struct[-1].split("\n")
    
    for temp_subtree_count, t in enumerate(temp_subtree):
        if temp_subtree_count == 0:
            temp_subtree[temp_subtree_count] = temp_subtree[temp_subtree_count].replace("├─", "└─")
        else:
            temp_subtree[temp_subtree_count] = temp_subtree[temp_subtree_count].replace("│", " ", 1)
    subtree_struct[-1] = "\n".join(temp_subtree)
    

    return ''.join(subtree_struct)

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
    tree_structure = return_current_structure(dirpath, current_depth, max_depth, filter_hidden)

    if output_path is not None:
        with open(output_path[0], 'w') as outf:
            outf.write(tree_structure)
    else:
        print(tree_structure)