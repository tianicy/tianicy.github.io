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
    
    /* 卡片容器 - 相对定位，用于容纳图片和内容 */
    .category-card {
        border: 1px solid rgba(97, 165, 250, 0.2);
        border-radius: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        position: relative;
        overflow: hidden;
        height: 240px; /* 固定卡片高度 */
    }
    
    /* 图片容器 - 绝对定位，仅显示在上部80%区域 */
    .category-image {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 80%; /* 上部占80% */
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        z-index: 0;
    }
    
    /* 内容容器 - 绝对定位，仅显示在下部20%区域 */
    .card-content {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 20%; /* 下部占20% */
        padding: 0.75rem 1rem;
        background: var(--bg-primary); /* 使用主题背景色，确保文字清晰可读 */
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
        z-index: 1;
    }
    
    .category-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 40px rgba(97, 165, 250, 0.15);
        border-color: var(--accent);
    }
    
    /* 分类名称样式 */
    .category-card h3 {
        margin: 0;
        font-size: 1.125rem;
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
    
    /* 分类描述样式 - 隐藏分类描述 */
    .category-card p {
        display: none;
    }
    
    /* 分类文章数量样式 */
    .category-count {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        background: rgba(97, 165, 250, 0.1);
        color: var(--accent);
        border-radius: 1rem;
        font-size: 0.75rem;
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
        // 1. 加载分类数据
        const categoriesResponse = await fetch('/categories/categories.json');
        if (!categoriesResponse.ok) throw new Error('Failed to fetch categories');
        
        const categories = await categoriesResponse.json();
        
        // 2. 动态加载分类卡片背景图片
        let categoryImages = ['/assets/categories/01.jpg']; // 默认图片，防止加载失败
        try {
            const imagesResponse = await fetch('/assets/categories_images.json');
            if (imagesResponse.ok) {
                categoryImages = await imagesResponse.json();
            }
        } catch (imagesError) {
            console.warn('Failed to fetch categories_images.json, using default image:', imagesError);
        }
        
        // 4. 基于文章数量排序（已排序，保持原有顺序）
        // 只显示前6个分类
        const topCategories = categories.slice(0, 6);
        
        // 5. 为每个分类分配图片
        container.innerHTML = topCategories.map((cat, index) => {
            // 使用轮询方式分配图片，如果图片不够则循环使用
            const imageIndex = index % categoryImages.length;
            const backgroundImage = categoryImages[imageIndex];
            
            return `
                <div class="category-card">
                    <!-- 图片区域 - 仅显示在上部80% -->
                    <div class="category-image" style="background-image: url('${backgroundImage}')"></div>
                    <!-- 内容区域 - 仅显示在下部20% -->
                    <div class="card-content">
                        <h3><a href="${encodeURIComponent(cat.name)}/">${cat.name}</a></h3>
                        <p>${cat.name}相关文章</p>
                        <span class="category-count">${cat.count} 篇文章</span>
                    </div>
                </div>
            `;
        }).join('');
        
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
