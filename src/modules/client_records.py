import asyncio
import json
import socket
import time
from queue import Queue
from typing import Optional

import chardet
from loguru import logger

# 检测文件编码
with open('./src/utils/weapon_dict.json', 'rb') as file:
    raw_data = file.read()
    encoding = chardet.detect(raw_data)['encoding']

# 读取JSON文件（使用检测到的编码）
with open('./src/utils/weapon_dict.json', 'r', encoding=encoding) as file:
    weapon_data = json.load(file)


class GameKillRecord:
    def __init__(self):
        self.server_ip = '127.0.0.1'
        self.server_port = 52002
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.bind((self.server_ip, self.server_port))
        self.kill_record_queue = Queue()
        self.server_name = "ddf1"

    async def kill_record_worker(self):
        """
        监听并处理游戏击杀记录的方法。

        该方法会一直循环监听客户端的数据，并根据接收到的数据进行处理。
        """
        while True:
            data, addr = self.client_socket.recvfrom(1024)
            kill = data.decode('utf-8')
            try:
                if kill.startswith('{'):
                    kill_data = json.loads(kill)
                    if kill_data['killer'] is None:
                        send_message = f"`{time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time()))}`服务器{self.server_name}玩家{kill_data['victim']['name']}由于意外事故自杀或被管理员击杀\n"
                        logger.info(send_message)
                    else:
                        send_message = f"`{time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time()))}`服务器{self.server_name}玩家`{kill_data['killer']['name']}`使用{self.translate_weapon(str(kill_data['killedBy']))}击杀`{kill_data['victim']['name']}`\n"
                        self.kill_record_queue.put(kill_data)
                        logger.info(send_message)
                    logger.info(kill_data)
            except Exception as e:
                logger.info(kill_data)
                logger.error(e)

    def start(self):
        """
        启动游戏击杀记录监听的方法。

        该方法会创建一个事件循环并运行 `kill_record_worker` 异步任务。
        """
        asyncio.ensure_future(self.kill_record_worker())

        loop = asyncio.get_event_loop()
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            loop.close()

    @staticmethod
    def translate_weapon(killed_by: str) -> Optional[str]:
        """
        根据被杀死的对象（killed_by）从 weapon_data 字典中获取对应的值。

        参数:
            killed_by: 被杀死的对象，用于查找 weapon_data 中的对应值

        返回值:
            - 如果找到对应的值，则返回 weapon_data[killed_by]（字符串类型）
            - 如果 weapon_data 中不存在对应的键，则记录错误日志并返回 None
        """
        try:
            return weapon_data[killed_by]
        except KeyError:
            logger.error(f"Invalid killedBy value: {killed_by}")
            return ""
