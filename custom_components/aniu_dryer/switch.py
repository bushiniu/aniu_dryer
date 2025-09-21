"""Switch platform for the aniu_dryer integration."""
from __future__ import annotations

import logging

import aiohttp
from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers import entity_registry as er

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities):
    """Set up aniu_dryer switch platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id].get("coordinator")
    if not coordinator:
        return

    async_add_entities([
        DryerSwitch(coordinator, entry),
        DryerExhaustValve(coordinator, entry),
    ])


class DryerSwitch(CoordinatorEntity, SwitchEntity):
    """Representation of a aniu_dryer switch."""

    def __init__(self, coordinator, entry):
        """Initialize the switch."""
        super().__init__(coordinator)
        self._host = entry.data["host"]
        self._attr_name = "启动烘干"
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
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get("ptc_is_on")

    async def async_turn_on(self, **kwargs):
        """Turn on the dryer."""
        url = f"http://{self._host}/api/control"
        
        registry = er.async_get(self.hass)

        temp_entity_id = registry.async_get_entity_id("number", DOMAIN, f"{self.coordinator.entry.entry_id}_set_temp_number")
        time_entity_id = registry.async_get_entity_id("number", DOMAIN, f"{self.coordinator.entry.entry_id}_set_time_number")
        
        if not temp_entity_id or not time_entity_id:
            _LOGGER.error("Temperature or time number entities not found in registry. This might be a timing issue.")
            return False

        temp = self.hass.states.get(temp_entity_id)
        time = self.hass.states.get(time_entity_id)

        if not temp or not time:
            _LOGGER.error("Temperature or time number entities not found. Please ensure they are set up correctly.")
            return False

        time_in_seconds = int(float(time.state) * 3600)

        payload = {
            "command": "start",
            "value": {
                "temp": float(temp.state),
                "time": time_in_seconds
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
        
        await self.coordinator.async_request_refresh()
        return True

    async def async_turn_off(self, **kwargs):
        """Turn off the dryer."""
        url = f"http://{self._host}/api/control"
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

        await self.coordinator.async_request_refresh()
        return True


class DryerExhaustValve(CoordinatorEntity, SwitchEntity):
    """Representation of a aniu_dryer exhaust valve switch."""

    def __init__(self, coordinator, entry):
        """Initialize the switch."""
        super().__init__(coordinator)
        self._host = entry.data["host"]
        self._attr_name = "排气阀"
        self._attr_unique_id = f"{entry.entry_id}_exhaust_valve_switch"
        self._attr_icon = "mdi:air-filter"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="耗材烘干机",
            manufacturer="扑腾的啊牛",
            model="单盘烘干机"
        )

    @property
    def is_on(self):
        """Return true if the exhaust valve is on."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get("exhaust_valve_state") == 1

    async def async_turn_on(self, **kwargs):
        """Turn on the exhaust valve."""
        url = f"http://{self._host}/api/control"
        payload = {
            "command": "operate_the_exhaust_valve",
            "value": 1
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, timeout=5) as response:
                    response.raise_for_status()
        except aiohttp.ClientError as err:
            _LOGGER.error("Error turning on exhaust valve: %s", err)
            return False
        await self.coordinator.async_request_refresh()
        return True

    async def async_turn_off(self, **kwargs):
        """Turn off the exhaust valve."""
        url = f"http://{self._host}/api/control"
        payload = {
            "command": "operate_the_exhaust_valve",
            "value": 0
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, timeout=5) as response:
                    response.raise_for_status()
        except aiohttp.ClientError as err:
            _LOGGER.error("Error turning off exhaust valve: %s", err)
            return False
        await self.coordinator.async_request_refresh()
        return True