import requests  # 用于发送HTTP请求
from bs4 import BeautifulSoup  # 用于解析HTML页面
import re  # 提供正则表达式工具，用于字符串处理
from tqdm import trange  # 提供进度条显示工具
import pandas as pd  # 用于数据操作和数据存储
import emoji  # 用于处理表情符号
from concurrent.futures import ThreadPoolExecutor  # 提供多线程并发功能

# 关键字，作为搜索内容
keyword = "呃錢"

# 初始化数据存储的列表
source_name = []  # 用于存储来源名称
keywords = []  # 用于存储搜索关键字
titles = []  # 用于存储文章标题
hrefs = []  # 用于存储文章链接
dates = []  # 用于存储文章发布时间
forums = []  # 用于存储论坛名称
authors = []  # 用于存储作者名称
nums = []  # 用于存储回复数量
lastposts = []  # 用于存储最后回复时间
main_contents = []  # 用于存储主要内容
other_contents = []  # 用于存储其他内容

# 爬取单个页面数据的函数
def crawl(index):
    url = "https://www.discuss.com.hk/search.php"  # 网站的搜索地址
    headers = {
        # 模拟浏览器请求头，防止被网站拦截
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
            # 网站验证身份所需的Cookie
            "Cookie":"nwtc=673029814a77f2.46438575; AB_18=B; AB_28=B; AB_29=A; AB_34=B; AB_61=A; AB_full=18-B_28-B_29-A_34-B_61-A; _sharedID=2524da7c-ff11-4907-87fe-c4b2ba8f6879; _sharedID_cst=zix7LPQsHA%3D%3D; panoramaId_expiry=1731814405886; _cc_id=6dfee4817b4724f1493b46db7b2343ee; panoramaId=378486a93210b83b9240d70655e1185ca02c0ce78b8487187a662e6eb6970dc2; _fbp=fb.2.1731209608224.498112152823542569; _ga=GA1.3.1621706410.1731209609; cookieconsent_status=dismiss; _pubcid=bc546050-fc42-45b7-9565-c1446bceb6fa; _pubcid_cst=zix7LPQsHA%3D%3D; iUUID=49a15111e5ee1c8e323eea2587846779; iUUID=49a15111e5ee1c8e323eea2587846779; freq.5e661e8b47e7043d03000003=1; freq.5f462d2c47e7044a01000002=1; freq.65279e2647e7041906000000=1; innity.dmp.cks.innity=1; jiyakeji_uuid=1dd8adb0-9f34-11ef-86a0-617a6ac604bb; trc_cookie_storage=taboola%2520global%253Auser-id%3Dcd596afa-e135-48d7-a2dd-4684574aa0d5-tucte29af08; _pbjs_userid_consent_data=6683316680106290; pbjs-unifiedid=%7B%22TDID%22%3A%22e61ca476-0d48-41dd-ad21-27203b899a18%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222024-10-10T07%3A20%3A02%22%7D; id5_storage=%7B%22signature%22%3A%22ID5_AsuwqdXEwbc4dDxkJUWbe3cgc7QaP28PpQ5SrRd5ZSaJkmIAzp5L45mcRSng-0YCjewohXZ9dBSpe74cDJUphhoKpo0ach9pjfYTokLBqBoZOwp3tIqhOQIdoUzqL_KdCj7IunE_m7d4uIQ_Jw72gwzusrrYHrzZF5aocgaszDinDVK1wCg%22%2C%22created_at%22%3A%222024-11-10T03%3A33%3A29.889Z%22%2C%22id5_consent%22%3Atrue%2C%22original_uid%22%3A%22ID5*QaHv7Ch3TwIVnjiGHd0JNFDuGJGGXHUWmCVpW6zj2DXXUjUnZ_UbUHIpVXCL3eYO%22%2C%22universal_uid%22%3A%22ID5*uSEdsdMS5KzRWMZ8xrjLYTCn8iiURzVJWOUTauImybDXUu5d97W9QMmD9tbUC3OD%22%2C%22link_type%22%3A2%2C%22cascade_needed%22%3Afalse%2C%22privacy%22%3A%7B%22jurisdiction%22%3A%22other%22%2C%22id5_consent%22%3Atrue%7D%2C%22ext%22%3A%7B%22linkType%22%3A2%2C%22pba%22%3A%22x5Auy3CHlnkMf9NJrpuFt7WDIPzjyLCDerF9yHFMck0%3D%22%7D%2C%22cache_control%22%3A%7B%22max_age_sec%22%3A7200%7D%7D; mission_menu_popup_status=true; connectId=%7B%22vmuid%22%3A%22-DSaKA55F04H2JwpIvo-SekwOO-mvQjjGyFeoQFiqdbuJIyNImrliSX6SRDPIZLv02mgJrAeZ_-njcA9UG18lw%22%2C%22connectid%22%3A%22-DSaKA55F04H2JwpIvo-SekwOO-mvQjjGyFeoQFiqdbuJIyNImrliSX6SRDPIZLv02mgJrAeZ_-njcA9UG18lw%22%2C%22connectId%22%3A%22-DSaKA55F04H2JwpIvo-SekwOO-mvQjjGyFeoQFiqdbuJIyNImrliSX6SRDPIZLv02mgJrAeZ_-njcA9UG18lw%22%2C%22ttl%22%3A86400000%2C%22he%22%3A%2236d9f1ddee3f64b3c341791fc24f3b9a6de2cef95b7a40cb264ea8b2606f759a%22%2C%22lastSynced%22%3A1731249660508%2C%22lastUsed%22%3A1731249660508%7D; _lr_geo_location=HK; _lr_env_src_ats=true; _clck=19mungt%7C2%7Cfqs%7C0%7C1775; cf_clearance=h6YUMdJzxcU1Edn_LMQcZ4eThPDzXIzqi_V8paMCWLc-1731290851-1.2.1.1-1DVxUqpiIwPAIUi8GrpOd42CU5H_LkZelfw7N2svj2aps6Cxf7qjsfpXQL3zp2shbbxyzhe7nQG2Ap0B1DMvAetmq0TJP9UkFcuxfA9.eCJulgsE8zIiDoSsjo1Y3jfE_n2hyzRcmiwFi8CAY0Enp009jj1GMYHRVxIm2nwidrJQu.9vvDVnaaTUQbb2EDT.ReFasKQ8GdfiyvGeffrX1yfgkapZUxWN3Iry1LbZryzeNC.mAQDzDtuAphQMmnVVlRrpe9ARwPwDV3eGDvIIDBeR9f5BUoVbFqGCVtiWkZHnYYDpq3VfHmp5bXjGSDq5QP3hFgCmunNGsMYhd.zdEBI0i34EC9owACoG4yDJLn4EARdE1v_6VG9mUV1im10G4OaQ5IaJc1sna6zQy8G.eP6dOKWenKXbKGHIms3hMG0B_uWRO6ePAzahsc2KmbkU; mission_unread=1; _lr_env=eyJ0aW1lc3RhbXAiOjE3MzEyOTE3NzYwNjYsInZlcnNpb24iOiIxLjYuMCIsImVudmVsb3BlIjoiQXRuclZ3NU5JX0ZIZDVsZkNyRGFhaWMtZ1pqb3p1U1NXUHh6bWFYUzloWEJLU09RTGJMMmVUeGROd0lNQjhXeHo4dXF1RG9qTW9KQjVNWjJQUWdTM1hBdHZKTUQwN29Bei1KRnBad3BvVTNCMi1SRHI4cGJRNVVMS1puQzloS3VDQ3dyUC1VN295NVJuaTlJYVhPY09TXzF5Vi00Q1lmR1VHTTlkLUhRLUZGTXRSWTd1dmt5ekRTdHF6MGtiZWxpQlZRbUg4dk0iLCJjcmVhdGlvblRpbWVzdGFtcCI6MTczMTI0OTY2MTE1MX0%3D; _lr_pairId=eyJ0aW1lc3RhbXAiOjE3MzEyOTE3NzYwNjYsInZlcnNpb24iOiIxLjYuMCIsImVudmVsb3BlIjpbIkFuS3pacW5SY0FVaHJxaWxvVG1KUTlOR0J1MVpJWnhZemhDUjRDbDRiamVHIl0sImNyZWF0aW9uVGltZXN0YW1wIjoxNzMxMjQ5NjYxMTUyfQ%3D%3D; OX_plg=wmp|pm; __qca=I0-623181819-1731291805284; cdb_fb_referer=https%3A%2F%2Fwww.discuss.com.hk%2Fsearch.php%3Fsearchsubmit%3Dtrue%26srchtxt%3DScam%26orderby%3Dmost_relevant%26tr_h%3DTOPKNcT5BOO%26page%3D3; cdb_auth=CYjRrt53WeLLBRTxa0CHZrKbRd0Krrzsrl0CbFc9cCtYXpdjqTP829k; nwu=7366378; ui_uid_up=hpS0/i14IluXT2n6WBDefA==; cf_chl_rc_i=2; cdb_sid=WxO02b; dfp_seg_ids=%5B%5D; _lr_sampling_rate=100; cto_bidid=yRLx2l9EWGt3QUZpTlF3UmNhaWJDSWMzbHFORkx3ZzM3Q2YxT0R2NU1laE5RVkhEJTJCV1NxWGQlMkZRTGlyJTJCVm5ENWZkS2NxYVpCNVJWdjM1RVprcWZLU1FrOXBZSjJKaWd4NjlTd0twMjdLaXhSeU9TYlZCQTlmUGFBRWFTVEVZemU1U243VA; cto_bundle=a4Vfz19McW8zRlFEdlRJOXd1clhHYkY5Wkx4VW5XMkhrSUVBNXhGOG1pUGxIc29YYVhld3BMJTJGbGRIREFXYyUyRiUyQkVjZndyYlFVRkZIUldUZ3gzbVV2ZiUyQnU5JTJGayUyRmdTVkh3TzREUFVzejE4RHZLTzlTdVVsYTRTbm9zWVFWakR1dEJBQnBnY3lPbTRPZmZRQ1lTYkJoZ3VqbTluc2clM0QlM0Q; innity.dmp.1.sess.id=212359249.1.1731298202177; cdb_oldtopics=D26322428D26377302D20739641D22539267D29174177D31175633D31475869D31557367D31513198D31459015D31517794D31516978D31686861D31749284D31544984D; cdb_urihistory=29174177-1%3B31175633-1%3B22539267-1%3B20739641-1%3B26377302-1%3B26322428-1%3B; cdb_urihistorycount=6; goowifq=1; screen_skin=true; up_c=1731299294; __gads=ID=82ef443055ee2664:T=1731209607:RT=1731299293:S=ALNI_MaeTTHFUcMG0wDFcG6vMPZSAFK0Aw; __gpi=UID=00000f89fa298557:T=1731209607:RT=1731299293:S=ALNI_MaUIlQaKBvYex9Ys5VMx2bun0JmtA; __eoi=ID=50d95f7d6e4955cf:T=1731209607:RT=1731299293:S=AA-AfjYWczKtF9ABydQ4759gXbAP; FCNEC=%5B%5B%22AKsRol-HgD7X81IjI2MjJx7kovpzWx-8xrjZG-MYzlnQGCUXwF58HuXz9__14u4rtykQtWxUTpCGH_OBxQMFyuiKNQbM94H15ZasU5SNMwn9CzMAevV1MC_o5TbhtfQfjfLbxyLE2Hu0H5Wgg-JaZLl1z-YJIinHSA%3D%3D%22%5D%5D; innityfq=1; innity.dmp.1.sess=5.1731298202177.1731299416484.1731299416576; curr_hostname=www.discuss.com.hk; def_crw=eyJpdiI6IitNVUFRRVpldTNvMHN1dDJLS01aeUE9PSIsInZhbHVlIjoiRldFRUcrOU5FV050VjFKblI2MW9rTXVpK0o3cmI3NVwvcjFNcEgyMGdhdkg4Yk1aUm51N0FJSmkyM3ppWnZIXC9QRkhSSEdEMjFzdTEzV1wvdldnYkRhRTNcL0dUVFwvQlVZR2hMVlV6MGd1VzJkdjRXTnQzWlhmamNvMWYzNnRpc1k3cTU3VWszMUdQT3g1ZFgwMkJKNVJzRUpSZVFoNnlcL1BhQnB6QlRaVXZPK0lEVW8zSGZwSXF0a3BzVTYrQnVoVm1UMytBOFNxajVuR1Q4WWs4SnVxRjNHVEc5ekV3Uk9lR1o4a1JIcktZc3pqST0iLCJtYWMiOiI5ODZhN2VhNTA4YjQ3NTlhOWI3MTdmZjczZDBjZTU4NGQ5YmFmZTZhZmNiYzAwZjRiYWI3YjhiNjg3MjRiNDZiIn0%3D; amvdofq=2; px1fq=1; ttd-web=1731299425; innity-web=1731299425; verizon-web=1731299425; _ga_8P52FKWN6G=GS1.3.1731290844.5.1.1731299426.0.0.0; cto_bundle=8l8Ze18yZzlLTkElMkZsc05saG9MZE5UcElabGlUbDRkVHBxQjN4TVF4cmxuUFhQQnp5V1Jzc2ZwRTZiQTcyb0oxQlFTNyUyRkMwSWh6ZVNLbyUyQkdvJTJCUTI5dUVXV3o3M1NZWGlJdnQxOSUyRjFNT3QzRWtrNEVhVUJ1MiUyRmhNelJVOVU2bEZ6ZmtaZXVzWVJVeSUyRk9BOFFxOE5tN0l5azglMkJnJTNEJTNE; cto_bundle=8l8Ze18yZzlLTkElMkZsc05saG9MZE5UcElabGlUbDRkVHBxQjN4TVF4cmxuUFhQQnp5V1Jzc2ZwRTZiQTcyb0oxQlFTNyUyRkMwSWh6ZVNLbyUyQkdvJTJCUTI5dUVXV3o3M1NZWGlJdnQxOSUyRjFNT3QzRWtrNEVhVUJ1MiUyRmhNelJVOVU2bEZ6ZmtaZXVzWVJVeSUyRk9BOFFxOE5tN0l5azglMkJnJTNEJTNE; _clsk=1kqpv15%7C1731299427720%7C73%7C1%7Cn.clarity.ms%2Fcollect; _clsk=1kqpv15%7C1731299427720%7C73%7C1%7Cn.clarity.ms%2Fcollect; cdb_lastrequest=X%2FRSNtfW%2F%2F%2FnlAJao%2BU1esxE; viewthread_history=22539267%7C26377302%7C26377302%7C26377302%7C26377302%7C20739641%7C31175633%7C29174177%7C31175633%7C31475869%7C31475869%7C31475869%7C31516978%7C31516978%7C31557367%7C31557367%7C31516978%7C31557367%7C31557367%7C31513198%7C31513198%7C31459015%7C31459015%7C31517794%7C31517794%7C31686861%7C31686861%7C31749284%7C31749284%7C31749284%7C31749284%7C31544984%7C31544984%7C31544984%7C31544984%7C31544984%7C31131094%7C31131094%7C31749070%7C31749070%7C29841369%7C28249281%7C28249281%7C30163347%7C29841369%7C31175633; vidcrunchfq=1",
            "Referer":"https://www.discuss.com.hk/search.php?searchsubmit=true&srchtxt=%E6%AC%BA%E9%A8%99&orderby=most_relevant&tr_h=NTR8UEgWu2a&page=1"  # 来源页面
            }
    params = {
            'searchsubmit': 'true',  # 搜索提交标志
            'srchtxt': f'{keyword}', # 搜索的关键词
            'orderby': 'most_relevant', # 排序规则，按相关性排序
            'tr_h': 'NTR8UEgWu2a',  # 网站特定参数
            'page': index # 当前爬取的页码
        }

    # 发起HTTP GET请求
    r = requests.get(url,headers=headers,params=params)
    r.encoding="utf-8"  # 将响应编码设置为UTF-8
    print(r.status_code)
    soup = BeautifulSoup(r.text,"html.parser")  # 使用BeautifulSoup解析HTML

