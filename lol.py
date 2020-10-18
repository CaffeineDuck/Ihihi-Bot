from mee6_py_api.api import API
import asyncio
from pprint import pprint

class TestClass:
    def __init__(self):
        self.mee6API = API(766213304141086731)

    async def run_tests(self):
        await self.test_get_leaderboard_page()
        

    async def test_get_leaderboard_page(self):
        leaderboard_page = await self.mee6API.levels.get_leaderboard_page()
        pprint(leaderboard_page)



def lol():
    if __name__ == "__main__":
        __spec__ = 'None'
        testClass = TestClass()
        loop = asyncio.get_event()
        asyncio.ensure_future(testClass.run_tests())