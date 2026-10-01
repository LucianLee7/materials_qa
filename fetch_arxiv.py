import requests
import xml.etree.ElementTree as ET
import json
from pathlib import Path

# 设置 API 地址和查询条件
url = "https://export.arxiv.org/api/query"

params = {
    "search_query": "cat:cond-mat.mtrl-sci",
    "start": 0,
    "max_results": 1500,
    "sortBy": "submittedDate",
    "sortOrder": "descending",
}

# 发送请求，检查 HTTP 错误
response = requests.get(url, params=params, timeout=60)
response.raise_for_status()

print("Request URL:", response.url)
print("HTTP status code:", response.status_code)

# 解析 XML，并设置 Atom 命名空间
root = ET.fromstring(response.content)

namespaces = {
    "atom": "http://www.w3.org/2005/Atom",
}

entries = root.findall("atom:entry", namespaces)

print("Number of records returned:", len(entries))

papers = []
# 提取论文信息，保留摘要原文
for entry in entries:
    arxiv_url = entry.findtext("atom:id", namespaces=namespaces)
    title = entry.findtext("atom:title", namespaces=namespaces)
    abstract = entry.findtext("atom:summary", namespaces=namespaces)
    published = entry.findtext("atom:published", namespaces=namespaces)
    updated = entry.findtext("atom:updated", namespaces=namespaces)
    paper = {
        "source_url": arxiv_url,
        "title": title,
        "abstract": abstract,
        "published": published, 
        "updated": updated
    }
    papers.append(paper)

# 创建原始数据目录
output_dir = Path("data/raw")
output_dir.mkdir(parents=True, exist_ok=True)

output_path = output_dir / "arxiv_sample.jsonl"

# 每一行保存一个完整的 JSON 对象
with output_path.open("w", encoding="utf-8") as file:
    for paper in papers:
        file.write(json.dumps(paper, ensure_ascii=False) + "\n")

print(f"Saved {len(papers)} records to {output_path}")