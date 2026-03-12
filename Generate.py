import csv
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from jinja2 import Template
import os


class TimelineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("时间轴数据编辑器 v2.0")
        self.root.geometry("800x600")

        self.current_file = None

        self.setup_ui()

    def setup_ui(self):
        # --- 顶部按钮栏 ---
        top_frame = tk.Frame(self.root, pady=10)
        top_frame.pack(fill=tk.X)

        tk.Button(top_frame, text="打开 CSV", command=self.load_csv).pack(side=tk.LEFT, padx=5)
        tk.Button(top_frame, text="保存 CSV", command=self.save_csv, bg="#e1f5fe").pack(side=tk.LEFT, padx=5)
        tk.Button(top_frame, text="生成 HTML", command=self.generate_html, bg="#4CAF50", fg="white").pack(side=tk.RIGHT, padx=10)

        # --- 中间表格区域 ---
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("year", "title", "subtitle", "description"),
            show='headings'
        )

        self.tree.heading("year", text="年份")
        self.tree.heading("title", text="标题")
        self.tree.heading("subtitle", text="副标题")
        self.tree.heading("description", text="描述")

        self.tree.column("year", width=60, anchor=tk.CENTER)
        self.tree.column("title", width=150)
        self.tree.column("subtitle", width=150)
        self.tree.column("description", width=300)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # --- 编辑区域 ---
        edit_frame = tk.LabelFrame(self.root, text="编辑/添加数据", padx=10, pady=10)
        edit_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(edit_frame, text="年份:").grid(row=0, column=0)
        self.ent_year = tk.Entry(edit_frame, width=10)
        self.ent_year.grid(row=0, column=1, padx=5)

        tk.Label(edit_frame, text="标题:").grid(row=0, column=2)
        self.ent_title = tk.Entry(edit_frame, width=15)
        self.ent_title.grid(row=0, column=3, padx=5)

        tk.Label(edit_frame, text="副标题:").grid(row=0, column=4)
        self.ent_subtitle = tk.Entry(edit_frame, width=15)
        self.ent_subtitle.grid(row=0, column=5, padx=5)

        tk.Label(edit_frame, text="描述:").grid(row=1, column=0, pady=5)
        self.ent_desc = tk.Entry(edit_frame, width=60)
        self.ent_desc.grid(row=1, column=1, columnspan=5, sticky="w", padx=5)

        btn_frame = tk.Frame(edit_frame)
        btn_frame.grid(row=2, column=0, columnspan=6, pady=10)

        tk.Button(btn_frame, text="添加/更新选中行", command=self.add_or_update).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="删除选中行", command=self.delete_item, fg="red").pack(side=tk.LEFT, padx=10)

        # 绑定选择事件
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    # --- 加载CSV ---
    def load_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not path:
            return

        self.current_file = path
        self.tree.delete(*self.tree.get_children())

        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.tree.insert(
                    "",
                    tk.END,
                    values=(row['year'], row['title'], row['subtitle'], row['description'])
                )

        messagebox.showinfo("加载成功", f"已加载: {os.path.basename(path)}")

    # --- 添加或更新 ---
    def add_or_update(self):
        year = self.ent_year.get()
        title = self.ent_title.get()
        sub = self.ent_subtitle.get()
        desc = self.ent_desc.get()

        if not year or not title:
            messagebox.showwarning("提示", "年份和标题不能为空")
            return

        selected = self.tree.selection()

        if selected:
            self.tree.item(selected[0], values=(year, title, sub, desc))
        else:
            self.tree.insert("", tk.END, values=(year, title, sub, desc))

        # 清空输入框
        for entry in [self.ent_year, self.ent_title, self.ent_subtitle, self.ent_desc]:
            entry.delete(0, tk.END)

        # 取消选中（关键修复）
        self.tree.selection_remove(self.tree.selection())

    # --- 删除 ---
    def delete_item(self):
        selected = self.tree.selection()
        if not selected:
            return

        if messagebox.askyesno("确认", "确定删除选中行吗？"):
            for item in selected:
                self.tree.delete(item)

    # --- 选中表格行 ---
    def on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0])['values']

        self.ent_year.delete(0, tk.END)
        self.ent_year.insert(0, values[0])

        self.ent_title.delete(0, tk.END)
        self.ent_title.insert(0, values[1])

        self.ent_subtitle.delete(0, tk.END)
        self.ent_subtitle.insert(0, values[2])

        self.ent_desc.delete(0, tk.END)
        self.ent_desc.insert(0, values[3])

    # --- 保存CSV ---
    def save_csv(self):
        if self.current_file:
            path = self.current_file
        else:
            path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV Files", "*.csv")]
            )
            if not path:
                return
            self.current_file = path

        with open(path, "w", encoding="utf-8", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["year", "title", "subtitle", "description"])

            for child in self.tree.get_children():
                writer.writerow(self.tree.item(child)['values'])

        messagebox.showinfo("保存成功", f"数据已保存至: {path}")

    # --- 生成HTML ---
    def generate_html(self):
        items = []

        for child in self.tree.get_children():
            v = self.tree.item(child)['values']
            items.append({
                "year": v[0],
                "title": v[1],
                "subtitle": v[2],
                "description": v[3]
            })

        if not items:
            messagebox.showwarning("空数据", "没有数据可以生成！")
            return

        try:
            if not os.path.exists("template.html"):
                messagebox.showerror("错误", "找不到 template.html 模板文件")
                return

            with open("template.html", "r", encoding="utf-8") as f:
                template = Template(f.read())

            result_html = template.render(items=items)

            with open("result.html", "w", encoding="utf-8") as f:
                f.write(result_html)

            messagebox.showinfo("成功", "🚀 HTML 生成成功！\n请查看同目录下的 result.html")

        except Exception as e:
            messagebox.showerror("错误", f"渲染失败: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = TimelineApp(root)
    root.mainloop()