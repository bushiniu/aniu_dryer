# """Switch platform for the aniu_dryer integration."""
# from __future__ import annotations

# import logging

# import aiohttp
# from homeassistant.components.switch import SwitchEntity
# from homeassistant.const import STATE_ON
# from homeassistant.core import HomeAssistant
# from homeassistant.helpers.entity import DeviceInfo
# from homeassistant.helpers.update_coordinator import CoordinatorEntity

# from . import DOMAIN

# _LOGGER = logging.getLogger(__name__)


# async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities):
#     """Set up aniu_dryer switch platform."""
#     coordinator = hass.data[DOMAIN][entry.entry_id].get("coordinator")
#     if not coordinator:
#         # The sensor platform creates the coordinator, so if it's not here,
#         # something is wrong.
#         return

#     async_add_entities([
#         DryerSwitch(coordinator, entry),
#     ])


# class DryerSwitch(CoordinatorEntity, SwitchEntity):
#     """Representation of a aniu_dryer switch."""

#     def __init__(self, coordinator, entry):
#         """Initialize the switch."""
#         super().__init__(coordinator)
#         self.coordinator = coordinator
#         self.entry = entry
#         self._host = entry.data["host"]
#         self._attr_name = "My Dryer"
#         self._attr_unique_id = f"{entry.entry_id}_switch"
#         self._attr_device_info = DeviceInfo(
#             identifiers={(DOMAIN, entry.entry_id)},
#             name="耗材烘干机",
#             manufacturer="扑腾的啊牛",
#             model="单盘烘干机"
#         )
    
#     @property
#     def is_on(self):
#         """Return true if the switch is on."""
#         # 增加对 self.coordinator.data 的检查，避免 NoneType 错误
#         # 只有当数据可用时才返回状态，否则返回 None
#         if self.coordinator.data is None:
#             return None
#         # return self.coordinator.data.get("remaining_time", 0) > 0
#         return self.coordinator.data.get("ptc_is_on", None)
    
#     async def async_turn_on(self, **kwargs):
#         """Turn on the dryer."""
#         url = f"http://{self._host}/api/control"
        
#         # We need to get the user's setpoint and time from the sensor attributes
#         # Since we don't have a way to directly get the input_number values from the integration
#         # we will use some default values or retrieve them from another source.
#         # For simplicity, we'll use a hardcoded value here. A more advanced
#         # integration would use a separate service call.
        
#         # Using hardcoded values for a simple test case. In a real-world scenario,
#         # you would need to retrieve these values from an input entity or a service.
#         temp = 50.0  # Default temperature
#         time = 3600  # Default time (1 hour)

#         payload = {
#             "command": "start",
#             "value": {
#                 "temp": temp,
#                 "time": time
#             }
#         }
#         _LOGGER.info("Sending start command to %s with payload: %s", url, payload)

#         try:
#             async with aiohttp.ClientSession() as session:
#                 async with session.post(url, json=payload, timeout=5) as response:
#                     response.raise_for_status()
#         except aiohttp.ClientError as err:
#             _LOGGER.error("Error sending start command: %s", err)
#             return False
        
#         # After sending the command, force a data refresh to update the state
#         await self.coordinator.async_request_refresh()
#         return True

#     async def async_turn_off(self, **kwargs):
#         """Turn off the dryer."""
#         url = f"http://{self._host}/api/control"
#         payload = {
#             "command": "stop",
#             "value": {
#                 "temp": 0,
#                 "time": 0
#             }
#         }
#         _LOGGER.info("Sending stop command to %s with payload: %s", url, payload)
        
#         try:
#             async with aiohttp.ClientSession() as session:
#                 async with session.post(url, json=payload, timeout=5) as response:
#                     response.raise_for_status()
#         except aiohttp.ClientError as err:
#             _LOGGER.error("Error sending stop command: %s", err)
#             return False

#         # After sending the command, force a data refresh to update the state
#         await self.coordinator.async_request_refresh()
#         return True
    



"""Switch platform for the aniu_dryer integration."""
from __future__ import annotations

import logging

import aiohttp
from homeassistant.components.switch import SwitchEntity
from homeassistant.const import STATE_ON
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities):
    """Set up aniu_dryer switch platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id].get("coordinator")
    if not coordinator:
        # The sensor platform creates the coordinator, so if it's not here,
        # something is wrong.
        return

    async_add_entities([
        DryerSwitch(coordinator, entry),
    ])


class DryerSwitch(CoordinatorEntity, SwitchEntity):
    """Representation of a aniu_dryer switch."""

    def __init__(self, coordinator, entry):
        """Initialize the switch."""
        super().__init__(coordinator)
        self.coordinator = coordinator
        self.entry = entry # 存储整个配置条目对象
        self._attr_name = "My Dryer"
        self._attr_unique_id = f"{entry.entry_id}_switch"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="耗材烘干机",
            manufacturer="扑腾的啊牛",
            model="单盘烘干机"
        )
    
    @property
    def is_on(self):
        """Return true if the switch is on."""
        # 增加对 self.coordinator.data 的检查，避免 NoneType 错误
        # 只有当数据可用时才返回状态，否则返回 None
        if self.coordinator.data is None:
            return None
        # return self.coordinator.data.get("remaining_time", 0) > 0
        return self.coordinator.data.get("ptc_is_on", None)
    
    async def async_turn_on(self, **kwargs):
        """Turn on the dryer."""
        # 动态获取最新的IP地址
        host = self.entry.data["host"]
        url = f"http://{host}/api/control"
        
        # We need to get the user's setpoint and time from the sensor attributes
        # Since we don't have a way to directly get the input_number values from the integration
        # we will use some default values or retrieve them from another source.
        # For simplicity, we'll use a hardcoded value here. A more advanced
        # integration would use a separate service call.
        
        # Using hardcoded values for a simple test case. In a real-world scenario,
        # you would need to retrieve these values from an input entity or a service.
        temp = 50.0  # Default temperature
        time = 3600  # Default time (1 hour)

        payload = {
            "command": "start",
            "value": {
                "temp": temp,
                "time": time
            }
        }
        _LOGGER.info("Sending start command to %s with payload: %s", url, payload)

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, timeout=5) as response:
                    response.raise_for_status()
        except aiohttp.ClientError as err:
            _LOGGER.error("Error sending start command: %s", err)
            return False
        
        # After sending the command, force a data refresh to update the state
        await self.coordinator.async_request_refresh()
        return True

    async def async_turn_off(self, **kwargs):
        """Turn off the dryer."""
        # 动态获取最新的IP地址
        host = self.entry.data["host"]
        url = f"http://{host}/api/control"
        payload = {
            "command": "stop",
            "value": {
                "temp": 0,
                "time": 0
            }
        }
        _LOGGER.info("Sending stop command to %s with payload: %s", url, payload)
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, timeout=5) as response:
                    response.raise_for_status()
        except aiohttp.ClientError as err:
            _LOGGER.error("Error sending stop command: %s", err)
            return False

        # After sending the command, force a data refresh to update the state
        await self.coordinator.async_request_refresh()
        return True
    



