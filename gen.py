#!python3
# -*- coding:utf8 -*-


def insert_toc():
    from pathlib import Path

    path = Path("src")
    for item in path.rglob("*"):
        if not item.is_file():
            continue

        if item.suffix != ".md":
            continue

        with open(item, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # 在第二行（索引1）插入两个新行
        lines.insert(1, "<!-- toc --> \n")

        # print("lines", lines[:4])

        with open(item, "w", encoding="utf-8") as f:
            f.writelines(lines)


if __name__ == "__main__":
    pass
    insert_toc()
