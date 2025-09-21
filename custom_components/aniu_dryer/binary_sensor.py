"""Binary sensor platform for the aniu_dryer integration."""
from __future__ import annotations

import logging

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up aniu_dryer binary sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id].get("coordinator")
    if not coordinator:
        return

    async_add_entities([
        DryerExhaustValveSensor(coordinator, entry),
    ])


class DryerExhaustValveSensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a aniu_dryer exhaust valve sensor."""

    def __init__(self, coordinator, entry):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = "排气阀状态"
        self._attr_unique_id = f"{entry.entry_id}_exhaust_valve_state"
        self._attr_icon = "mdi:air-filter"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="耗材烘干机",
            manufacturer="扑腾的啊牛",
            model="单盘烘干机"
        )
    
    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        if self.coordinator.data:
            return self.coordinator.data.get("exhaust_valve_state") == 1
        return None