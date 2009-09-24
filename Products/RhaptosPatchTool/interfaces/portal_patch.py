"""
Rhaptos Patch Tool Interface

Author: Brent Hendricks, J. Cameron Cooper
(C) 2005 Rice University

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""

from Interface import Interface, Attribute

class portal_patch(Interface):
    """Defines an interface for a tool that provides patch 
    (as in modification based on a diff) capabilities"""

    id = Attribute('id','Must be set to "portal_patch"')

    def createPatch(ob1, ob2, **kw):
        """Create and return a new patch object"""    
    
    def searchPatches(**kw):
        """Find patches with the specified parameters"""

