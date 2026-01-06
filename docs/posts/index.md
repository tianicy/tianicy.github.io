---
title: 文章列表
---

# 📝 文章列表

这里是我的所有文章，按时间顺序排列。

<div class="article-list" id="article-list">
    <div class="loading-state">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-[var(--accent)] mx-auto"></div>
        <p class="mt-4 text-[var(--text-secondary)]">正在加载文章...</p>
    </div>
</div>

<div id="pagination-container" class="pagination-container"></div>

<style>
    .article-list { display: flex; flex-direction: column; gap: 2rem; }
    .article-item { background: var(--bg-primary); padding: 1.5rem; border-radius: 0.75rem; border: 1px solid rgba(97, 165, 250, 0.2); transition: all 0.3s ease; }
    .article-item:hover { transform: translateY(-4px); box-shadow: 0 10px 40px rgba(97, 165, 250, 0.15); }
    .article-item h3 { margin: 0 0 0.5rem 0; font-size: 1.25rem; }
    .article-item h3 a { color: var(--text-primary); text-decoration: none; transition: color 0.3s ease; }
    .article-item h3 a:hover { color: var(--accent); text-decoration: none; }
    .article-meta { margin: 0 0 1rem 0; font-size: 0.875rem; color: var(--text-secondary); }
    .article-summary { color: var(--text-secondary); font-size: 0.9rem; line-height: 1.6; margin: 0.75rem 0; }
    .article-tags { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 1rem; }
    .tag { padding: 0.25rem 0.75rem; border-radius: 1rem; font-size: 0.75rem; font-weight: 500; }
    .loading-state { text-align: center; padding: 3rem; }
    .animate-spin { animation: spin 1s linear infinite; }
    @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
    .pagination-container { display: flex; justify-content: center; gap: 0.5rem; margin-top: 3rem; flex-wrap: wrap; }
    .pagination-btn { padding: 0.5rem 1rem; border-radius: 0.5rem; background: var(--bg-primary); border: 1px solid rgba(97, 165, 250, 0.2); color: var(--text-primary); cursor: pointer; transition: all 0.3s ease; text-decoration: none; }
    .pagination-btn:hover:not(.disabled):not(.active) { background: rgba(97, 165, 250, 0.1); border-color: var(--accent); }
    .pagination-btn.active { background: var(--accent); color: white; border-color: var(--accent); }
    .pagination-btn.disabled { opacity: 0.5; cursor: not-allowed; }
</style>

<script>
document.addEventListener('DOMContentLoaded', async () => {
    const container = document.getElementById('article-list');
    const paginationContainer = document.getElementById('pagination-container');
    const ARTICLES_PER_PAGE = 5;
    let currentPage = 1;
    let allArticles = [];
    
    try {
        const response = await fetch('/posts/articles.json');
        if (!response.ok) throw new Error('Failed to fetch articles');
        allArticles = await response.json();
        allArticles.sort((a, b) => new Date(b.date) - new Date(a.date));
        renderPage(1);
    } catch (error) {
        console.error('Error loading articles:', error);
        container.innerHTML = '<div class="loading-state"><p class="text-red-500">加载文章失败，请刷新页面重试。</p></div>';
    }
    
    function renderPage(page) {
        currentPage = page;
        const start = (page - 1) * ARTICLES_PER_PAGE;
        const end = start + ARTICLES_PER_PAGE;
        const pageArticles = allArticles.slice(start, end);
        container.innerHTML = pageArticles.map(article => `
            <div class="article-item">
                <h3><a href="${article.url}">${article.title}</a></h3>
                <p class="article-meta">${article.date} | <span class="category-tag" style="color: #61A5FA;">${article.category}</span>${article.reading_time ? ` | ${article.reading_time} 分钟阅读` : ''}</p>
                ${article.content ? `<p class="article-summary">${article.content.replace(/[#*`]/g, '').substring(0, 150)}${article.content.length > 150 ? '...' : ''}</p>` : ''}
                <div class="article-tags">${(article.tags || []).map(tag => `<span class="tag" style="background: #61A5FA; color: white;">#${tag}</span>`).join('')}</div>
            </div>
        `).join('');
        renderPagination();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    
    function renderPagination() {
        const totalPages = Math.ceil(allArticles.length / ARTICLES_PER_PAGE);
        if (totalPages <= 1) { paginationContainer.innerHTML = ''; return; }
        let html = `<button class="pagination-btn ${currentPage === 1 ? 'disabled' : ''}" onclick="changePage(${currentPage - 1})" ${currentPage === 1 ? 'disabled' : ''}>← 上一页</button>`;
        for (let i = 1; i <= totalPages; i++) {
            if (i === 1 || i === totalPages || (i >= currentPage - 1 && i <= currentPage + 1)) {
                html += `<button class="pagination-btn ${i === currentPage ? 'active' : ''}" onclick="changePage(${i})">${i}</button>`;
            } else if (i === currentPage - 2 || i === currentPage + 2) {
                html += `<span class="pagination-btn disabled">...</span>`;
            }
        }
        html += `<button class="pagination-btn ${currentPage === totalPages ? 'disabled' : ''}" onclick="changePage(${currentPage + 1})" ${currentPage === totalPages ? 'disabled' : ''}>下一页 →</button>`;
        paginationContainer.innerHTML = html;
    }
    
    window.changePage = function(page) {
        const totalPages = Math.ceil(allArticles.length / ARTICLES_PER_PAGE);
        if (page < 1 || page > totalPages) return;
        renderPage(page);
    };
});
</script>