#查找文章列表
    div = soup.find("div", class_="search-result__results")  # 定位到搜索结果列表的 HTML 元素，指定类名为 "search-result__results"
    tds_subject = div.find_all("td", class_="search-result-subject-box")  # 查找所有带有 "search-result-subject-box" 类的单元格，表示帖子主题
    tds_forum = div.find_all("td", class_="search-result-forum")  # 查找所有带有 "search-result-forum" 类的单元格，表示所属论坛
    tds_author = div.find_all("td", class_="search-result-author")  # 查找所有带有 "search-result-author" 类的单元格，表示作者信息
    tds_nums = div.find_all("td", class_="search-result-nums")  # 查找所有带有 "search-result-nums" 类的单元格，表示浏览量或回复数
    tds_lastpost = div.find_all("td", class_="search-result-lastpost")  # 查找所有带有 "search-result-lastpost" 类的单元格，表示最后回复信息

# 遍历主题单元格，提取标题和链接
    for td_subject in tds_subject:
        title = td_subject.a.text # 获取主题链接的文本内容作为标题
        titles.append(title) # 将标题添加到列表中
        href = td_subject.a.get("href") # 获取链接的 href 属性值
        hrefs.append(href) # 将链接添加到列表中
# 遍历论坛单元格，提取论坛名称
    for td_forum in tds_forum:
        forum = td_forum.a.text  # 获取论坛链接的文本内容作为论坛名称
        forums.append(forum)  # 将论坛名称添加到列表中
