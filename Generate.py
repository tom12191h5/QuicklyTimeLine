import csv
from jinja2 import Template


def build_timeline(inputfile):
    # 1. 加载数据
    items = []
    with open(inputfile, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            items.append(row)

    # 2. 读取 Jinja2 模板文件 (这里为了演示直接写在变量里，你也可以用 open 读取)
    # 建议做法：template = Environment(loader=FileSystemLoader('.')).get_template('template.html')
    with open("template.html", "r", encoding="utf-8") as f:
        tmpl_content = f.read()

    template = Template(tmpl_content)

    # 3. 渲染数据
    result_html = template.render(items=items)

    # 4. 保存结果
    with open("result.html", "w", encoding="utf-8") as f:
        f.write(result_html)

    print("🚀 进阶版 HTML 生成成功！请查看 timeline_pro.html")


if __name__ == "__main__":
    build_timeline(input("输入文件名:"))