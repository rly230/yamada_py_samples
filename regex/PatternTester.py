import re


def pattern_tester():
    print("テストする正規表現を入力してください。")
    pattern = re.compile(input())

    print("マッチさせる文字列を入力してください(Ctrl-dで終了)。")
    try:
        while True:
            next_line = input()  # 1行分の文字列を読み込む
            matcher = pattern.finditer(next_line)
            for match in matcher:
                print("マッチしました: " + match.group())
    except EOFError:  # Ctrl-d が押されたときに終了
        print("入力が終了しました。")


if __name__ == "__main__":
    pattern_tester()
