# 🏫 校园 IT 社团综合 Web 平台

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Django](https://img.shields.io/badge/Django-5.0.3-green)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple)
![MySQL](https://img.shields.io/badge/Database-MySQL%20%7C%20SQLite-orange)

一个专为校园 IT 社团设计的综合性 Web 平台，集成了博客分享、匿名社交（盲盒）、好友互动及即时通讯功能。旨在促进社团成员之间的技术交流与校园内的社交互动。

[查看演示](https://github.com/zvdfgb/basic_web) · [报告 Bug](https://github.com/zvdfgb/basic_web/issues) · [提出新功能](https://github.com/zvdfgb/basic_web/issues)

</div>

---

## 📖 目录

- [项目简介](#-项目简介)
- [核心功能](#-核心功能)
- [技术栈](#-技术栈)
- [快速开始](#-快速开始)
- [项目结构](#-项目结构)
- [贡献指南](#-贡献指南)
- [开源协议](#-开源协议)

---

## 📝 项目简介

本项目是一个基于 Python Django 5.0.3 框架开发的全栈 Web 应用程序。主要服务于校园 IT 技术社团，为社团成员提供了一个展示自我、分享技术文章以及进行趣味社交的综合性平台。

### 主要特点

- 🎨 **现代化界面**：前端采用 Bootstrap 5 响应式设计，界面简洁美观，完美适配手机、平板和桌面设备
- 🔐 **安全可靠**：支持邮箱验证码注册，保障用户账户安全
- 💬 **社交互动**：集成好友系统、私信功能和盲盒交友，让校园社交更有趣
- 📝 **内容创作**：强大的富文本编辑器支持，轻松发布图文并茂的技术文章
- 🚀 **易于部署**：支持 SQLite 和 MySQL 数据库，可快速搭建开发和生产环境

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
- **随机匹配**：点击抽取，系统自动从用户池中随机匹配一位用户（排除已匹配和自己）
- **即时开启**：匹配成功后可直接查看对方基础信息
- **趣味社交**：增加校园社交的神秘感和趣味性

### 4. 💬 即时通讯
- **私信系统**：支持用户之间的一对一实时聊天
- **消息通知**：新消息及时提醒功能
- **聊天记录**：保存历史对话记录，方便随时查看

---

## 🛠 技术栈

### 后端 (Backend)
- **语言**：Python 3.10+
- **框架**：Django 5.0.3
- **数据库**：
  - SQLite3（开发环境默认，无需额外配置）
  - MySQL 8.0+（生产环境推荐）
- **依赖库**：
  - Pillow - 图像处理和上传
  - django - Web 框架核心

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

### 📋 环境要求

- Python 3.10 或更高版本
- pip（Python 包管理器）
- MySQL 8.0+（可选，如果使用 MySQL 数据库）
- Git

### 1. 📥 克隆项目

```bash
git clone https://github.com/zvdfgb/basic_web.git
cd basic_web
```

### 2. 🔧 创建并激活虚拟环境

建议使用虚拟环境以避免依赖冲突。

**Windows 系统：**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**Linux/macOS 系统：**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. 📦 安装依赖

```bash
pip install django pillow
```

> **注意**：项目主要依赖 Django 和 Pillow。如果项目根目录有 `requirements.txt` 文件，也可以使用：
> ```bash
> pip install -r requirements.txt
> ```

### 4. 🗄️ 数据库配置

#### 使用 SQLite（默认，推荐用于开发）

项目默认使用 SQLite3 数据库，无需额外配置，可直接进行下一步。

#### 使用 MySQL（推荐用于生产环境）

如果你希望使用 MySQL：

1. 确保已安装并启动 MySQL 服务
2. 创建数据库：
   ```sql
   CREATE DATABASE django_it CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
3. 在项目根目录的 `my.cnf` 文件中配置数据库连接信息
4. 在 `Django_IT/settings.py` 中切换数据库配置为 MySQL
5. 安装 MySQL 客户端：
   ```bash
   pip install mysqlclient
   ```

### 5. 🔄 迁移数据库

执行数据库迁移，创建必要的数据表：

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. 👤 创建超级管理员

创建管理员账户以访问 Django 后台管理系统：

```bash
python manage.py createsuperuser
```

按照提示输入用户名、邮箱和密码。

### 7. 🚀 启动开发服务器

```bash
python manage.py runserver
```

服务器启动成功后，在浏览器中访问：
- **前台首页**：http://127.0.0.1:8000
- **后台管理**：http://127.0.0.1:8000/admin

使用刚才创建的超级管理员账户登录后台。

### 8. 🎉 开始使用

现在您可以：
- 注册新用户账号
- 发布技术博客文章
- 添加好友并发送私信
- 尝试盲盒交友功能
- 通过后台管理系统管理内容

---

## 📂 项目结构

```text
basic_web/
├── blind_box/          # 盲盒交友应用模块
│   ├── models.py       # 数据模型（盲盒逻辑）
│   ├── views.py        # 视图函数（随机匹配逻辑）
│   └── templates/      # 盲盒页面模板
├── blog/               # 博客系统应用模块
│   ├── forms.py        # 表单定义（文章发布表单）
│   ├── models.py       # 数据模型（文章、评论、标签）
│   ├── views.py        # 视图函数（文章 CRUD 操作）
│   └── templates/      # 博客相关页面模板
├── mauth/              # 用户认证与社交应用模块
│   ├── models.py       # 数据模型（用户档案、好友、消息）
│   ├── views.py        # 视图函数（登录注册、好友管理）
│   └── templates/      # 用户相关页面模板
├── Django_IT/          # Django 项目主配置目录
│   ├── settings.py     # 全局配置文件
│   ├── urls.py         # 根路由配置
│   └── wsgi.py         # WSGI 部署配置
├── static/             # 静态资源目录
│   ├── css/            # 样式表文件
│   ├── js/             # JavaScript 脚本
│   └── images/         # 图片资源
├── templates/          # 全局 HTML 模板目录
│   └── base.html       # 基础模板
├── media/              # 用户上传文件目录
│   ├── avatars/        # 用户头像
│   └── covers/         # 文章封面图
├── manage.py           # Django 命令行管理工具
├── my.cnf              # MySQL 数据库配置文件
├── db.sqlite3          # SQLite 数据库文件（开发环境）
└── readme.md           # 项目说明文档（本文件）
```

---

## 🤝 贡献指南

我们欢迎并感谢任何形式的贡献！

### 如何贡献

1. **Fork 本仓库**
   
   点击页面右上角的 Fork 按钮，将项目复制到你的 GitHub 账户

2. **克隆到本地**
   ```bash
   git clone https://github.com/你的用户名/basic_web.git
   cd basic_web
   ```

3. **创建新分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或者修复 bug
   git checkout -b fix/your-bug-fix
   ```

4. **进行开发**
   - 编写代码
   - 添加必要的测试
   - 确保代码符合项目规范

5. **提交更改**
   ```bash
   git add .
   git commit -m "描述你的更改"
   git push origin feature/your-feature-name
   ```

6. **创建 Pull Request**
   
   在 GitHub 上提交 Pull Request，详细描述你的更改内容

### 贡献建议

- 🐛 报告 Bug：在 [Issues](https://github.com/zvdfgb/basic_web/issues) 页面提交详细的问题报告
- 💡 提出新功能：在 Issues 中描述你的想法和建议
- 📝 改进文档：帮助完善项目文档和注释
- 🔧 修复问题：查看现有 Issues 并提交修复方案
- ⭐ Star 项目：如果觉得项目有帮助，欢迎给个 Star！

---

## 📄 开源协议

本项目基于 [MIT License](LICENSE) 开源协议发布。

这意味着你可以自由地：
- ✅ 使用本项目进行商业或非商业用途
- ✅ 修改源代码以满足你的需求
- ✅ 分发原始或修改后的代码
- ✅ 将代码集成到你的项目中

唯一的要求是在软件和软件的所有副本中都必须包含版权声明和许可声明。

---

## 💬 联系方式

如有任何问题或建议，欢迎通过以下方式联系：

- 📧 提交 [Issue](https://github.com/zvdfgb/basic_web/issues)
- 🐙 访问 [GitHub 仓库](https://github.com/zvdfgb/basic_web)

---

## 🙏 致谢

感谢所有为本项目做出贡献的开发者！

感谢以下开源项目：
- [Django](https://www.djangoproject.com/) - 强大的 Python Web 框架
- [Bootstrap](https://getbootstrap.com/) - 优秀的前端 UI 框架
- [WangEditor](https://www.wangeditor.com/) - 轻量级富文本编辑器
- [Particles.js](https://particles.js.org/) - 炫酷的粒子背景效果库

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给它一个 Star！⭐**

Made with ❤️ by Campus IT Club

</div>
