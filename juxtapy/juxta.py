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
SEP = os.path.sep
HTML = '''<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="description" content="Juxtpy File Comparison">
        <meta name="author" content="tmthydvnprt">

        <title>{title}</title>

        <link href='http://fonts.googleapis.com/css?family=Ubuntu+Mono' rel='stylesheet' type='text/css'>
        <link href="https://bootswatch.com/yeti/bootstrap.min.css" rel="stylesheet">
        <style>
            %(styles)s
        </style>
    </head>
    <body>
        <nav class="navbar navbar-inverse navbar-fixed-top">
            <div class="container-fluid">
                <div class="navbar-header">
                    <a class="navbar-brand" href="http://tmthydvnprt.github.io/juxtapy">Juxtapy</a>
                </div>
                <ul class="nav navbar-nav navbar-left">
                    <li><a href="{tree}">Directory Tree</a></li>
                </ul>
                <ul class="nav navbar-nav navbar-right">
                    <li><a href="https://github.com/tmthydvnprt/juxtapy">Source</a></li>
                    <li><a href="https://github.com/tmthydvnprt/juxtapy#juxtapy">Help</a></li>
                </ul>
            </div>
        </nav>
        <div class="container-fluid">
            <div class="row">
                <div class="col-xs-6 leftbreadcrumb">
                    <ol class="breadcrumb">
                        {frombreadcrumb}
                    </ol>
                </div>
                <div class="col-xs-6 rightbreadcrumb">
                    <ol class="breadcrumb">
                        {tobreadcrumb}
                    </ol>
                </div>
            </div>
            <div class="row">
                <div class="col-sm-12">
                    <div class="table-responsive">
                        %(table)s
                    </div>
                </div>
            </div>
            %(legend)s
        </div>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>
    </body>
</html>
'''
STYLES = '''
    html {
        position: relative;
        min-height: 100%;
    }
    body {
        padding-top: 50px;
        margin-bottom: 60px;
    }
    .navbar-header {
        float:left!important;
        margin-right: 0!important;
        margin-left: 0!important;
    }
    .navbar-brand {
        margin-left:0px!important;
    }
    .navbar-nav.navbar-left {
        float: left!important;
        margin: 0;
    }
    .navbar-nav.navbar-right {
        float: right!important;
        margin: 0;
    }
    .navbar-nav>li {
        float:left!important;
    }
    .navbar-nav>li>a {
        padding-top: 12px!important;
        padding-bottom: 12px!important;
    }
    .footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        height: 60px;
        background-color: #ffffff;
    }
    .footer hr {
        margin:4px;
        padding:4px;
    }
    .footer > .container {
        padding-right: 15px;
        padding-left: 15px;
    }
    .breadcrumb {
        margin-bottom: 8px;
        margin-left:48px;
        text-transform: none;
    }
    .leftbreadcrumb {
        padding-right:0px;
    }
    .rightbreadcrumb {
        padding-left:0px;
    }
    table.diff {
        font-size:100%;
        font-family: 'Ubuntu Mono'!important;
        border: 1px solid #5cb85c;
    }
    .diff th {
        text-align: center;
        border-left: 0px!important;
        border-right: 0px!important;
    }
    td[nowrap="nowrap"] {
        width:48%;
    }
    .diff td {
        padding:3px 6px!important;
        border-color:#f5f5f5!important;
    }
    .diff_next,
    .diff_header {
        width:1%;
        background-color:#EBEBEB;
        border-top: 0px!important;
        border-color: #EBEBEB!important;
    }
    .diff_next {
        background-color:#e0e0e0;
        border-color: #e0e0e0!important;
    }
    .diff_add {
        background-color:rgba(92, 184, 92, 0.5);
    }
    .diff_chg {
        background-color:rgba(240, 173, 78, 0.5);
    }
    .diff_sub {
        background-color:rgba(217, 83, 79, 0.5);
    }
    .legend {
        font-size:80%;
        margin-top:0px;
    }
    @media (min-width: 768px ) {
        .legend {
            font-size:100%;
            margin-top:0px;
        }
    }
'''
TABLE = '''
<table id="difflib_chg_%(prefix)s_top" class="diff table table-hover table-condensed">
    <thead>
        %(header_row)s
    </thead>
    <tbody>
        %(data_rows)s
    </tbody>
</table>
'''
LEGEND = '''
<footer class="footer">
    <div class="container">
        <hr>
        <p class="text-muted pull-left">&copy; 2014-2015 <a href="https://github.com/tmthydvnprt">tmthydvnprt</a></p>
        <p class="pull-right legend">
            <span class="label label-default diff_add">&nbsp;Added&nbsp;</span>
            <span class="label label-default diff_chg">Changed</span>
            <span class="label label-default diff_sub">Deleted</span>
            <br class="visible-xs">
            <span class="label label-info">(f)irst change</span>
            <span class="label label-info">(n)ext change</span>
            <span class="label label-info">(t)op</span>
        </p>
    </div>
</footer>
'''
INDEX_LEGEND = '''
<footer class="footer">
    <div class="container">
        <hr>
        <p class="text-muted pull-left">&copy; 2014-2015 <a href="https://github.com/tmthydvnprt">tmthydvnprt</a></p>
        <p class="pull-right">
            <span class="label label-default diff_add">&nbsp;Added&nbsp;</span>
            <span class="label label-default diff_chg">Changed</span>
            <span class="label label-default diff_sub">Deleted</span>
        </p>
    </div>
</footer>
'''
HEADER = '''<tr>
    <th class="diff_next"><br></th>
    <th class="diff_next"><br></th>
    <th nowrap="nowrap" class="diff_header">{from}</th>
    <th class="diff_next"><br></th>
    <th class="diff_next"><br></th>
    <th nowrap="nowrap" class="diff_header">{to}</th>
</tr>
'''
ROW = '''<tr>
    <td class="diff_next"><br></td>
    <td class="diff_next"><br></td>
    <td nowrap="nowrap" class="{type}"><a href="{compare}">{from}</a></td>
    <td class="diff_next"><br></td>
    <td class="diff_next"><br></td>
    <td nowrap="nowrap" class="{type}"><a href="{compare}">{to}</a></td>
</tr>
'''
TD = '''<li class="{}">{}</li>'''

