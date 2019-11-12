"""
magic_juxtapy.py - Define a custom magic functio to use juxtapy from iPython or Jupyter Notebook

To use this magic function, place this file in your iPython profile's startup/ directory
(e.g. ~/.ipython/profile_default/startup/)

Example:

    In [1]: %juxtapy path/to/fromfile path/to/tofile

"""

import subprocess
from IPython.core.magic import register_line_magic


@register_line_magic
def juxtapy(line):
    """Folder and File juxtaposing in Python"""
    args = line.split(' ')
    from_loc = args[0]
    to_loc = args[1]
    py_loc = args[2] if len(args) > 2 else '~/GitHub/juxtapy/juxtapy'
    cmd = 'python {} -f {} -t {}'.format(py_loc, from_loc, to_loc)
    print(subprocess.check_output(cmd, shell=True))
