"""
db.py

这个文件专门负责 SQLite 数据库相关操作。

教学版刻意使用“原生 SQL + 普通函数”的写法：
1. 方便学生看到 SQL 到底做了什么；
2. 不引入 ORM，降低第一版理解成本；
3. 不拆 repository/service，避免小 Demo 过度工程化。
"""

import sqlite3
from pathlib import Path


# BASE_DIR 指向项目根目录 single-blog-demo/
BASE_DIR = Path(__file__).resolve().parent.parent

# 数据库文件放在 data/ 目录下，便于学生找到。
DB_PATH = BASE_DIR / "data" / "blog.sqlite3"


def get_connection():
    """
    创建并返回一个 SQLite 连接。

    row_factory 的作用：
    默认查询结果是元组，例如 row[0]、row[1]。
    设置为 sqlite3.Row 后，可以像字典一样读取字段：
    row["title"]、row["content"]。
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    初始化数据库。

    FastAPI 启动时会调用这个函数。
    如果 articles 表不存在，就创建它。
    """
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                summary TEXT NOT NULL DEFAULT '',
                content TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def create_article(title: str, summary: str, content: str):
    """新增一篇文章。"""
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO articles (title, summary, content)
            VALUES (?, ?, ?)
            """,
            (title, summary, content),
        )
        return cursor.lastrowid


def list_articles():
    """查询文章列表，最新发布的文章排在前面。"""
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, title, summary, created_at, updated_at
            FROM articles
            ORDER BY id DESC
            """
        ).fetchall()
        return rows


def get_article(article_id: int):
    """根据 id 查询单篇文章；如果不存在，返回 None。"""
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT id, title, summary, content, created_at, updated_at
            FROM articles
            WHERE id = ?
            """,
            (article_id,),
        ).fetchone()
        return row


def update_article(article_id: int, title: str, summary: str, content: str):
    """更新一篇文章。"""
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE articles
            SET title = ?,
                summary = ?,
                content = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (title, summary, content, article_id),
        )


def delete_article(article_id: int):
    """删除一篇文章。"""
    with get_connection() as conn:
        conn.execute("DELETE FROM articles WHERE id = ?", (article_id,))
