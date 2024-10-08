import time
import urllib.parse

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# WebDriver
driver = None

# Google ローカル検索の1スポット
class Spot:
    def __init__(self, name, region):
        self.name = name
        self.region = region

def search(query):
    spot_list = []
    try:
        # Google検索にアクセス
        url_string = f"https://www.google.com/search?q={urllib.parse.quote(query, 'UTF-8')}"
        print(f"GET {url_string}")
        print()
        driver.get(url_string)

        # 待機 (ページ内のJavaScriptが動作しているはず)
        time.sleep(8)
		# ソースの表示
        print(driver.page_source)

        # ローカル検索のスポット一覧をリストで取得
        elements = driver.find_elements(By.XPATH, "//div[h1='検索結果']//a[@role='button']/div/div")
		# print(f"マッチした要素数: {len(elements)}")

        # 各スポットの名前と地域名を取得
        for element in elements:
            name = element.find_element(By.XPATH, "div[@role='heading']/span").text
            region = element.find_element(By.XPATH, "div[3]").text
            spot_list.append(Spot(name, region))
    except Exception as e:
         print(e)
    return spot_list

def main():
    # 検索質問
    # 　対応："遊園地", "テーマパーク", "レストラン", "ラーメン屋"
    #   非対応："駅", "病院"
    query = "遊園地"

    # ChromeDriver の場所を指定 (プロジェクトフォルダからの相対パス)
    driver_path = "driverのpath"
    service = Service(executable_path=driver_path)

    # GoogleChromeを起動
    global driver
    driver = webdriver.Chrome(service=service)

    # 検索の実行
    spot_list = search(query)

    # 取得したスポット情報の表示
    print(f"スポット({len(spot_list)}箇所):")
    for spot in spot_list:
        print(f"・{spot.name}({spot.region})")
    
    # 一時停止（人がブラウザの情報を確認するため）
    time.sleep(50)

    driver.quit()

if __name__ == "__main__":
    main()
