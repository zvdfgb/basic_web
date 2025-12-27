# 🏫 校园 IT 社团综合 Web 平台 (Campus IT Club Platform)

<div align="center">

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Django](https://img.shields.io/badge/Django-5.0.3-green)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple)
![MySQL](https://img.shields.io/badge/Database-MySQL%20%7C%20SQLite-orange)

一个专为校园 IT 社团设计的综合性 Web 平台，集成了博客分享、匿名社交（盲盒）、好友互动及即时通讯功能。旨在促进社团成员技术交流与校园内的社交互动。

[查看演示](#) · [报告 Bug](#) · [提出新功能](#)

</div>

---

## 📖 目录

- [项目简介](#-项目简介)
- [核心功能](#-核心功能)
- [技术栈](#-技术栈)
- [快速开始](#-快速开始)
- [项目结构](#-项目结构)
- [贡献指南](#-贡献指南)

---

## 📝 项目简介

本项目是一个基于 Python Django 框架开发的全栈 Web 应用。主要服务于校园 IT 技术社团，提供了一个成员展示自我、分享技术文章以及进行趣味社交的平台。前端采用 Bootstrap 5 响应式设计，界面简洁现代，适配多种设备。

## ✨ 核心功能

### 1. 👤 用户中心 (Mauth)
- **注册与登录**：支持邮箱验证码注册，保障账户真实性。
- **个人资料管理**：自定义头像、昵称、个性签名、性别、年龄及地区。
- **隐私设置**：用户可选择是否公开个人主页。
- **社交互动**：
  - 好友系统：发送、接受或拒绝好友请求。
  - 好友列表管理。

### 2. 📝 博客系统 (Blog)
- **文章发布**：集成 **WangEditor** 富文本编辑器，支持图文混排。
- **互动交流**：支持多级评论回复、文章点赞功能。
- **分类与标签**：通过标签系统对文章进行归档管理。
- **个性化封面**：支持上传自定义文章封面图。

### 3. 🎁 盲盒交友 (Blind Box)
- **随机匹配**：点击抽取，系统自动从用户池中随机匹配一位异性或同好（排除自己）。
- **即时开启**：匹配成功后可直接查看对方基础信息。

### 4. 💬 即时通讯
- **私信系统**：支持用户间的一对一实时聊天。
- **消息通知**：(开发中) 新消息提醒。

---

## 🛠 技术栈

### 后端 (Backend)
- **语言**：Python 3.13+
- **框架**：Django 5.0.3
- **数据库**：SQLite (开发环境默认) / MySQL (生产环境支持)
- **工具库**：Pillow (图像处理), Requests

### 前端 (Frontend)
- **基础框架**：HTML5, CSS3, JavaScript (ES6+)
- **UI 框架**：Bootstrap 5
- **库/插件**：
  - jQuery 3.7.1
  - WangEditor (富文本编辑器)
  - Particles.js (粒子背景特效)

---

## 🚀 快速开始

请按照以下步骤在本地搭建开发环境。

### 环境要求
- Python 3.10 或更高版本
- MySQL 8.0+ (如果选择使用 MySQL)

### 1. 克隆项目
```bash
git clone https://github.com/yourusername/Django_IT.git
cd Django_IT
```

### 2. 创建并激活虚拟环境
建议使用虚拟环境以避免依赖冲突。

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 数据库配置
项目默认使用 `sqlite3`。如果你希望使用 **MySQL**，请确保已安装 MySQL 并在项目根目录的 `my.cnf` 中配置好数据库连接信息，然后在 `Django_IT/settings.py` 中切换数据库配置。

### 5. 迁移数据库
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. 创建超级管理员
```bash
python manage.py createsuperuser
```

### 7. 启动服务器
```bash
python manage.py runserver
```
访问 http://127.0.0.1:8000 即可看到项目首页。

---

## 📂 项目结构

```text
Django_IT/
├── blind_box/          # 盲盒交友应用
│   ├── models.py       # 盲盒逻辑
│   └── views.py        # 随机匹配视图
├── blog/               # 博客应用
│   ├── forms.py        # 文章表单
│   ├── models.py       # 文章、评论、标签模型
│   └── templates/      # 博客相关页面
├── mauth/              # 用户认证与社交应用
│   ├── models.py       # 用户档案、好友、消息模型
│   └── views.py        # 登录注册、好友管理逻辑
├── Django_IT/          # 项目主配置
│   ├── settings.py     # 全局配置
│   └── urls.py         # 根路由
├── static/             # 静态资源 (CSS, JS, Images)
├── templates/          # 全局 HTML 模板
├── manage.py           # Django 命令行工具
├── requirements.txt    # 项目依赖列表
└── readme.md           # 项目说明文档
```

---

## 🤝 贡献指南

欢迎提交 Pull Request 或 Issue！

1. Fork 本仓库
2. 新建 Feat_xxx 分支
3. 提交代码
4. 新建 Pull Request

---

## 📄 开源协议

本项目遵循 MIT 开源协议。
