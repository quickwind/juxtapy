Juxtapy
=======
Folder and File juxtaposing in Python

Description
-----------

This program is a wrapper for python's `difflib.HtmlDiff` & `filecmp.dircmp` that generates an `html` site comparing two directory trees where files that differ contain links to their line-by-line comparisons. 

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

###Module Interface

```python
from juxtapy.juxta import Juxta

jxt = Juxta('/from/path', '/to/path', '/output/path', '*.pyc')
response = jxt.compare()
print repsonse
```

###Command-Line Interface

```sh
python juxtapy -f /from/path -t /to/path -o /output/path --file_filter *.pyc
```

Installation
------------
TBD, I just use it in a directory at the moment...

API Reference
-------------
```python
Help on class Juxta in module juxtapy.juxta:

class Juxta(__builtin__.object)
 |  compare folder and files by juxtaposing from (left) and to (right) directories
 |  
 |  Methods defined here:
 |  
 |  __init__(self, from_path='', to_path='', output_path='', file_filter=None, file_ignore=None)
 |      create Juxta Object
 |  
 |  compare(self)
 |      compare folders and/or files
```

Tests
-----
Tests are located in `tests/`

Todo
----
* [x] File comparison
* [x] Directory comparison
* [ ] Make the `html` more modern
* [ ] Nest Directory Tree

License
-------
[MIT]()
