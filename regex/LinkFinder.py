import re


def link_finder():
    pattern = re.compile(r'href="(.+?)"')
    matcher = pattern.search('<a href="index.html">トップへ</a>')

    if matcher:
        print(matcher.group(1))


if __name__ == "__main__":
    link_finder()
