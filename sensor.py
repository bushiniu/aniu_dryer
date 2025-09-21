# """Sensor platform for the aniu_dryer integration."""
# from __future__ import annotations

# from datetime import timedelta
# import logging

# import aiohttp
# from homeassistant.components.sensor import (
#     SensorEntity,
#     SensorDeviceClass,
#     SensorStateClass,
# )
# from homeassistant.const import PERCENTAGE
# from homeassistant.helpers.entity import DeviceInfo
# from homeassistant.helpers.update_coordinator import (
#     CoordinatorEntity,
#     DataUpdateCoordinator,
#     UpdateFailed,
# )
# from homeassistant.components.sensor import UnitOfTemperature
# from homeassistant.const import UnitOfTime

# from . import DOMAIN

# _LOGGER = logging.getLogger(__name__)

# SCAN_INTERVAL = timedelta(seconds=1)


# async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities):
#     """Set up aniu_dryer sensor platform."""
#     host = hass.data[DOMAIN][entry.entry_id]["host"]
    
#     # Check if a coordinator already exists for this entry
#     coordinator = hass.data[DOMAIN][entry.entry_id].get("coordinator")
#     if not coordinator:
#         coordinator = MyDryerDataUpdateCoordinator(hass, host)
#         # Store the coordinator in hass.data so other platforms can use it
#         hass.data[DOMAIN][entry.entry_id]["coordinator"] = coordinator

#     await coordinator.async_config_entry_first_refresh()

#     async_add_entities([
#         MyDryerSensor(coordinator, entry, "outlet_temp", "出风口温度", UnitOfTemperature.CELSIUS, "mdi:thermometer", SensorDeviceClass.TEMPERATURE, SensorStateClass.MEASUREMENT),
#         MyDryerSensor(coordinator, entry, "outlet_hum", "出风口湿度", PERCENTAGE, "mdi:water-percent", SensorDeviceClass.HUMIDITY, SensorStateClass.MEASUREMENT),
#         MyDryerSensor(coordinator, entry, "fan1_rpm", "风扇1转速", "RPM", "mdi:fan", None, SensorStateClass.MEASUREMENT),
#         MyDryerSensor(coordinator, entry, "fan2_rpm", "风扇2转速", "RPM", "mdi:fan", None, SensorStateClass.MEASUREMENT),
#         MyDryerSensor(coordinator, entry, "ptc_power", "PTC功率", "W", "mdi:power-socket-eu", None, SensorStateClass.MEASUREMENT),
#         # 修复了剩余时间传感器，它现在直接返回秒数，由Home Assistant处理显示格式
#         MyDryerSensor(coordinator, entry, "remaining_time", "剩余时间", UnitOfTime.SECONDS, "mdi:timer-outline", SensorDeviceClass.DURATION, SensorStateClass.MEASUREMENT),
#         MyDryerSensor(coordinator, entry, "set_temp", "设定温度", UnitOfTemperature.CELSIUS, "mdi:thermometer", SensorDeviceClass.TEMPERATURE, SensorStateClass.MEASUREMENT),
#         MyDryerSensor(coordinator, entry, "set_time", "设定时长", UnitOfTime.SECONDS, "mdi:timer", SensorDeviceClass.DURATION, SensorStateClass.MEASUREMENT),
#         MyDryerSensor(coordinator, entry, "ptc_is_on", "PTC工作状态", None, "mdi:power-heat", None, None),
#     ])


# class MyDryerDataUpdateCoordinator(DataUpdateCoordinator):
#     """Class to manage fetching data from the API."""

#     def __init__(self, hass: HomeAssistant, host: str):
#         """Initialize."""
#         self.host = host
#         self._url = f"http://{self.host}/api/data"
        
#         super().__init__(
#             hass,
#             _LOGGER,
#             name=DOMAIN,
#             update_interval=SCAN_INTERVAL,
#         )

#     async def _async_update_data(self):
#         """Fetch data from API endpoint."""
#         try:
#             async with aiohttp.ClientSession() as session:
#                 async with session.get(self._url, timeout=5) as response:
#                     response.raise_for_status()
#                     data = await response.json()
#                     _LOGGER.debug("Fetched data: %s", data)
#                     return data
#         except aiohttp.ClientError as err:
#             raise UpdateFailed(f"Error fetching data: {err}") from err
#         except Exception as err:
#             raise UpdateFailed(f"Unknown error: {err}") from err


# class MyDryerSensor(CoordinatorEntity, SensorEntity):
#     """Representation of a aniu_dryer sensor."""

