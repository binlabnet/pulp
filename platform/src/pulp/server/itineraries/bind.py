# Copyright (c) 2010 Red Hat, Inc.
#
# This software is licensed to you under the GNU General Public
# License as published by the Free Software Foundation; either version
# 2 of the License (GPLv2) or (at your option) any later version.
# There is NO WARRANTY for this software, express or implied,
# including the implied warranties of MERCHANTABILITY,
# NON-INFRINGEMENT, or FITNESS FOR A PARTICULAR PURPOSE. You should
# have received a copy of GPLv2 along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

import logging

from pulp.server.dispatch.call import CallRequest
from pulp.common.tags import action_tag, resource_tag
from pulp.server.dispatch import constants as dispatch_constants
from pulp.server.managers import factory as managers


_LOG = logging.getLogger(__name__)


# -- task callbacks ----------------------------------------------------------------------

def bind_succeeded(call_request, call_report):
    """
    The task succeeded callback.
    Updates the consumer request tracking on the binding.
    """
    manager = managers.consumer_bind_manager()
    action_id = call_request.id
    consumer_id, repo_id, distributor_id, options = call_request.args
    dispatch_report = call_report.result
    if dispatch_report['succeeded']:
        manager.action_succeeded(consumer_id, repo_id, distributor_id, action_id)
    else:
        manager.action_failed(consumer_id, repo_id, distributor_id, action_id)

def bind_failed(call_request, call_report):
    """
    The task failed callback.
    Updates the consumer request tracking on the binding.
    """
    manager = managers.consumer_bind_manager()
    action_id = call_request.id
    consumer_id, repo_id, distributor_id, options = call_request.args
    manager.action_failed(consumer_id, repo_id, distributor_id, action_id)

# just mapped to bind functions because the behavior is the same
# but want to use these names in the unbind itinerary for clarity.
unbind_succeeded = bind_succeeded
unbind_failed = bind_failed


# -- itineraries -------------------------------------------------------------------------


def bind_itinerary(consumer_id, repo_id, distributor_id, options):
    """
    Get the bind itinerary:
      1. Create the binding on the server.
      2. Request that the consumer (agent) perform the bind.
    @param consumer_id: A consumer ID.
    @type consumer_id: str
    @param repo_id: A repository ID.
    @type repo_id: str
    @param distributor_id: A distributor ID.
    @type distributor_id: str
    @param options: Bind options passed to the agent handler.
    @type options: dict
    @return: A list of call_requests.
    @rtype list
    """

    call_requests = []
    bind_manager = managers.consumer_bind_manager()
    agent_manager = managers.consumer_agent_manager()

    # bind

    resources = {
        dispatch_constants.RESOURCE_CONSUMER_TYPE:
            {consumer_id:dispatch_constants.RESOURCE_READ_OPERATION},
        dispatch_constants.RESOURCE_REPOSITORY_TYPE:
            {repo_id:dispatch_constants.RESOURCE_READ_OPERATION},
        dispatch_constants.RESOURCE_REPOSITORY_DISTRIBUTOR_TYPE:
            {distributor_id:dispatch_constants.RESOURCE_READ_OPERATION},
    }

    tags = [
        resource_tag(dispatch_constants.RESOURCE_CONSUMER_TYPE, consumer_id),
        resource_tag(dispatch_constants.RESOURCE_REPOSITORY_TYPE, repo_id),
        resource_tag(dispatch_constants.RESOURCE_REPOSITORY_DISTRIBUTOR_TYPE, distributor_id),
        action_tag('bind')
    ]

    args = [
        consumer_id,
        repo_id,
        distributor_id,
    ]

    bind_request = CallRequest(
        bind_manager.bind,
        args,
        resources=resources,
        weight=0,
        tags=tags)

    call_requests.append(bind_request)

    # notify agent

    tags = [
        resource_tag(dispatch_constants.RESOURCE_CONSUMER_TYPE, consumer_id),
        resource_tag(dispatch_constants.RESOURCE_REPOSITORY_TYPE, repo_id),
        resource_tag(dispatch_constants.RESOURCE_REPOSITORY_DISTRIBUTOR_TYPE, distributor_id),
        action_tag('agent.bind')
    ]

    args = [
        consumer_id,
        repo_id,
        distributor_id,
        options
    ]

    agent_request = CallRequest(
        agent_manager.bind,
        args,
        weight=0,
        asynchronous=True,
        archive=True,
        tags=tags)

    agent_request.add_life_cycle_callback(
        dispatch_constants.CALL_SUCCESS_LIFE_CYCLE_CALLBACK,
        bind_succeeded)

    agent_request.add_life_cycle_callback(
        dispatch_constants.CALL_FAILURE_LIFE_CYCLE_CALLBACK,
        bind_failed)

    call_requests.append(agent_request)

    agent_request.depends_on(bind_request.id)

    return call_requests


