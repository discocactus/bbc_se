
# coding: utf-8

# # 準備

# In[ ]:


import pandas as pd
import numpy as np
import sys
import time
import re
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


# 形態素解析
import treetaggerwrapper as ttw
from collections import Counter


# In[ ]:


import wget


# In[ ]:


from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.select import Select
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options


# In[ ]:


# pandas の最大表示列数を設定 (max_rows で表示行数の設定も可能)
pd.set_option('display.max_columns', 30)


# In[ ]:


bbc_se = pd.read_csv('BBC_SE.csv', index_col=0)


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


# # リスト作成

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


bbc_se.loc[8000:10000, 'Duration (seconds)'].sum()


# In[ ]:


bbc_se.loc[10000:12000, 'Duration (seconds)'].sum()


# In[ ]:


bbc_se['Duration (seconds)'].plot()


# In[ ]:


bbc_se.loc[8000:10000, 'Duration (seconds)'].plot()


# In[ ]:


bbc_se.loc[10000:12000, 'Duration (seconds)'].plot()


# In[ ]:


bbc_se.to_csv('BBC_SE.csv')


# # 長すぎるファイル名の調整 (200文字以下に)

# In[ ]:


bbc_se['file_name'].map(lambda x: len(x)).plot()


# In[ ]:


over200 = bbc_se['file_name'][bbc_se['file_name'].map(lambda x: len(x)) > 200].index


# In[ ]:


len(over200)


# In[ ]:


for idx in over200:
    print('{0}:\n{1}\n'.format(idx, bbc_se.loc[idx, 'file_name']))


# In[ ]:


bbc_se.loc[over200, 'file_name'].map(lambda x: len(x))
# bbc_se['file_name'][bbc_se['file_name'].map(lambda x: len(x)) > 200].map(lambda x: len(x))


# In[ ]:


bbc_se.loc[2211, 'file_name']


# In[ ]:


bbc_se.loc[2211, 'file_name'] = '07044122_Cultivated_land_(semi-arid)_in_late_Spring__midday_atmosphere_with_Woodlark__Booted_Eagle__Corn_Bunting__Hoopoe__Azure-Winged_Magpie__Spotless_Starling__grasshoppers___flies.wav'


# In[ ]:


bbc_se.loc[7633, 'file_name']


# In[ ]:


bbc_se.loc[7633, 'file_name'] = '07046158_Ship_launch_-_bottle_breaks__men_hammer_away_at_props__cheers_as_boat_begins_to_move__hits_water_at_1_43__three_cheers_given__general_atmosphere_-_1985_(2S23_reprocessed).wav'


# In[ ]:


bbc_se.loc[8109, 'file_name']


# In[ ]:


bbc_se.loc[8109, 'file_name'] = '07045087_Steam_Train_starts_into_constant_run__various_acoustic_changes_as_train_passes_through_cuttings__etc___alows___stops_in_station.wav'


# In[ ]:


bbc_se.loc[10118, 'file_name']


# In[ ]:


bbc_se.loc[10118, 'file_name'] = '07062038_Sheep__30_to_50_ewes___lambs_calling_in_field__scattered_then_approach__food_bucket_shaken__food_into_troughs__one_lamb_bleats_on_own__loud_bleats.wav'


# In[ ]:


bbc_se.loc[10292, 'file_name']


# In[ ]:


bbc_se.loc[10292, 'file_name'] = '07048127_Church_bells_and_village_band_outside_church_(Poland)_during_harvest_festival_celebrations__bells__chat__brass_band_(very_bad)_makes_circuit_of_church_playing_hymn_and_returns.wav'


# In[ ]:


bbc_se.loc[10341, 'file_name']


# In[ ]:


bbc_se.loc[10341, 'file_name'] = '07074009_Building_site_-_Manly__Australia__Large_site_as_heard_from_above_with_natural_reverberation__hammering__electric_saws__drilling__metal_sheeting_and_wood_dropped.wav'


