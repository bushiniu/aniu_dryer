# """The aniu_dryer integration."""
# import voluptuous as vol
# import homeassistant.helpers.config_validation as cv
# from homeassistant.const import CONF_HOST, Platform

# DOMAIN = "aniu_dryer"
# PLATFORMS = [Platform.SENSOR, Platform.SWITCH]

# CONFIG_SCHEMA = vol.Schema(
#     {
#         DOMAIN: vol.Schema(
#             {
#                 vol.Required(CONF_HOST): cv.string,
#             }
#         )
#     },
#     extra=vol.ALLOW_EXTRA,
# )

# async def async_setup(hass, config):
#     """Set up the aniu_dryer integration from configuration.yaml."""
#     hass.data.setdefault(DOMAIN, {})
#     return True

# async def async_setup_entry(hass, entry):
#     """Set up aniu_dryer from a config entry."""
#     host = entry.data[CONF_HOST]
#     hass.data[DOMAIN][entry.entry_id] = {"host": host}
#     await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
#     return True

# async def async_unload_entry(hass, entry):
#     """Unload a config entry."""
#     unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
#     if unload_ok:
#         hass.data[DOMAIN].pop(entry.entry_id)
#     return unload_ok
# async def async_update_entry(hass, entry):
#     """Update options of a config entry."""
#     # 重新加载配置条目，这将强制刷新所有平台和实体，并使用新的配置
#     await hass.config_entries.async_reload(entry.entry_id)

"""The aniu_dryer integration."""
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_HOST, Platform

DOMAIN = "aniu_dryer"
# PLATFORMS = [Platform.SENSOR, Platform.SWITCH]
PLATFORMS = [Platform.SENSOR, Platform.SWITCH]

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

async def async_setup_entry(hass, entry):
    """Set up aniu_dryer from a config entry."""
    host = entry.data[CONF_HOST]
    hass.data[DOMAIN][entry.entry_id] = {"host": host}
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass, entry):
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
async def async_update_entry(hass, entry):
    """Update options of a config entry."""
    # 重新加载配置条目，这将强制刷新所有平台和实体，并使用新的配置
    await hass.config_entries.async_reload(entry.entry_id)

