#! /usr/bin/python

""" Djvu XML to OCRML converter

	A Python utility to transform files
"""

__author__ = "Luis Aguilar"
__email__ = "luis@berkeley.edu"
 
from optparse import OptionParser
#import pdb
import os
import codecs
import sys
from lxml import etree

def processInput(path):
    """ Process the input directory

	    Process only djvu files that have not been transformed from
	    directory path parameter.
    """

    # check if passed path is to a directory or to a file
    if os.path.isfile(path):
        # extract absolute path from user submitted path value
        abs_path = os.path.dirname(os.path.abspath(path))
        filename = os.path.basename(path)
        processFile(abs_path, filename)
    elif os.path.isdir(path):
        # extract absolute path from user submitted path value
        abs_path = os.path.abspath(path)
        # loop through and open/transform djvu files
        for filename in os.listdir(abs_path):
            processFile(abs_path, filename)
    else:
        print "An invalid directory or file was passed as input"


def processFile(abs_path, filename):
    # establish file path for ocrml file
    ocrml_path = abs_path + '/' + filename.replace('djvu', 'ocrml')
    print ocrml_path
    # only process and create ocrml file if it doesn't already exist
    if filename.endswith("djvu.xml") and not os.path.isfile(ocrml_path):
        _transformDjvu(abs_path, filename, ocrml_path)    

def _transformDjvu(abs_path, filename, ocrml_path):
    djvu_path = abs_path + '/' + filename
    try:
    	# open transformer to process the djvu XML and convert to ocrml
    	transform = etree.XSLT(etree.parse('config/djvu_ocrml.xsl'))
        with open(djvu_path, "r") as f_djvu, \
        codecs.open(ocrml_path, "w", 'utf-8') as f_ocrml:
            # check for proper utf character sets
            djvu_xml = etree.XML(f_djvu.read())
            ocrml = transform(djvu_xml)
            #f_ocrml.write(ocrml)
            f_ocrml.write(unicode(ocrml))
    except IOError as e:
    	print "I/O error({0}): {1}".format(e.errno, e.strerror)
    except:
    	print "Unexpected error: ", sys.exc_info()
def _getInput():
    """ Command Line Input Parsing

	    Parse the user input
    """
    parser = OptionParser()
    parser.add_option('-i', '--input', dest='filepath', default='.')
    (option, args) = parser.parse_args()

    if not option.filepath:
	    return parser.error('Djvu file path not given, use --input="path.to.djvu.file.for.download"')

    return {'src': option.filepath}

def main():
    userInput = _getInput()
    processInput(userInput['src'])
    # close the transform global?

if __name__ == '__main__':
	main()