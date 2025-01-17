"""
juxta.py

project    : juxtapy
version    : 0.1.0
status     : development
modifydate : 2015-05-11 19:26:00 -0700
createdate : 2015-04-26 04:45:00 -0700
website    : https://github.com/tmthydvnprt/juxtapy
author     : tmthydvnprt
email      : tmthydvnprt@users.noreply.github.com
maintainer : tmthydvnprt
license    : MIT
copyright  : Copyright 2015, juxtapy
credits    :

"""

import os
import json
import codecs
import shutil
import fnmatch
import filecmp
import difflib
import xml

# pylint: disable=W0212
# pylint: disable=W0201

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
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
        <style>
            %(styles)s
        </style>
    </head>
    <body>
        <nav class="navbar navbar-inverse navbar-fixed-top">
            <div class="container-fluid">
                <ul class="nav navbar-nav navbar-left">
                    <li><a href="{tree}">Directory Tree</a></li>
                </ul>
            </div>
        </nav>
        {page}
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>
    </body>
</html>
'''
COMPARE_PAGE = '''<div class="container-fluid">
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
'''
HOME_PAGE = '''<div class="jumbotron text-center">
    <div class="container">
        <h1>Juxtapy</h1>
        <p>Folder and File juxtaposing in Python</p>
    </div>
</div>

<div class="container-fluid">
    <div class="row">
        <div class="col-sm-12 col-md-10 col-md-offset-1 col-lg-8 col-lg-offset-2 text-center">
            <p class="lead">A wrapper for python's <code>difflib.HtmlDiff</code> &amp; <code>filecmp.dircmp</code> that generates an <code>html</code> site comparing two directory trees where files link to their line-by-line comparisons.</p>
        </div>
    </div>
    <div class="row">
        <div class="col-md-2 col-md-offset-3 text-center">
            <a class="btn btn btn-primary" href="https://github.com/tmthydvnprt/juxtapy#juxtapy" role="button">View<br>Readme</a>
        </div>
        <div class="col-md-2 text-center">
            <a class="btn btn btn-info" href="from_compare_to/index.html" role="button">Example<br>Folder Output</a>
        </div>
        <div class="col-md-2 text-center">
            <a class="btn btn btn-success" href="from.txt_compare_to.txt.html" role="button">Example<br>File Output</a>
        </div>
    </div>