# In[ ]:


bbc_se.loc[10343, 'file_name']


# In[ ]:


bbc_se.loc[10343, 'file_name'] = '07074014_Ferry_arrives_at_Circular_Quay_Sydney__Australia_-_distant_horns__water_churning_as_large_ferry_arrives__indistinct_speech_and_calls_from_passengers.wav'


# In[ ]:


bbc_se.loc[10507, 'file_name']


# In[ ]:


bbc_se.loc[10507, 'file_name'] = '07058185_St__Sepulchre_s_Church__High_Holborn__exterior__tenor_bell_rung__ends__background_traffic_-_1985_(2B9).wav'


# In[ ]:


bbc_se.loc[10508, 'file_name']


# In[ ]:


bbc_se.loc[10508, 'file_name'] = '07058184_St__Sepulchre_s_Church__High_Holborn__exterior__tenor_bell_rung__with_background_traffic_-_1985_(2B9).wav'


# In[ ]:


bbc_se.loc[10512, 'file_name']


# In[ ]:


bbc_se.loc[10512, 'file_name'] = '07058199_Exterior__5_bells_rung_in_the_style_used_from_the_Reformation_until_about_the_17th_Century_-_rounds_and_call_changes_recorded_outside_church_-_1982_(2B8__reprocessed_).wav'


# In[ ]:


bbc_se.loc[10513, 'file_name']


# In[ ]:


bbc_se.loc[10513, 'file_name'] = '07058198_Interior__5_bells_rung_in_the_style_used_from_the_Reformation_until_about_the_17th_Century_-_rounds_and_call_changes_from_interior_of_church_-_1982_(2B8__reprocessed_).wav'


# In[ ]:


bbc_se.loc[10576, 'file_name']


# In[ ]:


bbc_se.loc[10576, 'file_name'] = '07072153_Quiet_safari_park_fairground_atmos___with_birdsong_and_some_ducks_quacking_at_start_-_May__1985_(5F4_reprocessed)_(tecnical_note_-_to_be_used_at_low_level).wav'


# In[ ]:


bbc_se.loc[11040, 'file_name']


# In[ ]:


bbc_se.loc[11040, 'file_name'] = '07062049_Cattle__interior__young_calves_feeding_from_buckets_in_sheds__one_sucking_through_teat_out_of_bucket_(close_perspective)__calf_scampers_in_straw__young_calf_moos__older_calves_moo.wav'


# In[ ]:


bbc_se.loc[13243, 'file_name']


# In[ ]:


bbc_se.loc[13243, 'file_name'] = '07074025_Claybird_shooting_-_several_shotgun_shots_preceded_by_noise_of_claybird_(aka_clay_pigeon)_firing_mechanism__with_comments_from_instructor_just_audible.wav'


# In[ ]:


bbc_se.loc[14701, 'file_name']


# In[ ]:


bbc_se.loc[14701, 'file_name'] = '07068045_Exterior_-_Dacia_(Romania_s_car)_in_the_rain__starts__police_whistles_and_heavy_traffic__Interior_-_engine_start_and_drive_on_wet_streets_in_heavy_traffic_-_exterior_-_car_drives_away_.wav'


# In[ ]:


bbc_se.loc[15486, 'file_name']


# In[ ]:


bbc_se.loc[15486, 'file_name'] = '07070203_Thai_Diesel_Express_Train__interior__atmosphere_in_third_class_carriage__constant_run__slow___stop__station_atmosphere__bell___train_horn__train_starts_into_run_.wav'


# In[ ]:


bbc_se.to_csv('BBC_SE.csv')


# # リストの内容

# In[ ]:


bbc_se = pd.read_csv('BBC_SE.csv', index_col=0)


# In[ ]:


bbc_se.groupby('Category').count()


# In[ ]:


bbc_se['Duration (seconds)'].sum()


# In[ ]:


bbc_se.loc[8000:10000, 'Duration (seconds)'].sum()


