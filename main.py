#!/usr/bin/env python
import websocket
import ssl
import requests
import random

PROXY = True
PROXY_HOST = "127.0.0.1"
PROXY_PORT = 8080
PROXY_PROT = "http"

session = requests.session()
phase = 6107 # random.randint(3000, 9999)

session_url = "https://push.ls-tc.de:443/lightstreamer/create_session.js"
headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://www.ls-tc.de",
        "Referer": "https://www.ls-tc.de/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Te": "trailers",
        "Connection": "close"
}

session_data = {
        "LS_phase": phase,
        "LS_cause": "new.api",
        "LS_polling": "true",
        "LS_polling_millis": "0",
        "LS_idle_millis": "0",
        "LS_client_version": "6.1",
        "LS_adapter_set": "WALLSTREETONLINE",
        "LS_container": "lsc"
}

proxy_domain = f"{PROXY_PROT}://{PROXY_HOST}:{PROXY_PORT}"
proxies = {} if not PROXY else {"http":proxy_domain, "https":proxy_domain}
res = requests.post(session_url, headers=headers, data=session_data, proxies=proxies, verify=False)

content = res.text
session_key = content.split("('")[-1].split("'")[0]
# session_key = "asd"

print("== SESSION ==")
print(session_key)
print("== Start WS ==")

# websocket.enableTrace(True)

url = "wss://push.ls-tc.de:443/lightstreamer"
headers = {
        "Sec-WebSocket-Version": "13",
        "Sec-WebSocket-Protocol": "js.lightstreamer.com"
}

ws = websocket.create_connection(
        url,
        header=headers,
        origin="https://www.ls-tc.de",
        http_proxy_host=PROXY_HOST if PROXY else None,
        http_proxy_port=f"{PROXY_PORT}" if PROXY else None,
        proxy_type=PROXY_PROT if PROXY else None,
        sslopt={"cert_reqs": ssl.CERT_NONE}
)

p = f"bind_session\r\nLS_session={session_key}&LS_phase={phase}&LS_cause=loop1&LS_container=lsc&"
ws.send(p)
# p = f"control\r\nLS_mode=MERGE&LS_id=70595%401%2070586%401%2070580%401%2070577%401%20349938%401&LS_schema=mid%20midTime%20midPerf1d%20midPerf1dRel%20categoryId%20currencySymbol%20currencyISO&LS_data_adapter=QUOTE&LS_snapshot=false&LS_table=1&LS_req_phase=747&LS_win_phase=51&LS_op=add&LS_session={session_key}&"
# ws.send(p)
result =  ws.recv()
print("Received '%s'" % result)
ws.close()