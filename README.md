# Shu_pwKey

![avatar](https://img.shields.io/badge/license-MIT-blue)
![avatar](https://img.shields.io/badge/pyppeteer-0.0.25-orange)
![avatar](https://img.shields.io/badge/fastapi-0.63.0-grenn)

- [Shu_pwKey](#shu_pwkey)
  - [目录结构](#%E7%9B%AE%E5%BD%95%E7%BB%93%E6%9E%84)
  - [说明](#%E8%AF%B4%E6%98%8E)
  - [最后](#%E6%9C%80%E5%90%8E)


上大登录的加密参数的生成

![image](https://github.com/crazyhubox/Shu_pwKey/blob/main/static/key.gif)

## 目录结构

```bash
.
├── LICENSE
├── README.md
├── goin            主执行shell脚本
├── key-server      运行server脚本
├── key-server-kill 关闭server以及以后善后处理的脚本
├── js
│   └── jiami.js    加密的js代码
├── cookie.py       获取cookie
└── server.py       服务的路由规定
```

## 说明

本项目所用依赖均是协程框架, 不熟悉协程编程模式的同学可以使用如下库替代实现.

```bash
pyppeteer ==> selenium

fastapi ==> flask
```

然后将读取的js放入selenium执行以达到同样的效果.

依赖安装

```bash
pip3 install pyppeteer  # 一个异步操作Chromium的框架
pip3 install fastapi    #一个巨快的异步服务器框架
pip3 install uvicorn    #巨快服务器框架的运行器
```

pyppeteer安装完成之后首次使用还需要安装chrome原核浏览器Chromium. 所以给一个试运行脚本,在pyppeteer库安装完成之后新建一个py文件尝试运行一下:

```python
import asyncio
from pyppeteer import launch

def pyppRun():
    async def main():
        # 使用launch方法调用浏览器，其参数可以传递关键字参数也可以传递字典。
        browser = await launch({'headless': False, 'args': ['--disable-infobars', '--window-size=1920,1080', '--no-sandbox']})
        # 打开一个页面
        page = await browser.newPage()
        await page.setViewport({'width': 1920, 'height': 1080})   # 设置页面的大小
        # 打开链接
        await page.goto('https://www.baidu.com') 

    asyncio.get_event_loop().run_until_complete(main())
    
if __name__ == "__main__":
    pyppRun()
```

如果成功运行浏览器并打开百度页面则安装成功.

先运行server.py然后根据路由规则进程访问测试

```bash
python3 -u server.py
curl 127.0.0.1:8989/key?pw=456 #如果是直接运行的的话
curl 127.0.0.1:8989/key\?pw\=456 #在命令行中可能需要转义
```

## 最后

为什么使用一个server来跑一个浏览器?

> 因为想法是需要一个浏览器对象,在后台就负责运行js代码, 不管是多进程还是多线程,实际程序中要与其通信开销和编程难度和可维护性都要差很多,这种起一个服务,并封装成rpc的使用,能够使得解密模块和真正的代码逻辑区分开来, 也能够使得调用和维护十分方便.

js代码是如何找到的?
> 这个要讲的话又要重新开一个仓库了...
