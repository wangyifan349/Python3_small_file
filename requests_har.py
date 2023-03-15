import json
import requests
with open('get_web_har.har', 'r') as f:
    har_data = json.load(f)
entries = har_data['log']['entries']
for entry in entries:
    if entry['request']['method'] == 'GET':#处理get请求的，post可能由于某些原因已经用不了了。
        url = entry['request']['url']
        headers = entry['request']['headers']
        response = requests.get(url, headers=headers)
        print(response.content)
    else:
      pass
