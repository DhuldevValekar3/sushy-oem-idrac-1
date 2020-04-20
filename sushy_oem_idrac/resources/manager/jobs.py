import logging
from sushy.resources import base
from sushy.resources import common

LOG = logging.getLogger(__name__)


class DellJobCollection(base.ResourceBase):

    identity = base.Field('Id', required=True)

    JOB_EXPAND = '?$expand=.($levels=1)'

    def __init__(self, connector, identity, redfish_version=None,
                 registries=None):
        """A class represents a DellJobCollection
        :param connector: A Connector instance
        :param identity: The identity of the DellJobCollection resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        :param registries: Dict of Redfish Message Registry objects to be
            used in any resource that needs registries to parse messages
        """
        super(DellJobCollection, self).__init__(
            connector, identity, redfish_version, registries)

    def get_unfinished_jobs(self):
        """ Returns a list of unfinished jobs from the job queue

        :returns: a list of unfinished jobs.
        """

        job_expand_uri = '%s%s' %(self._path, self.JOB_EXPAND)

        unfinished_jobs = []
        LOG.debug('Filtering unfnished jobs...')
        job_response = self._conn.get(job_expand_uri, verify=False)
        data = job_response.json()

        for job in data[u'Members']:
            if((job[u'JobState'] == 'Scheduled') or
                (job[u'JobState'] == 'Running')):

                unfinished_jobs.append(job['Id'])
        LOG.info('Filtered unfinished jobs')
        return unfinished_jobs

