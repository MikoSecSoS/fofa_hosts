import pickle

import requests

from bs4 import BeautifulSoup

ua = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"}

def fofa(url):
	ip = url.split("/")[-1]
	print(f"[Target] {ip}")
	req = requests.get(url, headers=ua, timeout=3)
	soup = BeautifulSoup(req.text, "lxml")
	componentInfo = soup.find("div", attrs={"class":"componentInfo"})
	if componentInfo == None: return None
	lists = componentInfo.find_all("div", attrs={"class":"lists"})
	if lists == None: return None
	datas = {"ip": ip, "data": []}
	for i in lists[1:]:
		print(i.text)
		datas["data"].append(i.text.split())
	if not datas["data"]: return None
	return datas

def save_to_file(filename, datas):
	print(f"[*] Save to file => {filename}")
	with open(filename, "w") as f:
		for data in datas:
			text = ""
			text += f"[IP] {data['ip']}"+"\n"
			text += "\n".join(["\t".join(i) for i in data["data"]])+"\n"
			text += "="*50+"\n"
			f.write(text)

def get_urls(address):
	# Good Code. hahaha
	return [ "https://fofa.so/hosts/"+address[:address.rfind(".")+1]+str(i) for i in tuple(map(lambda x: range(x[0],x[1]+1), [tuple(map(int, address.split(".")[-1].split("-")))]))[0]]

def main():
	urls = get_urls("127.0.0.1-255")
	datas = [fofa(url) for url in urls]
	datas = [i for i in datas if i != None]
	print(f"[*] Number of hosts => {len(datas)}")
	with open("datas.pkl", "wb") as file:
		pickle.dump(datas, file)
	save_to_file("output.txt", datas)
	
if __name__ == '__main__':
	main()