def unbind_itinerary(consumer_id, repo_id, distributor_id, options):
    """
    Get the unbind itinerary.
    The tasks in the itinerary are as follows:
      1. Mark the binding as (deleted) on the server.
      2. Request that the consumer (agent) perform the unbind.
      3. Delete the binding on the server.
    @param consumer_id: A consumer ID.
    @type consumer_id: str
    @param repo_id: A repository ID.
    @type repo_id: str
    @param distributor_id: A distributor ID.
    @type distributor_id: str
    @param options: Unbind options passed to the agent handler.
    @type options: dict
    @return: A list of call_requests.
    @rtype list
    """

    call_requests = []
    bind_manager = managers.consumer_bind_manager()
    agent_manager = managers.consumer_agent_manager()

    # unbind

    resources = {
        dispatch_constants.RESOURCE_CONSUMER_TYPE:
            {consumer_id:dispatch_constants.RESOURCE_READ_OPERATION},
    }

    tags = [
        resource_tag(dispatch_constants.RESOURCE_CONSUMER_TYPE, consumer_id),
        resource_tag(dispatch_constants.RESOURCE_REPOSITORY_TYPE, repo_id),
        resource_tag(dispatch_constants.RESOURCE_REPOSITORY_DISTRIBUTOR_TYPE, distributor_id),
        action_tag('unbind')
    ]

    args = [
        consumer_id,
        repo_id,
        distributor_id,
    ]

    unbind_request = CallRequest(
        bind_manager.unbind,
        args=args,
        resources=resources,
        tags=tags)

    call_requests.append(unbind_request)

    # notify agent

    tags = [
        resource_tag(dispatch_constants.RESOURCE_CONSUMER_TYPE, consumer_id),
        resource_tag(dispatch_constants.RESOURCE_REPOSITORY_TYPE, repo_id),
        resource_tag(dispatch_constants.RESOURCE_REPOSITORY_DISTRIBUTOR_TYPE, distributor_id),
        action_tag('agent.unbind')
    ]

    args = [
        consumer_id,
        repo_id,
        distributor_id,
        options,
    ]

    agent_request = CallRequest(
        agent_manager.unbind,
        args,
        weight=0,
        asynchronous=True,
        archive=True,
        tags=tags)

    agent_request.add_life_cycle_callback(
        dispatch_constants.CALL_SUCCESS_LIFE_CYCLE_CALLBACK,
        unbind_succeeded)

    agent_request.add_life_cycle_callback(
        dispatch_constants.CALL_FAILURE_LIFE_CYCLE_CALLBACK,
        unbind_failed)

    call_requests.append(agent_request)

    agent_request.depends_on(unbind_request.id)

    # delete the binding

    binding = bind_manager.get_bind(consumer_id, repo_id, distributor_id)
    bind_id = str(binding['_id'])

    resources = {
        dispatch_constants.RESOURCE_CONSUMER_TYPE:
            {consumer_id:dispatch_constants.RESOURCE_READ_OPERATION},
    }

    tags = [
        resource_tag(dispatch_constants.RESOURCE_CONSUMER_BINDING_TYPE, bind_id),
        action_tag('delete')
    ]

    args = [
        consumer_id,
        repo_id,
        distributor_id
    ]

    delete_request = CallRequest(
        bind_manager.delete,
        args=args,
        resources=resources,
        tags=tags)

    call_requests.append(delete_request)

    delete_request.depends_on(agent_request.id)

    return call_requests


def forced_unbind_itinerary(consumer_id, repo_id, distributor_id, options):
    """
    Get the unbind itinerary.
    A forced unbind immediately deletes the binding instead
    of marking it deleted and going through that lifecycle.
    It is intended to be used to clean up orphaned bindings
    caused by failed/unconfirmed unbind actions on the consumer.
    The itinerary is:
      1. Delete the binding on the server.
      2. Request that the consumer (agent) perform the unbind.
    @param consumer_id: A consumer ID.
    @type consumer_id: str
    @param repo_id: A repository ID.
    @type repo_id: str
    @param distributor_id: A distributor ID.
    @type distributor_id: str
    @param options: Unbind options passed to the agent handler.
    @type options: dict
    @return: A list of call_requests
    @rtype list
    """

    call_requests = []
    bind_manager = managers.consumer_bind_manager()
    agent_manager = managers.consumer_agent_manager()

    # unbind

    resources = {
        dispatch_constants.RESOURCE_CONSUMER_TYPE:
            {consumer_id:dispatch_constants.RESOURCE_READ_OPERATION},
        }

    tags = [
        resource_tag(dispatch_constants.RESOURCE_CONSUMER_TYPE, consumer_id),
        resource_tag(dispatch_constants.RESOURCE_REPOSITORY_TYPE, repo_id),
        resource_tag(dispatch_constants.RESOURCE_REPOSITORY_DISTRIBUTOR_TYPE, distributor_id),
        action_tag('unbind')
    ]

    args = [
        consumer_id,
        repo_id,
        distributor_id,
        True,
    ]

    delete_request = CallRequest(
        bind_manager.delete,
        args=args,
        resources=resources,
        tags=tags)

    call_requests.append(delete_request)

    # notify agent

    tags = [
        resource_tag(dispatch_constants.RESOURCE_CONSUMER_TYPE, consumer_id),
        resource_tag(dispatch_constants.RESOURCE_REPOSITORY_TYPE, repo_id),
        resource_tag(dispatch_constants.RESOURCE_REPOSITORY_DISTRIBUTOR_TYPE, distributor_id),
        action_tag('agent.unbind')
    ]

    args = [
        consumer_id,
        repo_id,
        distributor_id,
        options,
    ]

    agent_request = CallRequest(
        agent_manager.unbind,
        args,
        weight=0,
        asynchronous=True,
        archive=True,
        tags=tags)


    call_requests.append(agent_request)

    agent_request.depends_on(delete_request.id)

    return call_requests