# In[ ]:


bbc_se.loc[11894:, 'Duration (seconds)'].sum()


# In[ ]:


bbc_se['Duration (seconds)'].plot()


# In[ ]:


bbc_se.loc[11894:14000, 'Duration (seconds)'].plot()


# In[ ]:


bbc_se.loc[14000:15000, 'Duration (seconds)'].plot()


# In[ ]:


bbc_se.loc[15000:, 'Duration (seconds)'].plot()


# In[ ]:


bbc_se.loc[11894:, 'Duration (seconds)'].plot()


# In[ ]:


max(bbc_se['Duration (seconds)'])


# In[ ]:


hist = plt.hist(bbc_se['Duration (seconds)'], bins=np.arange(0, 1660, 60))
hist


# In[ ]:


db = pd.DataFrame(hist[1][:-1], columns=('sec',))
db['count'] = hist[0].astype(np.int64)
db['cum'] = db['count'].cumsum()
db


# In[ ]:


bbc_se.loc[bbc_se['Duration (seconds)'] >= 300, 'Duration (seconds)'].count()


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


for idx in range(12000, 14000):
    try:
        wget.download(url=bbc_se['URL'][idx], out='D:/BBC_SE/12001-14000/{0}'.format(bbc_se['file_name'][idx]))
    except Exception as e:
        print('\n{0}: {1}\n'.format(idx, e))
        failed.append(idx)
        
for idx in range(14000, len(bbc_se)):
    try:
        wget.download(url=bbc_se['URL'][idx], out='D:/BBC_SE/14001-16011/{0}'.format(bbc_se['file_name'][idx]))
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


idx = 15423
wget.download(url=bbc_se['URL'][idx], out='D:/BBC_SE/14001-16011/{0}'.format(bbc_se['file_name'][idx]))


# In[ ]:


list(range(110, 120))


# In[ ]:


# import sys, time
for num, i in enumerate(range(100)):
    sys.stdout.write("\r{0}".format(num))
    sys.stdout.flush()
    time.sleep(0.01)


# # 形態素解析

# In[ ]:


bbc_se


# In[ ]:


bbc_se['Description']


# In[ ]:


# https://yoshiiz.blog.fc2.com/blog-entry-888.html

text = bbc_se.loc[0, 'Description']

# word, pos, lemma からなるタブ区切りの文字列のリストを取得する。
tags_tabseparated = ttw.TreeTagger(TAGLANG='en').tag_text(text)

# word, pos, lemma からなるタプルのリストを作成する。
tags_tuple = ttw.make_tags(tags_tabseparated)  

# word, pos, lemma の一覧を表示する。
for tag in tags_tuple:
    print("{0}\t{1}\t{2}".format(tag[0], tag[1], tag[2]))


# In[ ]:


# xxx.xxx みたいにピリオドの直後に単語がくると構文として間違っているので?不正な値が返ってしまう
# xxx. xxx だったら大丈夫
ttw.TreeTagger(TAGLANG='en').tag_text("occas.distant")


# In[ ]:


# 2時間かかった
# 結果は下で csv に保存済み

failed = []

tags = pd.DataFrame()

for idx in range(len(bbc_se)):
    text = bbc_se.loc[idx, 'Description']
    print('\r{0}: {1}'.format(idx, text), end="")
    text = re.sub('[.,\'"()]', ' ', text)
    
    try:
        # word, pos, lemma からなるタブ区切りの文字列のリストを取得
        tags_tabseparated = ttw.TreeTagger(TAGLANG='en').tag_text(text)

        # word, pos, lemma からなるタプルのリストを作成
        tags_tuple = ttw.make_tags(tags_tabseparated)  

        # tags_tuple の中身を確認
        for tag in tags_tuple:
            # print("{0}\t{1}\t{2}".format(tag[0], tag[1], tag[2]))
            empty_test = tag[1] # 単語として判定できていないと要素がないはず
            
        tags = tags.append(tags_tuple)
        
    except Exception as e:
        print('\n{0}: {1}\nerror: {2}\n'.format(idx, text, e))
        failed.append(idx)
        
