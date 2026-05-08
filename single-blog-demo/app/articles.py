"""
articles.py

文章相关页面和接口。

这里同时包含前台和后台文章功能：
- 前台：首页、文章详情；
- 后台：列表、新建、编辑、删除。

教学版把它们放在一个文件中，是为了让学生更容易追踪“一个业务模块”的完整流程。
"""

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app import db
from app.auth import require_login


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    """前台首页：展示文章列表。"""
    articles = db.list_articles()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "articles": articles,
        },
    )


@router.get("/articles/{article_id}", response_class=HTMLResponse)
def detail(request: Request, article_id: int):
    """前台文章详情页。"""
    article = db.get_article(article_id)
    if article is None:
        return templates.TemplateResponse(
            "detail.html",
            {
                "request": request,
                "article": None,
            },
            status_code=404,
        )

    return templates.TemplateResponse(
        "detail.html",
        {
            "request": request,
            "article": article,
        },
    )


@router.get("/admin/articles", response_class=HTMLResponse)
def admin_list(request: Request):
    """后台文章列表。"""
    redirect = require_login(request)
    if redirect:
        return redirect

    articles = db.list_articles()
    return templates.TemplateResponse(
        "admin_list.html",
        {
            "request": request,
            "articles": articles,
        },
    )


@router.get("/admin/articles/new", response_class=HTMLResponse)
def admin_new_page(request: Request):
    """显示新建文章表单。"""
    redirect = require_login(request)
    if redirect:
        return redirect

    return templates.TemplateResponse(
        "admin_form.html",
        {
            "request": request,
            "mode": "new",
            "article": None,
        },
    )


@router.post("/admin/articles/new")
def admin_create(
    request: Request,
    title: str = Form(...),
    summary: str = Form(""),
    content: str = Form(...),
):
    """处理新建文章提交。"""
    redirect = require_login(request)
    if redirect:
        return redirect

    article_id = db.create_article(title=title, summary=summary, content=content)
    return RedirectResponse(url=f"/articles/{article_id}", status_code=303)


@router.get("/admin/articles/{article_id}/edit", response_class=HTMLResponse)
def admin_edit_page(request: Request, article_id: int):
    """显示编辑文章表单。"""
    redirect = require_login(request)
    if redirect:
        return redirect

    article = db.get_article(article_id)
    if article is None:
        return RedirectResponse(url="/admin/articles", status_code=303)

    return templates.TemplateResponse(
        "admin_form.html",
        {
            "request": request,
            "mode": "edit",
            "article": article,
        },
    )


@router.post("/admin/articles/{article_id}/edit")
def admin_update(
    request: Request,
    article_id: int,
    title: str = Form(...),
    summary: str = Form(""),
    content: str = Form(...),
):
    """处理编辑文章提交。"""
    redirect = require_login(request)
    if redirect:
        return redirect

    db.update_article(article_id=article_id, title=title, summary=summary, content=content)
    return RedirectResponse(url=f"/articles/{article_id}", status_code=303)


@router.post("/admin/articles/{article_id}/delete")
def admin_delete(request: Request, article_id: int):
    """删除文章。"""
    redirect = require_login(request)
    if redirect:
        return redirect

    db.delete_article(article_id)
    return RedirectResponse(url="/admin/articles", status_code=303)