# 遍历作者单元格，提取作者名称和发帖日期
    for td_author in tds_author:
        author = td_author.a.text.strip() # 获取作者链接的文本内容并去除多余空格
        authors.append(author) # 将作者名称添加到列表中
        date = td_author.find("div",class_="date").text # 查找包含日期的 div 元素并提取文本内容
        dates.append(date) # 将发帖日期添加到列表中
# 遍历浏览量/回复数单元格，提取数值
    for td_nums in tds_nums: 
        num = td_nums.text  # 获取单元格中的文本内容（可能是浏览量或回复数）
        nums.append(num)  # 将数值添加到列表中
# 遍历最后回复单元格，提取最后回复时间或用户名
    for td_lastpost in tds_lastpost:
        lastpost = td_lastpost.em.a.text  # 获取包含最后回复信息的链接文本内容
        lastposts.append(lastpost)  # 将最后回复信息添加到列表中

# 定义函数 `get_tid`，接收一个字符串参数 `href`，表示帖子链接
    # 示例链接：https://www.discuss.com.hk/viewthread.php?tid=31741054&feedback=1&num=1&tr_h=MUNCp3CZ9MV
    # 提供示例链接，方便说明正则表达式匹配的内容
def get_tid(href):
    # https://www.discuss.com.hk/viewthread.php?tid=31741054&feedback=1&num=1&tr_h=MUNCp3CZ9MV
    match = re.search(r'tid=(\d+)', href)
    # 使用正则表达式 `tid=(\d+)` 在链接中查找 `tid` 参数及其对应的数字值
    # `\d+` 表示匹配一个或多个数字，`()` 用于捕获匹配的数字部分
    tid = match.group(1)
    # 提取正则表达式捕获组中的第一个匹配项，即帖子 ID 的数字部分
    return int(tid)
    # 将帖子 ID 转换为整数类型并返回

