#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
不和谐家庭关系自助干预工具
单文件版 · 零依赖（可选 matplotlib 画图）
"""
import os
import time
import csv
import json
import datetime as dt
from pathlib import Path

# ---------- 基础工具 ----------
HOME = Path.home() / "harmony_recovery"
HOME.mkdir(exist_ok=True)
LOG_CSV = HOME / "log.csv"
LOG_TXT = HOME / "diary.txt"
CONFIG = HOME / "config.json"

def log_diary(text: str):
    with open(LOG_TXT, "a", encoding="utf-8") as f:
        f.write(f"{dt.datetime.now():%Y-%m-%d %H:%M:%S}  {text}\n")

def log_csv(row: dict):
    fieldnames = ["date", "phase", "item", "score", "note"]
    first_write = not LOG_CSV.exists()
    with open(LOG_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if first_write:
            writer.writeheader()
        writer.writerow(row)

def input_int(prompt, minv=0, maxv=10):
    while True:
        try:
            val = int(input(prompt))
            if minv <= val <= maxv:
                return val
        except ValueError:
            pass
        print(f"请输入 {minv}-{maxv} 之间的整数")

def countdown_animation(seconds: int, msg: str = "倒计时"):
    """终端动画倒计时，用于情绪饱和训练"""
    for i in range(seconds, 0, -1):
        print(f"\r{msg} {i}s ", end="", flush=True)
        time.sleep(1)
    print("\r" + " " * 20 + "\r", end="")

# ---------- 四步核心流程 ----------
def phase_1_awareness():
    print("\n====== 阶段① 觉察练习 ======")
    mood = input("今天最强烈的情绪是（如：愤怒/委屈/麻木）：")
    body = input("身体哪里最有感觉（如：喉咙紧/胃胀/手抖）：")
    trigger = input("触发事件（一句话）：")
    intensity = input_int("情绪强度 0-10：")
    log_csv({"date": today, "phase": "觉察", "item": "情绪强度", "score": intensity, "note": f"{mood}|{body}|{trigger}"})
    log_diary(f"觉察：{mood} 强度{intensity} 身体{body} 触发{trigger}")
    print("→ 已记录，明天继续。\n")

def phase_2_disidentify():
    print("\n====== 阶段② 去认同（正念呼吸） ======")
    print("坐下，脊柱挺直。跟我做：吸气 4 秒 → 屏住 2 秒 → 呼气 6 秒")
    for cycle in range(1, 6):
        print(f"第{cycle}/5 轮")
        countdown_animation(4, "吸气")
        countdown_animation(2, "屏住")
        countdown_animation(6, "呼气")
    log_csv({"date": today, "phase": "去认同", "item": "正念呼吸", "score": 5, "note": "完成5轮"})
    log_diary("完成正念呼吸5轮")
    print("→ 心率应有所下降，继续。\n")

def phase_3_rewrite():
    print("\n====== 阶段③ 重写入（情绪饱和训练） ======")
    print("① 闭眼回忆童年冲突画面，让情绪冲到峰值（最多30s）")
    input("准备好后按回车开始...")
    countdown_animation(30)
    print("② 想象你走过去，把年幼的自己带离现场，父母被静音")
    print("③ 重复 7 次（每次≤2min，自动计时）")
    for r in range(1, 8):
        print(f"第{r}/7 轮")
        countdown_animation(30)   # 峰值
        countdown_animation(90)   # 新结局
    log_csv({"date": today, "phase": "重写入", "item": "情绪饱和", "score": 7, "note": "完成7轮"})
    log_diary("完成情绪饱和训练7轮")
    print("→ 新结局已写入，继续。\n")

def phase_4_external():
    print("\n====== 阶段④ 外化测试 ======")
    print("今天主动提一次需求/边界，即使对方拒绝也算成功")
    demand = input("你提的需求/边界是：")
    anxiety = input_int("提之前焦虑 0-10：")
    after = input_int("提之后自我评分 0-10：")
    log_csv({"date": today, "phase": "外化", "item": "提需求焦虑", "score": anxiety, "note": demand})
    log_csv({"date": today, "phase": "外化", "item": "提后自评", "score": after, "note": demand})
    log_diary(f"外化：提需求『{demand}』焦虑{anxiety}→自评{after}")
    print("→ 已记录，恭喜完成一轮外化！\n")

# ---------- 每周自检雷达图 ----------
def weekly_check():
    print("\n====== 每周 3 分钟自检表 ======")
    week = dt.date.today().isocalendar()[1]
    a = input_int("① 本周情绪失控次数 0-10：")
    b = input_int("② 平均恢复小时数 0-10（小时÷2 取整）：")
    c = input_int("③ 自己值得被爱相信度 0-10：")
    log_csv({"date": today, "phase": "自检", "item": "失控次数", "score": a, "note": f"week{week}"})
    log_csv({"date": today, "phase": "自检", "item": "恢复小时", "score": b, "note": f"week{week}"})
    log_csv({"date": today, "phase": "自检", "item": "值得被爱", "score": c, "note": f"week{week}"})
    try:
        import matplotlib.pyplot as plt
        labels = ["失控次数", "恢复小时", "值得被爱"]
        values = [a, b, c]
        angles = [n / 3 * 2 * 3.14159 for n in range(3)]
        values += values[:1]
        angles += angles[:1]
        plt.figure(figsize=(3, 3))
        plt.polar(angles, values, 'o-')
        plt.xticks(angles[:-1], labels)
        plt.ylim(0, 10)
        plt.title(f"第{week}周自检")
        png = HOME / f"week{week}.png"
        plt.savefig(png, dpi=120)
        plt.close()
        print(f"→ 雷达图已保存：{png}")
    except ImportError:
        print("（未安装 matplotlib，跳过画图）")
    print("→ 自检完成，建议每 4 周对比一次趋势。\n")

# ---------- 主菜单 ----------
MENU = """
请选择：
1 阶段① 觉察
2 阶段② 去认同（正念）
3 阶段③ 重写入（情绪饱和）
4 阶段④ 外化测试
5 每周自检表
6 查看历史日志
0 退出
"""

def show_history():
    if not LOG_CSV.exists():
        print("暂无记录")
        return
    with open(LOG_CSV, encoding="utf-8") as f:
        print("\n日期       阶段   条目        分数 备注")
        for row in csv.DictReader(f):
            print(f"{row['date']} {row['phase']:>4} {row['item']:>10} {row['score']:>4} {row['note']}")

def main():
    global today
    today = str(dt.date.today())
    print("=== 不和谐家庭关系自助干预工具 ===")
    print("数据目录：", HOME)
    while True:
        print(MENU, end="")
        choice = input("> ").strip()
        if choice == "1":
            phase_1_awareness()
        elif choice == "2":
            phase_2_disidentify()
        elif choice == "3":
            phase_3_rewrite()
        elif choice == "4":
            phase_4_external()
        elif choice == "5":
            weekly_check()
        elif choice == "6":
            show_history()
        elif choice == "0":
            print("祝你温柔坚定，我们下次再见。")
            break
        else:
            print("输入 0-6 之间的数字")

if __name__ == "__main__":
    main()