import csv
import sys
import os

# 读取 GitHub Actions 提供的环境变量，用于生成可视化表格
GITHUB_STEP_SUMMARY = os.environ.get('GITHUB_STEP_SUMMARY')

THRESHOLD_P95 = 300      # 阈值 300ms
THRESHOLD_ERROR_RATE = 0.01 # 错误率 1%

jtl_path = "result.jtl"
elapsed_times = []
errors = 0

with open(jtl_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        elapsed_times.append(int(row['elapsed']))
        if row['success'] == 'false':
            errors += 1

total = len(elapsed_times)
elapsed_times.sort()
p95 = elapsed_times[int(total * 0.95)]
error_rate = errors / total

# 生成 Markdown 格式的汇报表格
status_icon = "✅ Pass" if (p95 <= THRESHOLD_P95 and error_rate <= THRESHOLD_ERROR_RATE) else "❌ Fail"
markdown_summary = f"""
### 🚦 性能门禁执行结果: {status_icon}

| 指标 | 实际值 | 阈值 | 状态 |
| :--- | :--- | :--- | :--- |
| **总请求数** | {total} | - | - |
| **P95 耗时** | {p95} ms | <= {THRESHOLD_P95} ms | {'🟢' if p95 <= THRESHOLD_P95 else '🔴'} |
| **错误率** | {error_rate * 100:.2f}% | <= {THRESHOLD_ERROR_RATE * 100}% | {'🟢' if error_rate <= THRESHOLD_ERROR_RATE else '🔴'} |
"""

print(markdown_summary)

# 将表格写入 GitHub 页面的 Summary 面板
if GITHUB_STEP_SUMMARY:
    with open(GITHUB_STEP_SUMMARY, 'a', encoding='utf-8') as f:
        f.write(markdown_summary)

if p95 > THRESHOLD_P95 or error_rate > THRESHOLD_ERROR_RATE:
    print("\n🚨 性能门禁未通过，流水线阻断！")
    sys.exit(1)
else:
    print("\n✅ 性能门禁通过，允许部署！")
    sys.exit(0)