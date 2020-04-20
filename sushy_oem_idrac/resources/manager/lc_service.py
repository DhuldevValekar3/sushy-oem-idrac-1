import logging
from sushy.resources import base
from sushy.resources import common

LOG = logging.getLogger(__name__)

class ActionsField(base.CompositeField):

    lc_service = common.ActionField("#DellLCService.GetRemoteServicesAPIStatus")


class DellLCService(base.ResourceBase):

    _actions = ActionsField('Actions')

    HEADERS = {'content-type': 'application/json'}

    IDRAC_READY_STATUS_CODE = 200
    IDRAC_READY_STATUS = 'Ready'

    identity = base.Field('Id', required=True)

    def __init__(self, connector, identity, redfish_version=None,
                 registries=None):
        """A class represents a DellLCService
        :param connector: A Connector instance
        :param identity: The identity of the DellLCService resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        :param registries: Dict of Redfish Message Registry objects to be
            used in any resource that needs registries to parse messages.
        """
        super(DellLCService, self).__init__(
            connector, identity, redfish_version, registries)

    def is_idrac_ready(self):
        """ Indicates if the iDRAC is ready to accept commands.
        Returns a remote service api status which indicates 
        the iDRAC is ready to accept commands. 

        """

        target_uri = self._actions.lc_service.target_uri

        LOG.debug('Checking to see if the iDRAC is ready...')
        idrac_ready_response = self._conn.post(target_uri,
                                    headers=self.HEADERS,
                                    data={},
                                    verify=False)
        if idrac_ready_response.status_code != self.IDRAC_READY_STATUS_CODE:
          return False
        data = idrac_ready_response.json()
        lc_status = data['LCStatus']
        return lc_status == self.IDRAC_READY_STATUS


