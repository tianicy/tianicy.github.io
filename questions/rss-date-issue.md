# RSS 插件日期提取问题解决方案

## 问题描述
在使用 mkdocs-rss-plugin 时，出现了日期无法提取的警告：
```
INFO    -  [RSS-plugin]: Dates could not be retrieved for page: <page_path>
```

## 根本原因
1. **日期格式问题**：RSS插件默认从文章front matter的`date`字段提取日期，但对日期格式有严格要求
2. **meta标签缺失**：插件尝试从页面meta标签获取日期，但自定义主题可能没有生成所需的meta标签
3. **git提交历史**：插件无法从git提交历史获取日期，因为文件尚未被提交

## 解决方案

### 1. 安装git-revision-date-localized插件
```yaml
# mkdocs.yml
plugins:
  - search
  - git-revision-date-localized
  - rss:
      enabled: true
```

### 2. 将文件提交到git仓库
```bash
git add .
git commit -m "Add files to git repository"
```

### 3. 工作原理
- `git-revision-date-localized`插件从git提交历史中提取文件的最后修改日期
- 该插件会为每个页面生成包含日期信息的meta标签
- `mkdocs-rss-plugin`可以从这些meta标签中获取日期信息

## 最终结果
- 构建过程中不再出现RSS插件日期警告
- RSS订阅功能正常工作
- 网站可以正常生成

## 适用场景
- 适用于使用git进行版本控制的MkDocs项目
- 解决了自定义主题中日期提取的问题
- 无需修改大量代码即可实现RSS功能

## 注意事项
- 确保所有内容文件都已提交到git
- 第一次提交后，需要重新构建网站
- 后续修改文件后，需要再次提交才能更新日期信息