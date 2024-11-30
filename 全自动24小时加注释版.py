# 导入 time 模块，用于执行延时操作
import time  
# 从 tqdm 模块导入 trange，用于显示进度条
from tqdm import trange 
# 导入 pandas，用于数据处理和分析
import pandas as pd 
# 导入 emoji 模块，用于处理文本中的表情符号
import emoji 
# 导入正则表达式模块，用于字符串匹配和替换
import re  
# 从 undetected_chromedriver 模块导入 Chrome，用于规避反爬虫检测的 Chrome 浏览器驱动
from undetected_chromedriver import Chrome 
# 从 selenium.webdriver.common.by 模块导入 By，用于元素定位
from selenium.webdriver.common.by import By  
# 从 selenium.webdriver.chrome.options 模块导入 Options，用于设置 Chrome 浏览器参数
from selenium.webdriver.chrome.options import Options  
# 导入 DesiredCapabilities，用于设置浏览器的启动配置
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities  

# 创建 Chrome 浏览器的选项实例
options = Options() 
# 复制 Chrome 浏览器的默认启动配置 
capabilities = DesiredCapabilities.CHROME.copy()  
# 设置页面加载策略为 'none'，以提高页面加载速度
capabilities["pageLoadStrategy"] = "none"  
# 初始化 Chrome 浏览器驱动，传入选项和启动配置
driver = Chrome(options=options, desired_capabilities=capabilities)  
# 访问指定的网址（香港討論區）
driver.get("https://www.discuss.com.hk/")  
# 将浏览器窗口最大化
driver.maximize_window()  
# 等待 5 秒，确保页面完全加载
time.sleep(5)  
# 以下代码用于登录操作，但目前被注释掉了
# driver.find_element(By.XPATH,f"/html/body/div[1]/main/section/section/div/form/fieldset/section[2]/section[1]/input").send_keys("usrname")  # 输入用户名
# driver.find_element(By.XPATH,f"/html/body/div[1]/main/section/section/div/form/fieldset/section[2]/section[2]/div/input").send_keys("code")  # 输入密码
# driver.find_element(By.XPATH,f"/html/body/div[1]/main/section/section/div/form/fieldset/button").click()  # 点击登录按钮
# time.sleep(10)  # 等待 10 秒，确保登录成功
# 点击页面上的某个元素（可能是关闭弹窗广告或确认按钮）
driver.find_element(By.XPATH,f"/html/body/div[1]/div/a").click()  

# 在搜索框中输入 'test'
driver.find_element(By.CSS_SELECTOR,"#header-search-text").send_keys("test")  # 在搜索框中输入 'test'
# 点击搜索按钮
driver.find_element(By.CSS_SELECTOR,"#searchform > div > button").click()  
# 等待 5 秒，确保搜索结果加载
time.sleep(5)  
# 点击搜索结果中的第二个链接
driver.find_element(By.CSS_SELECTOR,f"#mainbody > tbody > tr > td > div > div > div.search-result__text > div > div > a:nth-child(2)").click()  
# 刷新页面
driver.refresh()  
# 再次点击第二个链接
driver.find_element(By.CSS_SELECTOR,f"#mainbody > tbody > tr > td > div > div > div.search-result__text > div > div > a:nth-child(2)").click() 
# 等待 3 秒
time.sleep(3)  

# 初始化用于存储数据的列表
source_name = []
keywords = []
titles = []
hrefs = []
dates = []
forums = []
authors = []
nums = []
lastposts = []
main_contents = []
other_contents = []

