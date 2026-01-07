# GitHub Actions 部署 MkDocs 常见问题总结

## 问题一：缺少 requirements.txt 或 pyproject.toml 文件

### 错误信息
```
Run actions/setup-python@v5 
Installed versions 
Error: No file in /home/runner/work/tianicy.github.io/tianicy.github.io matched to [**/requirements.txt or **/pyproject.toml], make sure you have checked out the target repository
```

### 原因
GitHub Actions 的 `setup-python` 动作尝试缓存 Python 依赖，但找不到依赖配置文件。

### 解决方案
创建 `requirements.txt` 文件，列出所有必需的依赖：
```
mkdocs
mkdocs-git-revision-date-localized-plugin
mkdocs-rss-plugin
```

## 问题二：缺少 pymdownx 扩展模块

### 错误信息
```
Run mkdocs build 
ERROR   -  Config value 'markdown_extensions': Failed to load extension 'pymdownx.highlight'. 
ModuleNotFoundError: No module named 'pymdownx' 
Aborted with a configuration error!
```

### 原因
配置文件中使用了 `pymdownx` 系列扩展，但这些扩展并未安装。

### 解决方案
在 `requirements.txt` 中添加缺失的依赖：
```
pymdown-extensions  # 提供 pymdownx 系列扩展
pygments            # 用于代码高亮
```

## 完整的 requirements.txt 示例
```
mkdocs
mkdocs-git-revision-date-localized-plugin
mkdocs-rss-plugin
pymdown-extensions
pygments
```