import warnings

from ctparse import ctparse
from langchain_community.utilities.openweathermap import OpenWeatherMapAPIWrapper
from langchain_core.tools import Tool, tool

warnings.filterwarnings("ignore")

from pydantic import Field
from langchain import SerpAPIWrapper

search_wrapper = SerpAPIWrapper()

search_tool = Tool.from_function(
    func=search_wrapper.run,
    name="Search",
    description="用于搜索引擎从互联网所搜信息"
)


@tool("UserLocation")
def mocked_location_tool(foo: str) -> str:
    """用于获取用户当前位置(城市、区域)"""
    return "XinWu Distric, WuXi, CN"


# @tool("Calendar")
# def calendar_tool(
# 		date_exp: str = Field(
# 			description="Date expression to be parsed. It must be in English."
# 		),
# ) -> str:
# 	"""用于查询和计算日期/时间"""
# 	res = ctparse(date_exp)
# 	date = res.resolution
# 	return date.dt.strftime("%c")

weather = OpenWeatherMapAPIWrapper(openweathermap_api_key="c43b03a241a2a5a6ebf0fee47c82eccd")
weather_tool = Tool.from_function(
    func=weather.run,
    name="Weather",
    description="用于获取一个城市的天气信息, 城市需要以英文输入",
)