# 定义函数 `get_content`，接收两个参数：
    # `tid` 是帖子 ID，用于指定目标帖子。
    # `index` 是页码，用于指定帖子中具体的分页内容。
def get_content(tid, index):
    url = "https://www.discuss.com.hk/viewthread.php"  # 定义目标页面的基础 URL，指向 `viewthread.php`。
    # 定义请求头部信息，用于模拟浏览器行为，绕过反爬虫机制。
    # 指定浏览器用户代理，模拟最新版本的 Chrome 浏览器。
    # 包含登录和访问相关的 Cookie 信息，用于保持会话状态。
    # 需要具体网站的 Cookie 数据来访问权限受限的页面。
    # 设置来源页面地址，用于告知服务器当前请求从哪里发起（反爬虫技术之一）。
    headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36", 
            "Cookie":"nwtc=6709ccfb3429a3.14096557; AB_18=B; AB_28=B; AB_29=A; AB_34=B; AB_61=A; AB_full=18-B_28-B_29-A_34-B_61-A; _sharedID=9596a890-9a98-4d88-8a8f-50f843969734; _sharedID_cst=zix7LPQsHA%3D%3D; _cc_id=b061a5f00e358101850ed4ba63775d85; _fbp=fb.2.1728695562088.10633212018053565; _ga=GA1.3.232976884.1728695562; trc_cookie_storage=taboola%2520global%253Auser-id%3D16ecfcea-53e7-4d68-a50b-4aa76cfc9005-tuctdf401a4; cookieconsent_status=dismiss; jiyakeji_uuid=45def8a0-884b-11ef-9009-b566392e0530; _pbjs_userid_consent_data=6683316680106290; _pubcid=e5bae2f0-7b05-4d30-b059-2dde41627068; iUUID=e2845f0f5935d3fd60beed0dc5479a0e; iUUID=e2845f0f5935d3fd60beed0dc5479a0e; pbjs-unifiedid=%7B%22TDID%22%3A%22bf0f7259-e759-4b78-a6b1-b0f17982f6cd%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222024-10-09T01%3A38%3A12%22%7D; id5_storage=%7B%22signature%22%3A%22ID5_Au7sSKiTHaU-yFxPPyDf8YSF76YoQ7sIm_h_pQbX_6WifU75u3clZ1gzvphiaBVSp_-DGKGap5GQboFU8XK68XqX66g0cPzgbcYCfO55F6VCoOfpcsdTcSMtUSGJU9uQHTyh2IUV4lqDkOzaLqK09jKMjQeUFzHDm9CZ8chKUUqcVIVBf-8%22%2C%22created_at%22%3A%222024-09-30T09%3A55%3A26.782Z%22%2C%22id5_consent%22%3Atrue%2C%22original_uid%22%3A%22ID5*EDphq8B6pXForOMURpxwQ-OWSlnuWH_5pYZOEfpOBLbW_Y4ch2-dy9QbQyYCUkbY%22%2C%22universal_uid%22%3A%22ID5*n4Dpkj7Wh1umNmf3uQDzZMTwFoB-i1l1PviBWmvyVPXW_aafvcxFYCSQu7IEa9vv%22%2C%22link_type%22%3A2%2C%22cascade_needed%22%3Afalse%2C%22privacy%22%3A%7B%22jurisdiction%22%3A%22other%22%2C%22id5_consent%22%3Atrue%7D%2C%22ext%22%3A%7B%22linkType%22%3A2%2C%22pba%22%3A%22pcDvZbjGIu80r1dyBpC6m%2FaWQ%2BKw6t1ww5qutlWQMKw%3D%22%7D%2C%22cache_control%22%3A%7B%22max_age_sec%22%3A7200%7D%7D; cto_bidid=UyFXm19KMmxuY0VBRU5ldVFLa3lQOUVKVTNFJTJCdFVjRWZTckoyZmt1YXE0cTdJbWdnQzZZWUJCSVA5U3VIMWhtNW0zZk5KNEJlZDZGU1JaZnNiWSUyQlpITThUWDZ4Z0VKRnNkZHdpMCUyQk1Rc3JTcGZvVDJJQm5OWHVUbFp5JTJCbEElMkZCN213dmc; cto_bundle=DvOWzF8wMGh3Q0hJSUpIRFAlMkY2MTV2UE5ZUUZDWm5qN2JlRU93VVZKWXJ5RUJWMHMza2dvNXZZTmZzcmsySmduQWFKTThaVW53WExld2h2YUpZcFhKQm1wU0NBbE80c1NPMVppV0tmV0lMcWVZS3FtMGclMkZsaWZmYTBqWW9iUmNCJTJGRGhMNkQwajJmQ1VRUUlMdHloVmhkNjU0JTJCbVVWbWI3SlV5RG1aUnJzJTJGNmRGNEJvT3NVYWFQazNsNEtsbVlsaXRZZkhwbjVpaXhPV2J3TEJxdFJUOUhJN1NkUSUzRCUzRA; _pubcid_cst=Xyz5LAss%2Bw%3D%3D; cdb_auth=DNrU%2Bt91DbGIWAKyNhX8e%2FzQZOAnquvnnlBqZ0c6fmY%2BMdhl0FGsvqISZiWifB2baZynS7a8%2FH0iozRyXVbJA7aA6lsFyRdKppcUw85FVQzNh2c; uid2hash=92be07; _lr_env_src_ats=true; connectId=%7B%22vmuid%22%3A%22REch47Dje5_YP2AZxCMt2KeZhXcTO19ZIOnH9ulBW0t1AcIGyO-zrjJRk3X8EbSHHFAWTAHWGyNiDJmdNg067w%22%2C%22connectid%22%3A%22REch47Dje5_YP2AZxCMt2KeZhXcTO19ZIOnH9ulBW0t1AcIGyO-zrjJRk3X8EbSHHFAWTAHWGyNiDJmdNg067w%22%2C%22connectId%22%3A%22REch47Dje5_YP2AZxCMt2KeZhXcTO19ZIOnH9ulBW0t1AcIGyO-zrjJRk3X8EbSHHFAWTAHWGyNiDJmdNg067w%22%2C%22ttl%22%3A86400000%2C%22he%22%3A%224c6ce4d92aac6057c0c3931d5aa5f70bc84172b870488fe5f21a9acb204c8310%22%2C%22lastSynced%22%3A1732263008947%2C%22lastUsed%22%3A1732263008947%7D; panoramaId_expiry=1733156711098; panoramaId=c723bc3d5ce148a914f13c821a9616d53938d0ad6c74060b3b128266fe414572; nwu=7367025; ui_uid_up=G8fg1L1QLgNycd6k9nmXkg==; mission_unread=1; _lr_geo_location=HK; _clck=9fec3n%7C2%7Cfr8%7C0%7C1746; mission_menu_popup_status=true; mission_unread=0; cf_clearance=SJ8Z1Kb5OAnDiy098lErSogJ7orWhjdrqvfqlR7M7Ow-1732700510-1.2.1.1-MotKpv6ZbLcu.2j29XqqH7GRlvdf.T_fktRGotMlbgnfUepGL5EcGM3CeqtnKiFjhZYjGQHHvqMDAHb2sETGQoCPewJBoLCdH0GI2tCcoA.UatZs7DQOl8nQG2iRpGcuxrozS7LQnNIlr1NGS5B_JCtipW0QZWvr4rgMdSJDEGJY3BCb_FJzJatD8bGoMqF9YF2NgYGPVI_0xrX9o_ePV67sYxRpTmJI1qVGI6DRBekFxiQZ4hABH8zZJTBI4lmCSewNbUoZ19dntUQRpa.87Kltei1l0Xuz2ZwKYtI1vvFcxr4oZDqDWqOxVZmzG5S49Z.u72c3.ILqttC9ik1UzP1GrqBANOZ9jb7UBvADiHZaLtiogmON0OHCnN_cRqAKcuQSX.GsZrmiiL9fXC8skVGmQ1d1dA3Nw0JPZcIGe7QloN25QRPwhgSzmQ.xEFvI; cdb_sid=gGoFii; goowifq=1; ttd-web=1732700513; innity-web=1732700513; verizon-web=1732700513; ucf_uid=ba3e20d5-430e-4ddb-bb5f-82a9c4c0dcbf; up_c=1732700516; _lr_env=eyJ0aW1lc3RhbXAiOjE3MzI3MDA1MTYxMzgsInZlcnNpb24iOiIxLjYuMCIsImVudmVsb3BlIjoiQW9hSFpRUGRhZjVCY3g1QVBGNy1Pc1pnamt3NGpOUTByWTFLSEJCcGU3Zmt5RjI1akZDUW91b01CRXQzSTlldlNOM1VoQnBOeHZ6ZjN4NFdUS25xUzZIYUx6WW0ydlhCS3pzR1AxVWtBZ2owNVZqdHVvNF9fSVplcmhocnpkUEJkalE3OEhFVDNnN1hMdjJGM1d3NFJEXzVSUTJPRDZXbWF2NngxSjIzbFRfOWRGYnhHcFNfelVGQ2ZNUHZwSGZvRDRKX0hvMl8iLCJjcmVhdGlvblRpbWVzdGFtcCI6MTczMjY4Mzc5OTIxMn0%3D; _lr_pairId=eyJ0aW1lc3RhbXAiOjE3MzI3MDA1MTYxMzgsInZlcnNpb24iOiIxLjYuMCIsImVudmVsb3BlIjpbIkE0SnNjU0dTNndlK2szNWNtNlJ6VTRmVHhlY0hhRFFXTHpQTVJuNFJ3bzZqIl0sImNyZWF0aW9uVGltZXN0YW1wIjoxNzMyNjgzNzk5MjEzfQ%3D%3D; __uid2_advertising_token=A4AAAA4wUfFWCSYIGvpdASoM-YbFsWxwiC_-QqxsZF_37JnuCIhtOEWSEUPsEXQMtb1fZ2xfJ38Lxr-aKPwQ0Idk9pHFImh9tkxrDfLmQr3GCELdrHH59LskQ-Bih6AjexEjtC7b-Ni6cjDncosAnpByZYMEAicb9_IclVxMJGpS3jPUqxuUcKgfiLN2fc68qjC0ku4CK0KMpbV_v6nu00wfCA; __gads=ID=d0830cdf7ec272f0:T=1728695560:RT=1732700516:S=ALNI_MbeM4tSFStv5mERroMd2rwoXvZZaw; __gpi=UID=00000f3f58467c60:T=1728695561:RT=1732700516:S=ALNI_MZV2QSb_cSP22sgLx-Jay5h7UrV5Q; __eoi=ID=99e08a48eb6725f9:T=1728695561:RT=1732700516:S=AA-AfjYXTC03ud34gC6U_S0-91oa; curr_hostname=www.discuss.com.hk; px1fq=1; dfp_seg_ids=%5B%5D; cdb_oldtopics=D31770100D; cdb_fid1118=1732700502; cdb_urihistory=31770100-1%3B; cdb_urihistorycount=1; __uid_2=%7B%22refresh_from%22%3A1732704114717%2C%22refresh_expires%22%3A1735292514717%2C%22identity_expires%22%3A1732959714717%2C%22advertising_token%22%3A%22A4AAAA4wUfFWCSYIGvpdASoM-YbFsWxwiC_-QqxsZF_37JnuCIhtOEWSEUPsEXQMtb1fZ2xfJ38Lxr-aKPwQ0Idk9pHFImh9tkxrDfLmQr3GCELdrHH59LskQ-Bih6AjexEjtC7b-Ni6cjDncosAnpByZYMEAicb9_IclVxMJGpS3jPUqxuUcKgfiLN2fc68qjC0ku4CK0KMpbV_v6nu00wfCA%22%2C%22refresh_token%22%3A%22AAAADjGI5ygskY9CgXf4aENEpxuD1bYsSdwcEBy7GoGUDf18iXwQdzbvyL8Kwp6AFD%2BqyeSCFjsfoyS%2BhYWKIMUGTjXLK7XFbfyi27Kg7m0LRDgR0tiqy7zSEWXClB%2FHH12yx5gLtf3uG%2FgWmK3akI%2FGnpMICatN4Xp5QqncSfRY5ft%2FH01viypgVH6rc1J%2F0XpQavkYdK9mPvikKHSHaPnvQc%2Bs86NkLhn4T6iMpHLyxcZ%2BgXzCqBtqIst27GSr0ZVw012X4UifJ2IpbMQcNLVTAGGBqp%2BDRenQoH7Ql%2Bi1QTQAAcpr0Tg8SgRO4K7yS0XWJSQQp0e7MBUupY%2FTGfhZS%2F9TaCvTvhIl7WDeIhl817Suc%2Bct4IIjF%2B9BSB6B1jsa%22%2C%22refresh_response_key%22%3A%229xOcBGao1lX%2BSF8zY7U%2BliOF6pfqrAX%2BhFN3ZHoNyfw%3D%22%7D; screen_skin=true; cto_bundle=tYupc19PUkN3YWRNUlV4c1hwSHElMkJ0SzkyYWtSTmFQY3Z1Qm51bUtnZGdhTGRwSEprSkVqcVJHdDNWUVZGZHZtOHhtTHk3cnBENzJQTm5xUlhuJTJCT1clMkIlMkZJV0MlMkZSOFZiUEJvU2g2TGpuSTZlUFFUSk9sM3ZiY29WY2clMkJLZUExMExrR0g3aGtoazZXYmNRbVdKZzYzMkMzVjlOQ1RhSkRVQWxJS3pHM29TbnJjZnA3djNzVldmRE9lM1E0NVVOTVN1ajJjZ2hNZWh1ckhYJTJCakxVTDRSMFFpYlhUN2clM0QlM0Q; cto_bundle=tYupc19PUkN3YWRNUlV4c1hwSHElMkJ0SzkyYWtSTmFQY3Z1Qm51bUtnZGdhTGRwSEprSkVqcVJHdDNWUVZGZHZtOHhtTHk3cnBENzJQTm5xUlhuJTJCT1clMkIlMkZJV0MlMkZSOFZiUEJvU2g2TGpuSTZlUFFUSk9sM3ZiY29WY2clMkJLZUExMExrR0g3aGtoazZXYmNRbVdKZzYzMkMzVjlOQ1RhSkRVQWxJS3pHM29TbnJjZnA3djNzVldmRE9lM1E0NVVOTVN1ajJjZ2hNZWh1ckhYJTJCakxVTDRSMFFpYlhUN2clM0QlM0Q; _clsk=orl7rb%7C1732700528565%7C3%7C1%7Cq.clarity.ms%2Fcollect; innityfq=1; FCNEC=%5B%5B%22AKsRol92e7QdZM3V4bJud_G5y7E6SgHoTeS2y00rciwNSMNavAJqr0w9m0G4KJAEq9CtfFtHfTEFxYhiRWadhmQ-X5iCKVA7UMzEGrtRONfG2Y0sm0LMQ7wmTv4-qcXsmkETW7YDteDslNagdyrAeXEDKDkfo_-70w%3D%3D%22%5D%5D; freq.5e661e8b47e7043d03000003=1; freq.5f462d2c47e7044a01000002=1; freq.65279e2647e7041906000000=1; innity.dmp.cks.innity=1; innity.dmp.1.sess=1.1732700530607.1732700530607.1732700530607; innity.dmp.1.sess.id=9037025.1.1732700530607; cdb_lastrequest=C%2FdcbIHTqvrnlAJZpuw8e81O; viewthread_history=31770100%7C31770100%7C31592125%7C31592125%7C31592125%7C31692083%7C31692083%7C31766034%7C31766034%7C31766034%7C31731687%7C31731687%7C31731687%7C31756801%7C31756801%7C31391057%7C31391057%7C31391057%7C31391057%7C31741054%7C31741054%7C31741054%7C30856998%7C30856998%7C30856998%7C20814093%7C20814093%7C20814093%7C20814093%7C24459299%7C24459299%7C31718316%7C31718316%7C31718316%7C31132591%7C31746041%7C31746041%7C31231078%7C31514517%7C31514517%7C31518227%7C31518227%7C31749284%7C31749284%7C31544984%7C31544984%7C31611914%7C31611914%7C31207429%7C30735962; amvdofq=2; _ga_8P52FKWN6G=GS1.3.1732700516.53.1.1732700559.0.0.0",
            "Referer":"https://www.discuss.com.hk/search.php?searchsubmit=true&srchtxt=%E6%AC%BA%E9%A8%99&orderby=most_relevant&tr_h=NTR8UEgWu2a&page=1"
            }
    # 定义 URL 的查询参数，构成完整的 GET 请求。
    params = {
            'tid': tid, # `tid` 参数指定目标帖子的 ID。
            'extra': '', # 额外参数，目前为空字符串，可能用于拓展或兼容性。
            'page': index  # `page` 参数指定目标帖子的页码，用于分页获取内容。
            }
    
