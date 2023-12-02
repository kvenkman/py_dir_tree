Print directory structure for requested folder or pipe it to an output file. 

For example, 
```
> python pdt\pdt.py .
-\
 ├─ LICENSE.txt
 ├─ README.md
 ├─ test_file.txt
 ├─ __init__.py
 ├─ .git\
 │   ├─ config
 │   ├─ description
 │   ├─ HEAD
 │   ├─ hooks\
 │   │   ├─ applypatch-msg.sample
 │   │   ├─ commit-msg.sample
 │   │   ├─ fsmonitor-watchman.sample
 │   │   ├─ post-update.sample
 │   │   ├─ pre-applypatch.sample
 │   │   ├─ pre-commit.sample
 │   │   ├─ pre-merge-commit.sample
 │   │   ├─ pre-push.sample
 │   │   ├─ pre-rebase.sample
 │   │   ├─ pre-receive.sample
 │   │   ├─ prepare-commit-msg.sample
 │   │   ├─ push-to-checkout.sample
 │   │   └─ update.sample
 │   ├─ info\
 │   │   └─ exclude
 │   ├─ objects\
 │   │   ├─ info\
 │   │   └─ pack\
 │   └─ refs\
 │       ├─ heads\
 │       └─ tags\
 └─ pdt\
     ├─ pdt.py
     └─ __init__.py
```
or the output can be piped to a file:
```
> python pdt.py . -o test_output
> 
```
The script accepts a list of arguments:
```
> python pdt.py -h
usage: pdt.py [-h] [-p PATH] [-o OUTPUT_FILE] [-d DEPTH] [-f] path

Print directory structure for requested folder or pipe it to a folder

positional arguments:
  path

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  Directory tree will begin at this path (default:
                        current directory
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        If specified, directory tree will be written to this
                        file
  -d DEPTH, --depth DEPTH
                        Maximum depth to recurse (default: 5). Set to -1 to
                        recurse all the way to the bottom
  -f, --filter-hidden   Filter hidden files and folders (default: False)
  ```
  Lastly, it can also be installed:
  ```
  pip install .
  ```
  and can be imported in Python:
  ```
>>> from pdt.pdt import create_tree_dir
>>> create_dir_tree(filter_hidden=True)
-\
 ├─ LICENSE.txt
 ├─ README.md
 ├─ setup.py
 ├─ pdt\
 │   ├─ pdt.py
 │   ├─ __init__.py
  ```