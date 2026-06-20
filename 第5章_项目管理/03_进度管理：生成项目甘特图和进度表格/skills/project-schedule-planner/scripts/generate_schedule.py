#!/usr/bin/env python3
"""把项目任务 JSON 转成 CSV 进度表的最小示例。"""
import csv, json, sys
source = sys.argv[1] if len(sys.argv) > 1 else 'schedule-data.json'
target = sys.argv[2] if len(sys.argv) > 2 else 'project-schedule.csv'
with open(source, encoding='utf-8') as f:
    data = json.load(f)
fields = ['ID','阶段','任务','负责人','开始','结束','工期','依赖','状态','风险','备注']
with open(target, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(data.get('tasks', []))
print(target)
