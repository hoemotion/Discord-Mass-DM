# don't forget to leave a star <3 https://github.com/hoemotion/discord-mass-dm
import os, sys, time, random, asyncio, json , logging, base64; from datetime import datetime; from typing import Dict, Tuple
from lib.scrape import scrape
from pathlib import Path
try:
    import psutil; from aiohttp import ClientSession; from tasksio import TaskPool; from rich.table import Table; from rich.console import Console; from rich.highlighter import ReprHighlighter
except ImportError:
    print("ImportError: 1st")
    os.system("pip3 install aiohttp")
    os.system("pip3 install tasksio")
    os.system("pip3 install psutil")
    os.system("pip3 install rich")
    import psutil; from tasksio import TaskPool; from aiohttp import ClientSession; from rich.table import Table; from rich.console import Console; from rich.highlighter import ReprHighlighter
try:
    import websocket
    import asyncio
except ImportError:
    print("ImportError: 2nd")
    os.system("pip3 install websocket-client")

logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;9m[\x1b[0m%(asctime)s\x1b[38;5;9m]\x1b[0m %(message)s\x1b[0m",
    datefmt="%H:%M:%S"
)


class Discord(object):

    def __init__(self):
        if os.name == 'nt':
            self.clear = lambda: os.system("cls")
        else:
            self.clear = lambda: os.system("clear")

        self.clear()
        self.tokens = []
        self.blacklisted_users = []
        self.users = []

        self.guild_name = None
        self.guild_id = None
        self.channel_id = None
        self.invite = None
        self.g = "\033[92m"
        self.red = "\x1b[38;5;9m"
        self.rst = "\x1b[0m"
        self.success = f"{self.g}[+]{self.rst} "
        self.err = f"{self.red}[{self.rst}!{self.red}]{self.rst} "
        self.opbracket = f"{self.red}({self.rst}"
        self.opbracket2 = f"{self.g}[{self.rst}"
        self.closebrckt = f"{self.red}){self.rst}"
        self.closebrckt2 = f"{self.g}]{self.rst}"
        self.question = "\x1b[38;5;9m[\x1b[0m?\x1b[38;5;9m]\x1b[0m "
        self.arrow = f" {self.red}->{self.rst} "
        with open("data/useragents.txt", encoding="utf-8") as f:
            self.useragents = [i.strip() for i in f]
        path = Path(__file__).parent / "./data/tokens.json"
        try:
            with path.open() as file:
                tkns = json.load(file)
                if len(tkns) == 0:
                    logging.info(f"{self.err} No tokens: Please insert your tokens {self.opbracket}tokens.json{self.closebrckt}")
                    sys.exit()
                for tkn in tkns:
                    self.tokens.append(tkn)
        except Exception:
            logging.info(f"{self.err} Exception: Please insert your tokens correctly in {self.opbracket}tokens.json{self.closebrckt}")
            sys.exit()

        try:
            with open("data/message.json", "r") as file:
                data = json.load(file)
            msg = data['content']
        except Exception:
            logging.info(
                f"{self.err} Please insert your message correctly in {self.opbracket}message.json{self.closebrckt}\nRead the wiki if you need examples")
            sys.exit()
        try:
            with open("data/config.json", "r") as file:
                config = json.load(file)
                for user in config["blacklisted_users"]:
                    self.blacklisted_users.append(str(user))
                self.send_embed = config["send_embed"]
                self.send_message = config["send_normal_message"]
                self.captcha_api_key = config["captcha_api_key"]
                self.captcha_submit_url = config["captcha_submit_url"]
                self.captcha_get_url = config["captcha_get_url"]
                self.discord_hcaptcha_id = "4c672d35-0701-42b2-88c3-78380b0db560"
                self.discord_captcha_referer = "https://discord.com/channels/@me"
                not_counter = 0
                if not self.send_embed:
                    not_counter += 1
                    self.embd = ""
                else:
                    logging.info(f"{self.g}[+]{self.rst} You can build your embed link at {self.red}https://embed.rauf.wtf/{self.rst},\nyou could also host your own html file so the url becomes shorter")
                    self.embd = input(f"{self.question}Embed Link{self.arrow}")
                    self.hide = input(f"{self.question}Should the Embed link be hidden? (This will increase the message lenght by 1k characters, but the link will be invisible)\n(y/n){self.arrow}")
                    if self.hide.lower() == "y":
                        self.embd = f"\n ||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||__ {self.embd}"
                    else:
                        self.embd = f"\n{self.embd}"
                if not self.send_message:
                    not_counter += 1
                    msg = ""
                if not_counter == 2:
                    logging.info(f"{self.err} You can\'t set send message and send embed to false {self.opbracket}config.json{self.closebrckt}.\nIf you do this you would try to send an empty message\nRead the wiki if you need help")
                    sys.exit()
        except Exception:
            logging.info(
                f"{self.err} Please insert the configuration stuff correctly {self.opbracket}config.json{self.closebrckt}.\nRead the wiki if you need help")
            sys.exit()
        with open("data/proxies.txt", encoding="utf-8") as f:
            self.proxies = [i.strip() for i in f]

        logging.info(
            f"{self.g}[+]{self.rst} Successfully loaded {self.red}%s{self.rst} token(s)\n" % (len(self.tokens)))
        self.mode = input(f"{self.question}Use Proxies? {self.opbracket}y/n{self.closebrckt}{self.arrow}")
        if self.mode.lower() == "y":
            self.use_proxies = True
            self.proxy_typee = input(f"{self.opbracket2}1{self.closebrckt2} http   | {self.opbracket2}2{self.closebrckt2} https\n{self.opbracket2}3{self.closebrckt2} socks4 | {self.opbracket2}4{self.closebrckt2} socks5\n{self.question}Proxy type{self.arrow}")
            if self.proxy_typee == "1":
                self.proxy_type = "http"
            elif self.proxy_typee == "2":
                self.proxy_type = "https"
            elif self.proxy_typee == "3":
                self.proxy_type = "socks4"
            elif self.proxy_typee == "4":
                self.proxy_type = "socks5"
            else: self.use_proxies = False
        else:
            self.use_proxies = False

        self.message = msg
        self.embed = self.embd
        try:
            self.delay = float(input(f"{self.question}Delay{self.arrow}"))
        except Exception:
            self.delay = 5
        try:
            self.ratelimit_delay = float(input(f"{self.question}Rate limit Delay{self.arrow}"))
        except Exception:
            self.ratelimit_delay = 300
        self.total_tokens = len(self.tokens)
        self.invalid_tokens_start = 0
        self.locked_tokens_start = 0
        self.locked_tokens_total = 0
        self.invalid_tokens_total = 0
        self.valid_tokens_start = 0
        self.valid_tokens_end = 0
        self.total_rate_limits = 0
        self.total_server_joins_success = 0
        self.total_server_joins_locked = 0
        self.total_server_joins_invalid = 0
        self.total_dms_success = 0
        self.total_dms_fail = 0
        self.invalid_token_dm = 0
        self.locked_token_dm = 0
        self.total_server_leave_success = 0
        self.total_server_leave_locked = 0
        self.total_server_leave_invalid = 0

        print()

    def stop(self):
        process = psutil.Process(os.getpid())
        process.terminate()

    def nonce(self):
        date = datetime.now()
        unixts = time.mktime(date.timetuple())
        return str((int(unixts) * 1000 - 1420070400000) * 4194304)

    # need to overwrite the whole json when updating, luckily the database won't be enormous
    def overwrite_json(self, content):
        self.json_db = open(f"data/token_profiles.json", "w")
        self.clean_json = json.dumps(content, indent=4, separators=(",", ": "))
        self.json_db.write(self.clean_json)
        self.json_db.close()
    def find_index_in_db(self, data_to_search, token_to_find):
        token_to_find = str(token_to_find)
        for i in range(len(data_to_search)):
            if data_to_search[i]["token"] == token_to_find:
                # token already exists in json file
                return int(i), "none"

        # in this case, the token isnt in the json file yet
        # so we automatically create him
        data_to_search.append({
            "token": str(token_to_find),
            "dcfduid": "none",
            "sdcfduid": "none",
            "fingerprint": "none",
            "super_property": "none",
            "user_agent": "none"
            # will overwrite all the "none" with needed things later
        })
        # now that the token profile is created, re-check and return int

        for i in range(len(data_to_search)):
            if data_to_search[i]["token"] == token_to_find:
                return i, data_to_search

    async def setup(self, token):
        if not os.path.exists("data/token_profiles.json"):
            creating_file = open(f"data/token_profiles.json", "w")
            creating_file.write("""{\n\t"tokens": []
}""")
            creating_file.close()

        token_profiles = open("data/token_profiles.json")
        json_content = json.load(token_profiles)
        token_index, new_data = self.find_index_in_db(json_content["tokens"], token)
        if new_data != "none":
            json_content["tokens"] = new_data
        json_token_content = json_content["tokens"][token_index]

        if json_token_content["dcfduid"] == "none":
            async with ClientSession() as client:
                async with client.get("https://discord.com/app") as response:
                    cookies = str(response.cookies)
                    dcfduid = cookies.split("dcfduid=")[1].split(";")[0]
                    sdcfduid = cookies.split("sdcfduid=")[1].split(";")[0]
                async with client.get("https://discordapp.com/api/v9/experiments") as finger:
                    jsonn = await finger.json()
                    fingerprint = jsonn["fingerprint"]
                # logging.info(f"{self.success}Obtained dcfduid cookie: {dcfduid}")
                # logging.info(f"{self.success}Obtained sdcfduid cookie: {sdcfduid}")
                # logging.info(f"{self.success}Obtained fingerprint: {fingerprint}")
                useragent = random.choice(self.useragents)
                if "Windows" in useragent:
                    device = "Windows"
                elif "Macintosh" in useragent:
                    device = "Mac OS X"
                elif "Linux" in useragent:
                    device = "Ubuntu"
                elif "iPad" in useragent:
                    device = "iPadOS"
                elif "iPhone" in useragent:
                    device = "iOS"
                elif "Android" in useragent:
                    device = "Android 11"
                elif "X11" in useragent:
                    device = "Unix"
                elif "iPod" in useragent:
                    device = "iOS"
                elif "PlayStation" in useragent:
                    device = "Orbis OS"
                else:
                    device = "hoeOS"

                decoded_superproperty = '{"os":"%s","browser":"Discord Client","release_channel":"stable","client_version":"0.0.264","os_version":"15.6.0","os_arch":"x64","system_locale":"en-US","client_build_number":108924,"client_event_source":null}' % (
                    device)
                message_bytes = decoded_superproperty.encode('ascii')
                base64_bytes = base64.b64encode(message_bytes)
                x_super_property = base64_bytes.decode('ascii')
                if json_token_content["dcfduid"] == "none":
                    json_token_content["dcfduid"] = dcfduid
                if json_token_content["sdcfduid"] == "none":
                    json_token_content["sdcfduid"] = sdcfduid
                if json_token_content["fingerprint"] == "none":
                    json_token_content["fingerprint"] = fingerprint
                if json_token_content["super_property"] == "none":
                    json_token_content["super_property"] = x_super_property
                if json_token_content["user_agent"] == "none":
                    json_token_content["user_agent"] = useragent
                json_content["tokens"][token_index] = json_token_content
                self.overwrite_json(json_content)

    async def headers(self, token):
        token_profiles = open("data/token_profiles.json")
        json_content = json.load(token_profiles)
        token_index, new_data = self.find_index_in_db(json_content["tokens"], token)
        if new_data != "none":
            json_content["tokens"] = new_data
        json_token_content = json_content["tokens"][token_index]
        useragent = json_token_content["user_agent"]
        x_super_property = json_token_content["super_property"]
        dcfduid = json_token_content["dcfduid"]
        sdcfduid = json_token_content["sdcfduid"]
        fingerprint = json_token_content["fingerprint"]

        return {
            "Authorization": token,
            "accept": "*/*",
            "accept-language": "en-US",
            "connection": "keep-alive",
            "cookie": "__dcfduid=%s; __sdcfduid=%s; locale=en-US" % (dcfduid, sdcfduid),
            "DNT": "1",
            "origin": "https://discord.com",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "referer": "https://discord.com/channels/@me",
            "TE": "Trailers",
            "User-Agent": useragent,
            "x-debug-options": "bugReporterEnabled",
            "x-fingerprint": fingerprint,
            "X-Super-Properties": x_super_property
        }
    async def submit_cap_key(self, proxy):
        url = self.captcha_submit_url
        querystring = {
            "key": self.captcha_api_key,
            "method": "hcaptcha",
            "sitekey": self.discord_hcaptcha_id,
            "pageurl": self.discord_captcha_referer
        }
        headers = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}
        async with ClientSession(headers=headers) as mass_dm_brrr:
            async with mass_dm_brrr.post(url, params=querystring, proxy=proxy) as response:
                text = await response.text()
                return text.split("|", 1)[1]

    async def get_discord_captcha(self, captcha_key_response, proxy):
        params = {"key": self.captcha_api_key, "action": "get", "id": captcha_key_response}
        async with ClientSession() as mass_dm_brrr:
            async with mass_dm_brrr.get(self.captcha_get_url, params=params, proxy=proxy) as response:
                text = await response.text()
                return text.split("|", 1)

    async def getCaptcha(self, proxy):
        captcha_step_one = await self.submit_cap_key(proxy)
        logging.info(f"Captcha step one = {captcha_step_one}")
        looping = True
        while looping:
            logging.info('Sleeping 10 seconds')
            await asyncio.sleep(10)
            captcha_step_two = await self.get_discord_captcha(captcha_step_one, proxy)
            try:
                if len(captcha_step_two[1]) > 60:
                    logging.info("Captcha done")
                    return captcha_step_two[1]
            except IndexError:
                logging.info("Captcha Not Found!")

    async def login(self, token: str, proxy: str):
        try:
            headers = await self.headers(token)
            async with ClientSession(headers=headers) as mass_dm_brrr:
                async with mass_dm_brrr.get("https://discord.com/api/v9/users/@me/library", proxy=proxy) as response:
                    try:
                        json = await response.json()
                        jsoncode = json["code"]
                        code = f"{self.opbracket}{jsoncode}{self.closebrckt} | "
                    except:
                        code = ""
                    if response.status == 200:
                        logging.info(
                            f"{self.success}Successfully logged in {code}{self.opbracket}%s{self.closebrckt}" % (token[:59]))
                        self.valid_tokens_start += 1
                    if response.status == 401:
                        logging.info(f"{self.err}Invalid account {code}{self.opbracket}%s{self.closebrckt}" % (token[:59]))
                        self.invalid_tokens_start += 1
                        self.tokens.remove(token)
                    if response.status == 403:
                        logging.info(f"{self.err}Locked account {code}{self.opbracket}%s{self.closebrckt}" % (token[:59]))
                        self.locked_tokens_start += 1
                        self.tokens.remove(token)
                    if response.status == 429:
                        logging.info(f"{self.err}Rate limited {code}{self.opbracket}%s{self.closebrckt}" % (token[:59]))
                        time.sleep(self.ratelimit_delay)
                        self.total_rate_limits += 1
                        await self.login(token, proxy)
        except Exception:
            await self.login(token, proxy)

    async def join(self, token: str, proxy: str):
        try:
            headers = await self.headers(token)
            async with ClientSession(headers=headers) as hoemotion:
                async with hoemotion.post("https://discord.com/api/v9/invites/%s" % (self.invite), json={}, proxy=proxy) as response:
                    json = await response.json()
                    if response.status == 200:
                        self.guild_name = json["guild"]["name"]
                        self.guild_id = json["guild"]["id"]
                        self.channel_id = json["channel"]["id"]
                        logging.info(f"{self.success}Successfully joined %s {self.opbracket}%s{self.closebrckt}" % (
                        self.guild_name[:20], token[:59]))
                        self.total_server_joins_success += 1
                    elif response.status == 401:
                        logging.info(f"{self.err}Invalid account {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                        self.tokens.remove(token)
                        self.total_server_joins_invalid += 1
                    elif response.status == 403:
                        logging.info(f"{self.err}Locked account {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                        self.total_server_joins_locked += 1
                        self.tokens.remove(token)
                    elif response.status == 429:
                        logging.info(f"{self.err}Rate limited {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                        self.total_rate_limits += 1
                        time.sleep(self.ratelimit_delay)
                        await self.join(token, proxy)
                    elif response.status == 404:
                        logging.info(f"{self.err}Server-Invite is invalid or has expired :/")
                        self.stop()
                    elif response.status == 400:
                        logging.info(f"Bad Request, trying to join with hcaptcha..\n({json})")
                        captcha_key = await self.getCaptcha(proxy)
                        async with ClientSession(headers=headers) as hcap_join:
                            async with hcap_join.post("https://discord.com/api/v9/invites/%s" % (self.invite), json={"captcha_key": captcha_key}, proxy=proxy) as response:
                                if response.status == 200:
                                    self.guild_name = json["guild"]["name"]
                                    self.guild_id = json["guild"]["id"]
                                    self.channel_id = json["channel"]["id"]
                                    logging.info(
                                        f"{self.success}Successfully joined %s by using hcap bypass {self.opbracket}%s{self.closebrckt}" % (
                                            self.guild_name[:20], token[:59]))
                                    self.total_server_joins_success += 1
                                elif response.status == 401:
                                    logging.info(
                                        f"{self.err}Invalid account {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                                    self.tokens.remove(token)
                                    self.total_server_joins_invalid += 1
                                elif response.status == 403:
                                    logging.info(
                                        f"{self.err}Locked account {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                                    self.total_server_joins_locked += 1
                                    self.tokens.remove(token)
                                elif response.status == 429:
                                    logging.info(
                                        f"{self.err}Rate limited {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                                    self.total_rate_limits += 1
                                    time.sleep(self.ratelimit_delay)
                                    await self.join(token, proxy)
                                elif response.status == 404:
                                    logging.info(f"{self.err}Server-Invite is invalid or has expired :/")
                                    self.stop()
                                else:
                                    self.tokens.remove(token)

                    else:
                        self.tokens.remove(token)
        except Exception:
            await self.join(token, proxy)

    async def create_dm(self, token: str, user: str, proxy: str):
        try:
            headers = await self.headers(token)
            async with ClientSession(headers=headers) as chupapi_munanyo:
                async with chupapi_munanyo.post("https://discord.com/api/v9/users/@me/channels",
                                                json={"recipients": [user]}, proxy=proxy) as response:
                    json = await response.json()
                    if response.status == 200:
                        logging.info(
                            f"{self.success}Successfully created direct message with %s {self.opbracket}%s{self.closebrckt}" % (
                            json["recipients"][0]["username"], token[:59]))
                        return json["id"]
                    elif response.status == 401:
                        logging.info(f"{self.err}Invalid account {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                        self.invalid_tokens_total += 1
                        self.tokens.remove(token)
                        return False
                    elif response.status == 403:
                        logging.info(
                            f"{self.err}Can\'t message user {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                        self.tokens.remove(token)
                    elif response.status == 429:
                        logging.info(f"{self.err}Rate limited {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                        self.total_rate_limits += 1
                        time.sleep(self.ratelimit_delay)
                        return await self.create_dm(token, user, proxy)
                    elif response.status == 400:
                        logging.info(
                            f"{self.err}Can\'t create DM with yourself! {self.opbracket}%s{self.closebrckt}" % (
                            token[:59]))
                    elif response.status == 404:
                        logging.info(
                            f"{self.err}User doesn\'t exist! {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                    else:
                        return False
        except Exception:
            return await self.create_dm(token, user, proxy)

    async def direct_message(self, token: str, channel: str, user, proxy: str):
        embed = self.embed
        message = self.get_user_in_message(user)
        headers = await self.headers(token)
        async with ClientSession(headers=headers) as virgin:
            async with virgin.post("https://discord.com/api/v9/channels/%s/messages" % (channel),
                                   json={"content": f"{message}{embed}", "nonce": self.nonce(),
                                         "tts": False}, proxy=proxy) as response:
                json = await response.json()
                if response.status == 200:
                    logging.info(f"{self.success}Successfully sent message {self.opbracket}%s{self.red}){self.rst}" % (
                    token[:59]))
                    self.total_dms_success += 1
                elif response.status == 401:
                    logging.info(f"{self.err}Invalid account {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                    self.tokens.remove(token)
                    self.invalid_tokens_total += 1
                    self.invalid_token_dm += 1
                    return False
                elif response.status == 403 and json["code"] == 40003:
                    logging.info(f"{self.err}Rate limited {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                    time.sleep(self.ratelimit_delay)
                    self.total_rate_limits += 1
                    await self.direct_message(token, channel, user, proxy)
                elif response.status == 403 and json["code"] == 50007:
                    logging.info(f"{self.err}User has direct messages disabled {self.opbracket}%s{self.closebrckt}" % (
                    token[:59]))
                    self.total_dms_fail += 1
                elif response.status == 403 and json["code"] == 40002:
                    logging.info(f"{self.err}Locked {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                    self.locked_token_dm += 1
                    self.locked_tokens_total += 1
                    self.tokens.remove(token)
                    return False
                elif response.status == 429:
                    logging.info(f"{self.err}Rate limited {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                    time.sleep(self.ratelimit_delay)
                    self.total_rate_limits += 1
                    await self.direct_message(token, channel, user, proxy)
                elif response.status == 400:
                    self.total_dms_fail += 1
                    code = json["code"]
                    logging.info(f"{self.err}Can\'t DM this User! {self.opbracket}{code}{self.closebrckt} | {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                elif response.status == 404:
                    logging.info(f"{self.err}User doesn\'t exist! {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                else:
                    return False

    def get_user_in_message(self, user: str = None):
        mssage = self.message
        message = mssage.replace("<user>", f"<@{user}>")
        return message



    async def send(self, token: str, user: str, proxy: str):
        channel = await self.create_dm(token, user, proxy)
        if channel == False:
            return await self.send(random.choice(self.tokens), user, proxy)
        response = await self.direct_message(token, channel, user, proxy)
        if response == False:
            return await self.send(random.choice(self.tokens), user, proxy)

    async def leave(self, token: str, proxy: str):
        try:
            headers = await self.headers(token)
            async with ClientSession(headers=headers) as client:
                async with client.delete(f"https://discord.com/api/v9/users/@me/guilds/{self.guild_id}",
                                         json={"lurking": False}, proxy=proxy) as response:
                    json = await response.json()
                    message = json["message"]
                    code = json["code"]
                    if response.status == 200:
                        logging.info(
                            f"{self.success}Successfully left the Guild {self.opbracket}%s{self.closebrckt}" % (
                            token[:59]))
                        self.total_server_leave_success += 1
                    elif response.status == 204:
                        logging.info(
                            f"{self.success}Successfully left the Guild {self.opbracket}%s{self.closebrckt}" % (
                            token[:59]))
                        self.total_server_leave_success += 1
                    elif response.status == 404:
                        logging.info(
                            f"{self.success}Successfully left the Guild {self.opbracket}%s{self.closebrckt}" % (
                            token[:59]))
                        self.total_server_leave_success += 1
                    elif response.status == 403:
                        self.total_server_leave_locked += 1
                        logging.info(f"{self.err}{message} | {code} {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                    elif response.status == 401:
                        self.total_server_leave_invalid += 1
                        self.locked_tokens_total += 1
                        logging.info(f"{self.err}{message} | {code} {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                    elif response.status == 429:
                        self.total_rate_limits += 1
                        logging.info(f"{self.err}{message} | {code} {self.opbracket}%s{self.closebrckt}" % (token[:59]))
                        time.sleep(self.ratelimit_delay)
                        await self.leave(token, proxy)
                    else:
                        logging.info(
                            f"{self.err}{response.status} | {message} | {code} | {self.opbracket}%s{self.closebrckt}" % (
                            token[:59]))

        except Exception:
            await self.leave(token, proxy)

    async def start(self, first_start):
        if len(self.tokens) == 0:
            logging.info("No tokens loaded.")
            time.sleep(5)
            sys.exit()

        def table():

            table = Table(
                title=f"Total Users Scraped: {len(self.users)}",
                caption="github.com/hoemotion",
                caption_justify="right",
                caption_style="bright_yellow"
            )

            table.add_column("Tokens", header_style="bright_cyan", style="blue", no_wrap=True)
            table.add_column("Login Details", header_style="bright_magenta", style="magenta", justify="center")
            table.add_column("Join Details", justify="center", header_style="light_green", style="bright_green")
            table.add_column("DM Users", justify="center", header_style="magenta", style="blue")
            table.add_column("Leave Details", justify="center", header_style="bright_cyan", style="bright_green")

            table.add_row(
                f"[Total] Tokens: {self.total_tokens}",
                f"[Login] Valid Tokens: {self.valid_tokens_start}",
                f"[Join] Valid Tokens: {self.total_server_joins_success}",
                f"[DM] Total DMed: {self.total_dms_success}\n[DM] Total Failed: {self.total_dms_fail}",
                f"[Leave] Tokens Left Successfully: {self.total_server_leave_success}",
                style="on black",
                end_section=True,
            )
            table.add_row(
                f"[Total] Tokens Invalid: {self.invalid_tokens_total}",
                f"[Login] Tokens Invalid: {self.invalid_tokens_start}",
                f"[Join] Tokens Invalid: {self.total_server_joins_invalid}",
                f"[DM] Tokens Invalid: {self.invalid_token_dm}",
                f"[Leave] Tokens Invalid: {self.total_server_leave_invalid}",
                style="on black",
                end_section=True,
            )
            table.add_row(
                f"[Total] Tokens Locked: {self.locked_tokens_total}",
                f"[Login] Tokens Locked: {self.locked_tokens_start}",
                f"[Join] Tokens Locked: {self.total_server_joins_locked}",
                f"[DM] Tokens Locked: {self.locked_token_dm}",
                f"[Leave] Tokens Locked: {self.total_server_leave_locked}",
                style="on black",
                end_section=True,
            )

            def header(text: str) -> None:
                console.print()
                console.rule(highlight(text))
                console.print()

            console = Console()
            highlight = ReprHighlighter()

            table.width = None
            table.expand = False
            table.row_styles = ["dim", "none"]
            table.show_lines = True
            table.leading = 0
            header("MassDM analytics")
            console.print(table, justify="center")
            return

        if first_start == "true":
            print()
            logging.info(
                "Setting up the token_profiles.json file..\nThis might take a while depending on the amount of your tokens.")
            print()

            async with TaskPool(1_000) as pool:
                for token in self.tokens:
                    if len(self.tokens) != 0:
                        await pool.put(self.setup(token))
                    else:
                        self.stop()

            if len(self.tokens) == 0:
                self.stop()

        async def check_tokens():
            async with TaskPool(1_000) as pool:
                for token in self.tokens:
                    if len(self.tokens) != 0:
                        if self.use_proxies:
                            proxy = "%s://%s" % (self.proxy_type, random.choice(self.proxies))
                        else:
                            proxy = None
                        await pool.put(self.login(token, proxy))
                    else:
                        self.stop()

            if len(self.tokens) == 0:
                self.stop()
            return "success"

        async def join_server():
            self.invite = input(f"{self.question}Invite{self.arrow}discord.gg/").replace("/", "").replace("discord.com",
                                                                                                          "").replace(
                "discord.gg", "").replace("invite", "").replace("https:", "").replace("http:", "").replace(
                "discordapp.com", "")
            print()
            logging.info("Joining server.")
            print()

            async with TaskPool(1_000) as pool:
                for token in self.tokens:
                    if len(self.tokens) != 0:
                        if self.use_proxies:
                            proxy = "%s://%s" % (self.proxy_type, random.choice(self.proxies))
                        else:
                            proxy = None
                        await pool.put(self.join(token, proxy))
                        if self.delay != 0: await asyncio.sleep(self.delay)
                    else:
                        self.stop()

            if len(self.tokens) == 0:
                self.stop()
            return "success"

        async def scrape_users():
            self.guild_id = input(f"{self.question}Enter Guild ID{self.arrow}")
            self.channel_id = input(f"{self.question}Enter Channel ID{self.arrow}")
            self.invite = input(f"{self.question}Invite{self.arrow}discord.gg/").replace("/", "").replace("discord.com",
                                                                                                          "").replace(
                "discord.gg", "").replace("invite", "").replace("https:", "").replace("http:", "").replace(
                "discordapp.com", "")
            try:
                headers = await self.headers(self.tokens[0])
                async with ClientSession(headers=headers) as hoemotion:
                    async with hoemotion.get("https://discord.com/api/v9/invites/%s?with_counts=true&with_expiration=true" % (self.invite), json={}) as response:
                        json = await response.json()
                        if response.status == 200:
                            self.guild_name = json["guild"]["name"]
                        else:
                            self.tokens.remove(token)
                            self.guild_name = "Unknown Guild"
            except:
                self.guild_name = "Unknown Guild"


            print()
            logging.info("Scraping Users from %s...\nPlease be patient" % self.guild_name)
            print()

            members = scrape(self.tokens[0], self.guild_id, self.channel_id)
            with open('data/users.txt', 'w') as t:
                data = ''
                for member in members:
                    if member not in self.users:
                        self.users.append(member)
                        data += member + '\n'
                t.write(data)

            print()
            logging.info(f"Successfully scraped {self.red}%s{self.rst} members" % (len(self.users)))
            print()

            if len(self.tokens) == 0: self.stop()
            return "success"

        async def mass_dm():
            with open("data/users.txt", encoding="utf-8") as f:
                self.users = [i.strip() for i in f]
            logging.info("Sending messages to %s users." % (len(self.users)))
            async with TaskPool(1_000) as pool:
                for user in self.users:
                    if len(self.tokens) != 0:
                        if str(user) not in self.blacklisted_users:
                            if self.use_proxies:
                                proxy = "%s://%s" % (self.proxy_type, random.choice(self.proxies))
                            else:
                                proxy = None
                            await pool.put(self.send(random.choice(self.tokens), user, proxy))
                            if self.delay != 0: await asyncio.sleep(self.delay)
                        else:
                            logging.info(f"{self.err}Blacklisted User: {self.red}%s{self.rst}" % (user))
                    else:
                        table()
                        self.stop()
                return "success"

        async def leave_guild():
            self.guild_id = input(f"{self.question} Enter Guild ID{self.arrow}")

            logging.info("Leaving %s" % self.guild_id)
            print()
            async with TaskPool(1_000) as pool:
                if len(self.tokens) != 0:
                    for token in self.tokens:
                        if self.use_proxies:
                            proxy = "%s://%s" % (self.proxy_type, random.choice(self.proxies))
                        else:
                            proxy = None
                        await pool.put(self.leave(token, proxy))
                        if self.delay != 0:
                            await asyncio.sleep(self.delay)
                    logging.info("All Tasks are done")
                    table()
                    self.stop()
                else:
                    table()
                    self.stop()
            return "success"
        print(f"""
{self.opbracket2}1{self.closebrckt2} Join Server
{self.opbracket2}2{self.closebrckt2} Leave Server
{self.opbracket2}3{self.closebrckt2} Scrape Users
{self.opbracket2}4{self.closebrckt2} Mass DM
{self.opbracket2}5{self.closebrckt2} Check tokens
{self.opbracket2}6{self.closebrckt2} Exit""")
        list = ["1", "2", "3", "4", "5", "6"]
        choose = input(f"{self.question} Please Enter your option{self.arrow}")
        while choose not in list:
            choose = input(f"{self.question} Please Enter your option{self.arrow}")
        if choose == "1":
            lol = await join_server()
            if lol == "success":
                return await self.start(first_start="false")
        elif choose == "2":
            lol = await leave_guild()
            if lol == "success":
                return await self.start(first_start="false")
        elif choose == "3":
            lol = await scrape_users()
            if lol == "success":
                return await self.start(first_start="false")
        elif choose == "4":
            lol = await mass_dm()
            if lol == "success":
                return await self.start(first_start="false")
        elif choose == "5":
            lol = await check_tokens()
            if lol == "success":
                return await self.start(first_start="false")
        elif choose == "6":
            logging.info("Byee!")
            table()
            self.stop()

if __name__ == "__main__":
    client = Discord()
    asyncio.get_event_loop().run_until_complete(client.start(first_start="true"))
