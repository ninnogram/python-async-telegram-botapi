import requests, json, aiohttp, asyncio, sys
class ninnobotapi:
    #StartPolling function
    def startPolling(self):
        loop = asyncio.get_event_loop()
        try:
            f = loop.run_until_complete(self.Polling())
        except KeyboardInterrupt:
            print("Bye")
            sys.exit()
    async def webRequest(self, url=False, data=[], r='json', type="get"):
        if url != False:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.request(type, url, data=data) as resp:
                        if r == 'json':
                            data = await resp.json()
                        else:
                            data = await resp
                        return data
            except Exception as e:
                print(e)
                return False


    #ASYNC Api Requests
    async def apiRequest(self, method='getme', params=[]):
        url = '{}/bot{}/{}'.format(self.endpoint, self.token, method)
        #Init aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.request('post', url, data=params) as resp:
                data = await resp.json()
        if data["ok"] == False:
            raise Exception({"error_code":data["error_code"], "description":data["description"]})
            return
        return data["result"]

    #Methods
    def __getattr__(self, method):
        async def function(**kwargs):
            #Polling method
            if method.lower == "webrequest":
                return
            if method == "Polling":
                if self.handler != None:
                    update_id = 0
                    while True:
                        funct = self.handler
                        try:
                            update = await self.getUpdates(offset=update_id)
                            if len(update) > 0:
                                update_id = update[0]['update_id'] + 1
                                loop = asyncio.get_event_loop()
                                asyncio.ensure_future(funct(update[0]))
                        except Exception as e:
                            raise Exception(e)


            if 'reply_markup' in kwargs:
                kwargs['reply_markup'] = json.dumps(kwargs['reply_markup'])
            if 'results' in kwargs:
                kwargs['results'] = json.dumps(kwargs['results'])
            if 'mask_position' in kwargs:
                kwargs['mask_position'] = json.dumps(kwargs['mask_position'])
            if 'shipping_options' in kwargs:
                kwargs['shipping_options'] = json.dumps(kwargs['shipping_options'])
            return (await self.apiRequest(method, kwargs))
        return function
    #Init
    def __init__(self, token = None, endpoint = "https://api.telegram.org", handler_function=None, startup_info=False):
        self.token = token
        self.endpoint = endpoint
        self.handler = handler_function
        try:
            loop = asyncio.get_event_loop()
            bot_info = loop.run_until_complete(self.apiRequest('getMe', []))
            self.bot_info = bot_info
            print(f"Welcome back!\n\nBot name: {bot_info['first_name']}\nBot username: @{bot_info['username']}\nBot ID: {bot_info['id']}")
        except:
            raise Exception("Invalid token")

