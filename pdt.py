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
    
    current_file_spacing = ' |'*current_depth
    current_folder_spacing = ' |'*(current_depth-1)
    files_and_folders = list(this_path.glob('*'))
    files = [f.name for f in files_and_folders if not f.is_dir()]
    folders = [f for f in files_and_folders if f.is_dir()]

    if filter_hidden:
        files = list(filter(filter_hidden_files, files))
        folders = list(filter(filter_hidden_folders, folders))

    subtree_struct = f'{current_folder_spacing}-{this_path.name}{os.path.sep}\n'

    for f in files:
        subtree_struct += f'{current_file_spacing}-{f}\n'
    
    if len(folders) > 0:
        for f in sorted(folders):
            _s = return_current_structure(f, current_depth+1, max_depth, filter_hidden)
            
            subtree_struct += _s
        
    return subtree_struct

def create_dir_tree(dirpath=Path('.'), output_path=None, max_depth=5, filter_hidden=False):

    current_depth = 0
    tree_structure = return_current_structure(dirpath, current_depth+1, max_depth, filter_hidden)
    
    if output_path is not None:
        with open(output_path[0], 'w') as outf:
            outf.write(tree_structure)
    else:
        print(tree_structure)

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

    create_dir_tree(dirpath, output_path, max_depth, filter_hidden)