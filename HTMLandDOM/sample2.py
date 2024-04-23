import requests
from lxml import html


class BaseballDataHouse:
    NF3_URL = "https://nf3.sakura.ne.jp/Central/S/f/1_stat.htm"

    def __init__(self):
        try:
            # URLからHTMLデータを取得
            response = requests.get(self.NF3_URL)
            # HTMLデータをパース
            self.tree = html.fromstring(response.content)
        except Exception as e:
            print(e)

    def showData(self):
        try:
            # XPath の表現を扱う XPath オブジェクトを生成
            xPath = html.etree.XPathEvaluator(self.tree)
            xPath.register_namespace("h", "http://www.w3.org/1999/xhtml")

            # カウント別成績の tr 要素のリストを得る
            trList = xPath(
                "//h:div[@id='Cond2']/h:table[h:caption/h:div='カウント別成績']/h:tbody/h:tr"
            )

            print("カウント別成績")
            print()
            print("条件,    打率,打席,打数,安打,2塁,3塁,本塁,三振,四球,死球,犠打,犠飛,出塁率")
            for trNode in trList[1:]:  # 先頭の要素は除外
                th = trNode.find(
                    "h:th", namespaces={"h": "http://www.w3.org/1999/xhtml"}
                ).text
                print(th, end="")
                tdList = trNode.findall(
                    "h:td", namespaces={"h": "http://www.w3.org/1999/xhtml"}
                )
                for tdNode in tdList:
                    print(", " + tdNode.text, end="")
                print()
        except Exception as e:
            print(e)


def main():
    site = BaseballDataHouse()
    site.showData()


if __name__ == "__main__":
    main()
