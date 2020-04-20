import logging
from sushy.resources import base
from sushy.resources import common

LOG = logging.getLogger(__name__)

class ActionsField(base.CompositeField):

    delete_job_queue = common.ActionField("#DellJobService.DeleteJobQueue")


class DellJobService(base.ResourceBase):

    _actions = ActionsField('Actions')

    HEADERS = {'content-type': 'application/json'}

    identity = base.Field('Id', required=True)

    def __init__(self, connector, identity, redfish_version=None,
                 registries=None):
        """A class representing a DellJobService
        :param connector: A Connector instance
        :param identity: The identity of the DellJobService resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        :param registries: Dict of Redfish Message Registry objects to be
            used in any resource that needs registries to parse messages.
        """
        super(DellJobService, self).__init__(
            connector, identity, redfish_version, registries)

    def delete_jobs(self, job_ids=['JID_CLEARALL']):
        """ Deletes the given jobs, or all jobs

        :param job_ids: a list of job ids to delete. Clearing all the
            jobs may be accomplished using the keyword JID_CLEARALL
            as the job_id.
        """
        target_uri = self._actions.delete_job_queue.target_uri

        LOG.debug('Deleting the job queue ...')
        for job_id in job_ids:
            payload = {'JobID':job_id}
            self._conn.post(target_uri,
                            headers=self.HEADERS,
                            data=payload,
                            verify=False)
        LOG.info('Deleted the job queue')

