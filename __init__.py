"""这是一个示例天气查询插件

提供指定城市的天气查询功能。
使用 wttr.in API 获取天气数据。
"""

from typing import Dict

import httpx
from nekro_agent.api.schemas import AgentCtx
from nekro_agent.core import logger
from nekro_agent.services.plugin.base import ConfigBase, NekroPlugin, SandboxMethodType
from pydantic import Field

# TODO: 插件元信息，请修改为你的插件信息
plugin = NekroPlugin(
    name="天气查询插件",  # TODO: 插件名称
    module_name="weather",  # TODO: 插件模块名 (如果要发布该插件，需要在 NekroAI 社区中唯一)
    description="提供指定城市的天气查询功能",  # TODO: 插件描述
    version="1.0.0",  # TODO: 插件版本
    author="KroMiose",  # TODO: 插件作者
    url="https://github.com/KroMiose/nekro-plugin-template",  # TODO: 插件仓库地址
)


# TODO: 插件配置，根据需要修改
@plugin.mount_config()
class WeatherConfig(ConfigBase):
    """天气查询配置"""

    API_URL: str = Field(
        default="https://wttr.in/",
        title="天气API地址",
        description="天气查询API的基础URL",
    )
    TIMEOUT: int = Field(
        default=10,
        title="请求超时时间",
        description="API请求的超时时间(秒)",
    )


# 获取配置实例
config: WeatherConfig = plugin.get_config(WeatherConfig)


@plugin.mount_sandbox_method(SandboxMethodType.AGENT, name="查询天气", description="查询指定城市的实时天气信息")
async def query_weather(_ctx: AgentCtx, city: str) -> str:
    """查询指定城市的实时天气信息。

    Args:
        city: 需要查询天气的城市名称，例如 "北京", "London"。

    Returns:
        str: 包含城市实时天气信息的字符串。查询失败时返回错误信息。

    Example:
        查询北京的天气:
        query_weather(city="北京")
        查询伦敦的天气:
        query_weather(city="London")
    """
    try:
        async with httpx.AsyncClient(timeout=config.TIMEOUT) as client:
            response = await client.get(f"{config.API_URL}{city}?format=j1")
            response.raise_for_status()
            data: Dict = response.json()

        # 提取需要的天气信息
        # wttr.in 的 JSON 结构可能包含 current_condition 列表
        if not data.get("current_condition"):
            logger.warning(f"城市 '{city}' 的天气数据格式不符合预期，缺少 'current_condition'")
            return f"未能获取到城市 '{city}' 的有效天气数据，请检查城市名称是否正确。"

        # 处理获取到的天气数据
        current_condition = data["current_condition"][0]
        temp_c = current_condition.get("temp_C")
        feels_like_c = current_condition.get("FeelsLikeC")
        humidity = current_condition.get("humidity")
        weather_desc_list = current_condition.get("weatherDesc", [])
        weather_desc = weather_desc_list[0].get("value") if weather_desc_list else "未知"
        wind_speed_kmph = current_condition.get("windspeedKmph")
        wind_dir = current_condition.get("winddir16Point")
        visibility = current_condition.get("visibility")
        pressure = current_condition.get("pressure")

        # 格式化返回结果
        result = (
            f"城市: {city}\n"
            f"天气状况: {weather_desc}\n"
            f"温度: {temp_c}°C\n"
            f"体感温度: {feels_like_c}°C\n"
            f"湿度: {humidity}%\n"
            f"风向: {wind_dir}\n"
            f"风速: {wind_speed_kmph} km/h\n"
            f"能见度: {visibility} km\n"
            f"气压: {pressure} hPa"
        )
        logger.info(f"已查询到城市 '{city}' 的天气")
    except Exception as e:
        # 捕获其他所有未知异常
        logger.exception(f"查询城市 '{city}' 天气时发生未知错误: {e}")
        return f"查询 '{city}' 天气时发生内部错误。"
    else:
        return result


@plugin.mount_cleanup_method()
async def clean_up():
    """清理插件资源"""
    # 如果有使用数据库连接、文件句柄或其他需要释放的资源，在此处添加清理逻辑
    logger.info("天气查询插件资源已清理。")
