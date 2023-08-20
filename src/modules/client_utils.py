import asyncio
from typing import List, Union, Optional

import requests
from loguru import logger


class Utils:
    def __init__(self):
        self.gid_temp: List[int] = []
        self.server_name: str = "ddf"

    async def get_gid(self) -> Union[int, bool]:
        """
        获取游戏 ID。
        如果 self.gid_temp 中的游戏 ID 超过 50 个，则删除最早的 45 个 ID。
        尝试从服务器获取最新的游戏 ID，如果获取失败且 self.gid_temp 不为空，则返回最后一个游戏 ID，
        否则返回 False。
        返回值:
            - 如果成功获取到游戏 ID，则返回游戏 ID（整数类型）
            - 如果获取失败且 self.gid_temp 不为空，则返回最后一个游戏 ID
            - 如果获取失败且 self.gid_temp 为空，则返回 False
        """
        if len(self.gid_temp) > 50:
            del self.gid_temp[0:45]
        try:
            data = await self.get_server_data("server")
            self.gid_temp.append(data["gameId"])
            return data["gameId"]
        except Exception as e:
            if self.gid_temp:
                return self.gid_temp[-1]
            else:
                return False

    @staticmethod
    async def get_server_data(mode: str = "all") -> Optional[Union[bool, dict]]:
        """
        获取服务器数据。

        根据传入的 mode 参数选择相应的 API 接口，向服务器发送请求并获取数据。

        参数:
            mode: 请求的模式，可选值包括 "total" 和 "server"（字符串类型）

        返回值:
            - 如果成功获取到服务器数据，则返回相应的数据（字典类型）
            - 如果获取失败，则返回 None
        """
        url_total = 'http://127.0.0.1:10086/Player/GetAllPlayerList'
        url_server = 'http://127.0.0.1:10086/Server/GetServerData'
        headers = {"Connection": "keep-alive"}
        timeout = 3
        try:
            if mode == "total":
                response = await asyncio.to_thread(requests.get, url_total, headers=headers, timeout=timeout)
                return response.json().get('data')
            elif mode == "server":
                response = await asyncio.to_thread(requests.get, url_server, headers=headers, timeout=timeout)
                return response.json().get('data')
        except:
            logger.warning("未获取数据，请检查服务器是否开启")
            return None