tags = tags.reset_index(drop=True)

word_freq = Counter(tags['word'])
pos_freq = Counter(tags['pos'])
lemma_freq = Counter(tags['lemma'])


# In[ ]:


failed
# エラーなし


# In[ ]:


tags.to_csv('BBC_SE_tags.csv')


# In[ ]:


# 書き出したファイルの再読み込み用
# 形態素解析の実行後にテーブルを上書きしないように注意
tags = pd.read_csv('BBC_SE_tags.csv', index_col=0)
tags


# In[ ]:


word_freq_table = pd.DataFrame.from_dict(word_freq, orient='index')
word_freq_table = word_freq_table.sort_values(0, ascending=False).reset_index()
word_freq_table.columns = ['word', 'freq']

pos_freq_table = pd.DataFrame.from_dict(pos_freq, orient='index')
pos_freq_table = pos_freq_table.sort_values(0, ascending=False).reset_index()
pos_freq_table.columns = ['pos', 'freq']

lemma_freq_table = pd.DataFrame.from_dict(lemma_freq, orient='index')
lemma_freq_table = lemma_freq_table.sort_values(0, ascending=False).reset_index()
lemma_freq_table.columns = ['lemma', 'freq']


# In[ ]:


word_freq_table


# In[ ]:


pos_freq_table


# In[ ]:


lemma_freq_table


# In[ ]:


# エンコード指定なしで Excel 保存
# 出力後に全セルの書式設定を文字列に変更しておいた方がよさそう
writer = pd.ExcelWriter('BBC_SE_tags_freq.xlsx')
word_freq_table.to_excel(writer, sheet_name='word', index=False)
pos_freq_table.to_excel(writer, sheet_name='pos', index=False)
lemma_freq_table.to_excel(writer, sheet_name='lemma', index=False)
writer.save()


# In[ ]:


# 減量
exclude_pos = ['CC', 'CD', 'DT', 'IN', 'SYM', 'TO', ':']
tags_reduced = tags[~tags['pos'].isin(exclude_pos)]
tags_reduced = tags_reduced[tags_reduced['word'].apply(lambda x: len(str(x))) > 1]
tags_reduced


# In[ ]:


word_freq = Counter(tags_reduced['word'])
pos_freq = Counter(tags_reduced['pos'])
lemma_freq = Counter(tags_reduced['lemma'])

word_freq.most_common(100)


# In[ ]:


# 減量版の保存
word_freq_table = pd.DataFrame.from_dict(word_freq, orient='index')
word_freq_table = word_freq_table.sort_values(0, ascending=False).reset_index()
word_freq_table.columns = ['word', 'freq']

pos_freq_table = pd.DataFrame.from_dict(pos_freq, orient='index')
pos_freq_table = pos_freq_table.sort_values(0, ascending=False).reset_index()
pos_freq_table.columns = ['pos', 'freq']

lemma_freq_table = pd.DataFrame.from_dict(lemma_freq, orient='index')
lemma_freq_table = lemma_freq_table.sort_values(0, ascending=False).reset_index()
lemma_freq_table.columns = ['lemma', 'freq']

# エンコード指定なしで Excel 保存
# 出力後に全セルの書式設定を文字列に変更しておいた方がよさそう
writer = pd.ExcelWriter('BBC_SE_tags_freq_reduced.xlsx')
word_freq_table.to_excel(writer, sheet_name='word', index=False)
pos_freq_table.to_excel(writer, sheet_name='pos', index=False)
lemma_freq_table.to_excel(writer, sheet_name='lemma', index=False)
writer.save()


# In[ ]:


word_freq.most_common(100)


# In[ ]:


tags


# In[ ]:


tags_tuple


# In[ ]:


tags['word']


# In[ ]:


list(tag)


# In[ ]:


tags_tabseparated

