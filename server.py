from fastapi import FastAPI,Request
import uvicorn
from pyppeteer import launch
from cookie import Cookies

app = FastAPI()
page = None

async def open_browser():
    """
    Open the browser obj and return the page_obj used to run the js code.
    The headless param is true. 
    It means you will not see a browser window is launched.
    You can modify this param to False.

    :return : Page
    :rtype  : pyppeteer.Page
    """
    browser = await launch({'headless': True, 'args': ['--disable-infobars', '--window-size=1920,1080', '--no-sandbox']})
    page = await browser.newPage()
    return page
    


@app.middleware("http")
async def launch_the_browser(request: Request, call_next):
    """
    Launch the browser before the request is handled by route.
    Page obj have to be the global object.
    Because it runs over the entire life of the server app.

    This is a middleware function.
    It will check if the page object already exists.
    If not , create a page
    """
    global page
    if not page:
        page = await open_browser()
    response = await call_next(request)
    return response


@app.get("/cookies")
async def root(id:str,password:str):
    """
    Use the Page to visit the shu_report URL.
    GET the user cookies for report.

    :param user_id      : user_id
    :type user_id       : str
    :param password     : password
    :type password      : str
    :return             : cookies of user
    :rtype              : dict
    """
    print(id,password)
    return await Cookies(uid=id,password=password,page=page).Read()

@app.get("/key")
async def get_sKey(pw:str):
    c = Cookies("",pw,page=page)
    await c.get_key_()
    return c.password


if __name__ == '__main__':
    # uvicorn.run("server:app", host="0.0.0.0", port=8989,reload=True)
    uvicorn.run(app, host="0.0.0.0", port=8989)
