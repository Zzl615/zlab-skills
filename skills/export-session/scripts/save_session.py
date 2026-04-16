#!/usr/bin/env python3
"""
save_session.py — 将 stdin 读入的 Markdown 内容保存为文件。

用法：
    echo "<内容>" | python save_session.py [--path <输出路径>]

    --path  目标文件路径。省略时自动生成 session-YYYY-MM-DD.md（当前工作目录）。
            支持 ~ 展开和相对路径。
"""

import argparse
import os
import sys
from datetime import date


def main():
    parser = argparse.ArgumentParser(description="Save session markdown to file")
    parser.add_argument("--path", default=None, help="Output file path")
    args = parser.parse_args()

    content = sys.stdin.read()
    if not content.strip():
        print("Error: no content received from stdin", file=sys.stderr)
        sys.exit(1)

    if args.path:
        output_path = os.path.expanduser(args.path)
    else:
        filename = f"session-{date.today().isoformat()}.md"
        output_path = os.path.join(os.getcwd(), filename)

    # 创建父目录（如果不存在），避免因目录缺失而失败
    # 若父路径已存在但是一个文件（而非目录），提前报错，避免 os.makedirs 抛出
    # 令人困惑的 FileExistsError（exist_ok 只对已有目录生效，对文件无效）
    parent = os.path.dirname(output_path)
    if parent:
        if os.path.exists(parent) and not os.path.isdir(parent):
            print(f"Error: '{parent}' exists but is not a directory", file=sys.stderr)
            sys.exit(1)
        os.makedirs(parent, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Session saved to: {os.path.abspath(output_path)}")


if __name__ == "__main__":
    main()