# 发送 HTTP GET 请求到指定的 URL，附带请求头和查询参数，获取服务器返回的响应。
    r = requests.get(url,headers=headers,params=params)
    r.encoding="utf-8" # 设置响应的编码为 UTF-8，以确保解析内容时字符不会出现乱码。
# 检查返回的 HTML 内容中是否包含“請確認身份再繼續瀏覽”这一关键字。
    # 如果包含，表示当前页面需要身份验证。
    if "請確認身份再繼續瀏覽" in r.text:
        print("无效页面") # 如果页面无效，输出提示信息“无效页面”。
    soup = BeautifulSoup(r.text,"html.parser") # 使用 BeautifulSoup 解析 HTML 文本，将其转换为可操作的 DOM 结构。
    main_content = ""  # 初始化主内容变量 `main_content`，用于存储帖子首页的主要内容。
    other_content = "" # 初始化其他内容变量 `other_content`，用于存储分页内容的其他部分。
    div1 = soup.find_all("div",class_="mainbox viewthread mt-0")
    # 查找页面中所有类名为 `mainbox viewthread mt-0` 的 `<div>` 标签，
    # 这些通常包含帖子的主要结构。

    if div1 != []: # 如果找到这样的 `<div>` 元素（列表不为空），继续处理。
        div2 = div1[0].find_all("div",class_='postouter')  # 在第一个匹配的 `div1` 内，查找所有类名为 `postouter` 的 `<div>` 元素，
        if div2 != []:  # 如果找到这样的 `<div>` 元素（列表不为空），继续处理。
            span = div2[0].find_all("span")  # 在第一个匹配的 `div2` 内，查找所有 `<span>` 标签
            if span != []:  # 如果找到这样的 `<span>` 标签（列表不为空），继续处理。
                if index == 1:  # 检查 `index` 是否为 1，表示获取的是帖子首页的内容。
                    main_content = span[0].text.strip().replace("\n",'').replace('\r','') 
                # 提取第一个 `<span>` 标签的文本内容。
                # 使用 `strip()` 去除前后空格，并替换换行符 `\n` 和回车符 `\r` 为空字符串。
                # 将结果保存到 `main_content` 中。
                else: # 如果 `index` 不为 1，则表示获取的是帖子其他分页的内容。
                    other_content = other_content + span[0].text.strip().replace("\n",'').replace('\r','') + "\n"
                # 提取第一个 `<span>` 标签的文本内容，进行同样的清理。
                # 并将结果以换行符 `\n` 拼接到 `other_content` 中。

    # 使用 BeautifulSoup 查找页面中所有类名为 `mainbox viewthread` 的 `<div>` 元素，
    # 这些通常包含整个帖子的主要结构。               
    divs = soup.find_all("div",class_="mainbox viewthread")
    # 检查是否找到符合条件的 `<div>` 元素（即 `divs` 列表是否不为空）。
    # 如果为空，则说明页面中没有匹配的帖子内容。
    if divs != []:
        for div in divs:# 遍历 `divs` 列表中的每一个 `<div>` 元素，# 分别处理每个找到的帖子结构。
            div3 = div.find_all("div",class_='postouter') # 在当前 `div` 中，查找所有类名为 `postouter` 的 `<div>` 元素，
            if div3 != []:   # 检查是否找到符合条件的 `<div>` 元素（即 `div3` 列表是否不为空）。
                other_content =  other_content + div3[0].text.strip().replace("\n",'').replace('\r','') + "\n"
            # 提取 `div3` 中第一个 `<div>` 的文本内容，
            # 使用 `strip()` 去除前后空格，并替换换行符 `\n` 和回车符 `\r` 为空字符串。
            # 将清理后的文本与 `other_content` 拼接，并在末尾添加换行符 `\n`。
    return main_content, other_content
    # 返回提取的两个变量：
    # - `main_content`：主帖的内容，可能在其他部分生成。
    # - `other_content`：从分页中提取的帖子其他部分内容。

