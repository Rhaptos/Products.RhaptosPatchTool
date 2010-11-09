"""
Initialize RhaptosPatchTool Product

Author: Brent Hendricks
(C) 2005 Rice University

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""

import sys
from Products.CMFCore.DirectoryView import registerDirectory
from Products.CMFCore import utils

import PatchTool

this_module = sys.modules[ __name__ ]
product_globals = globals()
tools = ( PatchTool.PatchTool,)

# Make the skins available as DirectoryViews
registerDirectory('skins', globals())

def initialize(context):
    utils.ToolInit('Patch Tool',
                    tools = tools,
                    icon='tool.gif' 
                    ).initialize( context )