# helper functions
def list_diff(list1, list2):
    """return list1 items not in list2"""
    return [x for x in list1 if x not in set(list2)]

def read_file(file_path='', encoding='utf-8'):
    """read a file into a string. assumes utf-8 encoding."""
    source = ''
    if os.path.exists(file_path) and os.path.isfile(file_path):
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
    return SEP.join([l for l, r in zip(left.split(SEP), right.split(SEP)) if l == r])

def make_breadcrumb(path):
    """make bootstrap breadcrumb list from file path"""
    return '\n'.join([TD.format('active' if i == len(path.split(SEP))-1 else '', x) for i, x in enumerate(path.split(SEP))])

class DirCmp(filecmp.dircmp):
    """
    filecmp.dircmp sublass to override phase3 to compare file content
    """

    def phase3(self): # Find out differences between common files, with shallow=False
        x = filecmp.cmpfiles(self.left, self.right, self.common_files, shallow=False)
        self.same_files, self.diff_files, self.funny_files = x

    filecmp.dircmp.methodmap['same_files'] = phase3
    filecmp.dircmp.methodmap['diff_files'] = phase3
    filecmp.dircmp.methodmap['funny_files'] = phase3

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

    def file_compare(self, from_file_path, to_file_path):
        """ndiff file compare"""
        from_file = read_file(from_file_path).splitlines()
        to_file = read_file(to_file_path).splitlines()
        diff_html = difflib.HtmlDiff()
        diff_html._file_template = HTML.format(**{
            'tree'  : os.path.relpath(os.path.join(self.from_path, 'index.html'), os.path.dirname(from_file_path)),
            'title' : '{} | {}'.format(os.path.basename(from_file_path), os.path.basename(to_file_path)),
            'frombreadcrumb' : make_breadcrumb(from_file_path),
            'tobreadcrumb' : make_breadcrumb(to_file_path)
        })
        diff_html._styles = STYLES
        diff_html._table_template = TABLE
        diff_html._legend = LEGEND

        file_diff_html = diff_html.make_file(from_file, to_file,
                                             os.path.basename(from_file_path),
                                             os.path.basename(to_file_path))
        return file_diff_html

    def compare(self):
        """compare folders and/or files"""

        if self.compare_type == 'dir':
            # check and clear output directory
            if os.path.exists(self.output_path):
                shutil.rmtree(self.output_path)
            os.makedirs(self.output_path)
            # compare directory
            dcmp = DirCmp(self.from_path, self.to_path, self.file_ignore)
            compare = self.compare_dir(dcmp)
            compare = sorted(compare, key=lambda x: x["from"] or x["to"])
            file_rows = [ROW.format(**x) for x in compare]
            root = common_root(self.from_path, self.to_path) + SEP
            html = HTML.format(**{
                'tree'  : '#',
                'title' : '{}/ | {}/'.format(os.path.basename(self.from_path), os.path.basename(self.to_path)),
                'frombreadcrumb' : make_breadcrumb(self.from_path),
                'tobreadcrumb' : make_breadcrumb(self.to_path)
            })
            table = TABLE % ({
                'header_row' : HEADER.format(**{
                    'from' : self.from_path.replace(root, '') + SEP,
                    'to' : self.to_path.replace(root, '') + SEP,
                }),
                'data_rows' : '\n'.join(file_rows),
                'prefix' : '',
            })
            compare_html = html % {
                'styles' : STYLES,
                'table'  : table,
                'legend' : INDEX_LEGEND
            }
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

    def write_comparison(self, name, dcmp, compare_type=''):
        """compare and write files"""
        # paths
        from_file_path = os.path.join(dcmp.left, name)
        to_file_path = os.path.join(dcmp.right, name)

        if not os.path.exists(from_file_path):
            from_file_path = os.path.join(os.path.dirname(from_file_path), '')
        if not os.path.exists(to_file_path):
            to_file_path = os.path.join(os.path.dirname(to_file_path), '')

        compare_file_path = os.path.join(dcmp.left.replace(self.from_path, self.output_path), name) + '.html'
        # compare
        file_compare_html = self.file_compare(from_file_path, to_file_path)
        # write
        if not os.path.exists(os.path.dirname(compare_file_path)):
            os.makedirs(os.path.dirname(compare_file_path))
        write_file(compare_file_path, file_compare_html)

        diff = {
            'type'   : compare_type,
            'from'   : os.path.join(dcmp.left, name).replace(self.from_path+SEP, ''),
            'to'     : os.path.join(dcmp.right, name).replace(self.to_path+SEP, ''),
            'compare': compare_file_path.replace(self.output_path+SEP, '')
        }
        return diff

    def compare_dir(self, dcmp):
        """recursive directory and file compare"""

        diffs = []

        # compare same files
        for name in dcmp.same_files:
            if not fnmatch.fnmatch(name, self.file_filter):
                diffs.append(self.write_comparison(name, dcmp))

        # compare different files
        for name in dcmp.diff_files:
            if not fnmatch.fnmatch(name, self.file_filter):
                diffs.append(self.write_comparison(name, dcmp, 'diff_chg'))

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
            diffs.extend(self.compare_dir(DirCmp(from_dir, to_dir, self.file_ignore)))

        # compare close file matches
        for from_file_path, to_file_path in close_files:
            # paths
            compare_file_path = from_file_path.replace(self.from_path, self.output_path) + '.html'
            # compare
            file_compare_html = self.file_compare(from_file_path, to_file_path)
            diffs.append({
                'type'   : 'diff_chg',
                'from'   : from_file_path.replace(self.from_path+SEP, ''),
                'to'     : to_file_path.replace(self.to_path+SEP, ''),
                'compare': compare_file_path.replace(self.output_path+SEP, '')
            })
            # write
            write_file(compare_file_path, file_compare_html)

        # add no match files and directories to diffs
        for no_match in list_diff(dcmp.left_only, [os.path.basename(x[0]) for x in close_files+close_dirs]):
            if not fnmatch.fnmatch(no_match, self.file_filter):

                fromdiff = self.write_comparison(no_match, dcmp, 'diff_sub')
                fromdiff['to'] = ''
                diffs.append(fromdiff)

        for no_match in list_diff(dcmp.right_only, [os.path.basename(x[1]) for x in close_files+close_dirs]):
            if not fnmatch.fnmatch(no_match, self.file_filter):

                todiff = self.write_comparison(no_match, dcmp, 'diff_add')
                todiff['from'] = ''
                diffs.append(todiff)

        return diffs
