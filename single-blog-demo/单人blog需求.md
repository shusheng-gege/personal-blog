

方案 A 冻结版需求

核心目标：

用 FastAPI 做一个最小可运行的单人博客后台 Demo。  
支持管理员登录、文章发布、富文本编辑、图片上传、前台展示。  
教学版使用 SQLite。  
以后如果真要产品化，再单独扩展 MySQL，不在第一版里预留太多结构。

明确保留

+ FastAPI
+ SQLite
+ 原生 SQL
+ 单管理员
+ Quill 富文本编辑器
+ 正文保存 HTML
+ 图片上传到本地 uploads/
+ 文章列表
+ 文章详情
+ 后台新增 / 编辑 / 删除文章

明确删除 / 延后

这次先不要：

+ MySQL 建表文件
+ repository / service 分层
+ SEO 字段
+ 分类
+ 标签
+ 多用户
+ tests 目录
+ docs 目录
+ 复杂配置系统
+ 复杂权限系统
+ 云存储
+ AI 功能
+ Paddle / 支付
+ 产品化部署结构

⸻

简化后的项目结构

single-blog-demo/  
├── app/  
│   ├── main.py  
│   ├── db.py  
│   ├── auth.py  
│   ├── articles.py  
│   ├── uploads.py  
│   │  
│   ├── templates/  
│   │   ├── index.html  
│   │   ├── detail.html  
│   │   ├── login.html  
│   │   ├── admin_list.html  
│   │   └── admin_form.html  
│   │  
│   └── static/  
│       ├── style.css  
│       └── editor.js  
│  
├── uploads/  
│   └── .gitkeep  
│  
├── data/  
│   └── .gitkeep  
│  
├── requirements.txt  
├── .env.example  
├── .gitignore  
└── README.md

⸻

每个文件的职责

app/main.py

FastAPI 入口。

负责：

+ 创建应用
+ 注册路由
+ 挂载静态文件
+ 挂载上传图片目录
+ 配置模板

app/db.py

SQLite 数据库操作。

负责：

+ 连接数据库
+ 初始化文章表
+ 新增文章
+ 查询文章列表
+ 查询文章详情
+ 更新文章
+ 删除文章

第一版可以把 SQL 都放这里，不拆 repository。

app/auth.py

后台登录逻辑。

负责：

+ 显示登录页
+ 校验管理员密码
+ 写入 session
+ 退出登录
+ 判断是否已登录

第一版账号密码可以来自 .env。

app/articles.py

文章相关页面和接口。

负责：

+ 前台首页
+ 前台详情页
+ 后台文章列表
+ 新建文章
+ 编辑文章
+ 删除文章

app/uploads.py

图片上传接口。

负责：

+ 接收 Quill 上传的图片
+ 保存到 uploads/
+ 返回图片访问地址

app/templates/

页面模板。

app/static/editor.js

Quill 初始化和图片上传逻辑。

uploads/

本地图片保存目录。

data/

SQLite 数据库文件保存目录。

⸻

一次性创建命令

mkdir -p single-blog-demo/app/templates   
single-blog-demo/app/static   
single-blog-demo/uploads   
single-blog-demo/data  
touch single-blog-demo/app/main.py   
single-blog-demo/app/db.py   
single-blog-demo/app/auth.py   
single-blog-demo/app/articles.py   
single-blog-demo/app/uploads.py   
single-blog-demo/app/templates/index.html   
single-blog-demo/app/templates/detail.html   
single-blog-demo/app/templates/login.html   
single-blog-demo/app/templates/admin_list.html   
single-blog-demo/app/templates/admin_form.html   
single-blog-demo/app/static/style.css   
single-blog-demo/app/static/editor.js   
single-blog-demo/uploads/.gitkeep   
single-blog-demo/data/.gitkeep   
single-blog-demo/requirements.txt   
single-blog-demo/.env.example   
single-blog-demo/.gitignore   
single-blog-demo/README.md

⸻

业务流程自检

1. 核心业务是否闭环？

闭环。

管理员登录  
  ↓  
进入文章列表  
  ↓  
新建文章  
  ↓  
使用 Quill 编辑 HTML 正文  
  ↓  
上传图片到 uploads/  
  ↓  
保存文章到 SQLite  
  ↓  
前台首页显示文章  
  ↓  
点击进入详情页

2. 数据从哪里来，流向哪里？

文章数据：

后台表单  
  ↓  
articles.py  
  ↓  
db.py  
  ↓  
data/blog.sqlite3  
  ↓  
前台模板展示

图片数据：

Quill 图片上传  
  ↓  
uploads.py  
  ↓  
uploads/  
  ↓  
返回 /uploads/xxx.png  
  ↓  
插入正文 HTML  
  ↓  
随文章 HTML 保存到数据库

3. 是否存在暂时不知道怎么用的模块？

基本没有。

这个版本里每个文件都有明确用途，不提前放 MySQL、docs、tests、services、repositories。

4. 明显可延后的功能

全部延后：

+ MySQL
+ SEO 字段
+ slug
+ 分类标签
+ 多管理员
+ 图片云存储
+ 复杂安全策略
+ 产品化部署
+ AI 功能



