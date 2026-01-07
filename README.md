# 📝 MkDocs 博客系统

一个基于 MkDocs 的现代化博客系统，支持分类、标签、搜索、RSS 订阅等功能。

## 📋 目录结构

```
├── custom_theme/        # 自定义主题文件
├── docs/                # 博客内容目录
│   ├── assets/          # 静态资源
│   │   ├── categories/  # 分类页面背景图
│   │   ├── images/      # 首页和其他页面图片
│   │   └── welcome/     # 欢迎页面图片
│   ├── categories/      # 分类索引页面
│   ├── posts/           # 文章目录，按日期组织
│   │   ├── 2025-1-1/    # 2025年1月1日的文章
│   │   └── 2026-1-1/    # 2026年1月1日的文章
│   ├── tags/            # 标签索引页面
│   ├── archives/        # 归档页面
│   ├── about/           # 关于页面
│   └── index.md         # 首页
├── hooks.py             # 钩子脚本，动态生成分类和标签
├── mkdocs.yml           # MkDocs 配置文件
└── README.md            # 项目说明文档
```

## ✨ 功能特性

### 📄 文章管理
- 📅 按日期组织文章：`docs/YYYY-MM-DD/file.md`
- 📌 支持 `pin` 属性，置顶文章
- 📊 自动生成阅读时间
- 📖 支持 Markdown 扩展语法

### 🏷️ 分类和标签
- 📁 分类自动生成目录：`categories/{category_name}/`
- 🏷️ 标签自动生成目录：`tags/{tag_name}/`
- 🔢 分类只展示前6个，同时只生成前6个目录
- 🔢 标签只展示前12个，同时只生成前12个目录
- 📊 分类和标签按文章数量排序

### 🔍 搜索功能
- 🔦 内置搜索支持
- 🔵 搜索结果高亮显示
- ⌨️ 支持快捷键 Ctrl+K 触发搜索

### 📱 响应式设计
- 📱 适配移动端和桌面端
- 🌓 支持暗黑模式
- 🏄 流畅的动画效果

### 📰 归档功能
- 📅 按年月归档文章
- 📋 默认只展开最新年月的前10篇文章
- 🔽 其他年月默认折叠

### 📡 RSS 订阅
- 📡 基于 `mkdocs-rss` 插件实现
- 📬 支持 `feed_rss_created.xml` 和 `feed_rss_updated.xml`
- 🔄 自动获取文章日期

### 🌟 推荐文章
- ⭐ 展示4篇推荐文章
- 📌 `pin` 属性文章优先显示
- 🔢 否则按日期排序

## 🚀 快速开始

### 安装依赖
```bash
pip install mkdocs mkdocs-material mkdocs-rss-plugin git-revision-date-localized-plugin
```

### 启动开发服务器
```bash
mkdocs serve
```

访问 http://127.0.0.1:8000/ 查看博客

### 构建生产版本
```bash
mkdocs build
```

## 🛠️ 配置说明

### 站点基本信息
在 `mkdocs.yml` 中配置：
```yaml
site_name: zhaotian
site_description: with passion as my torch, I seek life's deep significance
site_url: http://localhost:8000/
repo_url: https://github.com/tianicy/tianicy.github.io
```

### 主题配置
```yaml
theme:
  name: null
  custom_dir: custom_theme
```

### 插件配置
```yaml
plugins:
  - search
  - git-revision-date-localized
  - rss:
      enabled: true
```

### 钩子配置
```yaml
hooks:
  - hooks.py
```

## 📝 文章发布指南

### 文章格式
```markdown
---
title: 文章标题
date: 2025-01-01
category: web
tags: ['python', 'django']
reading_time: 5
pin: true
---

# 文章标题

文章内容...
```

### 分类和标签
- **分类**：backends, web, db, AI, others, Internet
- **标签**：django, flask, fastapi, vue, react, python, javascript, html---css, 其他1, 其他2

## 🖼️ 图片管理

### 首页图片
- 首页使用 `assets/images/01.jpg` 到 `assets/images/05.jpg`
- 自动轮播展示

### 分类页面图片
- 读取 `assets/categories/` 目录下的图片
- 如果图片数量不足，自动轮询使用
- 图片按分类文章数量排序匹配

### 欢迎页面图片
- 读取 `assets/welcome/` 目录下的图片

## ⚠️ 注意事项

### 网站图标
- 图标文件：`docs/assets/images/favicon.svg`
- 🧹 更改后需要强制刷新浏览器清除缓存

### 标签命名规则
- `html & css` 会被转换为 `html---css`

### RSS 功能
- ⏱️ 会增加网站构建时长
- 📋 依赖 `git-revision-date-localized` 插件获取日期

### 硬编码内容
- 📱 部分站点信息为硬编码
- 🖼️ 部分图片引用为硬编码

## 🔧 常见问题

### 为什么 MkDocs serve 不实时更新？
- 🔍 检查 `watchdog` 是否安装
- 🔧 尝试使用 `mkdocs serve --verbose` 查看日志
- 🚀 尝试添加 `--dirtyreload` 参数

### 分类和标签页面没有内容？
- 🔧 确保 `hooks.py` 脚本正常运行
- 📋 检查文章的 front matter 是否包含正确的分类和标签

### RSS 订阅无法获取日期？
- 📋 确保文章有 `date` 属性
- 🔧 确保文件已提交到 git 仓库
- 🚀 检查 `git-revision-date-localized` 插件配置

## 🛠️ 技术栈

- 📋 **MkDocs**：静态站点生成器
- 🎨 **自定义主题**：基于 Material 主题扩展
- 📝 **Markdown**：文章编写格式
- 🐍 **Python**：钩子脚本和插件
- 🌐 **HTML & CSS**：页面结构和样式
- 💫 **JavaScript**：交互功能
- 📊 **Git**：版本控制和日期获取

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 联系方式

- 📧 邮箱：2630880751@qq.com
- 🐙 GitHub：https://github.com/tianicy/tianicy.github.io

---

✨ 感谢使用 MkDocs 博客系统！✨