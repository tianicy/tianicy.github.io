---
title: 其他1 标签文章列表
---

<div id="tag-header">
    <h1 id="tag-title">🔖 其他1</h1>
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
    .article-list { display: flex; flex-direction: column; gap: 2rem; margin-top: 2rem; }
    .article-item { background: var(--bg-primary); padding: 1.5rem; border-radius: 0.75rem; border: 1px solid rgba(97, 165, 250, 0.2); transition: all 0.3s ease; }
    .article-item:hover { transform: translateY(-4px); box-shadow: 0 10px 40px rgba(97, 165, 250, 0.15); }
    .article-item h3 { margin: 0 0 0.5rem 0; font-size: 1.25rem; }
    .article-item h3 a { color: var(--text-primary); text-decoration: none; transition: color 0.3s ease; }
    .article-item h3 a:hover { color: var(--accent); }
    .article-meta { margin: 0 0 1rem 0; font-size: 0.875rem; color: var(--text-secondary); }
    .article-tags { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 1rem; }
    .tag { padding: 0.25rem 0.75rem; border-radius: 1rem; font-size: 0.75rem; font-weight: 500; background: rgba(97, 165, 250, 0.2); color: var(--accent); }
    .loading-state { text-align: center; padding: 3rem; }
    .animate-spin { animation: spin 1s linear infinite; }
    @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
    .pagination-container { display: flex; justify-content: center; gap: 0.5rem; margin-top: 3rem; flex-wrap: wrap; }
    .pagination-btn { padding: 0.5rem 1rem; border-radius: 0.5rem; background: var(--bg-primary); border: 1px solid rgba(97, 165, 250, 0.2); color: var(--text-primary); cursor: pointer; transition: all 0.3s ease; }
    .pagination-btn:hover:not(.disabled):not(.active) { background: rgba(97, 165, 250, 0.1); border-color: var(--accent); }
    .pagination-btn.active { background: var(--accent); color: white; }
    .pagination-btn.disabled { opacity: 0.5; cursor: not-allowed; }
</style>

<script>
document.addEventListener('DOMContentLoaded', async () => {
    const container = document.getElementById('articles-container');
    const descEl = document.getElementById('tag-description');
    const paginationContainer = document.getElementById('pagination-container');
    const ARTICLES_PER_PAGE = 5;
    let currentPage = 1;
    let allArticles = [];
    
    try {
        const response = await fetch('/tags/其他1/articles.json');
        if (!response.ok) throw new Error('Failed');
        allArticles = await response.json();
        descEl.textContent = `共 ${allArticles.length} 篇文章`;
        renderPage(1);
    } catch (e) {
        container.innerHTML = '<div class="loading-state"><p class="text-red-500">加载失败</p></div>';
    }
    
    function renderPage(page) {
        currentPage = page;
        const start = (page - 1) * ARTICLES_PER_PAGE;
        container.innerHTML = allArticles.slice(start, start + ARTICLES_PER_PAGE).map(a => `
            <div class="article-item">
                <h3><a href="${a.url}">${a.title}</a></h3>
                <p class="article-meta">${a.date} | <span style="color:#61A5FA">${a.category}</span>${a.reading_time ? ` | ${a.reading_time}分钟` : ''}</p>
                <div class="article-tags">${(a.tags||[]).map(t=>`<span class="tag">#${t}</span>`).join('')}</div>
            </div>
        `).join('');
        renderPagination();
    }
    
    function renderPagination() {
        const total = Math.ceil(allArticles.length / ARTICLES_PER_PAGE);
        if (total <= 1) { paginationContainer.innerHTML = ''; return; }
        let h = `<button class="pagination-btn ${currentPage===1?'disabled':''}" onclick="changePage(${currentPage-1})" ${currentPage===1?'disabled':''}>←上一页</button>`;
        for (let i=1; i<=total; i++) {
            if (i===1||i===total||(i>=currentPage-1&&i<=currentPage+1)) h+=`<button class="pagination-btn ${i===currentPage?'active':''}" onclick="changePage(${i})">${i}</button>`;
            else if (i===currentPage-2||i===currentPage+2) h+=`<span class="pagination-btn disabled">...</span>`;
        }
        h+=`<button class="pagination-btn ${currentPage===total?'disabled':''}" onclick="changePage(${currentPage+1})" ${currentPage===total?'disabled':''}>下一页→</button>`;
        paginationContainer.innerHTML = h;
    }
    
    window.changePage = function(p) {
        const total = Math.ceil(allArticles.length / ARTICLES_PER_PAGE);
        if (p<1||p>total) return;
        renderPage(p);
    };
});
</script>
