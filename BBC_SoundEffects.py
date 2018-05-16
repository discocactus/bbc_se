
# coding: utf-8

# # 準備

# In[ ]:


import pandas as pd
import sys
import time
import re
import wget
from selenium import webdriver
from selenium.webdriver.common.by import By
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.select import Select
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options


# In[ ]:


# pandas の最大表示列数を設定 (max_rows で表示行数の設定も可能)
pd.set_option('display.max_columns', 30)


# # 試行錯誤

# In[ ]:


url = 'http://bbcsfx.acropolis.org.uk/'


# In[ ]:


# ヘッドあり Chrome の WebDriver オブジェクトを作成する
driver = webdriver.Chrome()


# In[ ]:


driver.set_window_size(1200, 1000)


# In[ ]:


# ページを開く
driver.get(url)


# In[ ]:


sort_description = driver.find_element_by_css_selector('#example > thead > tr > th:nth-child(1)')


# In[ ]:


sort_description.click()


# In[ ]:


sort_category = driver.find_element_by_css_selector('#example > thead > tr > th:nth-child(2)')


# In[ ]:


sort_category.click()


# In[ ]:


# Description
driver.find_element_by_css_selector('#example > tbody > tr:nth-child(1) > td:nth-child(1)').text


# In[ ]:


# Category
driver.find_element_by_css_selector('#example > tbody > tr:nth-child(1) > td:nth-child(2)').text


# In[ ]:


# Duration
driver.find_element_by_css_selector('#example > tbody > tr:nth-child(1) > td:nth-child(3)').text


# In[ ]:


# URL
driver.find_element_by_css_selector('#example > tbody > tr:nth-child(1) > td:nth-child(5) > a').get_attribute('href')


# In[ ]:


# Description
for tr in trs:
    print(tr.find_element_by_css_selector('td:nth-child(1)').text)


# In[ ]:


# Category
for tr in trs:
    print(tr.find_element_by_css_selector('td:nth-child(2)').text)


# In[ ]:


# Duration
for tr in trs:
    print(tr.find_element_by_css_selector('td:nth-child(3)').text)


# In[ ]:


# URL
for tr in trs:
    print(tr.find_element_by_css_selector('td:nth-child(5) > a').get_attribute('href'))


# In[ ]:


tbl = driver.find_element_by_css_selector('#example > tbody')


# In[ ]:


trs = tbl.find_elements(By.TAG_NAME, 'tr')


# In[ ]:


len(trs)


# In[ ]:


urls = []
for tr in trs:
    urls.append(tr.find_element_by_css_selector('td:nth-child(5) > a').get_attribute('href'))


# In[ ]:


urls


# In[ ]:


result = driver.page_source


# In[ ]:


df = pd.read_html(driver.page_source, header=0)[0]


# In[ ]:


df['URL'] = urls


# In[ ]:


df = df.iloc[:,[0, 1, 2, 5]]


# In[ ]:


df


# In[ ]:


next_btn = driver.find_element_by_id('example_next')


# In[ ]:


next_btn.click()


# In[ ]:


bbc_se = pd.DataFrame()


# In[ ]:


bbc_se = bbc_se.append(df)


# In[ ]:


bbc_se


# # リスト完成

# In[ ]:


url = 'http://bbcsfx.acropolis.org.uk/'


# In[ ]:


# ヘッドあり Chrome の WebDriver オブジェクトを作成する
driver = webdriver.Chrome()
driver.set_window_size(1200, 1000)

# ページを開く
driver.get(url)

sort_description = driver.find_element_by_css_selector('#example > thead > tr > th:nth-child(1)')
sort_description.click()
sort_category = driver.find_element_by_css_selector('#example > thead > tr > th:nth-child(2)')
sort_category.click()


# In[ ]:


bbc_se = pd.DataFrame()

for i in range(1, 642):
    print('page {0}'.format(i))
    
    result = driver.page_source
    df = pd.read_html(driver.page_source, header=0)[0]

    tbl = driver.find_element_by_css_selector('#example > tbody')
    trs = tbl.find_elements(By.TAG_NAME, 'tr')
    urls = []
    for tr in trs:
        urls.append(tr.find_element_by_css_selector('td:nth-child(5) > a').get_attribute('href'))

    df['URL'] = urls
    df = df.iloc[:,[0, 1, 2, 5]]

    bbc_se = bbc_se.append(df)

    next_btn = driver.find_element_by_id('example_next')
    next_btn.click()
    time.sleep(1)


# In[ ]:


# driver を終了
driver.quit()


# In[ ]:


bbc_se = bbc_se.reset_index(drop=True)


# In[ ]:


bbc_se['file_name'] = ""


# In[ ]:


bbc_se.loc[9, 'file_name']


# In[ ]:


for idx in range(len(bbc_se)):
    bbc_se.loc[idx, 'file_name'] = '{0}_{1}.wav'.format(re.search(r'[0-9]+', bbc_se['URL'][idx]).group(),
                                                        re.sub("[\\/:*?\"<>| `',.~!@#$%^&*;]", '_', bbc_se['Description'][idx]))


# In[ ]:


bbc_se


# In[ ]:


bbc_se.groupby('Category').count()


# In[ ]:


bbc_se['Duration (seconds)'].sum()


# In[ ]:


bbc_se.loc[2000:3000, 'Duration (seconds)'].sum()


# In[ ]:


bbc_se['Duration (seconds)'].plot()


# In[ ]:


bbc_se.to_csv('BBC_SE.csv')


# # ダウンロード
# ファイル名使用禁止文字
# \/：*?"<>|
# 追加で使用したくない文字
#  ',.!@#$%^&*;
# In[ ]:


bbc_se = pd.read_csv('BBC_SE.csv', index_col=0)


# In[ ]:


bbc_se['Description'][8]


# In[ ]:


re.sub("[\\/:*?\"<>| `',.~!@#$%^&*;]", '_', bbc_se['Description'][8])


# In[ ]:


bbc_se['URL'][8]


# In[ ]:


re.search(r'[0-9]+', bbc_se['URL'][8]).group()


# In[ ]:


'D:\BBC_SE\{0}_{1}.wav'.format(re.search(r'[0-9]+', bbc_se['URL'][8]).group(),
                              re.sub("[\\/:*?\"<>| `',.~!@#$%^&*;]", '_', bbc_se['Description'][8]))


# In[ ]:


wget.download(url=bbc_se['URL'][8], out='D:\BBC_SE\{0}_{1}.wav'.format(
    re.search(r'[0-9]+', bbc_se['URL'][8]).group(),
    re.sub("[\\/:*?\"<>| `',.~!@#$%^&*;]", '_', bbc_se['Description'][8])))


# In[ ]:


failed = []


# In[ ]:


for idx in range(2013, 3000):
    try:
        wget.download(url=bbc_se['URL'][idx], out='D:\BBC_SE\{0}'.format(bbc_se['file_name'][idx]))
    except Exception as e:
        print('\n{0}: {1}\n'.format(idx, e))
        failed.append(idx)


# In[ ]:


failed


# In[ ]:


pd.Series(failed).to_csv('download_failed.csv')


# In[ ]:


bbc_se['file_name'][741]


# In[ ]:


idx = 741
wget.download(url=bbc_se['URL'][idx], out='D:\BBC_SE\{0}'.format(bbc_se['file_name'][idx]))


# In[ ]:


list(range(110, 120))


# In[ ]:


# import sys, time
for num, i in enumerate(range(100)):
    sys.stdout.write("\r{0}".format(num))
    sys.stdout.flush()
    time.sleep(0.01)

