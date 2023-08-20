from src.modules.client_records import GameKillRecord
import asyncio


async def main():
    game_kill_record = GameKillRecord()
    game_kill_record.start()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
