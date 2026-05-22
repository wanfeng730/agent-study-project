import requests

# Get请求
url1 = 'https://www.tanzy.cloud/icms/normative_file/list_file_tree'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36',
    'Accept': 'application/json',
    'Content-Type': 'application/json',

    'Ic_re_token': '？？？'
}
params = {

}
response = requests.get(url=url1, params=params, headers=headers)
res_content = response.json()
print(f"request get url1 status: {res_content['message']}");




# Post请求
url2 = 'https://www.tanzy.cloud/icms/department/list_department'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36',
    'Accept': 'application/json',
    'Content-Type': 'application/json',

    'Ic_re_token': '？？？'
}
data = {
    "filterList": [
        {
            "fieldName": "ic_enterprise_id",
            "fieldType": "long",
            "operate": 5,
            "value": "1001074397883000205"
        }
    ],
    "pageInfo": {
        "currentPage": 1,
        "pageSize": 20
    },
    "sortList": [
        {
            "fieldName": "create_date",
            "sortType": "desc"
        }
    ]
}
response = requests.post(url=url2, headers=headers, data=data);
res_content = response.json()
print(f"request post url2 status: {res_content['message']}");





# 文件上传
url3 = 'https://www.tanzy.cloud/icms/normative_file/upload_file'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36',
    'Accept': 'application/json',
    # 不要在任何包含文件上传的请求中手动设置 Content-Type，让 requests 自动处理。

    'Ic_re_token': '？？？'
}
params = {
    "parentId": "1051074397884015126"
}
# 使用with...as 自动关闭文件
with open('resources/RMRB-20240126.pdf', 'rb') as file1:
    files = {
        'multipartFile': file1
        # "multipartFile": ("自定义文件名.pdf", open("report.pdf", "rb"), "application/pdf")
    }
    response = requests.post(url3, headers=headers, params=params, files=files);
    res_content = response.json()
    print(f"request post url3 status: {res_content['message']}");


