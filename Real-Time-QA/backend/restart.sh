#!/bin/bash

# 重启脚本 - 重启FastAPI应用

# 设置工作目录为脚本所在目录
cd "$(dirname "$0")"

echo "正在重启应用..."

# 先停止应用
./stop.sh

# 等待一会儿确保完全停止
sleep 2

# 启动应用
./deploy.sh

echo "重启完成！" 