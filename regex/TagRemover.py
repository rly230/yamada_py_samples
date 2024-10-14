import re
import requests


def tag_remover():
    try:
        url = "https://www.mlab.im.dendai.ac.jp/wiki/index.php"
        response = requests.get(url)
        response.encoding = "utf-8"

        pattern = re.compile(r"<.+?>")

        lines = response.text.splitlines()
        for line in lines:
            plain_text = pattern.sub("", line)
            if plain_text.strip():
                print(plain_text)

    except Exception as e:
        print(f"エラーが発生しました: {e}")


if __name__ == "__main__":
    tag_remover()
