"""
Integrated Langchain Tool-Based Agent
Combines file operations, database operations, and mathematical calculations
Uses ChatOllama with create_agent for proper tool binding
"""

from typing import List, Dict, Any, Optional
from langchain.agents import create_agent as langchain_create_agent
# from langchain.agents import create_tool_calling_agent, AgentExecutor
# from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import Tool
import logging
from datetime import datetime
from langchain_openai import AzureChatOpenAI
from agent_registry import AgentRegistry
from agent_card import AgentCard

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
# Import tools from other modules
from tools.navigation_tools import (
    get_navigation_status,
    get_current_location,
    set_navigation_destination,
    cancel_navigation,
    update_current_location
)

from file_operations import (
    read_file_tool, write_file_tool, append_file_tool, list_files_tool,
    delete_file_tool, copy_file_tool, read_json_tool, write_json_tool
)
from database_operations import (
    create_table_tool, insert_record_tool, insert_records_tool,
    query_database_tool, update_database_tool, get_table_schema_tool,
    list_tables_tool, delete_records_tool, drop_table_tool
)
from math_operations import (
    add_tool, subtract_tool, multiply_tool, divide_tool, power_tool,
    square_root_tool, absolute_tool, average_tool, sum_tool, min_tool,
    max_tool, factorial_tool, gcd_tool, lcm_tool, percentage_tool,
    median_tool, standard_deviation_tool, variance_tool, round_tool
)

from tools.ambient_status import (
    get_ambient_light_status, set_ambient_light_power
)

from tools.audio_tools import (
    get_eq_band_value, get_touch_sound_status, get_audio_settings,
    set_eq_band_value, set_touch_sound, set_eq_presets
)

from tools.bluetooth_tools import (
    get_bluetooth_status, get_paired_devices, get_bt_music_availability,
    set_bluetooth_power, set_pair_device, set_disconnect_device
)

from tools.camera_tools import (
    get_camera_status, get_camera_view,
    set_camera_power, set_camera_view
)

from tools.climate_tools import (
    get_temperature, get_fan_speed, get_vent_mode, get_hvac_status,
    set_temperature, set_fan_speed, set_vent_mode,
    set_hvac_power, set_hvac_auto_mode, set_fan_power
)

from tools.display_tools import (
    get_screen_status,  
    get_brightness,
    get_theme_mode,
    set_screen_power,
    set_brightness,
    set_theme_mode
)

from tools.contacts_tools import (
    get_contacts_list, get_contact_image_status, set_contact_image_display
)

from tools.media_tools import (
    get_volume, get_media_status, get_sources, set_volume, set_mute,
    set_media_power, set_media_play, set_source
)

from tools.local_media_tools import (
    get_media_source, get_radio_frequency, get_favorite_station,
    get_preset_station, set_media_source, set_radio_frequency,
    set_favorite_station, set_preset_station
)

from tools.notification_tools import (
    get_notification_status, get_notification_count, get_notification_settings,
    set_notifications_enable, set_message_notifications
)

from tools.phone_tools import (
    get_phone_pairing_status, get_call_history, set_phone_redial, set_phone_call
)

from tools.screensaver_tools import (
     get_screensaver_status, get_screensaver_availability, set_screensaver_activate
)

from tools.usb_tools import (
    get_usb_connection_status, get_usb_music_availability, get_usb_sync_status, set_usb_sync, set_usb_eject
)

from tools.system_tools import (
    get_system_error_status, get_da3_source_availability, set_system_reset, set_system_diagnostics
)

from router.tool_router import route_request

