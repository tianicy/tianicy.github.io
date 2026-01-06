---
title: 标签云
---

# 🏷️ 标签云

通过标签快速找到相关文章。

<div class="tag-cloud" id="tag-cloud-container">
    <!-- Loading State -->
    <div class="loading-state">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-[var(--accent)] mx-auto"></div>
        <p class="mt-4 text-[var(--text-secondary)]">正在加载标签...</p>
    </div>
</div>

<style>
    .tag-cloud {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        margin-top: 2rem;
        justify-content: center;
        align-items: center;
    }
    
    .tag-item {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 2rem;
        text-decoration: none;
        font-weight: 500;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .tag-item::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .tag-item:hover::before {
        left: 100%;
    }
    
    .tag-item:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        z-index: 10;
    }
    
    .tag-count {
        font-size: 0.75em;
        background: rgba(255, 255, 255, 0.2);
        padding: 0.25rem 0.5rem;
        border-radius: 1rem;
        font-weight: 600;
    }
    
    /* 标签大小 */
    .tag-item { font-size: 0.875rem; padding: 0.5rem 1rem; }
    
    /* 标签颜色 */
    .color-1 { color: #61A5FA; border-color: rgba(97, 165, 250, 0.5); }
    .color-2 { color: #4DEEEA; border-color: rgba(77, 238, 234, 0.5); }
    .color-3 { color: #B39EF3; border-color: rgba(179, 158, 243, 0.5); }
    .color-4 { color: #FFA8A8; border-color: rgba(255, 168, 168, 0.5); }
    .color-5 { color: #A8FFA8; border-color: rgba(168, 255, 168, 0.5); }
    .color-6 { color: #FFD7A8; border-color: rgba(255, 215, 168, 0.5); }
    
    .color-1:hover { background: rgba(97, 165, 250, 0.1); }
    .color-2:hover { background: rgba(77, 238, 234, 0.1); }
    .color-3:hover { background: rgba(179, 158, 243, 0.1); }
    .color-4:hover { background: rgba(255, 168, 168, 0.1); }
    .color-5:hover { background: rgba(168, 255, 168, 0.1); }
    .color-6:hover { background: rgba(255, 215, 168, 0.1); }
    
    .loading-state {
        text-align: center;
        padding: 3rem;
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
    const container = document.getElementById('tag-cloud-container');
    
    try {
        const response = await fetch('/tags/tags.json');
        if (!response.ok) throw new Error('Failed to fetch tags');
        
        const tags = await response.json();
        
        // 颜色类名循环
        const colors = ['color-1', 'color-2', 'color-3', 'color-4', 'color-5', 'color-6'];
        
        // 渲染标签云
        container.innerHTML = tags.map((tag, index) => `
            <a href="${tag.slug}/" class="tag-item ${colors[index % colors.length]}">
                ${tag.name} 
                <span class="tag-count">${tag.count}</span>
            </a>
        `).join('');
        
    } catch (error) {
        console.error('Error loading tags:', error);
        container.innerHTML = `
            <div class="loading-state">
                <p class="text-red-500">加载标签失败，请刷新页面重试。</p>
            </div>
        `;
    }
});
</script>
