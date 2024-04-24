# 数字混响师——卡拉 OK 混响系统

- [数字混响师——卡拉 OK 混响系统](#数字混响师——卡拉OK混响系统)
  - [🌍 运行环境](#运行环境)
  - [⚡️ 快速开始](#️快速开始)
    - [1. 安装](#1-安装)
    - [2. 使用](#2-使用)

## 🌍 运行环境

推荐环境：

- Python 3.12+
- Poetry 1.8.2+
- Vue 3.0+
- pnpm 8.15.7+
- sox 14.4.2+

[sox 下载地址](https://www.videohelp.com/download/sox-14.4.0-libmad-libmp3lame.zip)(带有 libmad.dll 和 libmp3lame.dll，否则无法处理 mp3 文件)

## ⚡️ 快速开始

### <a name="1"></a>1. 安装

克隆本项目并进入项目根目录

```bash
git clone https://github.com/ylingu/DigitalSignalProcessing_SoA.git
cd DigitalSignalProcessing_SoA
```

安装依赖

```bash
cd backend && poetry install
cd frontend && pnpm install
```

### <a name="2"></a>2. 使用

运行后端示例(基础实验)

```bash
cd backend
poetry run exp
```

运行前端示例(Vue 示例)

```bash
cd frontend
pnpm run dev
```
