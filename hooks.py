"""
MkDocs hooks - 在构建时自动生成 articles.json, tags.json, categories.json
支持 posts 目录下的子目录结构 (如 posts/2026-1-1/article.md)
"""
import os
import json
import re
import yaml
from pathlib import Path


def on_pre_build(config):
    """在构建前生成所有 JSON 数据"""
    generate_articles_json(config)
    generate_tags_json(config)
    generate_categories_json(config)


def on_serve(server, config, builder):
    """开发服务器启动时也生成"""
    generate_articles_json(config)
    generate_tags_json(config)
    generate_categories_json(config)
    return server


def get_all_articles(posts_dir: Path) -> list:
    """递归遍历 posts 目录及子目录，获取所有文章"""
    articles = []
    
    # 遍历 posts 目录下的所有 .md 文件（包括子目录）
    for md_file in posts_dir.rglob('*.md'):
        # 跳过 index.md
        if md_file.name == 'index.md':
            continue
        
        try:
            article = parse_article(md_file, posts_dir)
            if article:
                articles.append(article)
        except Exception as e:
            print(f"[hooks] 解析文章失败 {md_file}: {e}")
    
    return articles


def parse_article(md_file: Path, posts_dir: Path) -> dict:
    """解析单篇文章的 front matter 和内容"""
    content = md_file.read_text(encoding='utf-8')
    
    # 提取 front matter (YAML)
    front_matter = {}
    body = content
    
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            try:
                front_matter = yaml.safe_load(parts[1]) or {}
                body = parts[2].strip()
            except yaml.YAMLError as e:
                print(f"[hooks] YAML 解析失败 {md_file.name}: {e}")
    
    # 生成 URL - 支持子目录结构
    # posts/2026-1-1/article.md -> /posts/2026-1-1/article/
    relative_path = md_file.relative_to(posts_dir)
    url_path = str(relative_path.with_suffix('')).replace('\\', '/')
    url = f"/posts/{url_path}/"
    
    # 提取摘要
    summary = extract_summary(body)
    
    return {
        'title': front_matter.get('title', md_file.stem),
        'date': str(front_matter.get('date', '2000-01-01')),
        'category': front_matter.get('category', 'others'),
        'tags': front_matter.get('tags', []),
        'reading_time': front_matter.get('reading_time', estimate_reading_time(body)),
        'pin': front_matter.get('pin', False),
        'url': url,
        'content': summary
    }


def extract_summary(body: str, max_length: int = 200) -> str:
    """提取文章摘要"""
    lines = body.split('\n')
    content_lines = []
    for line in lines:
        if line.strip().startswith('#'):
            continue
        if not line.strip():
            continue
        if line.strip().startswith('```'):
            continue
        content_lines.append(line.strip())
    
    text = ' '.join(content_lines)
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    text = re.sub(r'[*_`#]', '', text)
    
    if len(text) > max_length:
        text = text[:max_length]
    
    return text


def estimate_reading_time(body: str) -> int:
    """估算阅读时间（分钟）"""
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', body))
    english_words = len(re.findall(r'[a-zA-Z]+', body))
    reading_time = (chinese_chars / 400) + (english_words / 200)
    return max(1, round(reading_time))


def generate_articles_json(config):
    """生成 articles.json"""
    docs_dir = Path(config['docs_dir'])
    posts_dir = docs_dir / 'posts'
    
    if not posts_dir.exists():
        print(f"[hooks] posts 目录不存在: {posts_dir}")
        return
    
    articles = get_all_articles(posts_dir)
    
    # 写入 articles.json
    output_path = posts_dir / 'articles.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    
    print(f"[hooks] 已生成 articles.json，共 {len(articles)} 篇文章")


