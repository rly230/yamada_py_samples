import os
import re

from lxml import etree
import pandas as pd
import requests
import sudachipy as sudachi
from sudachipy import SplitMode as mode

emotion_name_map = {}
emotion_map_list = []

# 感情辞書の読み込み
def read_emotion_dict(filename):
    global emotion_name_map, emotion_map_list

    # パスの結合
    file_path = os.path.join(os.path.dirname(__file__), filename)
    # データフレームに読み込み
    wb = pd.read_excel(file_path, sheet_name=None)

    emotion_map_list = []

    for sheet_name in wb.keys():
        if sheet_name == "感情分類":
            # 感情記号-感情分類名のdictを生成
            emotion_name_map = {row.iloc[0]: row.iloc[1] for index, row in wb[sheet_name].iterrows()}
        else:
            # 1作業者の感情表現-感情dictを生成
            emotions_map = {row.iloc[0]: row.iloc[2] for index, row in wb[sheet_name].iterrows()}
            emotion_map_list.append(emotions_map)

# XML文書（URL指定) からの要素リストの抽出
def get_node_list(url_string, xpath_string, encoding="utf-8"):
    # フィードに接続
    responce = requests.get(url_string)
    # DOMツリーの構築
    dom = etree.fromstring(responce.text.encode(encoding))
    # XPathにより要素のリストを得る
    node_list = dom.xpath(xpath_string, namespaces=dom.nsmap)

    return node_list

# 指定した語が指定した感情のうちの少なくとも1つを持っていると判断した作業者数を返す
def get_emotion_count(word, symbols):
    count = 0
    for emotions_map in emotion_map_list:
        if len(set(emotions_map.get(word, "")) & set(symbols)) > 0:
            count += 1

    return count

#  デモ用main関数
def main():
    # 辞書の読み込み
    read_emotion_dict("D18-2018.7.24.xlsx")

    # 解析対象のフィード
    url_string = "https://www.cosme.net/latest-reviews/format/rss"
    # フィードの解析
    node_list = get_node_list(url_string, "//item/content:encoded")
    # sudachiの準備
    tokenizer = sudachi.Dictionary().create()

    # アッパーな感情の例
    upper_emotions = ("安", "楽", "親", "尊", "感", "気", "誇", "動", "喜", "好", "幸", "祝", "穏")

    # 各要素を形態素解析
    for node in node_list:
        # 要素の内容をプレーンテキストとして得る
        node_string = re.sub("<.+?>", "", node.text)
        print(f"Text: {node_string}")
        # 形態素解析
        for morpheme in tokenizer.tokenize(node_string, mode=mode.C):  # 文単位で形態素リストへ
            #pos0 = morpheme.part_of_speech()[0]    # 品詞
            word = morpheme.dictionary_form()   # 原型
            emotion_count = get_emotion_count(word, upper_emotions) # wordをupperと評価した人数
            if emotion_count > 0:
                print(f"\t{word}: {emotion_count}")
        print()

if __name__ == "__main__":
    main()
