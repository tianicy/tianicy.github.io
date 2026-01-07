# GitHub Pages 部署方案说明

## 方案一：gh-pages 分支部署（当前使用）

### 工作原理
1. 在 `main` 分支存放源代码
2. GitHub Actions 自动构建静态文件
3. 将构建结果推送到 `gh-pages` 分支
4. GitHub Pages 从 `gh-pages` 分支部署网站

### 配置步骤
1. **工作流配置**：
   - 确保 `.github/workflows/deploy.yml` 文件存在
   - 工作流会自动创建和更新 `gh-pages` 分支

2. **GitHub Pages 配置**：
   - 进入仓库 Settings → Pages
   - Source: Deploy from a branch
   - Branch: gh-pages / (root)
   - 点击 Save

### 优势
- 分离源码与构建产物
- 完整的构建历史记录
- 支持复杂的构建流程

## 方案二：从 main 分支的 docs 目录部署

### 工作原理
1. 在 `main` 分支的 `docs/` 目录存放 Markdown 源文件
2. GitHub Pages 自动使用 MkDocs 构建并部署网站
3. 无需额外的 GitHub Actions 工作流
4. 无需创建 `gh-pages` 分支

### 配置步骤
1. **mkdocs.yml 配置**：
   ```yaml
   site_name: zhaotian
   site_url: https://tianicy.github.io/
   repo_url: https://github.com/tianicy/tianicy.github.io
   docs_dir: docs
   ```

2. **GitHub Pages 配置**：
   - 进入仓库 Settings → Pages
   - Source: GitHub Actions
   - 或选择：Source: Deploy from a branch → Branch: main / docs
   - 点击 Save

3. **目录结构**：
   ```
   ├── docs/
   │   ├── index.md
   │   ├── posts/
   │   └── ...
   ├── mkdocs.yml
   └── requirements.txt
   ```

### 优势
- 简化部署流程
- 无需额外分支
- GitHub 自动处理构建

## 方案选择建议

### 选择方案一（gh-pages 分支）的情况
- 需要自定义构建流程
- 使用了自定义主题
- 需要安装额外插件
- 有复杂的构建需求

### 选择方案二（main 分支 docs 目录）的情况
- 简单的 MkDocs 站点
- 不需要自定义构建流程
- 想要简化部署配置
- 喜欢保持单一分支

## 切换方案的注意事项

### 从方案一切换到方案二
1. 更新 `mkdocs.yml` 配置
2. 修改 GitHub Pages 配置
3. 可以删除 `gh-pages` 分支（可选）
4. 删除 `.github/workflows/deploy.yml` 文件（可选）

### 从方案二切换到方案一
1. 创建 `.github/workflows/deploy.yml` 文件
2. 更新 `mkdocs.yml` 配置
3. 修改 GitHub Pages 配置
4. 首次推送会自动创建 `gh-pages` 分支

## 常见问题

### 方案一问题
- **构建失败**：检查 `requirements.txt` 是否包含所有依赖
- **部署超时**：检查构建步骤是否过于复杂

### 方案二问题
- **主题不生效**：GitHub Pages 只支持默认主题或少数官方主题
- **插件不工作**：GitHub Pages 只支持有限的插件

## 最佳实践

1. **备份配置**：定期备份 `mkdocs.yml` 和其他配置文件
2. **测试部署**：在本地测试构建结果后再推送
3. **使用分支**：开发时使用 feature 分支，合并到 main 分支后部署
4. **监控部署**：定期检查部署状态和网站访问情况