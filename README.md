TextRank Keyword Extractor – Cloud Computing Project

这个项目是一个基于 PySpark + Streamlit + Docker 的关键词提取平台，实现了经典论文 TextRank 所提出的无监督关键词提取算法。

支持上传 .pdf、.txt 或直接输入文本进行关键词分析。后端支持分布式 PySpark 处理，前端为交互式 Streamlit 应用。


✅ 已实现功能

🔧 技术架构
	•	Docker Compose 多容器部署
	•	Spark Master + Worker（分布式任务调度）
	•	Jupyter Notebook（用于调试 PySpark 算法）
	•	Streamlit Web App（用户界面）
	•	基于 TextRank 的关键词提取
	•	基于共现窗口构建词图
	•	使用 PageRank 算法评分关键词
	•	支持多词短语合并
	•	文本处理
	•	支持上传 .txt 和 .pdf 文件
	•	支持直接输入文本
	•	前端（Streamlit）
	•	实时显示提取结果
	•	关键词输出支持手动查看


🗂 项目结构

nlg-docker/
├── data/                  # 文本输入样本（挂载给前后端）
│   └── text_corpus.txt
├── docker-compose.yml     # 管理所有服务
├── frontend/              # Streamlit 前端服务
│   ├── app.py             # 主应用入口
│   ├── utils.py           # TextRank 核心逻辑
│   ├── Dockerfile
│   └── requirements.txt
├── jupyter/               # Jupyter + Spark 容器配置
│   ├── Dockerfile
│   └── requirements.txt
├── notebooks/             # PySpark 原型代码
│   └── textrank_demo.py
└── README.md              # 当前文档


🚀 启动方式

确保你已安装 Docker & Docker Compose。

# 克隆项目后在项目根目录执行
docker-compose up --build

启动成功后访问：

服务	地址
📊 Streamlit	http://localhost:8501
🧪 Jupyter	http://localhost:8888
🖥 Spark UI	http://localhost:8080



⸻

✍️ 使用方式（前端）
	1.	打开 http://localhost:8501
	2.	上传 .pdf / .txt 文件或直接粘贴文本
	3.	点击 “🔍 Extract Keywords”
	4.	查看关键词结果

⸻

🛠️ TODO / 下一步计划

功能	状态
Streamlit 关键词提取基本功能	✅ 已完成
PDF / TXT 支持	✅ 已完成
Jupyter + PySpark 本地调试	✅ 已完成
Docker 多服务部署	✅ 已完成
💾 关键词导出为 CSV	🔜 推荐添加
🌈 添加关键词词云图	🔜 推荐添加
🔗 接入 PySpark 后端服务	🔜 规划中（REST API 接 Spark）
☁️ 接入 HDFS 支持海量文本	🔜 可选目标
🧠 替换为 KeyBERT / YAKE 等高级模型	🧪 未来可拓展



⸻

📚 参考资源
	•	TextRank 原始论文：Mihalcea & Tarau, 2004
	•	Streamlit 官方文档：https://docs.streamlit.io
	•	Spark 中文站：https://spark.apachecn.org

