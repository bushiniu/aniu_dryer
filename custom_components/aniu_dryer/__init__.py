"""The aniu_dryer integration."""
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_HOST, Platform
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.core import HomeAssistant
import logging
import aiohttp
from datetime import timedelta

_LOGGER = logging.getLogger(__name__)
DOMAIN = "aniu_dryer"
PLATFORMS = [Platform.SENSOR, Platform.SWITCH, Platform.NUMBER, Platform.BINARY_SENSOR]

SCAN_INTERVAL = timedelta(seconds=1)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_HOST): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

async def async_setup(hass, config):
    """Set up the aniu_dryer integration from configuration.yaml."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry):
    """Set up aniu_dryer from a config entry."""
    host = entry.data[CONF_HOST]
    
    coordinator = MyDryerDataUpdateCoordinator(hass, host, entry)
    
    try:
        await coordinator.async_config_entry_first_refresh()
    except UpdateFailed as err:
        raise ConfigEntryNotReady(f"Failed to connect to device: {err}") from err
    
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {"coordinator": coordinator, "host": host}
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry):
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok

async def async_update_entry(hass: HomeAssistant, entry):
    """Update options of a config entry."""
    await hass.config_entries.async_reload(entry.entry_id)


class MyDryerDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(self, hass: HomeAssistant, host: str, entry):
        """Initialize."""
        self.host = host
        self._url = f"http://{self.host}/api/data"
        self.entry = entry
        
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )

    async def _async_update_data(self):
        """Fetch data from API endpoint."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self._url, timeout=5) as response:
                    response.raise_for_status()
                    data = await response.json()
                    _LOGGER.debug("Fetched data: %s", data)
                    return data
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error fetching data: {err}") from err
        except Exception as err:
            raise UpdateFailed(f"Unknown error: {err}") from err