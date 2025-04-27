
import os
import re

IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.svg')

def main():
    md_file = 'index.md'

    # 1. 扫描当前目录中的图片文件，删除文件名中的空格，并重命名
    renamed = {}
    for fname in os.listdir('.'):
        if fname.lower().endswith(IMAGE_EXTENSIONS) and ' ' in fname:
            new_fname = fname.replace(' ', '')
            os.rename(fname, new_fname)
            renamed[fname] = new_fname

    # 2. 读取 Markdown 内容
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 3. 替换 Obsidian Wiki 链接为 Markdown 语法
    #    并应用文件名映射
    img_pattern = re.compile(r'!\[\[([^\]]+\.(?:png|jpe?g|gif|svg))\]\]')
    def repl(m):
        old = m.group(1)
        new = renamed.get(old, old)
        return f"![]({new})"
    new_content = img_pattern.sub(repl, content)

    # 4. 替换内容中所有其他直接文件名引用（如 ![](old name.png) 或裸文件名）
    for old, new in renamed.items():
        new_content = new_content.replace(old, new)

    # 5. 写回 index.md
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print('所有图片文件及引用已删除空格并更新为 Markdown 语法。')

if __name__ == '__main__':
    main()