def remove_emojis(text): # 定义一个函数，用于移除文本中的表情符号。
    text = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text) # 使用正则表达式移除文本中的控制字符（不可见字符）。
    return ''.join(char for char in text if not emoji.is_emoji(char)) # 遍历文本中的每个字符，过滤掉所有属于表情符号的字符，并返回清理后的文本。

# 遍历从 1 到 50 的数字，表示需要爬取 50 页内容。
    # `trange` 是 tqdm 提供的进度条显示方法，显示进度条。
for i in trange(1,51):
    crawl(i) # 调用 `crawl` 函数爬取第 `i` 页的数据。

if __name__ == "__main__": # 检查当前脚本是否作为主程序运行（避免模块导入时执行）。
    for i in trange(len(hrefs)):  # 遍历 `hrefs` 列表中每个链接，`hrefs` 应该是存储页面 URL 的列表。
        source_name.append("香港討論區") # 添加数据来源名称 "香港討論區" 到 `source_name` 列表。
        keywords.append(f"{keyword}") # 将当前爬取的关键词存储到 `keywords` 列表中。
        cur_main_content = '' # 初始化变量，用于存储当前链接的主内容.
        cur_other_content = ''# 初始化变量，用于存储当前链接的其他内容。
        tid = get_tid(hrefs[i]) # 调用 `get_tid` 函数，从当前链接中提取帖子的唯一 ID。
        match = re.search(r'([\d.]+)(K)?\s*/', nums[i]) # 使用正则表达式解析 `nums` 列表中的数字内容，提取数字部分和单位（如 K）。
        
        if match.group(2) == "K":# 如果正则匹配到单位是 "K"（表示千），将帖子数量设为 60。
            number = 60
        else:  # 否则，将帖子数量设置为 `nums` 中的数字部分，但不超过 60。
            number = min(int(match.group(1)), 60)
        index = (number // 15) # 计算帖子页数（每页最多 15 条帖子）。
        if (number % 15) > 0: # 如果剩余的帖子数量无法整除 15，则页数加 1。
            index += 1
        # 使用 ThreadPoolExecutor 来多线程获取内容
        with ThreadPoolExecutor(max_workers=32) as executor: # 创建一个最大线程数为 32 的线程池
            # 使用 map 函数批量传递 (tid, j) 参数元组
            results = executor.map(lambda args: get_content(*args), [(tid, j) for j in range(1, index + 1)])  # 构造帖子页码列表，从第 1 页到 `index` 页。
        
        # 处理 results 中的返回结果
        for main_content, other_content in results: # 遍历多线程返回的结果，每个结果包含主内容和其他内容。
            cur_main_content += main_content # 累加当前主内容。
            cur_other_content += other_content # 累加当前其他内容。
        # for j in range(1, index + 1):
        #     main_content, other_content = get_content(tid, j)
        #     cur_main_content += main_content
        #     cur_other_content += other_content
            
        main_contents.append(cur_main_content) # 将当前链接的主内容存储到 `main_contents` 列表中。
        other_contents.append(cur_other_content) # 将当前链接的其他内容存储到 `other_contents` 列表中。


    dic = {}  # 创建一个空字典，用于存储数据
    dic["title"] = titles  # 添加标题列表到字典
    dic["username"] = authors  # 添加用户名列表到字典
    dic["post_time"] = dates  # 添加发帖时间列表到字典
    dic["post_content"] = main_contents  # 添加主帖内容列表到字典
    dic["replies"] =  other_contents  # 添加回帖内容列表到字典
    dic["url"] = hrefs  # 添加帖子链接列表到字典
    dic["keyword"] = keywords  # 添加关键词列表到字典
    dic["platform"] = source_name  # 添加数据来源列表到字典
    dic["forum"] = forums  # 添加板块名称列表到字典
    dic["replies counts/views"] = nums  # 添加回复数/查看数列表到字典
    dic["last_published_date"] = lastposts  # 添加最后回复时间列表到字典

    mt = pd.DataFrame(dic)  # 将字典转换为 pandas 数据框
    mt["post_content"] = mt["post_content"].apply(remove_emojis)  # 对主帖内容进行表情符号清理
    mt["replies"] = mt["replies"].apply(remove_emojis)  # 对回帖内容进行表情符号清理
    mt.to_excel(f"D:/{keyword}.xlsx")  # 将数据框保存为 excel 文件