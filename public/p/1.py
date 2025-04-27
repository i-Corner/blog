
import os
import re

def main():
    md_file = 'index.md'
    # 只匹配带有图片后缀的 Obsidian Wiki 链接
    img_pattern = re.compile(r'!\[\[([^\]]+\.(?:png|jpe?g|gif|svg))\]\]')

    # 读取 Markdown 内容
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    renamed = {}
    # 查找所有图片引用并重命名文件
    for match in img_pattern.findall(content):
        old_name = match
        new_name = old_name.replace(' ', '_')
        # 若文件存在且名称有变化，则重命名
        if old_name != new_name and os.path.exists(old_name):
            os.rename(old_name, new_name)
        renamed[old_name] = new_name

    # 用 Markdown 语法替换 Wiki 链接
    def repl(m):
        old = m.group(1)
        new = renamed.get(old, old)
        return f"![]({new})"

    new_content = img_pattern.sub(repl, content)

    # 写回 index.md
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print('图片链接及文件名处理完成。')

if __name__ == '__main__':
    main()

