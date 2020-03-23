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

import sushy
from sushy_oem_idrac import asynchronous

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
    lc_status = data['LCStatus']
    return lc_status == IDRAC_READY_STATUS