def generate_tags_json(config):
    """生成标签索引和每个标签的文章列表"""
    docs_dir = Path(config['docs_dir'])
    posts_dir = docs_dir / 'posts'
    tags_dir = docs_dir / 'tags'
    
    if not posts_dir.exists():
        return
    
    # 收集所有标签
    tags_map = {}
    articles = get_all_articles(posts_dir)
    
    for article in articles:
        for tag in article.get('tags', []):
            if tag not in tags_map:
                tags_map[tag] = []
            tags_map[tag].append({
                'title': article['title'],
                'date': article['date'],
                'category': article['category'],
                'tags': article['tags'],
                'url': article['url'],
                'reading_time': article.get('reading_time', 1)
            })
    
    # 生成标签索引
    tags_index = []
    for tag_name, tag_articles in tags_map.items():
        tags_index.append({
            'name': tag_name,
            'count': len(tag_articles),
            'slug': tag_name.lower().replace(' ', '-').replace('.', '-').replace('&', '-')
        })
    
    tags_index.sort(key=lambda x: x['count'], reverse=True)
    
    # 写入 tags.json
    tags_dir.mkdir(exist_ok=True)
    with open(tags_dir / 'tags.json', 'w', encoding='utf-8') as f:
        json.dump(tags_index, f, ensure_ascii=False, indent=2)
    
    print(f"[hooks] 已生成 tags.json，共 {len(tags_index)} 个标签")
    
    # 为每个标签生成文章列表和 index.md
    for tag_name, tag_articles in tags_map.items():
        tag_slug = tag_name.lower().replace(' ', '-').replace('.', '-').replace('&', '-')
        tag_dir = tags_dir / tag_slug
        tag_dir.mkdir(exist_ok=True)
        
        tag_articles.sort(key=lambda x: x['date'], reverse=True)
        
        with open(tag_dir / 'articles.json', 'w', encoding='utf-8') as f:
            json.dump(tag_articles, f, ensure_ascii=False, indent=2)
        
        with open(tag_dir / 'index.md', 'w', encoding='utf-8') as f:
            f.write(generate_tag_index_md(tag_name, tag_slug))
    
    print(f"[hooks] 已生成所有标签的文章列表")


def generate_categories_json(config):
    """生成分类索引和每个分类的文章列表"""
    docs_dir = Path(config['docs_dir'])
    posts_dir = docs_dir / 'posts'
    categories_dir = docs_dir / 'categories'
    
    if not posts_dir.exists():
        return
    
    # 收集所有分类
    categories_map = {}
    articles = get_all_articles(posts_dir)
    
    for article in articles:
        category = article.get('category', 'others')
        if category not in categories_map:
            categories_map[category] = []
        categories_map[category].append({
            'title': article['title'],
            'date': article['date'],
            'category': category,
            'tags': article['tags'],
            'url': article['url'],
            'reading_time': article.get('reading_time', 1)
        })
    
    # 生成分类索引
    categories_index = []
    for cat_name, cat_articles in categories_map.items():
        categories_index.append({
            'name': cat_name,
            'count': len(cat_articles),
            'slug': cat_name
        })
    
    categories_index.sort(key=lambda x: x['count'], reverse=True)
    
    # 写入 categories.json
    categories_dir.mkdir(exist_ok=True)
    with open(categories_dir / 'categories.json', 'w', encoding='utf-8') as f:
        json.dump(categories_index, f, ensure_ascii=False, indent=2)
    
    print(f"[hooks] 已生成 categories.json，共 {len(categories_index)} 个分类")
    
    # 为每个分类生成文章列表和 index.md
    for cat_name, cat_articles in categories_map.items():
        cat_dir = categories_dir / cat_name
        cat_dir.mkdir(exist_ok=True)
        
        cat_articles.sort(key=lambda x: x['date'], reverse=True)
        
        with open(cat_dir / 'articles.json', 'w', encoding='utf-8') as f:
            json.dump(cat_articles, f, ensure_ascii=False, indent=2)
        
        with open(cat_dir / 'index.md', 'w', encoding='utf-8') as f:
            f.write(generate_category_index_md(cat_name))
    
    print(f"[hooks] 已生成所有分类的文章列表")


