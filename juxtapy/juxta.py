"""
juxta.py

"""

import os
import codecs
import shutil
import fnmatch
import filecmp
import difflib

# Constants
HTML_STR = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
          "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
    <meta http-equiv="Content-Type"
          content="text/html; charset=ISO-8859-1" />
    <title>{title}</title>
    <style type="text/css">
        table.diff {{font-family:Courier; border:medium;}}
        .diff_header {{background-color:#e0e0e0}}
        td.diff_header {{text-align:right}}
        .diff_next {{background-color:#c0c0c0}}
        .diff_add {{background-color:#aaffaa}}
        .diff_chg {{background-color:#ffff77}}
        .diff_sub {{background-color:#ffaaaa}}
    </style>
</head>
<body>
    <table class="diff" id=""
           cellspacing="0" cellpadding="0" rules="groups" >
        <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup>
        <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup>
        <thead>
            <tr><td><a href="{from}">{from} (From)</a></td><td><a href="{to}">{to} (To)</a></td></tr>
        </thead>
        <tbody>
        {rows}
        </tbody>
    </table>
    <table class="diff" summary="Legends">
        <tr> <th colspan="2"> Legends </th> </tr>
        <tr> <td> <table border="" summary="Colors">
                      <tr><th> Colors </th> </tr>
                      <tr><td class="diff_add">&nbsp;Added&nbsp;</td></tr>
                      <tr><td class="diff_chg">Changed</td> </tr>
                      <tr><td class="diff_sub">Deleted</td> </tr>
                  </table></td>
             </tr>
    </table>
</body>
</html>'''

ROW_STR = '<tr><td class="{type}"><a href="{compare}">{from}</a></td><td class="{type}"><a href="{compare}">{to}</a></td></tr>'

# helper functions
def list_diff(list1, list2):
    """return list1 items not in list2"""
    return [x for x in list1 if x not in set(list2)]

def read_file(file_path='', encoding='utf-8'):
    """read a file into a string. assumes utf-8 encoding."""
    source = ''
    if os.path.exists(file_path):
        fid = codecs.open(file_path, mode='r', encoding=encoding)
        source = fid.read()
        fid.close()
    return source

def write_file(file_path='', data=''):
    """write a file from a string."""
    fid = codecs.open(file_path, 'w')
    fid.write(data)
    fid.close()

def common_root(left='', right=''):
    """find common root between two file paths"""
    return os.path.sep.join([l for l, r in zip(left.split(os.path.sep), right.split(os.path.sep)) if l == r])

class Juxta(object):
    """compare folder and files by juxtaposing from (left) and to (right) directories"""

    def __init__(self, from_path='', to_path='', output_path='', file_filter=None, file_ignore=None):
        """create Juxta Object"""

        # set inputs
        self.file_filter = file_filter if file_filter else '*.pyc'
        self.file_ignore = file_ignore if file_ignore else ['.DS_Store', '.localized']
        self.from_path = from_path
        self.to_path = to_path
        self.compare_name = '{}_compare_{}'.format(os.path.basename(from_path), os.path.basename(to_path))

        # check for comparison type
        if os.path.isdir(from_path) and os.path.isdir(to_path):
            self.compare_type = 'dir'
        elif os.path.isfile(from_path) and os.path.isfile(to_path):
            self.compare_type = 'file'
        else:
            self.compare_type = 'error'

        # set output based on type
        self.output_path = os.path.join(output_path, self.compare_name)
        if self.compare_type == 'file':
            self.output_path += '.html'

    def dircmp(self, from_path, to_path):
        """compare folders"""
        return filecmp.dircmp(from_path, to_path, self.file_ignore)

    @staticmethod
    def file_compare(from_file_path, to_file_path):
        """ndiff file compare"""
        from_file = read_file(from_file_path).splitlines()
        to_file = read_file(to_file_path).splitlines()
        file_diff_html = difflib.HtmlDiff().make_file(from_file, to_file)
        return file_diff_html

    def compare(self):
        """compare folders and/or files"""

        if self.compare_type == 'dir':
            # check and clear output directory
            if os.path.exists(self.output_path):
                shutil.rmtree(self.output_path)
            os.makedirs(self.output_path)
            # compare directory
            compare = self.compare_dir(self.dircmp(self.from_path, self.to_path))
            compare = sorted(compare, key=lambda x: x["from"] or x["to"])
            file_rows = [ROW_STR.format(**x) for x in compare]
            root = os.path.dirname(common_root(self.from_path, self.to_path))
            compare_html = HTML_STR.format(**{
                'title' : self.compare_name,
                'from' : self.from_path.replace(root, ''),
                'to' : self.to_path.replace(root, ''),
                'rows' :'\n'.join(file_rows)
            })
            # write
            write_file(os.path.join(self.output_path, 'index.html'), compare_html)

            return 'COMPARED: {}'.format(self.output_path)

        elif self.compare_type == 'file':
            # compare file
            file_compare_html = self.file_compare(self.from_path, self.to_path)
            # write
            write_file(self.output_path, file_compare_html)

            return 'COMPARED: {}'.format(self.output_path)

        else:
            return 'ERROR: from and to patch are not compatible'

    def write_comparison(self, name, dcmp):
        """compare and write files"""
        # paths
        from_file_path = os.path.join(dcmp.left, name)
        to_file_path = os.path.join(dcmp.right, name)
        compare_file_path = os.path.join(dcmp.left.replace(self.from_path, self.output_path), name) + '.html'
        # compare
        file_compare_html = self.file_compare(from_file_path, to_file_path)
        # write
        if not os.path.exists(os.path.dirname(compare_file_path)):
            os.makedirs(os.path.dirname(compare_file_path))
        write_file(compare_file_path, file_compare_html)

        diff = {
            'type'   : '',
            'from'   : os.path.join(dcmp.left, name).replace(self.from_path+os.path.sep, ''),
            'to'     : os.path.join(dcmp.right, name).replace(self.to_path+os.path.sep, ''),
            'compare': compare_file_path.replace(self.output_path+os.path.sep, '')
        }
        return diff

    def compare_dir(self, dcmp):
        """recursive directory and file compare"""

        diffs = []

        # show same files
        for name in dcmp.same_files:
            if not fnmatch.fnmatch(name, self.file_filter):
                diffs.append(self.write_comparison(name, dcmp))

        # compare different files
        for name in dcmp.diff_files:
            if not fnmatch.fnmatch(name, self.file_filter):
                diffs.append(self.write_comparison(name, dcmp))

        # compare common subdirectories
        for sub_dcmp in dcmp.subdirs.values():
            diffs.extend(self.compare_dir(sub_dcmp))

        # check for close file and subdirectory matches
        close_dirs = []
        close_files = []
        for left in dcmp.left_only:
            match = difflib.get_close_matches(left, dcmp.right_only, 1)
            if match:
                close_paths = (os.path.join(dcmp.left, left), os.path.join(dcmp.right, match[0]))
                if all([os.path.isdir(x) for x in close_paths]):
                    close_dirs.append(close_paths)
                else:
                    close_files.append(close_paths)

        # compare close subdirectory matches
        for from_dir, to_dir in close_dirs:
            diffs.extend(self.compare_dir(self.dircmp(from_dir, to_dir)))

        # compare close file matches
        for from_file_path, to_file_path in close_files:
            # paths
            compare_file_path = from_file_path.replace(self.from_path, self.output_path) + '.html'
            # compare
            file_compare_html = self.file_compare(from_file_path, to_file_path)
            diffs.append({
                'type'   : 'diff_chg',
                'from'   : from_file_path.replace(self.from_path+os.path.sep, ''),
                'to'     : to_file_path.replace(self.to_path+os.path.sep, ''),
                'compare': compare_file_path.replace(self.output_path+os.path.sep, '')
            })
            # write
            write_file(compare_file_path, file_compare_html)

        # add no match files and directories to diffs
        for no_match in list_diff(dcmp.left_only, [os.path.basename(x[0]) for x in close_files+close_dirs]):
            if not fnmatch.fnmatch(no_match, self.file_filter):
                diffs.append({
                    'type'   : 'diff_sub',
                    'from'   : os.path.join(dcmp.left, no_match).replace(self.from_path+os.path.sep, ''),
                    'to'     : '',
                    'compare': ''
                })
        for no_match in list_diff(dcmp.right_only, [os.path.basename(x[1]) for x in close_files+close_dirs]):
            if not fnmatch.fnmatch(no_match, self.file_filter):
                diffs.append({
                    'type'   : 'diff_add',
                    'from'   : '',
                    'to'     : os.path.join(dcmp.right, no_match).replace(self.to_path+os.path.sep, ''),
                    'compare': ''
                })

        return diffs
