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
    release_date = None                  # 출시일
    price = None                         # 가격
    evaluation = None                    # 총평가
    evaluation_detail = None             # 세부평가
    title = None                         # 제목
    genre = None                         # 장르
    developer = None                     # 개발
    publisher = None                     # 배급
    single = None                        # 싱글플레이어
    multi = None                         # 멀티플레이어
    online_PvP = None                    # 온라인 PvP
    lan_PvP = None                       # LAN PvP
    shared_Split_Screen_PvP = None       # 스크린 공유 및 분할 PvP
    online_Coop = None                   # 온라인 협동
    lan_Coop = None                      # LAN 협동
    shared_Split_Screen_Coop = None      # 스크린 공유 및 분할 협동
    cross_Platform_Multiplayer = None    # 플롯폼간 멀티플레이어
    lang = None                          # 언어
    req_min_os = None                    # 최저사양 os
    req_min_process = None               # 최저사양 프로세서
    req_min_memory = None                # 최저사양 메모리
    req_min_graphiccard = None           # 최저사양 그래픽
    req_min_storage = None               # 최저사양 저장공간
    req_rec_os = None                    # 권장사양 os
    req_rec_process = None               # 권장사양 프로세서
    req_rec_memory = None                # 권장사양 메모리
    req_rec_graphiccard = None           # 권장사양 그래픽
    req_rec_storage = None               # 권장사양 저장공간
    
    
    print('---출시일')
    temp = row.find_element(By.CLASS_NAME, 'col.search_released.responsive_secondrow')
    if temp == []:
        pass
    else:
        print(temp.text)
        release_date = temp.text
    
    print('---가격')
    price = row.find_element(By.CLASS_NAME, 'col.search_price_discount_combined.responsive_secondrow').text
    print(price)
    
    
    print('---총 평가')
    if row.find_elements(By.CLASS_NAME, 'search_review_summary') == []:
        evaluation = 'None'
        pass
    else:
        review_point = row.find_element(By.CLASS_NAME, 'search_review_summary').get_attribute('data-tooltip-html').split('<br>')
        print(review_point[0])
        evaluation = review_point[0]
        a = review_point[1].split()
        print('---세부 평가')
        say = a[3] + '명의 사용자 평가했고, 그 중 ' + a[0] + '가 긍정적으로 평가한 게임입니다.'
        print(say)
        evaluation_detail = say
        
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
                title = tbody.find_element(By.ID, 'appHubAppName').text

                rightcol = tbody.find_element(By.CLASS_NAME, 'rightcol.game_meta_data')

                genr = rightcol.find_element(By.ID, 'genresAndManufacturer')
                print('---장르\n', genr.find_element(By.TAG_NAME, 'span').text)   # 장르
                genre = genr.find_element(By.TAG_NAME, 'span').text
                
                """
                    개발자
                    배급사
                """

                print('---개발,배급')
                developer = genr.find_elements(By.TAG_NAME, 'div')[0].text
                publisher = genr.find_elements(By.TAG_NAME, 'div')[1].text
                print(developer)
                print(publisher)

                print('---특징')
                features_list = rightcol.find_element(By.CLASS_NAME, 'game_area_features_list_ctn').text
                
                Single = None
                Multi = None
                Online_PvP = None
                LAN_PvP = None
                Shared_Split_Screen_PvP = None
                Online_Coop = None
                LAN_Coop = None
                Shared_Split_Screen_Coop = None
                Cross_Platform_Multiplayer = None
                
                if 'Single' in features_list:
                    single = '싱글플레이어'
                    print(single)
                    
                if 'Multi' in features_list:
                    Multi = '멀티플레이어'
                    print(Multi)
                    
                if 'Online PvP' in features_list:  #이거만 v 대문자인데 맞음?
                    Online_PvP = '온라인 PvP'
                    print(Online_PvP)
                    
                if 'LAN PvP' in features_list:
                    LAN_PvP = 'LAN PvP'
                    print(LAN_PvP)
                    
                if 'Shared/Split Screen PvP' in features_list:
                    Shared_Split_Screen_PvP = '스크린 공유 및 분할 PvP'
                    print(Shared_Split_Screen_PvP)
                    
                if 'Online Co-op' in features_list:
                    Online_Coop = '온라인 협동'
                    print(Online_Coop)
                    
                if 'LAN Co-op' in features_list:
                    LAN_Coop = 'LAN 협동'
                    print(LAN_Coop)
                    
                if 'Shared/Split Screen Co-op' in features_list:
                    Shared_Split_Screen_Coop = '스크린 공유 및 분할 협동'
                    print(Shared_Split_Screen_Coop)
                    
                if 'Cross-Platform Multiplayer' in features_list:
                    Cross_Platform_Multiplayer = '플랫폼간 멀티플레이어'
                    print(Cross_Platform_Multiplayer)
                
                    

                print('---사양')
                sys_req_tb = tbody.find_element(By.CLASS_NAME, 'game_area_sys_req')
                sys_req = sys_req_tb.find_elements(By.TAG_NAME, 'li')
                n=int(len(sys_req)/2)
                print('최소사양')
                
                
                req_min_os = None
                req_min_proc = None
                req_min_mem = None
                req_min_grap = None
                req_min_stor = None
                req_rec_os = None
                req_rec_pros = None
                req_rec_mem = None
                req_rec_grap = None
                req_rec_stor = None
                
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
                lang = ''
                for language in languages[1:]:
                    print(language.find_elements(By.TAG_NAME, 'td')[0].get_attribute('innerHTML').replace('\r','').replace('\n','').replace('\t',''))
                    lang += language.find_elements(By.TAG_NAME, 'td')[0].get_attribute('innerHTML').replace('\r','').replace('\n','').replace('\t','')

                print('======================================================================================\n')

                driver1.close()
            else:                         # 패키지인 상품
                tbody = driver1.find_element(By.CLASS_NAME, 'page_content_ctn')

                print('---제목\n', tbody.find_element(By.CLASS_NAME, 'pageheader').text)
                title = tbody.find_element(By.CLASS_NAME, 'pageheader').text

                rightcol = tbody.find_element(By.CLASS_NAME, 'rightcol.game_meta_data')

                genr = rightcol.find_element(By.CLASS_NAME, 'details_block')
                print('---장르\n', genr.find_element(By.TAG_NAME, 'span').text)   # 장르
                genre = genr.find_element(By.TAG_NAME, 'span').text

                """
                    개발자
                    배급사
                """

                print('---개발,배급')
                developer = genr.find_elements(By.TAG_NAME, 'div')[0].text
                publisher = genr.find_elements(By.TAG_NAME, 'div')[1].text
                print(developer)
                print(publisher)

                print('---특징')
                features_list = rightcol.find_element(By.CLASS_NAME, 'game_area_details_specs_ctn').text
                
                Single = None
                Multi = None
                Online_PvP = None
                LAN_PvP = None
                Shared_Split_Screen_PvP = None
                Online_Coop = None
                LAN_Coop = None
                Shared_Split_Screen_Coop = None
                Cross_Platform_Multiplayer = None
                
                if 'Single' in features_list:
                    single = '싱글플레이어'
                    print(single)
                    
                if 'Multi' in features_list:
                    Multi = '멀티플레이어'
                    print(Multi)
                    
                if 'Online PvP' in features_list:
                    Online_PvP = '온라인 PvP'
                    print(Online_PvP)
                    
                if 'LAN PvP' in features_list:
                    LAN_PvP = 'LAN PvP'
                    print(LAN_PvP)
                    
                if 'Shared/Split Screen PvP' in features_list:
                    Shared_Split_Screen_PvP = '스크린 공유 및 분할 PvP'
                    print(Shared_Split_Screen_PvP)
                    
                if 'Online Co-op' in features_list:
                    Online_Coop = '온라인 협동'
                    print(Online_Coop)
                    
                if 'LAN Co-op' in features_list:
                    LAN_Coop = 'LAN 협동'
                    print(LAN_Coop)
                    
                if 'Shared/Split Screen Co-op' in features_list:
                    Shared_Split_Screen_Coop = '스크린 공유 및 분할 협동'
                    print(Shared_Split_Screen_Coop)
                    
                if 'Cross-Platform Multiplayer' in features_list:
                    Cross_Platform_Multiplayer = '플랫폼간 멀티플레이어'
                    print(Cross_Platform_Multiplayer)

                print('---언어')
                language = rightcol.find_element(By.CLASS_NAME, 'language_list')
                print(language.text.replace('\nListed languages may not be available for all games in the package. View the individual games for more details.','').replace('LANGUAGES: ',''))
                

                print('======================================================================================\n')

                driver1.close()
        #===================================================================================
        else:              # 나이 확인창 X
            if 'app' in body['class']:   # 패키지가 아닌 상품
                print('---제목\n', tbody.select_one('#appHubAppName').text)
                title = tbody.select_one('#appHubAppName').text

                rightcol = tbody.select_one('div.rightcol.game_meta_data')
                genr = rightcol.select_one('#genresAndManufacturer')
                if genr.find('span') == None:
                    genre = 'None'
                    pass
                else:
                    print('---장르\n', genr.find('span').text)   # 장르
                    genre = genr.find('span').text

                """
                    개발자
                    배급사
                """

                print('---개발,배급')
                developer = genr.find_elements(By.TAG_NAME, 'div')[0].text
                publisher = genr.find_elements(By.TAG_NAME, 'div')[1].text
                print(developer)
                print(publisher)

                print('---특징')
                if rightcol.select_one('div.game_area_features_list_ctn') == None:
                    Single = None
                    Multi = None
                    Online_PvP = None
                    LAN_PvP = None
                    Shared_Split_Screen_PvP = None
                    Online_Coop = None
                    LAN_Coop = None
                    Shared_Split_Screen_Coop = None
                    Cross_Platform_Multiplayer = None
                    pass
                
                else:
                    features_list = rightcol.select_one('div.game_area_features_list_ctn').text
                if 'Single' in features_list:
                    single = '싱글플레이어'
                    print(single)
                    
                if 'Multi' in features_list:
                    Multi = '멀티플레이어'
                    print(Multi)
                    
                if 'Online PvP' in features_list:
                    Online_PvP = '온라인 PvP'
                    print(Online_PvP)
                    
                if 'LAN PvP' in features_list:
                    LAN_PvP = 'LAN PvP'
                    print(LAN_PvP)
                    
                if 'Shared/Split Screen PvP' in features_list:
                    Shared_Split_Screen_PvP = '스크린 공유 및 분할 PvP'
                    print(Shared_Split_Screen_PvP)
                    
                if 'Online Co-op' in features_list:
                    Online_Coop = '온라인 협동'
                    print(Online_Coop)
                    
                if 'LAN Co-op' in features_list:
                    LAN_Coop = 'LAN 협동'
                    print(LAN_Coop)
                    
                if 'Shared/Split Screen Co-op' in features_list:
                    Shared_Split_Screen_Coop = '스크린 공유 및 분할 협동'
                    print(Shared_Split_Screen_Coop)
                    
                if 'Cross-Platform Multiplayer' in features_list:
                    Cross_Platform_Multiplayer = '플랫폼간 멀티플레이어'
                    print(Cross_Platform_Multiplayer)
                
                print('---사양')
                sys_req_tb = tbody.select_one('div.game_area_sys_req')
                
                req_min_os = None
                req_min_proc = None
                req_min_mem = None
                req_min_grap = None
                req_min_stor = None
                req_rec_os = None
                req_rec_pros = None
                req_rec_mem = None
                req_rec_grap = None
                req_rec_stor = None
                
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
                    lang = None
                    pass
                else:
                    lang = ''
                    languages = rightcol.select_one('table.game_language_options').find_all('tr')
                    for language in languages[1:]:
                        print(language.find_all('td')[0].text.replace('\r','').replace('\n','').replace('\t',''))
                        lang += language.find_all('td')[0].text.replace('\r','').replace('\n','').replace('\t','')

                print('======================================================================================\n')
            
            else:                         # 패키지인 상품
                print('---제목\n', tbody.select_one('h2.pageheader').text)
                title = tbody.select_one('h2.pageheader').text

                rightcol = tbody.select_one('div.rightcol.game_meta_data')

                genr = rightcol.select('span')
                genre = genr[0].text
                print('---장르\n', genr[0].text)   # 장르

                """
                    개발자
                    배급사
                """

                print('---개발,배급')
                developer = genr.find_elements(By.TAG_NAME, 'div')[0].text
                publisher = genr.find_elements(By.TAG_NAME, 'div')[1].text
                print(developer)
                print(publisher)
                
                print('---특징')
                features_list = rightcol.select_one('div.details_block.details_specs_ctn')
                if features_list == None:
                    features_list = rightcol.select('div.details_block')[1].text
                    Single = None
                    Multi = None
                    Online_PvP = None
                    LAN_PvP = None
                    Shared_Split_Screen_PvP = None
                    Online_Coop = None
                    LAN_Coop = None
                    Shared_Split_Screen_Coop = None
                    Cross_Platform_Multiplayer = None
                
                else:
                    features_list = features_list.text
                if 'Single' in features_list:
                    single = '싱글플레이어'
                    print(single)
                    
                if 'Multi' in features_list:
                    Multi = '멀티플레이어'
                    print(Multi)
                    
                if 'Online PvP' in features_list:
                    Online_PvP = '온라인 PvP'
                    print(Online_PvP)
                    
                if 'LAN PvP' in features_list:
                    LAN_PvP = 'LAN PvP'
                    print(LAN_PvP)
                    
                if 'Shared/Split Screen PvP' in features_list:
                    Shared_Split_Screen_PvP = '스크린 공유 및 분할 PvP'
                    print(Shared_Split_Screen_PvP)
                    
                if 'Online Co-op' in features_list:
                    Online_Coop = '온라인 협동'
                    print(Online_Coop)
                    
                if 'LAN Co-op' in features_list:
                    LAN_Coop = 'LAN 협동'
                    print(LAN_Coop)
                    
                if 'Shared/Split Screen Co-op' in features_list:
                    Shared_Split_Screen_Coop = '스크린 공유 및 분할 협동'
                    print(Shared_Split_Screen_Coop)
                    
                if 'Cross-Platform Multiplayer' in features_list:
                    Cross_Platform_Multiplayer = '플랫폼간 멀티플레이어'
                    print(Cross_Platform_Multiplayer)
                
                print('---언어')
                language = rightcol.select_one('span.language_list')
                print(language.text.replace('Listed languages may not be available for all games in the package. View the individual games for more details.','').replace('LANGUAGES: ','').replace('\n','').replace('\t','').replace('Languages: ',''))
                print('======================================================================================\n')
    except:
        print('error')