class SubAgent:
    def __init__(self, llm, tools, name, registry=None):
        self.name = name
        self.llm = llm
        self.tools = tools
        self.registry = registry

        self.executor = langchain_create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=f"""
You are {name} Agent.

Rules:
- Handle ONLY your domain
- NEVER mention limitations
- NEVER say "I can't"
- If another domain is needed → delegate silently
- Always return final result
"""     )

    def run(self, query, depth=0):
        print(f"\n🧠 {self.name} Agent processing: {query}")

        # 🔴 Prevent infinite loops
        if depth > 2:
            return {
                "success": True,
                "output": f"{self.name} handled partial request (depth limit reached)"
            }

        q = query.lower()

        # =========================
        # 🧭 NAVIGATION AGENT
        # =========================
        if self.name == "Navigation":

            nav_output = ""

            if "navigate" in q or "destination" in q:
                result = self.executor.invoke(
                    {"messages": [{"role": "user", "content": query}]}
                )
                nav_output = self._extract_output(result)

            # Delegate ONLY media task
            if any(word in q for word in ["volume", "music", "play"]):
                print("➡️ NavigationAgent delegating media task")

                media_res = self.registry.get("media").send(
                    "increase volume"
                )

                return {
                    "success": True,
                    "output": f"{nav_output}\n{media_res['output']}".strip()
                }

            return {
                "success": True,
                "output": nav_output
            }

        # =========================
        # 🔊 MEDIA AGENT
        # =========================
        if self.name == "Media":

            media_output = ""

            if any(word in q for word in ["volume", "music", "play"]):
                result = self.executor.invoke(
                    {"messages": [{"role": "user", "content": query}]}
                )
                media_output = self._extract_output(result)

            # Delegate ONLY navigation task
            if "navigate" in q or "destination" in q:
                print("➡️ MediaAgent delegating navigation task")

                nav_res = self.registry.get("navigation").send(
                    "navigate to destination"
                )

                return {
                    "success": True,
                    "output": f"{media_output}\n{nav_res['output']}".strip()
                }

            return {
                "success": True,
                "output": media_output
            }

        # =========================
        # 📞 COMMUNICATION AGENT
        # =========================
        if self.name == "Communication":
            result = self.executor.invoke(
                {"messages": [{"role": "user", "content": query}]}
            )

            return {
                "success": True,
                "output": self._extract_output(result)
            }

        # =========================
        # 🔄 DEFAULT FALLBACK
        # =========================
        result = self.executor.invoke(
            {"messages": [{"role": "user", "content": query}]}
        )

        return {
            "success": True,
            "output": self._extract_output(result)
        }

    def _extract_output(self, result):
        messages = result.get("messages", [])

        for m in reversed(messages):
            content = getattr(m, "content", "")
            if content and content.strip():
                return content

        return "No response"

