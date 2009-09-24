from Products.CMFCore.utils import getToolByName
from Products.CMFCore.Expression import Expression
from Products.CMFCore.DirectoryView import addDirectoryViews
from Products.RhaptosPatchTool import product_globals
from StringIO import StringIO
import string

def install(self):
    """Add the tool"""
    out = StringIO()

    # Add the tool
    urltool = getToolByName(self, 'portal_url')
    portal = urltool.getPortalObject();

    # Skip installation of tool if it's already there since we don't
    # want to lose data
    if getattr(portal.aq_base, 'portal_patch', None) is None:
        portal.manage_addProduct['RhaptosPatchTool'].manage_addTool('CMF Patch Tool', None)

    # Make sure Members are allowed to create patches
    pt = getToolByName(self, 'portal_patch')
    pt.manage_permission('Add portal content', ('Member',), acquire=1)

    out.write("Added Patch Tool\n")

    # New 'Patch' type based on ChangeSet
    types_tool = getToolByName(portal, 'portal_types')

    # Delete portal type if it already exists
    if 'Patch' in types_tool.objectIds():
        types_tool.manage_delObjects('Patch')

    types_tool.manage_addTypeInformation(id='Patch',
                                         add_meta_type="Factory-based Type Information",
                                         typeinfo_name="CMFDiffTool: Change Set")
    patch = getattr(types_tool, 'Patch')
    actions = patch._cloneActions()
    for a in actions:
        if a.id == 'view':
            a.action = Expression('string:${object_url}/patch_view')
        elif a.id == 'edit':
            a.visible = 0
    patch._actions=actions

    # Register patch workflow
    wf_tool = getToolByName(portal, 'portal_workflow')

    # Delete workflow if it already exists
    if 'patch_workflow' in wf_tool.objectIds():
        wf_tool.manage_delObjects('patch_workflow')

    wf_tool.manage_addWorkflow(id='patch_workflow', workflow_type='patch_workflow (Patch Workflow [Rhaptos])')
    wf_tool.setChainForPortalTypes(['Patch'],'patch_workflow')

    # Add orig_id to the catalog indices so we can find patches
    catalog = getToolByName(portal, 'portal_catalog')
    if 'orig_id' not in catalog.indexes():
        catalog.addIndex('orig_id', 'FieldIndex')

    # Register skins
    skinstool = getToolByName(portal, 'portal_skins')

    if 'rhaptos_patch' in skinstool.objectIds():
        skinstool.manage_delObjects('rhaptos_patch')

    # We need to add Filesystem Directory Views for any directories
    # in our skins/ directory.  These directories should already be
    # configured.
    addDirectoryViews(skinstool, 'skins', product_globals)
    out.write("Added 'rhaptos_patch' directory view to portal_skins\n")

    # Now we need to go through the skin configurations and insert
    # 'rhaptos_patch' into the configurations.  Preferably, this
    # should be right before where 'custom' is placed.  Otherwise, we
    # append it to the end.
    skins = skinstool.getSkinSelections()
    for skin in skins:
        path = skinstool.getSkinPath(skin)
        path = map(string.strip, string.split(path,','))
        if 'rhaptos_patch' not in path:
            try:
                path.insert(path.index('custom')+1, 'rhaptos_patch')
            except ValueError:
                path.append('rhaptos_patch')
                
            path = string.join(path, ', ')
            # addSkinSelection will replace existing skins as well.
            skinstool.addSkinSelection(skin, path)
            out.write("Added 'rhaptos_patch' to %s skin\n" % skin)
        else:
            out.write("Skipping %s skin, 'rhaptos_patch' is already set up\n" % (skin))

    return out.getvalue()