def generate_tag_index_md(tag_name: str, tag_slug: str) -> str:
    return f"""---
title: {tag_name} 标签文章列表
---

<div id="tag-header">
    <h1 id="tag-title">🔖 {tag_name}</h1>
    <p id="tag-description" class="text-[var(--text-secondary)]"></p>
</div>

<div class="article-list" id="articles-container">
    <div class="loading-state">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-[var(--accent)] mx-auto"></div>
        <p class="mt-4 text-[var(--text-secondary)]">正在加载文章...</p>
    </div>
</div>

<div id="pagination-container" class="pagination-container"></div>

<style>
    .article-list {{ display: flex; flex-direction: column; gap: 2rem; margin-top: 2rem; }}
    .article-item {{ background: var(--bg-primary); padding: 1.5rem; border-radius: 0.75rem; border: 1px solid rgba(97, 165, 250, 0.2); transition: all 0.3s ease; }}
    .article-item:hover {{ transform: translateY(-4px); box-shadow: 0 10px 40px rgba(97, 165, 250, 0.15); }}
    .article-item h3 {{ margin: 0 0 0.5rem 0; font-size: 1.25rem; }}
    .article-item h3 a {{ color: var(--text-primary); text-decoration: none; transition: color 0.3s ease; }}
    .article-item h3 a:hover {{ color: var(--accent); }}
    .article-meta {{ margin: 0 0 1rem 0; font-size: 0.875rem; color: var(--text-secondary); }}
    .article-tags {{ display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 1rem; }}
    .tag {{ padding: 0.25rem 0.75rem; border-radius: 1rem; font-size: 0.75rem; font-weight: 500; background: rgba(97, 165, 250, 0.2); color: var(--accent); }}
    .loading-state {{ text-align: center; padding: 3rem; }}
    .animate-spin {{ animation: spin 1s linear infinite; }}
    @keyframes spin {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
    .pagination-container {{ display: flex; justify-content: center; gap: 0.5rem; margin-top: 3rem; flex-wrap: wrap; }}
    .pagination-btn {{ padding: 0.5rem 1rem; border-radius: 0.5rem; background: var(--bg-primary); border: 1px solid rgba(97, 165, 250, 0.2); color: var(--text-primary); cursor: pointer; transition: all 0.3s ease; }}
    .pagination-btn:hover:not(.disabled):not(.active) {{ background: rgba(97, 165, 250, 0.1); border-color: var(--accent); }}
    .pagination-btn.active {{ background: var(--accent); color: white; }}
    .pagination-btn.disabled {{ opacity: 0.5; cursor: not-allowed; }}
</style>

<script>
document.addEventListener('DOMContentLoaded', async () => {{
    const container = document.getElementById('articles-container');
    const descEl = document.getElementById('tag-description');
    const paginationContainer = document.getElementById('pagination-container');
    const ARTICLES_PER_PAGE = 5;
    let currentPage = 1;
    let allArticles = [];
    
    try {{
        const response = await fetch('/tags/{tag_slug}/articles.json');
        if (!response.ok) throw new Error('Failed');
        allArticles = await response.json();
        descEl.textContent = `共 ${{allArticles.length}} 篇文章`;
        renderPage(1);
    }} catch (e) {{
        container.innerHTML = '<div class="loading-state"><p class="text-red-500">加载失败</p></div>';
    }}
    
    function renderPage(page) {{
        currentPage = page;
        const start = (page - 1) * ARTICLES_PER_PAGE;
        container.innerHTML = allArticles.slice(start, start + ARTICLES_PER_PAGE).map(a => `
            <div class="article-item">
                <h3><a href="${{a.url}}">${{a.title}}</a></h3>
                <p class="article-meta">${{a.date}} | <span style="color:#61A5FA">${{a.category}}</span>${{a.reading_time ? ` | ${{a.reading_time}}分钟` : ''}}</p>
                <div class="article-tags">${{(a.tags||[]).map(t=>`<span class="tag">#${{t}}</span>`).join('')}}</div>
            </div>
        `).join('');
        renderPagination();
    }}
    
    function renderPagination() {{
        const total = Math.ceil(allArticles.length / ARTICLES_PER_PAGE);
        if (total <= 1) {{ paginationContainer.innerHTML = ''; return; }}
        let h = `<button class="pagination-btn ${{currentPage===1?'disabled':''}}" onclick="changePage(${{currentPage-1}})" ${{currentPage===1?'disabled':''}}>←上一页</button>`;
        for (let i=1; i<=total; i++) {{
            if (i===1||i===total||(i>=currentPage-1&&i<=currentPage+1)) h+=`<button class="pagination-btn ${{i===currentPage?'active':''}}" onclick="changePage(${{i}})">${{i}}</button>`;
            else if (i===currentPage-2||i===currentPage+2) h+=`<span class="pagination-btn disabled">...</span>`;
        }}
        h+=`<button class="pagination-btn ${{currentPage===total?'disabled':''}}" onclick="changePage(${{currentPage+1}})" ${{currentPage===total?'disabled':''}}>下一页→</button>`;
        paginationContainer.innerHTML = h;
    }}
    
    window.changePage = function(p) {{
        const total = Math.ceil(allArticles.length / ARTICLES_PER_PAGE);
        if (p<1||p>total) return;
        renderPage(p);
    }};
}});
</script>
"""


