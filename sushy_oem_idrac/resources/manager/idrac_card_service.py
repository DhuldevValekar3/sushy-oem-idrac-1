import logging
from sushy import exceptions
from sushy.resources import base
from sushy.resources import common

LOG = logging.getLogger(__name__)

class ActionsField(base.CompositeField):

    reset_idrac = common.ActionField("#DelliDRACCardService.iDRACReset")

class DelliDRACCardService(base.ResourceBase):

    _actions = ActionsField('Actions')

    identity = base.Field('Id', required=True)

    def __init__(self, connector, identity, redfish_version=None,
                 registries=None):
        """A class represents a DelliDRACCardService
        :param connector: A Connector instance
        :param identity: The identity of the DelliDRACCardService resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        :param registries: Dict of Redfish Message Registry objects to be
            used in any resource that needs registries to parse messages.
        """
        super(DelliDRACCardService, self).__init__(
            connector, identity, redfish_version, registries)

    def reset_idrac(self, force="Graceful"):
        """ Resets the iDRAC
        :param force: does a force reset when caller pass "Force" as value 
        and it defaults to a graceful reset. 
        """

        payload = {"Force": force}

        target_uri = self._actions.reset_idrac.target_uri

        LOG.debug('Resetting the iDRAC %s ...', self.identity)
        self._conn.post(target_uri, data = payload)
        LOG.info('The iDRAC %s is being reset', self.identity)

