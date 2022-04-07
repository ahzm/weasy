import requests

url = "http://localhost:8080/transformation/vbpmn/transform/pif2bpmn"

payload={}

files=[
		('file1',('filename.pif',open('C:/directory/filename.pif','rb').read(),'application/octet-stream'))
]
headers = {
		'Connection': 'keep-alive',
		'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="91", "Chromium";v="91"',
		'Accept': '*/*',
		'X-Requested-With': 'XMLHttpRequest',
		'sec-ch-ua-mobile': '?0',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.41',
		'Origin': 'http://localhost:8080',
		'Sec-Fetch-Site': 'same-origin',
		'Sec-Fetch-Mode': 'cors',
		'Sec-Fetch-Dest': 'empty',
		'Referer': 'http://localhost:8080/transformation/transform.html',
		'Accept-Language': 'es-419,es;q=0.9,es-ES;q=0.8,en;q=0.7,en-GB;q=0.6,en-US;q=0.5,fr;q=0.4,de;q=0.3'
}

response = requests.post(url, headers=headers, files=files)

print(response.text)
