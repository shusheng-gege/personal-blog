# personal-blog

# 个人博客系统 (FastAPI + SQLite)

## 项目简介
这是一个极简轻量的个人博客后端系统，基于 FastAPI 框架开发，使用 SQLite 作为数据库并通过原生 SQL 操作数据。系统采用单管理员权限设计，集成 Quill 富文本编辑器，支持文章的完整增删改查与本地图片上传，适合作为个人独立博客的快速建站方案或 FastAPI 全栈学习项目。

## 技术栈
| 模块 | 技术选型 |
|------|----------|
| 后端框架 | FastAPI |
| 数据库 | SQLite |
| 数据库操作 | 原生 SQL |
| 权限设计 | 单管理员模式 |
| 富文本编辑 | Quill 编辑器 |
| 内容存储 | 正文保存 HTML 格式 |
| 图片存储 | 本地 uploads/ 目录 |

## 核心功能
✅ 文章列表页：按时间倒序展示所有文章标题与摘要
✅ 文章详情页：完整展示富文本内容与图片
✅ 后台管理：单管理员登录后，支持新增、编辑、删除文章
✅ 富文本编辑：集成 Quill 编辑器，支持排版、图片插入等
✅ 图片上传：自动保存到本地 uploads/ 目录并返回访问链接
✅ 轻量部署：基于 SQLite，无需额外配置数据库服务

## 快速开始
1. 克隆项目：`git clone [(https://github.com/shusheng-gege/personal-blog.git)]`
2. 安装依赖：`pip install fastapi uvicorn python-multipart`
3. 启动服务：`uvicorn main:app --reload`
4. 访问接口文档：`http://127.0.0.1:8000/docs`