#     def __init__(self, coordinator, entry, key, name, unit, icon, device_class, state_class):
#         """Initialize the sensor."""
#         super().__init__(coordinator)
#         self._key = key
#         self._attr_name = name
#         self._attr_unit_of_measurement = unit
#         self._attr_icon = icon
#         self._attr_device_class = device_class
#         self._attr_state_class = state_class
#         self._attr_unique_id = f"{entry.entry_id}_{key}"
#         self._attr_device_info = DeviceInfo(
#             identifiers={(DOMAIN, entry.entry_id)},
#             name="耗材烘干机(交流Q群:1012505167)",
#             manufacturer="扑腾的啊牛",
#             model="单盘烘干模块"
#         )
    
#     @property
#     def native_value(self):
#         """Return the state of the sensor."""
#         return self.coordinator.data.get(self._key)


"""Sensor platform for the aniu_dryer integration."""
from __future__ import annotations

from datetime import timedelta
import logging

import aiohttp
from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import PERCENTAGE
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.components.sensor import UnitOfTemperature
from homeassistant.const import UnitOfTime

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=1)


async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities):
    """Set up aniu_dryer sensor platform."""
    host = hass.data[DOMAIN][entry.entry_id]["host"]
    
    # Check if a coordinator already exists for this entry
    coordinator = hass.data[DOMAIN][entry.entry_id].get("coordinator")
    if not coordinator:
        # 传入整个 entry 对象
        coordinator = MyDryerDataUpdateCoordinator(hass, entry)
        hass.data[DOMAIN][entry.entry_id]["coordinator"] = coordinator

    await coordinator.async_config_entry_first_refresh()

    async_add_entities([
        MyDryerSensor(coordinator, entry, "outlet_temp", "出风口温度", UnitOfTemperature.CELSIUS, "mdi:thermometer", SensorDeviceClass.TEMPERATURE, SensorStateClass.MEASUREMENT),
        MyDryerSensor(coordinator, entry, "outlet_hum", "出风口湿度", PERCENTAGE, "mdi:water-percent", SensorDeviceClass.HUMIDITY, SensorStateClass.MEASUREMENT),
        MyDryerSensor(coordinator, entry, "fan1_rpm", "风扇1转速", "RPM", "mdi:fan", None, SensorStateClass.MEASUREMENT),
        MyDryerSensor(coordinator, entry, "fan2_rpm", "风扇2转速", "RPM", "mdi:fan", None, SensorStateClass.MEASUREMENT),
        MyDryerSensor(coordinator, entry, "ptc_power", "PTC功率", "W", "mdi:power-socket-eu", None, SensorStateClass.MEASUREMENT),
        # 修复了剩余时间传感器，它现在直接返回秒数，由Home Assistant处理显示格式
        MyDryerSensor(coordinator, entry, "remaining_time", "剩余时间", UnitOfTime.SECONDS, "mdi:timer-outline", SensorDeviceClass.DURATION, SensorStateClass.MEASUREMENT),
        MyDryerSensor(coordinator, entry, "set_temp", "设定温度", UnitOfTemperature.CELSIUS, "mdi:thermometer", SensorDeviceClass.TEMPERATURE, SensorStateClass.MEASUREMENT),
        MyDryerSensor(coordinator, entry, "set_time", "设定时长", UnitOfTime.SECONDS, "mdi:timer", SensorDeviceClass.DURATION, SensorStateClass.MEASUREMENT),
        MyDryerSensor(coordinator, entry, "ptc_is_on", "PTC工作状态", None, "mdi:power-heat", None, None),
    ])


class MyDryerDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(self, hass: HomeAssistant, entry):
        """Initialize."""
        # 存储整个配置条目对象
        self._entry = entry
        
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )

    async def _async_update_data(self):
        """Fetch data from API endpoint."""
        try:
            # 动态获取最新的IP地址
            host = self._entry.data["host"]
            url = f"http://{host}/api/data"
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=5) as response:
                    response.raise_for_status()
                    data = await response.json()
                    _LOGGER.debug("Fetched data: %s", data)
                    return data
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error fetching data: {err}") from err
        except Exception as err:
            raise UpdateFailed(f"Unknown error: {err}") from err

class MyDryerSensor(CoordinatorEntity, SensorEntity):
    """Representation of a aniu_dryer sensor."""

    def __init__(self, coordinator, entry, key, name, unit, icon, device_class, state_class):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._key = key
        self._attr_name = name
        self._attr_unit_of_measurement = unit
        self._attr_icon = icon
        self._attr_device_class = device_class
        self._attr_state_class = state_class
        self._attr_unique_id = f"{entry.entry_id}_{key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="耗材烘干机(交流Q群:1012505167)",
            manufacturer="扑腾的啊牛",
            model="单盘烘干模块"
        )
    
    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get(self._key)




