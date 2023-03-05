#!python3
# -*- coding:utf8 -*-

import os
import shutil

blog_path = '/Users/junjunyi/git-code/codeup-aliyun/blog/content'
src_path = '/Users/junjunyi/git-code/codeup-aliyun/book/src'
summary_md = 'SUMMARY.md'


def from_blog(only_md=False):
    for root, _, files in os.walk(blog_path, topdown=False):
        leaf_name = os.path.basename(root)

        index_md = os.path.join(root, '_index.md')
        dir_md = os.path.join(src_path, leaf_name + '.md')
        shutil.copy(index_md, dir_md)

        if only_md:
            continue

        webp_dir = os.path.join(src_path, 'webp', leaf_name)
        os.makedirs(webp_dir, exist_ok=True)

        for webp in [name for name in files if name.endswith(".webp")]:
            shutil.copy(os.path.join(root, webp), os.path.join(webp_dir, webp))


def change_webp():
    import glob
    import re

    webp_re = re.compile(r'!\[.*\]\((.*\.webp).*\)')
    md_list = glob.glob(os.path.join(src_path, "*.md"))
    for md_file in md_list:
        leaf_name = os.path.basename(md_file).strip('.md')
        found = False
        with open(md_file, encoding='utf-8') as f:
            # print('md_file', md_file, leaf_name)
            ctx = f.read()
            webp_list = [webp.group(1) for webp in webp_re.finditer(ctx)]
            for webp in webp_list:
                # print('webp', f'webp/{leaf_name}/{webp}')
                ctx = ctx.replace(webp, f'webp/{leaf_name}/{webp}')
                found = True

        if not found:
            continue
        with open(md_file, mode='w+', encoding='utf-8') as f:
            f.write(ctx)
        # break


def change_title():
    import glob
    import re

    src_path = '/Users/junjunyi/git-code/codeup-aliyun/book/src/golang'
    title_re = re.compile(r'title:\s*"(.*)"', re.M)
    md_list = glob.glob(os.path.join(src_path, "*.md"))
    for md_file in md_list:
        if md_file == summary_md:
            continue
        leaf_name = os.path.basename(md_file).strip('.md')
        with open(md_file, encoding='utf-8') as f:
            ctx = f.read()
        with open(md_file, mode='w+', encoding='utf-8') as f:
            title_line = title_re.search(ctx)
            if title_line is None:
                print('md_file', md_file, leaf_name)
                continue
            new_title = '# ' + title_line.group(1)
            ctx = ctx.replace(title_line.group(0), new_title)
            # print(leaf_name, title_line.group(0), new_title)
            f.write(ctx)


def change_mermaid():
    import glob
    import re

    src_path = '/Users/junjunyi/git-code/codeup-aliyun/book/src/golang'
    begin_mermaid_re = re.compile(r'\{\s*\{\s*<\s*mermaid\s*>\s*\}\s*\}', re.M)
    end_mermaid_re = re.compile(r'\{\s*\{\s*<\s*/mermaid\s*>\s*\}\s*\}', re.M)
    md_list = glob.glob(os.path.join(src_path, "*.md"))
    for md_file in md_list:
        if md_file == summary_md:
            continue
        ctx = []
        found = False
        with open(md_file, encoding='utf-8') as f:
            for line in f:
                if begin_mermaid_re.search(line):
                    ctx.append('```mermaid\n')
                    found = True
                elif end_mermaid_re.search(line):
                    ctx.append('```\n')
                    found = True
                else:
                    ctx.append(line)

        if not found:
            continue
        with open(md_file, mode='w+', encoding='utf-8') as f:
            f.writelines(ctx)


def summary():
    import glob
    import re

    title_re = re.compile(r'#\s*(.*)', re.M)
    md_list = glob.glob(os.path.join(src_path, "*.md"))
    line_list = []
    for md_file in md_list:
        leaf_name = os.path.basename(md_file)
        if leaf_name == summary_md:
            continue
        only_name = leaf_name.strip('.md')
        with open(md_file) as f:
            title = title_re.search(f.read())
            if title:
                only_name = title.group(1)
        line_list.append(f'[{only_name}]({leaf_name})\n')

    with open('src/SUMMARY.md', mode='w+', encoding='utf-8') as summary_file:
        summary_file.writelines(line_list)


if __name__ == '__main__':
    pass
    # from_blog(only_md=True)
    # change_webp()
    # change_title()
    # change_mermaid()
    # summary()