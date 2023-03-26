# весь код занимает:
# ~20 минут для выгрузки всех блузок
# ~20 минут для выгрузки всех блузок

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import requests
import numpy as np
from tqdm import tqdm

import PIL
import pandas as pd
import os
import cv2
from PIL import Image

# функция сохранения картинок по папкам
def fig_save(link,cls, clsf):

    if clsf == 'bluzy':
        path = 'C:/Users/Агния/Desktop/lamoda/bluzy/'
    else:
        path = 'C:/Users/Агния/Desktop/lamoda/bryuki/'

    filename = path + cls +'_'+'_'.join(link.split('/')[-1].split('_')[:2])+'.jpg'
    link = 'https:'+link.replace('236x341','600x866')

    with open(filename,'wb') as f:
        f.write(requests.get(link, stream=True).content)


driver = webdriver.Chrome()

bluzy_urls = ['https://www.lamoda.ru/c/2483/clothes-bluzy/']
bryuki_urls = ['https://www.lamoda.ru/c/401/clothes-bryuki-shorty-kombinezony/']

# добавление ссылок со страницами, для перехода по страницам
for page in range(154):

    next_page = bluzy_urls[0] + '?page=' + str(page)
    bluzy_urls.append(next_page)

    next_page = bryuki_urls[0] + '?page=' + str(page)
    bryuki_urls.append(next_page)

# поиск картинок для класса "Блузки" и их сохранение
for url in tqdm(bluzy_urls):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'lxml')

    cls=url.split('/')[-2]
    [fig_save(x['src'], cls, 'bluzy') for x in soup.find_all('img',class_="x-product-card__pic-img")]

# поиск картинок для класса "Брюки" и их сохранение
for url in tqdm(bryuki_urls):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'lxml')

    cls=url.split('/')[-2]
    [fig_save(x['src'], cls, 'bryuki') for x in soup.find_all('img',class_="x-product-card__pic-img")]

# код, который сформировал DataFrame с названием всех картинок, их классом и размерностью
path_bluzy = 'C:/Users/Агния/Desktop/lamoda//bluzy/'
path_bryuki = 'C:/Users/Агния/Desktop/lamoda/bryuki/'

X_bluzy = [np.array(Image.open(os.path.join(path_bluzy, x))).shape for x in os.listdir(path_bluzy)]
X_bryuki = [np.array(Image.open(os.path.join(path_bryuki, x))).shape for x in os.listdir(path_bryuki)]

df1 = pd.DataFrame(os.listdir(path_bryuki), columns=['img_name'])
df1['img_shape'] = X_bryuki
df1['class'] = 'bryuki'

df2 = pd.DataFrame(os.listdir(path_bluzy), columns=['img_name'])
df2['img_shape'] = X_bluzy
df2['class'] = 'bluzy'

pd.concat([df1,df2]).to_csv('C:/Users/Агния/Desktop/lamoda/images_lamoda_products.csv', index=False)