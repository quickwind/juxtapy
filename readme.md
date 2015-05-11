Juxtapy
=======
Folder and File juxtaposing in Python

Description
-----------

This program is a wrapper for python's `difflib.HtmlDiff` & `filecmp.dircmp` that generates an `html` site comparing two directory trees where files that differ contain links to their line-by-line comparisons. http://tmthydvnprt.github.io/juxtapy

### Features
* ignore specific files
* filter out file types
* Five types of comparisons are captured:
    * same path, same content (common, no change)
    * same path, different content (common, change)
    * similar path, different content (similar, change)
    * from path only (subtractions)
    * to path only (additions)
* `difflib.HtmlDiff` is used to generate inter/intra line comparisons between two files.
* `filecmp.dircmp` is used to create comparison between two directories
* `difflib.get_close_matches` is used to find similar directory/file paths

Code Examples
-------------

### Module Interface

```python
from juxtapy.juxta import Juxta

jxt = Juxta('/from/path', '/to/path', '/output/path', '*.pyc')
response = jxt.compare()
print repsonse
```

### Command-Line Interface

```sh
machine:~ user$ python juxtapy -f /from/path -t /to/path -o /output/path --file_filter *.pyc
```

Installation
------------
TBD, I just use it in a directory at the moment...

API Reference
-------------

### Module Interface
```python

class Juxta(__builtin__.object)
 |  compare folder and files by juxtaposing from (left) and to (right) directories
 |  
 |  Methods defined here:
 |  
 |  __init__(self, from_path='', to_path='', output_path='', file_filter=None, file_ignore=None, quiet=False)
 |      create Juxta Object
 |  
 |  compare(self)
 |      compare folders and/or files
 |  
 |  compare_dir(self, dcmp=None)
 |      recursive directory and file compare
 |  
 |  file_compare(self, from_file_path='', to_file_path='')
 |      ndiff file compare
 |  
 |  write_comparison(self, name='', dcmp=None, compare_type='')
 |      compare and write files
```

### Command Line Interface
```sh
usage: juxtapy [-h] [-f STR] [-t STR] [-o STR] [--file_filter STR]
               [--file_ignore STR] [--q] [--version]

Juxtapy

Folder and File juxtaposing in Python

optional arguments:
  -h, --help                 show this help message and exit
  -f STR, --from_path STR    from (left) directory or file path
  -t STR, --to_path STR      to (right) directory or file path
  -o STR, --output_path STR  output path
  --file_filter STR          fnmatch file filter string (default: '*.pyc')
  --file_ignore STR          comma separated files to ignore (default:
                             '.DS_Store,.localized')
  --q, --quiet               show no info
  --version                  display the program's version

happy comparing
```

Tests
-----
Tests are located in `tests/`.  Example output located [here](http://tmthydvnprt.github.io/juxtapy/from_compare_to/index.html).

Todo
----
* [x] File comparison
* [x] Directory comparison
* [x] Make the `html` more modern
* [ ] Nest Directory Tree
* [ ] Add options:
    * [ ] skip comparing same files
    * [ ] quiet run
* [ ] 

License
-------
[MIT](https://github.com/tmthydvnprt/juxtapy/blob/master/LICENSE)
