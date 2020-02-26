# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging
import time
import retrying

import sushy
from sushy_oem_idrac import asynchronous
from sushy_oem_idrac import constants

LOG = logging.getLogger(__name__)

IDRAC_READY_STATUS = 'Ready'
IDRAC_READY_STATUS_CODE = 200

def reboot_system(system):
    if system.power_state != sushy.POWER_STATE_OFF:
        system.reset_system(sushy.RESET_FORCE_OFF)
        LOG.info('Requested system power OFF')

    while system.power_state != sushy.POWER_STATE_OFF:
        time.sleep(30)
        system.refresh()

    LOG.info('System is powered OFF')

    system.reset_system(sushy.RESET_ON)

    LOG.info('Requested system power ON')

    while system.power_state != sushy.POWER_STATE_ON:
        time.sleep(30)
        system.refresh()

    LOG.info('System powered ON')

def wait_until_idrac_is_ready(oem_manager, retries=None, retry_delay=None):
    """Waits until the iDRAC is in a ready state

    :param retries: The number of times to check if the iDRAC is
                    ready. If None, the value of ready_retries that
                    was provided when the object was created is
                    used.
    :param retry_delay: The number of seconds to wait between
                        retries. If None, the value of
                        ready_retry_delay that was provided when the
                        object was created is used.
    """

    if retries is None:
        retries = constants.IDRAC_IS_READY_RETRIES

    if retry_delay is None:
        retry_delay = constants.IDRAC_IS_READY_RETRY_DELAY_SEC

    while retries > 0:
        LOG.debug("Checking to see if the iDRAC is ready")

        if is_idrac_ready(oem_manager):
            LOG.debug("The iDRAC is ready")
            return

        LOG.debug("The iDRAC is not ready")
        retries -= 1
        if retries > 0:
            time.sleep(retry_delay)

    if retries == 0:
        err_msg = "Timed out waiting for the iDRAC to become ready after reset"
        LOG.error(err_msg)
        raise

def is_idrac_ready(oem_manager):
    """Indicates if the iDRAC is ready to accept commands

       Returns a boolean indicating if the iDRAC is ready to accept
       commands.

    :returns: Boolean indicating iDRAC readiness
    """

    response = asynchronous.http_call(
                    oem_manager._conn, 'post',
                    oem_manager.get_remote_service_api_uri,
                    headers=oem_manager.HEADERS,
                    data={},
                    verify=False)
    if response.status_code != IDRAC_READY_STATUS_CODE:
        return False
    data = response.json()
    ls_status = data['LCStatus']
    return ls_status == IDRAC_READY_STATUS

