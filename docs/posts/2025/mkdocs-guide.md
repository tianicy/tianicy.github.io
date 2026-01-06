---
title: MkDocs 自定义主题开发指南
date: 2025-1-1
category: web
tags: ['html & css']
reading_time: 8
pin: true
---

# MkDocs 自定义主题开发指南

深入了解 MkDocs 的主题定制机制，从零开始构建属于自己的独特博客主题。

## MkDocs 主题结构

MkDocs 主题基于 Jinja2 模板引擎，主要包含以下文件：

### 基础模板文件

```
custom_theme/
├── base.html          # 基础模板
├── main.html          # 内容页模板
├── home.html          # 首页模板
└── partials/          # 可重用组件
    ├── header.html
    ├── footer.html
    └── sidebar.html
```

## Jinja2 模板语法

### 变量输出

```jinja
{{ config.site_name }}
{{ page.title }}
{{ page.content }}
```

### 条件判断

```jinja
{% if page.meta.date %}
    <span>{{ page.meta.date }}</span>
{% endif %}
```

### 循环遍历

```jinja
{% for nav_item in config.nav %}
    <a href="{{ nav_item.url }}">{{ nav_item.title }}</a>
{% endfor %}
```

## 自定义配置

在 `mkdocs.yml` 中指定自定义主题：

```yaml
theme:
  name: null
  custom_dir: custom_theme
```

## 实用技巧

1. **使用模板继承**：通过 `{% extends "base.html" %}` 减少重复代码
2. **组件化设计**：将可重用部分抽取到 `partials/` 目录
3. **CSS 变量**：使用 CSS 变量实现主题切换
4. **响应式设计**：使用媒体查询适配不同设备

## 总结

MkDocs 的主题系统灵活强大，通过 Jinja2 模板可以实现各种自定义需求。