def generate_category_index_md(category_name: str) -> str:
    return f"""---
title: {category_name}文章列表
---

<div id="category-header">
    <h1 id="category-title">🔧 {category_name}</h1>
    <p id="category-description" class="text-[var(--text-secondary)]"></p>
</div>

<div class="article-list" id="articles-container">
    <div class="loading-state">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-[var(--accent)] mx-auto"></div>
        <p class="mt-4 text-[var(--text-secondary)]">正在加载文章...</p>
    </div>
</div>

<div id="pagination-container" class="pagination-container"></div>

<style>
    .article-list {{ display: flex; flex-direction: column; gap: 2rem; margin-top: 2rem; }}
    .article-item {{ background: var(--bg-primary); padding: 1.5rem; border-radius: 0.75rem; border: 1px solid rgba(97, 165, 250, 0.2); transition: all 0.3s ease; }}
    .article-item:hover {{ transform: translateY(-4px); box-shadow: 0 10px 40px rgba(97, 165, 250, 0.15); }}
    .article-item h3 {{ margin: 0 0 0.5rem 0; font-size: 1.25rem; }}
    .article-item h3 a {{ color: var(--text-primary); text-decoration: none; transition: color 0.3s ease; }}
    .article-item h3 a:hover {{ color: var(--accent); }}
    .article-meta {{ margin: 0 0 1rem 0; font-size: 0.875rem; color: var(--text-secondary); }}
    .article-tags {{ display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 1rem; }}
    .tag {{ padding: 0.25rem 0.75rem; border-radius: 1rem; font-size: 0.75rem; font-weight: 500; background: rgba(97, 165, 250, 0.2); color: var(--accent); }}
    .loading-state {{ text-align: center; padding: 3rem; }}
    .animate-spin {{ animation: spin 1s linear infinite; }}
    @keyframes spin {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
    .pagination-container {{ display: flex; justify-content: center; gap: 0.5rem; margin-top: 3rem; flex-wrap: wrap; }}
    .pagination-btn {{ padding: 0.5rem 1rem; border-radius: 0.5rem; background: var(--bg-primary); border: 1px solid rgba(97, 165, 250, 0.2); color: var(--text-primary); cursor: pointer; transition: all 0.3s ease; }}
    .pagination-btn:hover:not(.disabled):not(.active) {{ background: rgba(97, 165, 250, 0.1); border-color: var(--accent); }}
    .pagination-btn.active {{ background: var(--accent); color: white; }}
    .pagination-btn.disabled {{ opacity: 0.5; cursor: not-allowed; }}
</style>

<script>
document.addEventListener('DOMContentLoaded', async () => {{
    const container = document.getElementById('articles-container');
    const descEl = document.getElementById('category-description');
    const paginationContainer = document.getElementById('pagination-container');
    const ARTICLES_PER_PAGE = 5;
    let currentPage = 1;
    let allArticles = [];
    
    try {{
        const response = await fetch('/categories/{category_name}/articles.json');
        if (!response.ok) throw new Error('Failed');
        allArticles = await response.json();
        descEl.textContent = `共 ${{allArticles.length}} 篇文章`;
        renderPage(1);
    }} catch (e) {{
        container.innerHTML = '<div class="loading-state"><p class="text-red-500">加载失败</p></div>';
    }}
    
    function renderPage(page) {{
        currentPage = page;
        const start = (page - 1) * ARTICLES_PER_PAGE;
        container.innerHTML = allArticles.slice(start, start + ARTICLES_PER_PAGE).map(a => `
            <div class="article-item">
                <h3><a href="${{a.url}}">${{a.title}}</a></h3>
                <p class="article-meta">${{a.date}} | <span style="color:#61A5FA">${{a.category}}</span>${{a.reading_time ? ` | ${{a.reading_time}}分钟` : ''}}</p>
                <div class="article-tags">${{(a.tags||[]).map(t=>`<span class="tag">#${{t}}</span>`).join('')}}</div>
            </div>
        `).join('');
        renderPagination();
    }}
    
    function renderPagination() {{
        const total = Math.ceil(allArticles.length / ARTICLES_PER_PAGE);
        if (total <= 1) {{ paginationContainer.innerHTML = ''; return; }}
        let h = `<button class="pagination-btn ${{currentPage===1?'disabled':''}}" onclick="changePage(${{currentPage-1}})" ${{currentPage===1?'disabled':''}}>←上一页</button>`;
        for (let i=1; i<=total; i++) {{
            if (i===1||i===total||(i>=currentPage-1&&i<=currentPage+1)) h+=`<button class="pagination-btn ${{i===currentPage?'active':''}}" onclick="changePage(${{i}})">${{i}}</button>`;
            else if (i===currentPage-2||i===currentPage+2) h+=`<span class="pagination-btn disabled">...</span>`;
        }}
        h+=`<button class="pagination-btn ${{currentPage===total?'disabled':''}}" onclick="changePage(${{currentPage+1}})" ${{currentPage===total?'disabled':''}}>下一页→</button>`;
        paginationContainer.innerHTML = h;
    }}
    
    window.changePage = function(p) {{
        const total = Math.ceil(allArticles.length / ARTICLES_PER_PAGE);
        if (p<1||p>total) return;
        renderPage(p);
    }};
}});
</script>
"""
