# GitHub Actions 工作流使用指南

## 1. 前置条件

### 1.1 环境准备
- 安装 Git
- 配置 Git 用户名和邮箱
- 拥有 GitHub 账号
- 已将代码仓库克隆到本地

### 1.2 仓库配置
- 确保仓库已启用 GitHub Pages
- 确保 `.github/workflows/deploy.yml` 文件存在
- 确保 `requirements.txt` 文件包含所有必需的依赖

## 2. 代码推送与部署

### 2.1 本地开发
1. 在本地修改代码或添加新内容
2. 使用 `git status` 查看修改状态
3. 使用 `git add .` 添加所有修改
4. 使用 `git commit -m "描述你的修改"` 提交修改
5. 使用 `git push origin main` 将修改推送到 GitHub

### 2.2 部署触发
- 当代码推送到 `main` 分支时，GitHub Actions 会自动触发工作流
- 也可以通过 GitHub UI 手动触发：
  1. 进入仓库页面
  2. 点击 "Actions" 选项卡
  3. 选择 "Deploy MkDocs to GitHub Pages" 工作流
  4. 点击 "Run workflow" 按钮
  5. 选择分支，点击 "Run workflow"

## 3. 查看部署状态

### 3.1 查看工作流状态
1. 进入仓库页面
2. 点击 "Actions" 选项卡
3. 在左侧边栏选择 "Deploy MkDocs to GitHub Pages" 工作流
4. 点击最新的工作流运行记录
5. 查看工作流的执行状态和日志

### 3.2 查看部署日志
1. 在工作流运行记录页面，点击 "build-and-deploy" 作业
2. 展开各个步骤查看详细日志
3. 如果部署失败，查看错误信息进行调试

## 4. 访问部署后的站点

### 4.1 访问地址
部署完成后，您的站点将通过以下地址访问：
`https://tianicy.github.io`

### 4.2 访问时间
- 部署通常需要 1-2 分钟完成
- 首次部署可能需要更长时间
- 可以在工作流日志中查看确切的部署时间

## 5. 常见操作

### 5.1 修改站点内容
1. 在本地修改 Markdown 文件
2. 推送修改到 GitHub
3. 等待 GitHub Actions 自动部署
4. 访问站点查看更新

### 5.2 修改站点配置
1. 修改 `mkdocs.yml` 文件
2. 推送修改到 GitHub
3. 等待 GitHub Actions 自动部署
4. 访问站点查看配置更新效果

### 5.3 添加新插件
1. 在 `requirements.txt` 中添加新插件
2. 在 `mkdocs.yml` 中配置插件
3. 推送修改到 GitHub
4. 等待 GitHub Actions 自动部署

## 6. 调试与故障排除

### 6.1 查看错误日志
- 在 GitHub Actions 面板查看详细的错误日志
- 根据错误信息进行调试
- 常见错误包括：
  - 依赖缺失：确保 `requirements.txt` 包含所有必需的依赖
  - 配置错误：检查 `mkdocs.yml` 配置是否正确
  - 代码错误：检查 Markdown 文件是否有语法错误

### 6.2 本地测试
- 在本地运行 `mkdocs serve` 进行预览
- 本地运行 `mkdocs build` 检查构建是否成功
- 本地测试通过后再推送到 GitHub

## 7. 最佳实践

### 7.1 代码组织
- 定期提交代码，避免一次性提交大量修改
- 提交信息要清晰、描述性强
- 使用分支管理功能，避免直接修改 `main` 分支

### 7.2 配置管理
- 定期更新依赖版本
- 保持 `requirements.txt` 与实际使用的依赖一致
- 备份重要的配置文件

### 7.3 安全注意事项
- 不要在代码中包含敏感信息（如密码、密钥等）
- 使用环境变量管理敏感配置
- 定期检查工作流权限设置

## 8. 其他资源

### 8.1 官方文档
- [GitHub Actions 官方文档](https://docs.github.com/zh/actions)
- [MkDocs 官方文档](https://www.mkdocs.org/)
- [peaceiris/actions-gh-pages 文档](https://github.com/peaceiris/actions-gh-pages)

### 8.2 常见问题
- 查看 `github-actions-deploy-issues.md` 文件了解常见部署问题
- 查看 `github-actions-workflow-principle.md` 文件了解工作流原理