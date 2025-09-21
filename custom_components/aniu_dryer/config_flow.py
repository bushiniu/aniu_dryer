# """Config flow for the aniu_dryer integration."""
# import voluptuous as vol
# from homeassistant import config_entries
# from homeassistant.const import CONF_HOST
# from homeassistant.core import callback
# import asyncio


# async def validate_input(hass, host):
#     """Validate the user input allows us to connect to the device."""
#     try:
#         reader, writer = await asyncio.open_connection(host, 80)
#         writer.close()
#         await writer.wait_closed()
#         return True
#     except asyncio.TimeoutError:
#         return False
#     except (ConnectionRefusedError, OSError):
#         return False
#     except Exception as e:
#         print(f"Error during connection validation: {e}")
#         return False


# class AniuDryerConfigFlow(config_entries.ConfigFlow, domain="aniu_dryer"):
#     """Handle a config flow for aniu_dryer."""

#     VERSION = 1

#     async def async_step_user(self, user_input=None):
#         """Handle the initial step."""
#         errors = {}
#         if user_input is not None:
#             host = user_input[CONF_HOST]
#             if await validate_input(self.hass, host):
#                 return self.async_create_entry(title="耗材烘干机——扑腾的啊牛", data={"host": host})
#             else:
#                 errors["base"] = "cannot_connect"

#         data_schema = vol.Schema({vol.Required(CONF_HOST): str})
#         return self.async_show_form(
#             step_id="user",
#             data_schema=data_schema,
#             errors=errors,
#         )

#     @staticmethod
#     @callback
#     def async_get_options_flow(config_entry):
#         """Get the options flow for this handler."""
#         return AniuDryerOptionsFlow()


# class AniuDryerOptionsFlow(config_entries.OptionsFlow):
#     """Options flow for aniu_dryer."""
#     async def async_step_init(self, user_input=None):
#         """Manage the options."""
#         return await self.async_step_user(user_input)

# config_flow.py

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST
from homeassistant.core import callback
import asyncio

async def validate_input(hass, host):
    """Validate the user input allows us to connect to the device."""
    try:
        reader, writer = await asyncio.open_connection(host, 80)
        writer.close()
        await writer.wait_closed()
        return True
    except asyncio.TimeoutError:
        return False
    except (ConnectionRefusedError, OSError):
        return False
    except Exception as e:
        print(f"Error during connection validation: {e}")
        return False

class AniuDryerConfigFlow(config_entries.ConfigFlow, domain="aniu_dryer"):
    """Handle a config flow for aniu_dryer."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            host = user_input[CONF_HOST]
            if await validate_input(self.hass, host):
                return self.async_create_entry(title="耗材烘干机——扑腾的啊牛", data={"host": host})
            else:
                errors["base"] = "cannot_connect"

        data_schema = vol.Schema({vol.Required(CONF_HOST): str})
        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return AniuDryerOptionsFlow(config_entry)


class AniuDryerOptionsFlow(config_entries.OptionsFlow):
    """Options flow for aniu_dryer."""

    # 直接移除 __init__ 方法
    def __init__(self, config_entry):
        self.config_entry = config_entry
    
    async def async_step_init(self, user_input=None):
        """Manage the options."""
        errors = {}
        if user_input is not None:
            host = user_input[CONF_HOST]
            if await validate_input(self.hass, host):
                self.hass.config_entries.async_update_entry(self.config_entry, data={"host": host})
                await self.hass.config_entries.async_reload(self.config_entry.entry_id)
                return self.async_create_entry(title="", data=None)
            else:
                errors["base"] = "cannot_connect"

        data_schema = vol.Schema({vol.Required(CONF_HOST, default=self.config_entry.data.get(CONF_HOST)): str})
        return self.async_show_form(
            step_id="init",
            data_schema=data_schema,
            errors=errors,
        )