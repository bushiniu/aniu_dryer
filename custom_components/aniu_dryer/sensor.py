"""Sensor platform for the aniu_dryer integration."""
from __future__ import annotations

import logging

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import PERCENTAGE, UnitOfPower, UnitOfTime, UnitOfTemperature
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up aniu_dryer sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id].get("coordinator")
    if not coordinator:
        return

    async_add_entities([
        MyDryerSensor(coordinator, entry, "outlet_temp", "出风口温度", UnitOfTemperature.CELSIUS, "mdi:thermometer", SensorDeviceClass.TEMPERATURE, SensorStateClass.MEASUREMENT),
        MyDryerSensor(coordinator, entry, "outlet_hum", "出风口湿度", PERCENTAGE, "mdi:water-percent", SensorDeviceClass.HUMIDITY, SensorStateClass.MEASUREMENT),
        MyDryerSensor(coordinator, entry, "fan1_rpm", "风扇1转速", "RPM", "mdi:fan", None, SensorStateClass.MEASUREMENT),
        MyDryerSensor(coordinator, entry, "fan2_rpm", "风扇2转速", "RPM", "mdi:fan", None, SensorStateClass.MEASUREMENT),
        MyDryerSensor(coordinator, entry, "ptc_power", "PTC功率", PERCENTAGE, "mdi:power-socket-eu", SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT),
        MyDryerSensor(coordinator, entry, "remaining_time", "剩余时间", UnitOfTime.SECONDS, "mdi:timer-outline", SensorDeviceClass.DURATION, SensorStateClass.MEASUREMENT),
        MyDryerSensor(coordinator, entry, "set_temp", "设定温度", UnitOfTemperature.CELSIUS, "mdi:thermometer", SensorDeviceClass.TEMPERATURE, SensorStateClass.MEASUREMENT),
        MyDryerSensor(coordinator, entry, "set_time", "设定时长", UnitOfTime.HOURS, "mdi:timer", SensorDeviceClass.DURATION, SensorStateClass.MEASUREMENT),
        MyDryerSensor(coordinator, entry, "ptc_is_on", "PTC加热器状态", None, "mdi:lightbulb-on-10", None, None),
    ])


class MyDryerSensor(CoordinatorEntity, SensorEntity):
    """Representation of a aniu_dryer sensor."""

    def __init__(self, coordinator, entry, key, name, unit, icon, device_class, state_class):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._key = key
        self._attr_name = name
        self._attr_icon = icon
        self._attr_device_class = device_class
        self._attr_state_class = state_class
        self._attr_unique_id = f"{entry.entry_id}_{key}"
        self._unit = unit
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="耗材烘干机(交流Q群:1012505167)",
            manufacturer="扑腾的啊牛",
            model="单盘烘干模块"
        )
    
    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self.coordinator.data:
            value = self.coordinator.data.get(self._key)
            if self._key in ["outlet_temp", "outlet_hum", "ptc_power"] and isinstance(value, (float, int)):
                return round(value, 3)
            if self._key == "set_time" and isinstance(value, (float, int)):
                return round(value / 3600, 2)
            return value
        return None

    @property
    def native_unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit