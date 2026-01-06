---
title: 分类列表
---

# 📚 分类列表

<div class="categories-container" id="categories-container">
    <div class="loading-state">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-[var(--accent)] mx-auto"></div>
        <p class="mt-4 text-[var(--text-secondary)]">正在加载分类...</p>
    </div>
</div>

<style>
    .categories-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin-top: 2rem;
    }
    
    .category-card {
        background: var(--bg-primary);
        border: 1px solid rgba(97, 165, 250, 0.2);
        border-radius: 1rem;
        padding: 2rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .category-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 40px rgba(97, 165, 250, 0.15);
        border-color: var(--accent);
    }
    
    .category-card h3 {
        margin: 0 0 0.5rem 0;
        font-size: 1.25rem;
    }
    
    .category-card h3 a {
        color: var(--accent);
        text-decoration: none;
        transition: color 0.2s ease;
    }
    
    .category-card h3 a:hover {
        color: var(--accent-secondary);
        text-decoration: underline;
    }
    
    .category-card p {
        margin: 0 0 1rem 0;
        color: var(--text-secondary);
        font-size: 0.875rem;
    }
    
    .category-count {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        background: rgba(97, 165, 250, 0.1);
        color: var(--accent);
        border-radius: 1rem;
        font-size: 0.875rem;
        font-weight: 500;
    }
    
    .loading-state {
        text-align: center;
        padding: 3rem;
        grid-column: 1 / -1;
    }
    
    .animate-spin {
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
</style>

<script>
document.addEventListener('DOMContentLoaded', async () => {
    const container = document.getElementById('categories-container');
    
    try {
        const response = await fetch('/categories/categories.json');
        if (!response.ok) throw new Error('Failed to fetch categories');
        
        const categories = await response.json();
        
        container.innerHTML = categories.map(cat => `
            <div class="category-card">
                <h3><a href="${encodeURIComponent(cat.name)}/">${cat.name}</a></h3>
                <p>${cat.name}相关文章</p>
                <span class="category-count">${cat.count} 篇文章</span>
            </div>
        `).join('');
        
    } catch (error) {
        console.error('Error loading categories:', error);
        container.innerHTML = `
            <div class="loading-state">
                <p class="text-red-500">加载分类失败，请刷新页面重试。</p>
            </div>
        `;
    }
});
</script>