# 定义要搜索的关键词列表
for keyword in ['Scam','Cheating','Fraud','欺騙','行騙','詐騙','詐欺','電騙','骗','騙徒','電信詐骗','騙錢','网络诈骗','呃人','呃錢','電話騙案','網上騙案','網上呃錢','網上詐騙','騙徒手法層出不窮','電郵騙案','網上情緣騙案','交友 app 騙案','facebook 騙案']:
    driver.find_element(By.CSS_SELECTOR,"#search-text").clear()  # 清空搜索框
    driver.find_element(By.CSS_SELECTOR,"#search-text").send_keys(keyword)  # 输入关键词
    driver.find_element(By.CSS_SELECTOR,"#search-form > div > button").click()  # 点击搜索按钮
    driver.refresh()  # 刷新页面，确保搜索结果更新
    time.sleep(2)  # 等待 2 秒

    for j in range(49):  # 设定最多爬取 49 页
        title_elements = driver.find_elements(By.XPATH,f"/html/body/table/tbody/tr/td/div/div/div[4]/table/tbody/tr/td[1]/span/a")  # 获取当前页的所有帖子标题元素
        if title_elements == []:  # 如果当前页没有帖子，跳出循环
            break
        for i in range(len(title_elements)):  # 遍历当前页的所有帖子
            title_elements = driver.find_elements(By.XPATH,f"/html/body/table/tbody/tr/td/div/div/div[4]/table/tbody/tr/td[1]/span/a")  # 重新获取标题元素，防止元素过期
            date_elements = driver.find_elements(By.XPATH,f"/html/body/table/tbody/tr/td/div/div/div[4]/table/tbody/tr/td[3]/div[2]")  # 获取日期元素
            forum_elements = driver.find_elements(By.XPATH,f"/html/body/table/tbody/tr/td/div/div/div[4]/table/tbody/tr/td[2]/a")  # 获取论坛板块元素
            author_elements = driver.find_elements(By.XPATH,f"/html/body/table/tbody/tr/td/div/div/div[4]/table/tbody/tr/td[3]/div[1]/a")  # 获取作者元素
            num_elements = driver.find_elements(By.XPATH,f"/html/body/table/tbody/tr/td/div/div/div[4]/table/tbody/tr/td[4]")  # 获取回复数或查看数元素
            lastpost_elements = driver.find_elements(By.XPATH,f"/html/body/table/tbody/tr/td/div/div/div[4]/table/tbody/tr/td[5]/em/a")  # 获取最后回复时间元素

            title = title_elements[i].text  # 提取帖子标题文本
            href = title_elements[i].get_attribute('href')  # 提取帖子链接
            date = date_elements[i].text  # 提取发帖日期
            forum = forum_elements[i].text  # 提取所属板块
            author = author_elements[i].text  # 提取作者名称
            num = num_elements[i].text  # 提取回复数或查看数
            lastpost = lastpost_elements[i].text  # 提取最后回复时间
            titles.append(title)  # 将标题添加到列表
            hrefs.append(href)  # 将链接添加到列表
            dates.append(date)  # 将日期添加到列表
            forums.append(forum)  # 将板块名称添加到列表
            authors.append(author)  # 将作者名称添加到列表
            nums.append(num)  # 将回复数/查看数添加到列表
            lastposts.append(lastpost)  # 将最后回复时间添加到列表
            source_name.append("香港討論區")  # 添加数据来源名称
            keywords.append(keyword)  # 添加对应的搜索关键词

            title_elements[i].click()  # 点击帖子标题，进入帖子详情页
            driver.switch_to.window(driver.window_handles[1])  # 切换到新打开的标签页
            time.sleep(1)  # 等待 1 秒
            driver.refresh()  # 刷新页面
            time.sleep(1)  # 等待 1 秒

            main_content = ""  # 初始化主帖内容变量
            other_content = ""  # 初始化回帖内容变量

            content_elements = driver.find_elements(By.XPATH,f"/html/body/div[7]/div[5]/table/tbody/tr/td[1]/div[1]/div/table/tbody/tr[1]/td[2]/div[3]/div/div[3]/span")  # 获取帖子内容元素
            if len(content_elements) == 0:  # 如果没有获取到内容元素
                main_contents.append(main_content)  # 主帖内容添加空字符串
                other_contents.append(other_content)  # 回帖内容添加空字符串
            elif len(content_elements) == 1:  # 如果只有一个内容元素，表示只有主帖
                main_content += content_elements[0].text.replace("\n",'').replace('\r','')  # 提取主帖内容，并去除换行符
                main_contents.append(main_content)  # 将主帖内容添加到列表
                other_contents.append(other_content)  # 回帖内容添加空字符串
            else:  # 如果有多个内容元素，表示有回帖
                main_content += content_elements[0].text.replace("\n",'').replace('\r','')  # 提取主帖内容
                main_contents.append(main_content)  # 添加主帖内容到列表
                for k in range(1, len(content_elements)):  # 遍历回帖内容
                    other_content = other_content + content_elements[k].text.replace("\n",'').replace('\r','') + "\n"  # 累加回帖内容，并添加换行符
                other_contents.append(other_content)  # 将回帖内容添加到列表
                
            driver.close()  # 关闭当前标签页
            driver.switch_to.window(driver.window_handles[0])  # 切换回原始标签页
            time.sleep(1)  # 等待 1 秒
            driver.refresh()  # 刷新页面
            time.sleep(1)  # 等待 1 秒
                
        # print(titles)
        # print(hrefs)
        # print(dates)
        # print(forums)
        # print(authors)
        # print(nums)
        # print(lastposts)
        # print(main_contents)
        # print(other_contents)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # 将页面滚动到底部，确保加载更多内容
        next_page = driver.find_elements(By.CSS_SELECTOR,f"#mainbody > tbody > tr > td > div > div > div.search-result__pagination > div > div > a.next")  # 查找“下一页”按钮
        if next_page != []:  # 如果存在下一页按钮
            next_page[0].click()  # 点击下一页按钮
        else:
            break  # 如果没有下一页，跳出循环
        time.sleep(0.5)  # 等待 0.5 秒
        driver.refresh()  # 刷新页面
        time.sleep(1)  # 等待 1 秒

def remove_emojis(text):
    text = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text)  # 使用正则表达式去除控制字符
    return ''.join(char for char in text if not emoji.is_emoji(char))  # 去除文本中的表情符号

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
mt.to_csv("D:/香港讨论区数据/香港討論區.csv", index=False, encoding="utf-8")  # 将数据框保存为 CSV 文件
