"""Number platform for the aniu_dryer integration."""
from __future__ import annotations

import logging

from homeassistant.components.number import NumberEntity
from homeassistant.const import UnitOfTemperature, UnitOfTime
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.event import async_call_later
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities):
    """Set up aniu_dryer number platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id].get("coordinator")
    if not coordinator:
        return

    async_add_entities([
        DryerSetTemp(coordinator, entry, hass),
        DryerSetTime(coordinator, entry, hass),
    ])


class DryerSetTemp(CoordinatorEntity, NumberEntity):
    """Representation of a aniu_dryer temperature setting."""

    def __init__(self, coordinator, entry, hass: HomeAssistant):
        """Initialize the number entity."""
        super().__init__(coordinator)
        self.hass = hass
        self._attr_name = "设定温度"
        self._attr_unique_id = f"{entry.entry_id}_set_temp_number"
        self._attr_device_class = "temperature"
        self._attr_native_min_value = 25.0
        self._attr_native_max_value = 80.0
        self._attr_native_step = 0.5
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="耗材烘干机",
            manufacturer="扑腾的啊牛",
            model="单盘烘干机"
        )
        self._native_value = None
        self._is_user_overridden = False
        self._reset_timer = None
    
    @property
    def native_value(self):
        """Return the current temperature setting."""
        if self._is_user_overridden and self._native_value is not None:
            return self._native_value
        return self.coordinator.data.get("set_temp")

    async def async_set_native_value(self, value):
        """Update the temperature setting."""
        self._native_value = value
        self._is_user_overridden = True
        
        if self._reset_timer:
            self._reset_timer()
            self._reset_timer = None
        
        self._reset_timer = async_call_later(
            self.hass, 30, self._async_reset_value
        )
        self.async_write_ha_state()
        _LOGGER.debug("Temperature setting changed to: %s. User override started.", value)

    @callback
    def _async_reset_value(self, _):
        """Reset the value to the current value from the coordinator."""
        _LOGGER.debug("Temperature reset timer finished. Re-syncing with device data.")
        self._is_user_overridden = False
        self._native_value = None
        self.async_write_ha_state()
        self._reset_timer = None


class DryerSetTime(CoordinatorEntity, NumberEntity):
    """Representation of a aniu_dryer time setting."""

    def __init__(self, coordinator, entry, hass: HomeAssistant):
        """Initialize the number entity."""
        super().__init__(coordinator)
        self.hass = hass
        self._attr_name = "设定时长"
        self._attr_unique_id = f"{entry.entry_id}_set_time_number"
        self._attr_device_class = "duration"
        # 单位转换为小时
        self._attr_native_min_value = 1
        self._attr_native_max_value = 24
        self._attr_native_step = 1
        self._attr_native_unit_of_measurement = UnitOfTime.HOURS
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="耗材烘干机",
            manufacturer="扑腾的啊牛",
            model="单盘烘干机"
        )
        self._native_value = None
        self._is_user_overridden = False
        self._reset_timer = None
    
    @property
    def native_value(self):
        """Return the current time setting in hours."""
        if self._is_user_overridden and self._native_value is not None:
            # 返回用户设定的值（小时）
            return self._native_value
        # 返回设备数据（秒）转换为小时
        device_value_seconds = self.coordinator.data.get("set_time")
        if device_value_seconds is not None:
            return round(device_value_seconds / 3600, 2)
        return None

    async def async_set_native_value(self, value):
        """Update the time setting."""
        self._native_value = value
        self._is_user_overridden = True
        
        if self._reset_timer:
            self._reset_timer()
            self._reset_timer = None
        
        self._reset_timer = async_call_later(
            self.hass, 30, self._async_reset_value
        )
        self.async_write_ha_state()
        _LOGGER.debug("Time setting changed to: %s. User override started.", value)

    @callback
    def _async_reset_value(self, _):
        """Reset the value to the current value from the coordinator."""
        _LOGGER.debug("Time reset timer finished. Re-syncing with device data.")
        self._is_user_overridden = False
        self._native_value = None
        self.async_write_ha_state()
        self._reset_timer = None