"""
Rhaptos Patch tool - allows users to send and receive patches for content
objects

Author: Brent Hendricks
(C) 2005 Rice University

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""

from zope.interface import implements

import AccessControl
from Globals import InitializeClass
from DateTime import DateTime
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.CMFCore.utils import UniqueObject
from Products.CMFCore.permissions import ManagePortal
from Products.CMFCore.PortalFolder import PortalFolder

from interfaces.portal_patch import portal_patch as IPatchTool

class PatchTool (UniqueObject, PortalFolder):
    """
    This tool provides a way to request a collaboration with another
    user and allows them to accept or decline
    """

    implements(IPatchTool)

    id = 'portal_patch'
    title = 'Patches'
    meta_type = 'CMF Patch Tool'

    security = AccessControl.ClassSecurityInfo()
    
    manage_options=( ({'label':'Overview', 'action':'manage_overview'},
                      )
                     + PortalFolder.manage_options
                     )

    #
    #   ZMI methods
    #
    security.declareProtected(ManagePortal, 'manage_overview')
    manage_overview = PageTemplateFile( 'zpt/explainPatchTool', globals())

    # We have to override the PortalFolder __init__ method with
    # something that takes no arguments
    def __init__(self):
        pass

    def view(self):
        """View a list of patches"""
        return self.patches()

    security.declarePublic('createPatch')
    def createPatch(self, ob1, ob2, **kw):
        """Create and return a new patch object"""
        id = self._createId()
        self.invokeFactory(id=id, type_name='Patch')
        patch = self[id]
        patch.title = 'Suggested Edits for ' + ob1.objectId
        patch.computeDiff(ob1, ob2, **kw)
        # Store the location of the original
        patch.orig_id = ob1.objectId
        patch.orig_version = ob1.version
        patch.reindexObject()

        return patch

    def _createId(self):
        now=DateTime()
        id = 'Patch.'+now.strftime('%Y-%m-%d')+'.'+now.strftime('%M%S')
        count = 0
        while hasattr(self.aq_base, id):
            id = 'Patch.'+now.strftime('%Y-%m-%d')+'.'+now.strftime('%M%S')+'.'+str(count)
            count = count + 1
        return id

    security.declarePublic('addPatchRequest')
    def searchPatches(self, **kw):
        """Find patches with the specified parameters"""
        kw['portal_type'] = 'Patch'
        return self.portal_catalog.searchResults(**kw)
    
InitializeClass(PatchTool)