class LangchainToolAgent:
    """
    Integrated Langchain agent with file operations, database operations,
    and mathematical calculations tools.
    Always uses LLM with tools (no tools-only mode).
    """
    def __init__(self, llm, verbose: bool = True):
        """
        Initialize the agent with LLM and setup A2A architecture

        Args:
            llm: Language model to use
            verbose: Enable verbose logging and show full conversation
        """
        if llm is None:
            raise ValueError("LLM is required. Please provide a valid LLM instance.")

        self.llm = llm
        self.verbose = verbose

        # =========================
        # STEP 1: Initialize ALL tools (existing system)
        # =========================
        self.tools = self._initialize_tools()

        # =========================
        # STEP 2: Create base executor (fallback agent)
        # =========================
        self.executor = None
        self._create_agent_with_tools()

        # =========================
        # STEP 3: Group tools by domain
        # =========================
        self.tool_groups = self._group_tools()

        # =========================
        # STEP 4: Create Agent Registry (NEW - A2A)
        # =========================
        from agent_registry import AgentRegistry
        from agent_card import AgentCard

        self.registry = AgentRegistry()

        # =========================
        # STEP 5: Create Sub-Agents WITH registry (IMPORTANT)
        # =========================
        self.navigation_agent = SubAgent(
            self.llm,
            self.tool_groups["navigation"],
            "Navigation",
            self.registry
        )

        self.media_agent = SubAgent(
            self.llm,
            self.tool_groups["media"],
            "Media",
            self.registry
        )

        self.communication_agent = SubAgent(
            self.llm,
            self.tool_groups["communication"],
            "Communication",
            self.registry
        )

        # =========================
        # STEP 6: Register agents using AgentCard (A2A communication layer)
        # =========================
        self.registry.register("navigation", AgentCard("Navigation", self.navigation_agent))
        self.registry.register("media", AgentCard("Media", self.media_agent))
        self.registry.register("communication", AgentCard("Communication", self.communication_agent))

        # =========================
        # STEP 7: Store sub-agents
        # =========================
        self.sub_agents = {
            "navigation": self.navigation_agent,
            "media": self.media_agent,
            "communication": self.communication_agent
        }

        # =========================
        # LOGGING
        # =========================
        logger.info(f"✓ LangchainToolAgent initialized with {len(self.tools)} tools")
        logger.info(f"✓ Sub-agents initialized: {list(self.sub_agents.keys())}")
        logger.info("✓ A2A Agent Registry initialized")
            
       
    def _group_tools(self):
        return {
            "navigation": [
                get_navigation_status,
                get_current_location,
                set_navigation_destination,
                cancel_navigation,
                update_current_location
            ],
            "media": [
                get_volume,
                set_volume,
                set_media_play,
                set_media_power
            ],
            "communication": [
                get_contacts_list,
                set_phone_call
            ],
            "system": self.tools  # fallback → ALL tools
        }


    def _initialize_tools(self) -> List[Tool]:
        """Initialize all available tools"""
        tools = [
            # File operation tools
            read_file_tool,
            write_file_tool,
            append_file_tool,
            list_files_tool,
            delete_file_tool,
            copy_file_tool,
            read_json_tool,
            write_json_tool,
            
            # Database operation tools
            create_table_tool,
            insert_record_tool,
            insert_records_tool,
            query_database_tool,
            update_database_tool,
            get_table_schema_tool,
            list_tables_tool,
            delete_records_tool,
            drop_table_tool,
            
            # Mathematical calculation tools
            add_tool,
            subtract_tool,
            multiply_tool,
            divide_tool,
            power_tool,
            square_root_tool,
            absolute_tool,
            average_tool,
            sum_tool,
            min_tool,
            max_tool,
            factorial_tool,
            gcd_tool,
            lcm_tool,
            percentage_tool,
            median_tool,
            standard_deviation_tool,
            variance_tool,
            round_tool,

          # Ambient status tools
            get_ambient_light_status,   
            set_ambient_light_power,

            # Audio tools
            get_eq_band_value,
            get_touch_sound_status,
            get_audio_settings,
            set_eq_band_value,
            set_touch_sound,
            set_eq_presets,

            # Bluetooth tools
            get_bluetooth_status,
            get_paired_devices,
            get_bt_music_availability,
            set_bluetooth_power,
            set_pair_device,
            set_disconnect_device,

            # Camera tools
            get_camera_status,
            get_camera_view,
            set_camera_power,
            set_camera_view,

            # Climate tools
            get_temperature,
            get_fan_speed,
            get_vent_mode,
            get_hvac_status,
            set_temperature,
            set_fan_speed,
            set_vent_mode,
            set_hvac_power,
            set_hvac_auto_mode,
            set_fan_power,

            # Contact tools
            get_contacts_list,
            get_contact_image_status,
            set_contact_image_display,
 
            # Display tools
            get_screen_status,
            get_brightness,
            get_theme_mode,
            set_screen_power,
            set_brightness,
            set_theme_mode,

            # Media tools
            get_volume,
            get_media_status,
            get_sources,    
            set_volume,
            set_mute,
            set_media_power,
            set_media_play,
            set_source, 

            # Local media tools
            get_media_source,   
            get_radio_frequency,
            get_favorite_station,
            get_preset_station,
            set_media_source,
            set_radio_frequency,
            set_favorite_station,
            set_preset_station,

            # Notification tools
            get_notification_status,
            get_notification_count,
            get_notification_settings,
            set_notifications_enable,
            set_message_notifications,

            # Phone tools
            get_phone_pairing_status,
            get_call_history,
            set_phone_redial,
            set_phone_call,

            # Screensaver tools
            get_screensaver_status,
            get_screensaver_availability,
            set_screensaver_activate,

            # USB tools 
            get_usb_connection_status,
            get_usb_music_availability,
            get_usb_sync_status,
            set_usb_sync,
            set_usb_eject,

            # System tools
            get_system_error_status,
            get_da3_source_availability,
            set_system_reset,
            set_system_diagnostics,

            # Navigation tools
            get_navigation_status,
            get_current_location,
            set_navigation_destination,
            cancel_navigation,
            update_current_location,
        ]
        
        logger.info(f"Initialized {len(tools)} tools")
        return tools
    
    

    def _create_agent_with_tools(self):
        """Create agent with proper tool binding using langchain's create_agent"""
        try:
            # create_agent takes 'model' (not 'llm'), 'tools', and optional 'system_prompt'
            # self.executor = langchain_create_agent(
            #     model=self.llm,
            #     tools=self.tools,
            #     system_prompt="You are a helpful assistant. Use the available tools to help the user."
            # )
            

            self.executor = langchain_create_agent(
                 model=self.llm,
                tools=self.tools,
                 system_prompt="""
You are a vehicle infotainment assistant.

You MUST always use a tool to answer device-related questions.

Never answer from your own knowledge.

If the user asks about:
- ambient light
- bluetooth
- media
- display
- audio
- climate
- phone
- usb
- notifications
- contacts
- camera
-navigation

you MUST call the corresponding tool.

Examples:

User: what is the ambient light status
Tool: get_ambient_light_status

User: turn on bluetooth
Tool: set_bluetooth_power

Rules:
- Status questions → use get_* tools
- Action questions → use set_* tools
- Never ask clarification for known systems
- Never answer without calling a tool
"""
)

            logger.info("✓ Agent created successfully with tools")
        except Exception as e:
            logger.error(f"✗ Agent creation failed: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def _setup_agent(self):
        """Setup the agent with LLM if available (deprecated - use _create_agent_with_tools)"""
        self._create_agent_with_tools()
    
    def get_tools_info(self) -> Dict[str, List[str]]:
        """Get information about available tools grouped by category"""
        tools_info = {
            "file_operations": [
                "read_file", "write_file", "append_file", "list_files", "delete_file", "copy_file", "read_json", "write_json"
            ],
            "database_operations": [
                "create_table", "insert_record", "insert_records", "query_database", "update_database", "get_table_schema", "list_tables", "delete_records", "drop_table"
            ],
            "math_operations": [
                "add", "subtract", "multiply", "divide", "power", "square_root", "absolute", "average", "sum", "min", "max", "factorial", "gcd", "lcm", "percentage", "median", "standard_deviation", "variance", "round"
            ],
            "ambient_status": [
                "get_ambient_light_status", "set_ambient_light_power"
            ],
            "audio_tools": [
                "get_eq_band_value", "get_touch_sound_status", "get_audio_settings", "set_eq_band_value", "set_touch_sound", "set_eq_presets"
            ],
            "bluetooth_tools": [
                "get_bluetooth_status", "get_paired_devices", "get_bt_music_availability", "set_bluetooth_power", "set_pair_device", "set_disconnect_device"
            ],
            "camera_tools": [
                "get_camera_status", "get_camera_view", "set_camera_power", "set_camera_view"
            ],
            "climate_tools": [
                "get_temperature", "get_fan_speed", "get_vent_mode", "get_hvac_status", "set_temperature", "set_fan_speed", "set_vent_mode", "set_hvac_power", "set_hvac_auto_mode", "set_fan_power"
            ],
            "contacts_tools": [
                "get_contacts_list", "get_contact_image_status", "set_contact_image_display"
            ],
            "display_tools": [
                "get_screen_status", "get_brightness", "get_theme_mode", "set_screen_power", "set_brightness", "set_theme_mode"
            ],
            "media_tools": [
                "get_volume", "get_media_status", "get_sources", "set_volume", "set_mute", "set_media_power", "set_media_play", "set_source"
            ],
            "local_media_tools": [
                "get_media_source", "get_radio_frequency", "get_favorite_station", "get_preset_station", "set_media_source", "set_radio_frequency", "set_favorite_station", "set_preset_station"
            ],
            "notification_tools": [
                "get_notification_status", "get_notification_count", "get_notification_settings", "set_notifications_enable", "set_message_notifications"
            ],
            "phone_tools": [
                "get_phone_pairing_status", "get_call_history", "set_phone_redial", "set_phone_call"
            ],
            "screensaver_tools": [
                "get_screensaver_status", "get_screensaver_availability", "set_screensaver_activate"
            ],
            "usb_tools": [
                "get_usb_connection_status", "get_usb_music_availability", "get_usb_sync_status", "set_usb_sync", "set_usb_eject"
            ],
            "system_tools": [
                "get_system_error_status", "get_da3_source_availability", "set_system_reset", "set_system_diagnostics"
            ],
            "navigation_tools": [
                "get_navigation_status",
                "get_current_location",
                "set_navigation_destination",
                "cancel_navigation",
                "update_current_location"
            ]
            
                
            
        }
        return tools_info
    
    def print_tools_info(self):
        """Print information about all available tools"""
        tools_info = self.get_tools_info()
        print("\n" + "="*60)
        print("AVAILABLE TOOLS")
        print("="*60)
        for category, tool_list in tools_info.items():
            print(f"\n{category.upper()}:")
            for i, tool_name in enumerate(tool_list, 1):
                print(f"  {i}. {tool_name}")
        print("\n" + "="*60)
    
    def run(self, input_text: str) -> Dict[str, Any]:
        try:
            print("\n🚀 MAIN AGENT RECEIVED:", input_text)

            query = input_text.lower()

            # =========================
            # STEP 1: CHOOSE PRIMARY AGENT (IMPORTANT)
            # =========================
            if any(word in query for word in ["navigate", "route", "destination", "eta", "go to"]):
                primary_agent = self.sub_agents["navigation"]

            elif any(word in query for word in ["volume", "music", "play", "song", "audio"]):
                primary_agent = self.sub_agents["media"]

            elif any(word in query for word in ["call", "contact", "phone"]):
                primary_agent = self.sub_agents["communication"]

            else:
                # fallback to base executor
                print("⚠️ No intent detected → using fallback agent")

                res = self.executor.invoke(
                    {"messages": [{"role": "user", "content": input_text}]}
                )

                messages = res.get("messages", [])
                output = ""

                for m in reversed(messages):
                    content = getattr(m, "content", "")
                    if content and content.strip():
                        output = content
                        break

                return {
                    "success": True,
                    "output": output,
                    "timestamp": datetime.now().isoformat()
                }

            print(f"🎯 Routing to {primary_agent.name} Agent")

            # =========================
            # STEP 2: SINGLE AGENT EXECUTION (A2A ENTRY POINT)
            # =========================
            response = primary_agent.run(input_text)

            # =========================
            # STEP 3: RETURN FINAL OUTPUT
            # =========================
            return {
                "success": True,
                "output": response["output"],
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error running agent: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            
        def execute_task(self, task_type: str, **kwargs) -> Dict[str, Any]:
            """Deprecated: Use natural language requests instead. This method is no longer supported."""
            raise NotImplementedError(
                "execute_task() is deprecated. Please use natural language requests with run() method instead.\n"
                "Example: agent.run('Create a table called users with id and name columns')"
            )


def create_agent(llm) -> LangchainToolAgent:
    """
    Factory function to create and setup a Langchain tool agent
    
    Args:
        llm: Language model instance (ChatOllama required)
        
    Returns:
        Configured LangchainToolAgent instance
    """
    if llm is None:
        raise ValueError("LLM is required. Please provide a ChatOllama instance.")
    return LangchainToolAgent(llm=llm, verbose=True)


if __name__ == "__main__":
    # Example: Create an agent with ChatOllama and run it
    import os

    print("Initializing Langchain Tool Agent with Model Farm...")

    llm = AzureChatOpenAI(
        azure_endpoint="https://aoai-farm.bosch-temp.com/api",
        api_key=os.getenv("MODEL_FARM_API_KEY"),
        api_version="2025-04-01-preview",
        deployment_name="gpt-5-nano-2025-08-07",
        temperature=1
    )
    
    agent = create_agent(llm=llm)
    
    # Example request
    result = agent.run("Create a table called users with columns: id INTEGER PRIMARY KEY, name TEXT, email TEXT")
    print(result)
    print(f"\nFinal result: {result['output']}")