</div>
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
    .breadcrumb > li + li::before {
        padding: 0px 1px!important;
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
    td.nowrap {
        width:48%;
        max-width:512px;
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
'''
INDEX_LEGEND = '''
'''
HEADER = '''<tr>
    <th class="diff_next"><br></th>
    <th class="diff_next"><br></th>
    <th class="diff_header nowrap">{from}</th>
    <th class="diff_next"><br></th>
    <th class="diff_next"><br></th>
    <th class="diff_header nowrap">{to}</th>
</tr>
'''
ROW = '''<tr>
    <td class="diff_next"><br></td>
    <td class="diff_next"><br></td>
    <td class="{type} nowrap"><a href="{compare}">{from}</a></td>
    <td class="diff_next"><br><b>{result}</b></td>
    <td class="diff_next"><br></td>
    <td class="{type} nowrap"><a href="{compare}">{to}</a></td>
</tr>
'''
TD = '''<li class="{}">{}</li>'''

# helper functions
def list_diff(list1=None, list2=None):
    """return list1 items not in list2"""
    return [x for x in list1 if x not in set(list2)]

def read_file(file_path=''):
    """read a file into a string. assumes utf-8 encoding."""
    source = ''
    if os.path.exists(file_path) and os.path.isfile(file_path):
        fid = codecs.open(file_path, 'r', 'utf-8')
        try:
            source = fid.read()
        except (UnicodeEncodeError, UnicodeDecodeError):
            source = 'error: could not read file'
        fid.close()
    _, file_extension = os.path.splitext(os.path.basename(file_path))
    if file_extension.lower() == '.json':
        try:
            parsed = json.loads(source)
            source = json.dumps(parsed, indent=2, sort_keys=True)
        except Exception:
            print('Failed to beautify JSON file: {}'.format(file_path))
    elif file_extension.lower() == '.xml' and source.count('\n') <= 2:
        try:
            dom = xml.dom.minidom.parse(source)
            source = dom.toprettyxml()
        except Exception:
            print('Failed to beautify XML file: {}'.format(file_path))
    return source

def write_file(file_path='', data=''):
    """write a file from a string."""
    fid = codecs.open(file_path, 'w', 'utf-8')
    try:
        fid.write(data)
    except (UnicodeEncodeError, UnicodeDecodeError):
        fid.write('error: could not write file')
    fid.close()

def common_root(left='', right=''):
    """find common root between two file paths"""
    return SEP.join([l for l, r in zip(left.split(SEP), right.split(SEP)) if l == r])

def make_breadcrumb(path=''):
    """make bootstrap breadcrumb list from file path"""
    return '\n'.join([TD.format('active' if i == len(path.split(SEP))-1 else '', x if i == len(path.split(SEP))-1 else (x + SEP)) for i, x in enumerate(path.split(SEP))])

def write_index(path=''):
    """write home page"""
    html = HTML.format(**{
        'tree'  : 'from_compare_to/index.html',
        'title' : 'Juxtapy',
        'page'  : HOME_PAGE
    }) % {'styles' : STYLES}
    # write
    write_file(os.path.join(path, 'index.html'), html)

class DirCmp(filecmp.dircmp):
    """filecmp.dircmp sublass to override phase3 to compare file content"""

    def phase3(self):
        """ Find out differences between common files, with shallow=False """
        x = filecmp.cmpfiles(self.left, self.right, self.common_files, shallow=False)
        self.same_files, self.diff_files, self.funny_files = x

    # override method map with custom phase3 function
    filecmp.dircmp.methodmap['same_files'] = phase3
    filecmp.dircmp.methodmap['diff_files'] = phase3
    filecmp.dircmp.methodmap['funny_files'] = phase3

class Juxta(object):
    """compare folder and files by juxtaposing from (left) and to (right) directories"""

    def __init__(self, from_path='', to_path='', output_path='', file_filter=None, file_ignore=None, quiet=False):
        """create Juxta Object"""

        # set inputs
        self.quiet = quiet
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
        if not output_path:
            output_path = os.path.dirname(from_path)
        self.output_path = os.path.join(output_path, self.compare_name)
        if self.compare_type == 'file':
            self.output_path += '.html'

    def file_compare(self, from_file_path='', to_file_path=''):
        """ndiff file compare"""

        # initialize comparison
        from_file = read_file(from_file_path).splitlines()
        to_file = read_file(to_file_path).splitlines()
        diff_html = difflib.HtmlDiff()

        # override template strings
        diff_html._file_template = HTML.format(**{
            'tree'  : os.path.relpath(os.path.join(self.from_path, 'index.html'), os.path.dirname(from_file_path)),
            'title' : '{} | {}'.format(os.path.basename(from_file_path), os.path.basename(to_file_path)),
            'page' : COMPARE_PAGE.format(**{
                'frombreadcrumb' : make_breadcrumb(from_file_path),
                'tobreadcrumb' : make_breadcrumb(to_file_path)
            })
        })
        diff_html._styles = STYLES
        diff_html._table_template = TABLE
        diff_html._legend = LEGEND

        # compare files
        file_diff_html = diff_html.make_file(from_file, to_file,
                                             os.path.basename(from_file_path),
                                             os.path.basename(to_file_path))
        return file_diff_html.replace('nowrap="nowrap"', 'class="nowrap"')

    def compare(self):
        """compare folders and/or files"""

        if self.compare_type == 'dir':
            root = common_root(self.from_path, self.to_path)
            # check and clear output directory
            if os.path.exists(self.output_path):
                shutil.rmtree(self.output_path)
            os.makedirs(self.output_path)
            # compare directory
            dcmp = DirCmp(self.from_path, self.to_path, self.file_ignore)
            compare = self.compare_dir(dcmp)
            compare = sorted(compare, key=lambda x: x["from"] or x["to"])
            for item in compare:
                item['from'] = item['from'].replace(self.from_path, '')
                item['to'] = item['to'].replace(self.to_path, '')
            file_rows = [ROW.format(**x) for x in compare]
            if not root.endswith('/'):
                root = root + SEP
            html = HTML.format(**{
                'tree'  : '#',
                'title' : '{}/ | {}/'.format(os.path.basename(self.from_path), os.path.basename(self.to_path)),
                'page' : COMPARE_PAGE.format(**{
                    'frombreadcrumb' : make_breadcrumb(self.from_path),
                    'tobreadcrumb' : make_breadcrumb(self.to_path)
                })
            })
            table = TABLE % ({
                'header_row' : HEADER.format(**{
                    'from' : self.from_path.replace(root, ''),
                    'to' : self.to_path.replace(root, ''),
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

            return 'COMPARED: file://{}'.format(os.path.join(self.output_path, 'index.html'))

        elif self.compare_type == 'file':
            # compare file
            file_compare_html = self.file_compare(self.from_path, self.to_path)
            # write
            write_file(self.output_path, file_compare_html)

            return 'COMPARED: {}'.format(self.output_path)

        else:
            return 'ERROR: from and to path are not compatible'

    def write_comparison(self, name='', dcmp=None, compare_type=''):
        """compare and write files"""
        # paths
        from_file_path = os.path.join(dcmp.left, name)
        to_file_path = os.path.join(dcmp.right, name)

        if not os.path.exists(from_file_path):
            from_file_path = os.path.join(os.path.dirname(from_file_path), '')
        if not os.path.exists(to_file_path):
            to_file_path = os.path.join(os.path.dirname(to_file_path), '')

        if compare_type:
            compare_file_path = os.path.join(dcmp.left.replace(self.from_path, self.output_path), name) + '.html'

            # compare
            file_compare_html = self.file_compare(from_file_path, to_file_path)
            # write
            if not os.path.exists(os.path.dirname(compare_file_path)):
                os.makedirs(os.path.dirname(compare_file_path))
            write_file(compare_file_path, file_compare_html)
        else:
            compare_file_path = os.path.join(dcmp.left.replace(self.from_path, self.output_path), name)
            os.makedirs(os.path.dirname(compare_file_path), exist_ok=True)
            shutil.copy(from_file_path, compare_file_path)

        diff = {
            'type'   : compare_type,
            'from'   : os.path.join(dcmp.left, name).replace(self.from_path+SEP, ''),
            'to'     : os.path.join(dcmp.right, name).replace(self.to_path+SEP, ''),
            'compare': compare_file_path.replace(self.output_path+SEP, ''),
            'result' : '&ne;' if compare_type else '='
        }
        return diff

    def compare_dir(self, dcmp=None):
        """recursive directory and file compare"""

        diffs = []

        # compare same files
        for name in dcmp.same_files:
            if not fnmatch.fnmatch(name, self.file_filter):
                if not self.quiet:
                    print('same ', name)
                diffs.append(self.write_comparison(name, dcmp))

        # compare different files
        for name in dcmp.diff_files:
            if not fnmatch.fnmatch(name, self.file_filter):
                if not self.quiet:
                    print('diff ', name)
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
            if not fnmatch.fnmatch(from_file_path, self.file_filter):
                if not self.quiet:
                    print('close', os.path.basename(from_file_path), os.path.basename(to_file_path))

                # paths
                compare_file_path = from_file_path.replace(self.from_path, self.output_path) + '.html'
                # compare
                file_compare_html = self.file_compare(from_file_path, to_file_path)
                diffs.append({
                    'type'   : 'diff_chg',
                    'from'   : from_file_path.replace(self.from_path+SEP, ''),
                    'to'     : to_file_path.replace(self.to_path+SEP, ''),
                    'compare': compare_file_path.replace(self.output_path+SEP, ''),
                    'result' : '&ne;' #'&asymp;'
                })
                # write
                write_file(compare_file_path, file_compare_html)

        # add no match files and directories to diffs
        for no_match in list_diff(dcmp.left_only, [os.path.basename(x[0]) for x in close_files+close_dirs]):
            if not fnmatch.fnmatch(no_match, self.file_filter):
                if not self.quiet:
                    print('left ', no_match)

                fromdiff = self.write_comparison(no_match, dcmp, 'diff_sub')
                fromdiff['to'] = ''
                diffs.append(fromdiff)

        for no_match in list_diff(dcmp.right_only, [os.path.basename(x[1]) for x in close_files+close_dirs]):
            if not fnmatch.fnmatch(no_match, self.file_filter):
                if not self.quiet:
                    print('right', no_match)

                todiff = self.write_comparison(no_match, dcmp, 'diff_add')
                todiff['from'] = ''
                diffs.append(todiff)

        return diffs
