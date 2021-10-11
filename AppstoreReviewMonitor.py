from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.common.keys import Keys
import time


def infinityScroll():
    #무한 스크롤
    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


driver = webdriver.Chrome('./chromedriver')
driver.get('https://apps.apple.com/kr/app/%EC%A0%84%EB%B6%81%EC%9D%80%ED%96%89-%EB%89%B4%EC%8A%A4%EB%A7%88%ED%8A%B8%EB%B1%85%ED%82%B9/id1071766252')

driver.implicitly_wait(3)

#driver.find_elements_by_partial_link_text('모두 보기').click()
#driver.find_element_by_xpath("//*[@id='ember733']").click()
#aa = driver.find_elements_by_xpath("//a[contains(@title,'모두 보기')]")

#모두보기클릭
driver.find_element_by_link_text('모두 보기').click()


#무한 스크롤 다운
infinityScroll()


driver.implicitly_wait(3)
#
#리뷰 텍스트 가져오기
#we-customer-review lockup ember-view
reviews = driver.find_elements(by=By.XPATH, value="//div[contains(@class,'we-customer-review') and contains(@class, 'ember-view')]")
print(len(reviews))
for review in reviews:    
    try:
        #더보기버튼이 있는경우..
        #more = review.find_element(by=By.XPATH, value="//button[contains(@class,'we-truncate__button')and contains(@class, 'link')]")
        more = review.find_element_by_tag_name('button')
        #더보기 클릭
        #more.click()
        more.send_keys(Keys.RETURN)

        #팝업창에서 내용찾기
        modal = more.find_element(by=By.XPATH, value="//div[contains(@class,'we-modal__content__wrapper')]")
        #내용 출력
        print(modal.text)

        #닫기버튼 찾기
        closeButton = modal.find_element(by=By.XPATH, value="//button[contains(@class,'we-modal__close')]")        
        #닫기버튼 클릭
        closeButton.click()
    except NoSuchElementException:
        print(review.text)
    

