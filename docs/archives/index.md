---
title: 文章归档
---

# 📅 文章归档

按时间顺序查看所有文章。

<div class="archive-container" id="archive-container">
    <div class="loading-state">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-[var(--accent)] mx-auto"></div>
        <p class="mt-4 text-[var(--text-secondary)]">正在加载归档...</p>
    </div>
</div>

<style>
    .archive-container { margin-top: 2rem; }
    .archive-year { margin-bottom: 1rem; border: 1px solid rgba(97, 165, 250, 0.2); border-radius: 0.75rem; overflow: hidden; background: var(--bg-primary); }
    .year-header { display: flex; justify-content: space-between; align-items: center; padding: 1rem 1.5rem; cursor: pointer; background: rgba(97, 165, 250, 0.05); transition: all 0.2s ease; margin: 0; }
    .year-header:hover { background: rgba(97, 165, 250, 0.1); }
    .year-title { font-size: 1.5rem; font-weight: 700; color: var(--accent); }
    .toggle-icon { font-size: 1rem; color: var(--text-secondary); transition: transform 0.2s ease; }
    .archive-month { margin: 0.5rem 1rem; border-bottom: 1px solid rgba(97, 165, 250, 0.1); }
    .archive-month:last-child { border-bottom: none; }
    .month-header { display: flex; justify-content: space-between; align-items: center; padding: 0.75rem 1rem; cursor: pointer; transition: all 0.2s ease; margin: 0; }
    .month-header:hover { background: rgba(97, 165, 250, 0.05); border-radius: 0.5rem; }
    .month-title { font-size: 1.125rem; font-weight: 600; color: var(--text-primary); }
    .month-content { padding: 0.5rem 1rem 1rem 2rem; transition: all 0.3s ease; }
    .month-content.hidden { display: none; }
    .year-content.hidden { display: none; }
    .article-list { margin: 0; padding: 0; list-style: none; }
    .article-list li { margin: 0.5rem 0; padding: 0.25rem 0; border-bottom: 1px dashed rgba(97, 165, 250, 0.1); }
    .article-list li:last-child { border-bottom: none; }
    .article-list a { color: var(--accent); text-decoration: none; transition: color 0.2s ease; }
    .article-list a:hover { color: var(--accent-secondary); text-decoration: underline; }
    .article-list li::before { content: "📝"; margin-right: 0.5rem; color: var(--text-secondary); }
    .loading-state { text-align: center; padding: 3rem; }
    .animate-spin { animation: spin 1s linear infinite; }
    @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
</style>

<script>
const MONTH_NAMES = ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月'];
let allGroupedData = {}; // 全局存储所有文章数据

document.addEventListener('DOMContentLoaded', async () => {
    const container = document.getElementById('archive-container');
    
    try {
        const response = await fetch('/posts/articles.json');
        if (!response.ok) throw new Error('Failed to fetch articles');
        
        const articles = await response.json();
        articles.sort((a, b) => new Date(b.date) - new Date(a.date));
        
        // 按年月分组
        const grouped = {};
        articles.forEach(article => {
            const date = new Date(article.date);
            const year = date.getFullYear();
            const month = date.getMonth() + 1;
            const key = `${year}-${month}`;
            
            if (!grouped[year]) grouped[year] = {};
            if (!grouped[year][month]) grouped[year][month] = [];
            grouped[year][month].push(article);
        });
        
        // 存储到全局变量
        allGroupedData = grouped;
        
        // 渲染
        const years = Object.keys(grouped).sort((a, b) => b - a);
        container.innerHTML = years.map((year, yearIdx) => {
            const months = Object.keys(grouped[year]).sort((a, b) => b - a);
            return `
                <div class="archive-year">
                    <h2 class="year-header" onclick="toggleYear('year-${year}')">
                        <span class="year-title">${year} 年</span>
                        <span class="toggle-icon">${yearIdx === 0 ? '▼' : '▶'}</span>
                    </h2>
                    <div class="year-content ${yearIdx === 0 ? '' : 'hidden'}" id="year-${year}">
                        ${months.map((month, monthIdx) => `
                            <div class="archive-month">
                                <h3 class="month-header" onclick="toggleMonth('month-${year}-${month}')">
                                    <span class="month-title">${MONTH_NAMES[month - 1]} <span style="font-size: 0.85rem; color: var(--text-secondary); font-weight: normal;">(${grouped[year][month].length}篇)</span></span>
                                    <span class="toggle-icon">${yearIdx === 0 && monthIdx === 0 ? '▼' : '▶'}</span>
                                </h3>
                                <div class="month-content ${yearIdx === 0 && monthIdx === 0 ? '' : 'hidden'}" id="month-${year}-${month}" data-all-loaded="false">
                                    <ul class="article-list">
                                        ${grouped[year][month].slice(0, 10).map(article => 
                                            `<li><a href="${article.url}">${article.title}</a> - ${article.date}</li>`
                                        ).join('')}
                                    </ul>
                                    ${grouped[year][month].length > 10 ? `
                                        <div class="show-more" style="text-align: center; padding: 0.75rem; margin-top: 0.5rem;">
                                            <button class="show-more-btn" onclick="showAllArticles('month-${year}-${month}')" style="color: var(--accent); background: none; border: none; cursor: pointer; font-size: 0.9rem; transition: all 0.2s;">
                                                ... 查看更多 (${grouped[year][month].length - 10}篇)
                                            </button>
                                        </div>
                                    ` : ''}
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        }).join('');
        
    } catch (error) {
        console.error('Error loading articles:', error);
        container.innerHTML = '<div class="loading-state"><p class="text-red-500">加载归档失败，请刷新页面重试。</p></div>';
    }
});

function toggleYear(yearId) {
    const yearContent = document.getElementById(yearId);
    const yearHeader = yearContent.previousElementSibling;
    const toggleIcon = yearHeader.querySelector('.toggle-icon');
    
    if (yearContent.classList.contains('hidden')) {
        yearContent.classList.remove('hidden');
        toggleIcon.textContent = '▼';
    } else {
        yearContent.classList.add('hidden');
        toggleIcon.textContent = '▶';
    }
}

function toggleMonth(monthId) {
    const monthContent = document.getElementById(monthId);
    const monthHeader = monthContent.previousElementSibling;
    const toggleIcon = monthHeader.querySelector('.toggle-icon');
    
    if (monthContent.classList.contains('hidden')) {
        monthContent.classList.remove('hidden');
        toggleIcon.textContent = '▼';
    } else {
        monthContent.classList.add('hidden');
        toggleIcon.textContent = '▶';
    }
}

function showAllArticles(monthId) {
    const monthContent = document.getElementById(monthId);
    const articleList = monthContent.querySelector('.article-list');
    const showMoreDiv = monthContent.querySelector('.show-more');
    
    // 检查是否已经加载
    if (monthContent.getAttribute('data-all-loaded') === 'true') {
        return;
    }
    
    // 从 monthId 提取 year 和 month
    const parts = monthId.replace('month-', '').split('-');
    const year = parts[0];
    const month = parts[1];
    
    // 获取剩余文章
    const remainingArticles = allGroupedData[year][month].slice(10);
    
    // 添加剩余文章
    remainingArticles.forEach(article => {
        const li = document.createElement('li');
        li.innerHTML = `<a href="${article.url}">${article.title}</a> - ${article.date}`;
        articleList.appendChild(li);
    });
    
    // 隐藏"查看更多"按钮
    if (showMoreDiv) {
        showMoreDiv.style.display = 'none';
    }
    
    // 标记为已加载
    monthContent.setAttribute('data-all-loaded', 'true');
}
</script>
