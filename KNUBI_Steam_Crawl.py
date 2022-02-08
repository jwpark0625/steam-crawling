from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import datetime as dt
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

driver = webdriver.Chrome()
driver.maximize_window() # 브라우저 화면 최대화
driver.get('https://store.steampowered.com/search/?filter=topsellers&os=win')
time.sleep(1)
SCROLL_PAUSE_SEC = 1


# 스크롤 높이 가져옴
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # 끝까지 스크롤 다운
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # 1초 대기
    time.sleep(SCROLL_PAUSE_SEC)

    # 스크롤 다운 후 스크롤 높이 다시 가져옴
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

tbody = driver.find_element(By.ID, 'search_resultsRows') # 챠트 리스트
rows = tbody.find_elements(By.TAG_NAME, 'a')

for row in rows:
    print('---출시일')
    if row.find_element(By.CLASS_NAME, 'col.search_released.responsive_secondrow') == []:
        pass
    else:
        print(row.find_element(By.CLASS_NAME, 'col.search_released.responsive_secondrow').text)
    
    print('---가격')
    print(row.find_element(By.CLASS_NAME, 'col.search_price_discount_combined.responsive_secondrow').text)
    
    print('---총 평가')
    if row.find_elements(By.CLASS_NAME, 'search_review_summary') == []:
        pass
    else:
        review_point = row.find_element(By.CLASS_NAME, 'search_review_summary').get_attribute('data-tooltip-html').split('<br>')
        print(review_point[0])
        a = review_point[1].split()
        print('---세부 평가')
        print(a[3] + '명의 사용자 평가했고, 그 중 ' + a[0] + '%가 긍정적으로 평가한 게임입니다.')

    try:
        
        url = row.get_attribute('href')
        response = requests.get(url)
        response.raise_for_status()
            # Response에서 에러가 발생할 때
            # 프로그램을 중단하도록 할 때는
            # Response 객체의 raise_for_status() 메서드를 호출하여 코드를 불러옴

        if response.status_code == 200:  # 정상
            html = response.text

            soup = BeautifulSoup(html, 'html.parser')
            body = soup.select_one('body')
            tbody = soup.select_one('#tabletGrid > div.page_content_ctn')
        else :
            print(response.status_code)
            exit()
        
