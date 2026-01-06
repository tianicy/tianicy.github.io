# Tailwind CSS Browser CDN @apply 指令不支持问题

## 问题现象

使用 `@tailwindcss/browser` CDN 引入 Tailwind CSS v4 时，页面出现布局异常，只显示 Tailwind 图标，样式完全失效。

## 问题原因

### 核心原因：Browser 版本不支持 `@apply` 指令

Tailwind CSS v4 的 Browser CDN 版本（`@tailwindcss/browser@4`）是为浏览器运行时设计的轻量版本，**不支持构建时的 `@apply` 指令**。

### 技术背景

1. **Tailwind CSS v4 架构变化**
   - v4 完全重构，分为两个版本：
     - **CLI/Build 版本**：支持完整功能，包括 `@apply`、`@layer` 等指令
     - **Browser 版本**：运行时版本，仅支持基础的 Tailwind 类名

2. **`@apply` 指令的工作原理**
   - `@apply` 是 **构建时指令**，需要在编译阶段将 Tailwind 类名转换为 CSS
   - Browser 版本在浏览器中运行，无法进行构建时处理
   - 因此所有包含 `@apply` 的样式块都会被忽略

3. **问题代码示例**

```html
<!-- 错误的使用方式 -->
<style type="text/tailwindcss">
    .glass {
        @apply backdrop-blur-xl bg-opacity-60 border border-white/10;
    }
    
    .card-hover {
        @apply transition-all duration-300 ease-out;
    }
    
    .prose h1 {
        @apply text-3xl font-bold mt-8 mb-4;
    }
</style>
```

这些样式在 Browser CDN 版本中**全部失效**，导致页面布局完全错乱。

## 解决方案

### 方案一：使用纯 CSS 替代 `@apply`（本次采用）

将所有 `@apply` 指令替换为标准 CSS：

```html
<style>
    /* 替换前 */
    .glass {
        @apply backdrop-blur-xl bg-opacity-60 border border-white/10;
    }
    
    /* 替换后 */
    .glass {
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        background-color: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* 替换前 */
    .card-hover {
        @apply transition-all duration-300 ease-out;
    }
    
    /* 替换后 */
    .card-hover {
        transition: all 0.3s ease-out;
    }
    
    /* 替换前 */
    .prose h1 {
        @apply text-3xl font-bold mt-8 mb-4;
    }
    
    /* 替换后 */
    .prose h1 {
        font-size: 1.875rem;
        line-height: 2.25rem;
        font-weight: 700;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
</style>
```

### 方案二：使用构建工具（不适合本项目）

如果需要使用 `@apply`，必须：
1. 安装 `tailwindcss` npm 包
2. 配置 Vite 或其他构建工具
3. 在构建时编译 CSS

**为什么本项目不采用**：
- 需求文档明确要求使用 **CDN 方式引入**
- MkDocs 静态博客不需要额外的构建流程
- Browser CDN 版本更符合项目定位

## 修复涉及的文件

1. **custom_theme/base.html**
   - 移除 `<style type="text/tailwindcss">` 中的所有 `@apply`
   - 替换为标准 CSS 属性

2. **custom_theme/main.html**
   - `.prose` 相关样式的 `@apply` 全部替换
   - 确保 Markdown 渲染样式正常

## 经验总结

### 使用 Tailwind Browser CDN 的注意事项

1. **直接使用 Tailwind 类名**
   ```html
   <!-- ✅ 正确：直接在 HTML 中使用 -->
   <div class="backdrop-blur-xl bg-opacity-60 border border-white/10">
   ```

2. **自定义样式使用纯 CSS**
   ```html
   <!-- ✅ 正确：自定义类用纯 CSS -->
   <style>
       .glass { backdrop-filter: blur(24px); }
   </style>
   ```

3. **避免使用构建时指令**
   ```html
   <!-- ❌ 错误：Browser 版本不支持 -->
   @apply, @layer, @variants, theme() 函数
   ```

### Tailwind CSS v4 版本选择指南

| 场景 | 推荐版本 | 原因 |
|------|---------|------|
| 静态网站、MkDocs | Browser CDN | 无需构建，即时生效 |
| Vue/React 项目 | npm + 构建工具 | 支持完整功能 |
| 需要 `@apply` | npm + 构建工具 | Browser 不支持 |
| 快速原型 | Browser CDN | 开发速度快 |

## 参考资料

- [Tailwind CSS v4 文档](https://tailwindcss.com/)
- [Browser CDN 限制说明](https://tailwindcss.com/docs/installation#using-tailwind-via-cdn)
- 需求文档：`d:/05_laboratory/test/Mkdocs/需求文档.txt`

## 修复时间

- 问题发现：2026-01-05 22:58
- 修复完成：2026-01-05 23:03
- 影响范围：所有使用 `@apply` 的样式文件
