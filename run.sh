#!/bin/bash

echo "🚀 正在启动 Spark + Jupyter 环境..."

# 启动容器（如果已在运行不会重复）
docker compose up -d

# 等待 Jupyter 容器完全启动
echo "⏳ 等待 Jupyter 容器启动..."
sleep 10

# 提取 token 登录地址
JUPYTER_URL=$(docker logs spark-jupyter 2>&1 | grep -o 'http://127.0.0.1:8888/lab?token=[a-z0-9]*' | tail -n1)

if [[ -z "$JUPYTER_URL" ]]; then
    echo "⚠️ 未能自动找到 Jupyter token 地址，您可以手动运行："
    echo "docker logs spark-jupyter"
    echo "并查找包含 token 的 URL"
else
    echo "✅ 成功获取 Jupyter 地址："
    echo "$JUPYTER_URL"

    # 自动打开浏览器（仅 macOS）
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open "$JUPYTER_URL"
    else
        echo "📝 请复制以上链接到浏览器打开"
    fi
fi