#===========================================================        
        if tbody == None:    # 나이 확인창
            driver1 = webdriver.Chrome()
            driver1.maximize_window() # 브라우저 화면 최대화
            driver1.get(url)
            time.sleep(1)
            
            abc = driver1.find_element(By.ID, 'ageYear')
            abc.find_elements(By.TAG_NAME, 'option')[40].click()
            driver1.find_element(By.CLASS_NAME, 'btnv6_blue_hoverfade.btn_medium').click()
            time.sleep(1)
            
            body = driver1.find_element(By.TAG_NAME, 'body')
            
            if 'app' in body.get_attribute('class'):   # 패키지가 아닌 상품

                tbody = driver1.find_element(By.CLASS_NAME, 'page_content_ctn')

                print('---제목\n', tbody.find_element(By.ID, 'appHubAppName').text)

                rightcol = tbody.find_element(By.CLASS_NAME, 'rightcol.game_meta_data')

                genr = rightcol.find_element(By.ID, 'genresAndManufacturer')
                print('---장르\n', genr.find_element(By.TAG_NAME, 'span').text)   # 장르

                """
                    개발자
                    배급사
                """

                print('---개발,배급')
                for i in genr.find_elements(By.TAG_NAME, 'div')[0:2]:
                    print(i.text)

                print('---특징')
                features_list = rightcol.find_element(By.CLASS_NAME, 'game_area_features_list_ctn').text
                if 'Single' in features_list:
                    print('싱글플레이어')
                if 'Multi' in features_list:
                    print('멀티플레이어')
                if 'Online PVP' in features_list:
                    print('온라인 PvP')
                if 'LAN PvP' in features_list:
                    print('LAN PVP')
                if 'Shared/Split Screen PvP' in features_list:
                    print('스크린 공유 및 분할 PvP')
                if 'Online Co-op' in features_list:
                    print('온라인 협동')
                if 'LAN Co-op' in features_list:
                    print('LAN 협동')
                if 'Shared/Split Screen Co-op' in features_list:
                    print('스크린 공유 및 분할 협동')
                if 'Cross-Platform Multiplayer' in features_list:
                    print('플랫폼간 멀티플레이어')

                print('---사양')
                sys_req_tb = tbody.find_element(By.CLASS_NAME, 'game_area_sys_req')
                sys_req = sys_req_tb.find_elements(By.TAG_NAME, 'li')
                n=int(len(sys_req)/2)
                print('최소사양')
                for i in range(n):
                    if 'OS:' in sys_req[i].text:
                        req_min_os = sys_req[i].text.replace('OS: ','')
                        print(req_min_os)
                    if 'Processor:' in sys_req[i].text:
                        req_min_proc = sys_req[i].text.replace('Processor: ','')
                        print(req_min_proc)
                    if 'Memory:' in sys_req[i].text:
                        req_min_mem = sys_req[i].text.replace('Memory: ','')
                        print(req_min_mem)
                    if 'Graphics:' in sys_req[i].text:
                        req_min_grap = sys_req[i].text.replace('Graphics: ','')
                        print(req_min_grap)
                    if 'Storage:' in sys_req[i].text:
                        req_min_stor = sys_req[i].text.replace('Storage: ','')
                        print(req_min_stor)
                print('권장사양')
                for i in range(n,2*n):
                    if 'OS:' in sys_req[i].text:
                        req_rec_os = sys_req[i].text.replace('OS: ','')
                        print(req_rec_os)
                    if 'Processor:' in sys_req[i].text:
                        req_rec_proc = sys_req[i].text.replace('Processor: ','')
                        print(req_rec_proc)
                    if 'Memory:' in sys_req[i].text:
                        req_rec_mem = sys_req[i].text.replace('Memory: ','')
                        print(req_rec_mem)
                    if 'Graphics:' in sys_req[i].text:
                        req_rec_grap = sys_req[i].text.replace('Graphics: ','')
                        print(req_rec_grap)
                    if 'Storage:' in sys_req[i].text:
                        req_rec_stor = sys_req[i].text.replace('Storage: ','')
                        print(req_rec_stor)

                '---언어'
                languages = rightcol.find_element(By.CLASS_NAME, 'game_language_options').find_elements(By.TAG_NAME, 'tr')
                for language in languages[1:]:
                    print(language.find_elements(By.TAG_NAME, 'td')[0].get_attribute('innerHTML').replace('\r','').replace('\n','').replace('\t',''))

                print('======================================================================================\n')

                driver1.close()
            else:                         # 패키지인 상품
                tbody = driver1.find_element(By.CLASS_NAME, 'page_content_ctn')

                print('---제목\n', tbody.find_element(By.CLASS_NAME, 'pageheader').text)

                rightcol = tbody.find_element(By.CLASS_NAME, 'rightcol.game_meta_data')

                genr = rightcol.find_element(By.CLASS_NAME, 'details_block')
                print('---장르\n', genr.find_element(By.TAG_NAME, 'span').text)   # 장르

                """
                    개발자
                    배급사
                """

                print('---개발,배급')
                for i in genr.find_elements(By.TAG_NAME, 'div')[0:2]:
                    print(i.text)

                print('---특징')
                features_list = rightcol.find_element(By.CLASS_NAME, 'game_area_details_specs_ctn').text
                if 'Single' in features_list:
                    print('싱글플레이어')
                if 'Multi' in features_list:
                    print('멀티플레이어')
                if 'Online PVP' in features_list:
                    print('온라인 PvP')
                if 'LAN PvP' in features_list:
                    print('LAN PVP')
                if 'Shared/Split Screen PvP' in features_list:
                    print('스크린 공유 및 분할 PvP')
                if 'Online Co-op' in features_list:
                    print('온라인 협동')
                if 'LAN Co-op' in features_list:
                    print('LAN 협동')
                if 'Shared/Split Screen Co-op' in features_list:
                    print('스크린 공유 및 분할 협동')
                if 'Cross-Platform Multiplayer' in features_list:
                    print('플랫폼간 멀티플레이어')

                print('---언어')
                language = rightcol.find_element(By.CLASS_NAME, 'language_list')
                print(language.text.replace('\nListed languages may not be available for all games in the package. View the individual games for more details.','').replace('LANGUAGES: ',''))

                print('======================================================================================\n')

                driver1.close()
        #===================================================================================
        else:              # 나이 확인창 X
            if 'app' in body['class']:   # 패키지가 아닌 상품
                print('---제목\n', tbody.select_one('#appHubAppName').text)

                rightcol = tbody.select_one('div.rightcol.game_meta_data')
                genr = rightcol.select_one('#genresAndManufacturer')
                if genr.find('span') == None:
                    pass
                else:
                    print('---장르\n', genr.find('span').text)   # 장르

                """
                    개발자
                    배급사
                """

                print('---개발,배급')
                for i in genr.select('div > a')[0:2]:
                    print(i.text)

                print('---특징')
                if rightcol.select_one('div.game_area_features_list_ctn') == None:
                    pass
                else:
                    features_list = rightcol.select_one('div.game_area_features_list_ctn').text
                    if 'Single' in features_list:
                        print('싱글플레이어')
                    if 'Multi' in features_list:
                        print('멀티플레이어')
                    if 'Online PVP' in features_list:
                        print('온라인 PvP')
                    if 'LAN PvP' in features_list:
                        print('LAN PVP')
                    if 'Shared/Split Screen PvP' in features_list:
                        print('스크린 공유 및 분할 PvP')
                    if 'Online Co-op' in features_list:
                        print('온라인 협동')
                    if 'LAN Co-op' in features_list:
                        print('LAN 협동')
                    if 'Shared/Split Screen Co-op' in features_list:
                        print('스크린 공유 및 분할 협동')
                    if 'Cross-Platform Multiplayer' in features_list:
                        print('플랫폼간 멀티플레이어')

                print('---사양')
                sys_req_tb = tbody.select_one('div.game_area_sys_req')
                if sys_req_tb == None:
                    pass
                else:
                    sys_req = sys_req_tb.find_all('li')
                    n=int(len(sys_req)/2)
                    print('최소사양')
                    for i in range(n):
                        if 'OS:' in sys_req[i].text:
                            req_min_os = sys_req[i].text.replace('OS: ','')
                            print(req_min_os)
                        if 'Processor:' in sys_req[i].text:
                            req_min_proc = sys_req[i].text.replace('Processor: ','')
                            print(req_min_proc)
                        if 'Memory:' in sys_req[i].text:
                            req_min_mem = sys_req[i].text.replace('Memory: ','')
                            print(req_min_mem)
                        if 'Graphics:' in sys_req[i].text:
                            req_min_grap = sys_req[i].text.replace('Graphics: ','')
                            print(req_min_grap)
                        if 'Storage:' in sys_req[i].text:
                            req_min_stor = sys_req[i].text.replace('Storage: ','')
                            print(req_min_stor)
                    print('권장사양')
                    for i in range(n,2*n):
                        if 'OS:' in sys_req[i].text:
                            req_rec_os = sys_req[i].text.replace('OS: ','')
                            print(req_rec_os)
                        if 'Processor:' in sys_req[i].text:
                            req_rec_proc = sys_req[i].text.replace('Processor: ','')
                            print(req_rec_proc)
                        if 'Memory:' in sys_req[i].text:
                            req_rec_mem = sys_req[i].text.replace('Memory: ','')
                            print(req_rec_mem)
                        if 'Graphics:' in sys_req[i].text:
                            req_rec_grap = sys_req[i].text.replace('Graphics: ','')
                            print(req_rec_grap)
                        if 'Storage:' in sys_req[i].text:
                            req_rec_stor = sys_req[i].text.replace('Storage: ','')
                            print(req_rec_stor)

                print('---언어')
                if rightcol.select_one('table.game_language_options') == None:
                    pass
                else:
                    languages = rightcol.select_one('table.game_language_options').find_all('tr')
                    for language in languages[1:]:
                        print(language.find_all('td')[0].text.replace('\r','').replace('\n','').replace('\t',''))

                print('======================================================================================\n')
            
            else:                         # 패키지인 상품
                print('---제목\n', tbody.select_one('h2.pageheader').text)

                rightcol = tbody.select_one('div.rightcol.game_meta_data')

                genr = rightcol.select('span')
                print('---장르\n', genr[0].text)   # 장르

                """
                    개발자
                    배급사
                """

                print('---개발,배급')
                for i in genr[1:3]:
                    print(i.text)

                print('---특징')
                features_list = rightcol.select_one('div.details_block.details_specs_ctn')
                if features_list == None:
                    features_list = rightcol.select('div.details_block')[1].text
                else:
                    features_list = features_list.text
                if 'Single' in features_list:
                    print('싱글플레이어')
                if 'Multi' in features_list:
                    print('멀티플레이어')
                if 'Online PvP' in features_list:
                    print('온라인 PvP')
                if 'LAN PvP' in features_list:
                    print('LAN PVP')
                if 'Shared/Split Screen PvP' in features_list:
                    print('스크린 공유 및 분할 PvP')
                if 'Online Co-op' in features_list:
                    print('온라인 협동')
                if 'LAN Co-op' in features_list:
                    print('LAN 협동')
                if 'Shared/Split Screen Co-op' in features_list:
                    print('스크린 공유 및 분할 협동')
                if 'Cross-Platform Multiplayer' in features_list:
                    print('플랫폼간 멀티플레이어')

                print('---언어')
                language = rightcol.select_one('span.language_list')
                print(language.text.replace('Listed languages may not be available for all games in the package. View the individual games for more details.','').replace('LANGUAGES: ','').replace('\n','').replace('\t','').replace('Languages: ',''))
                print('======================================================================================\n')
    except:
        print('error')
