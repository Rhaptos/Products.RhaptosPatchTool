## Script (Python) "patch_update"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=action, workspace=None, message=''
##title= Apply the patch to the specified workspace

from Products.CMFDiffTool import MergeError

id = context.orig_id

if action != 'accept':
    context.portal_workflow.doActionFor(context, 'reject', comment=message)
    psm = context.translate("message_edits_rejected", domain="rhaptos", default="Edits rejected.")
    return state.set(status='rejected', context=context.portal_url.getPortalObject(), portal_status_message=psm)

m_tool = context.portal_membership

# If the ws is our personal workspace, look for it there
if not workspace or workspace == m_tool.getAuthenticatedMember().getId():
    target = m_tool.getHomeFolder()
else:
    target = context.portal_groups.getGroupareaFolder(workspace)

if id not in target.objectIds():
    # FIXME: Don't assume that it's a Module
    target.invokeFactory(id=id, type_name="Module")
    item = target[id]
    item.setState('published')
    item.checkout(id)
else:
    item = target[id]

if item.state == 'published':
    item.checkout()

try:
    context.testChanges(item)
except MergeError, (msg, field, val1, val2):
    if field == 'data':
        error = context.translate("message_file_contents_not_match", {"msg":msg}, domain="rhaptos", default="%s: File contents did not match" % msg)
    else:
        error = context.translate("message_expected_for_got_instead", {"msg":msg, "val2":val2, "field":field, "val1":val1}, domain="rhaptos", default="%s: Expected %s for %s, got %s instead" % (msg, val2, field, val1))
    psm = context.translate("message_conflict_error", domain="rhaptos", default="")
    return state.set(status='failure', portal_status_message=psm, error=error)

context.applyChanges(item)
context.portal_workflow.doActionFor(context, 'apply', comment=message)

psm = context.translate("message_edits_applied", domain="rhaptos", default="Edits applied.")
return state.set(status='applied', context=item, portal_status_message=psm)
