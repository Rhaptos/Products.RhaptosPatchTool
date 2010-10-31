"""
Patch workflow - custom DCWorkflow for patch objects

Author: Brent Hendricks
(C) 2005 Rice University

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""

from Products.CMFCore.permissions import ModifyPortalContent, View, \
     AccessContentsInformation
from Products.CMFCalendar.EventPermissions import ChangeEvents

from Products.CMFCore.WorkflowTool import addWorkflowFactory
from Products.DCWorkflow.DCWorkflow import DCWorkflowDefinition
from Products.DCWorkflow.Default import setupDefaultWorkflowRev2

from Products.CMFCore.permissions import RequestReview, ReviewPortalContent
     
def configureEventPermissions(wf):
    """ Since events use a unique set of Permissions we 
        need to add it to the workflow definition and make
        it conform to other tranistions/states 
    """
    pass

def createPatchWorkflow(id):
    wf=DCWorkflowDefinition(id)
    wf.setProperties(title='Patch Workflow [Rhaptos]')

    for s in ('created', 'submitted', 'applied', 'rejected'):
        wf.states.addState(s)
    for t in ('submit', 'apply', 'reject'):
        wf.transitions.addTransition(t)
    for v in ('action', 'actor', 'comments', 'review_history', 'time'):
        wf.variables.addVariable(v)

    wf.states.setInitialState('created')

    # Configure states
    sdef = wf.states['created']
    sdef.setProperties(title='Newly created', transitions=('submit',))

    sdef = wf.states['submitted']
    sdef.setProperties(title='Submitted and pending review', transitions=('apply', 'reject',),
                       description='Waiting on a reviewer to accept the patch and apply it to the correct content')

    sdef = wf.states['applied']
    sdef.setProperties(title='Accepted by a reviwer',
                       description='The patch has been accepted and applied to a working copy of the content item.  The changes will not be public, however, until the item is published')

    sdef = wf.states['rejected']
    sdef.setProperties(title='Rejected by a reviwer',
                       description='The changes have been rejected by a reviewer.')
        
    # Configure transitions
    tdef = wf.transitions['apply']
    tdef.setProperties(title='Reviewer applies changes', new_state_id='applied')
                       
    tdef = wf.transitions['reject']
    tdef.setProperties(title='Reviewer rejects changes', new_state_id='rejected')

    tdef = wf.transitions['submit']
    tdef.setProperties(title='Submit for review', new_state_id='submitted')

    # Configure variables
    wf.variables.setStateVar('review_state')

    vdef = wf.variables['action']
    vdef.setProperties(description='The last transition',
                       default_expr='transition/getId|nothing',
                       for_status=1, update_always=1)

    vdef = wf.variables['actor']
    vdef.setProperties(description='The ID of the user who performed '
                       'the last transition',
                       default_expr='user/getId',
                       for_status=1, update_always=1)

    vdef = wf.variables['comments']
    vdef.setProperties(description='Comments about the last transition',
                       default_expr="python:state_change.kwargs.get('comment', '')",
                       for_status=1, update_always=1)

    vdef = wf.variables['review_history']
    vdef.setProperties(description='Provides access to workflow history',
                       default_expr="state_change/getHistory",
                       props={'guard_permissions': View})

    vdef = wf.variables['time']
    vdef.setProperties(description='Time of the last transition',
                       default_expr="state_change/getDateTime",
                       for_status=1, update_always=1)


    configureEventPermissions(wf)
    return wf

addWorkflowFactory(createPatchWorkflow, id='patch_workflow', title='Patch Workflow [Rhaptos]')
                    

