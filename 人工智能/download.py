import requests
base_url = "https://media.wanmen.org/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"
}
name_list = []
url_list = []
with open("mulu.txt","r",encoding="utf-8")as fp:
    for index,line in enumerate(fp):
        line = line.strip()
        if index % 2 == 0:
            name_list.append(line)
        else:
            url_list.append(base_url + line)
    datas = zip(name_list,url_list)


def download_data(data):
    name,url = data
    base_url,numbers = url.split("high")[0]+"high",int(url.split("high")[1].split(".")[0])+1
    with open(name, "wb") as fp:
        content = b""
        for number in range(numbers):
            url = base_url + str(number) + ".ts"
            print(url)
            content += download_content(url)
        fp.write(content)

def download_content(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content
    else:
        download_content(url)

for data in datas:
    print(data)
    download_data(data)
#
#
# copy_url = "15895432-cbd3-4eff-9e6c-002e090f6956_pc_high77.ts"
# number = 78
# prefix = copy_url.split("_")[0]
#
# with open(连续性.ts,"wb")as fp:
#     response = b""
#     for i in range(number):
#         print("正在下载第%s.ts"%i)
#         url = base_url+ prefix + "_pc_high" +"{}.ts".format(i)
#         response += requests.get(url,headers=headers).content
#
#     fp.write(response)