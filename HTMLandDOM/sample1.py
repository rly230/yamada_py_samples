from lxml import html
import requests

# 遊戯王の新着商品情報
class YugiohLatestProducts:
    # 遊戯王の商品情報ページのURL
    YUGIOH_PRODUCTS_URL = "https://www.yugioh-card.com/japan/products/"
    # コンストラクタ
    def __init__(self):
        # 新着商品のリスト
        self.productList = []
        try:
            response = requests.get(self.YUGIOH_PRODUCTS_URL)
            tree = html.fromstring(response.content)
            itemList = tree.xpath("//dl[@id='latest-products']/dd/ul/li")

            print("商品数:", len(itemList), "\n")

            for item in itemList:
                # 商品情報を取得
                category = item.xpath(".//div[@class='latest-info']/span[contains(@class, 'class')]/text()")[0].strip()
                name1 = item.xpath(".//div[@class='latest-info']/strong/span[1]/text()")[0].strip()
                name2 = item.xpath(".//div[@class='latest-info']/strong/span[2]/text()")[0].strip()
                name3 = item.xpath(".//div[@class='latest-info']/strong/span[3]/text()")[0].strip()
                date = item.xpath(".//div[@class='latest-info']/span[@class='date-price date ']/text()")[0].strip()
                price = item.xpath(".//div[@class='latest-info']/span[@class='date-price price ']/text()")[0].strip()

                # 商品情報をリストに追加
                self.productList.append(YugiohProduct(category, name1, name2, name3, date, price))
        except Exception as e:
            print(e)

    def getProductList(self):
        return self.productList

    def __str__(self):
        return "\n".join([str(product) for product in self.productList])

class YugiohProduct:
    def __init__(self, category, name1, name2, name3, date, price):
        self.category = category
        self.name1 = name1
        self.name2 = name2
        self.name3 = name3
        self.date = date
        self.price = price

    def __str__(self):
        return f"{self.category}\n{self.name1} {self.name2} {self.name3}\n発売日: {self.date}, 希望小売価格: {self.price}\n"


def main():
    products = YugiohLatestProducts()
    print(products)

if __name__ == "__main__":
    main()
