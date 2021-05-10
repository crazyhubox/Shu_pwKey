from pyppeteer import launch
import requests
import os

def get_key_path(key_file_name:str):
    pro_path = os.path.dirname(os.path.abspath(__file__))
    key_path = os.path.join(pro_path,key_file_name)
    return key_path

KEY_PATH = get_key_path("js/jiami.js")

class Cookies:

    def __init__(self,uid:str,password:str,page=None) -> None:
        self.page =  page
        self.username  = uid
        self.password = password
        
    def post_(self):
        data = {
            'username': self.username,
            'password': self.password
        }
        response = requests.post('https://newsso.shu.edu.cn/login/eyJ0aW1lc3RhbXAiOjE2MTg5OTUyNzg0ODkwMzA1MjYsInJlc3BvbnNlVHlwZSI6ImNvZGUiLCJjbGllbnRJZCI6IldVSFdmcm50bldZSFpmelE1UXZYVUNWeSIsInNjb3BlIjoiMSIsInJlZGlyZWN0VXJpIjoiaHR0cHM6Ly9zZWxmcmVwb3J0LnNodS5lZHUuY24vTG9naW5TU08uYXNweD9SZXR1cm5Vcmw9JTJmRGVmYXVsdC5hc3B4Iiwic3RhdGUiOiIifQ==', data=data)
        for each in response.history:
            for k, v in each.cookies.items():
                if k == '.ncov2019selfreport':
                    return f'{k}={v}'
        return None

    async def Read(self):
        await self.get_key_()
        if not isinstance(self.password,str) or len(self.password) < 20:
            return 'erropw'
        cookies = self.post_()
        if not cookies:
            return 'nocookie'
        return cookies

    @staticmethod
    def read_js(path) -> str:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()


    async def get_key_(self):
        key_js = self.read_js(KEY_PATH)
        key_js += f'\ntest("{self.password}")'

        key_value = await self.page.evaluate(key_js)
        self.password = key_value

    async def open_browser(self):
        """
        Open the browser obj

        :return : Page
        :rtype  : pyppeteer.Page
        """
        if self.page:
            return 
        browser = await launch({'headless': True, 'args': ['--disable-infobars', '--window-size=1920,1080', '--no-sandbox']})
        # 打开一个页面
        page = await browser.newPage()
        # await page.setViewport({'width': 1920, 'height': 1080})   # 设置页面的大小
        self.page = page
        return page

    async def test_single(self):
       
        print(self.password)
        page = await self.open_browser()
        password = await self.get_key_(page=page,password=self.password)
        data = {
            'username': self.username,
            'password': password
        }
        if not isinstance(password,str):
            return 
        return self.post_(data=data)

async def run():
    c = Cookies("","12131")
    page = await c.open_browser()
    c.page = page
    await c.get_key_()
    return c.password


if __name__ == '__main__':
    import asyncio
    res = asyncio.get_event_loop().run_until_complete(run())
    print(res)
