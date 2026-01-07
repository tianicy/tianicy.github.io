# MkDocs 部署方案说明

本文档介绍了两种将 MkDocs 站点部署到 GitHub Pages 的方案。

## 方案一：gh-pages 分支部署

### 文件名
`deploy-gh-pages.yml`

### 工作原理
1. 当代码推送到 `main` 分支时，工作流自动触发
2. 构建 MkDocs 站点生成静态文件
3. 将构建产物推送到 `gh-pages` 分支
4. GitHub Pages 从 `gh-pages` 分支部署站点

### 特点
- **产生新分支**：会在仓库中创建并更新 `gh-pages` 分支
- **可视化构建产物**：可以在 `gh-pages` 分支中查看构建生成的静态文件
- **传统部署模式**：GitHub Pages 早期就支持的成熟方案
- **适合需要查看构建产物的场景**

### 配置步骤
1. 将 `deploy-gh-pages.yml` 复制到 `.github/workflows/` 目录
2. 在仓库 Settings → Pages 中设置：
   - Source: Deploy from a branch
   - Branch: gh-pages / (root)
3. 推送代码到 `main` 分支触发部署

## 方案二：GitHub Actions 直接部署

### 文件名
`deploy-direct.yml`

### 工作原理
1. 当代码推送到 `main` 分支时，工作流自动触发
2. 构建 MkDocs 站点生成静态文件
3. 使用 GitHub Actions 的内置部署功能直接部署
4. 不创建或更新任何分支，构建产物存储在 GitHub Pages 服务中

### 特点
- **无额外分支**：不会在仓库中创建新分支
- **不可见构建产物**：构建产物不会存储在仓库中，而是直接部署到 GitHub Pages 服务
- **现代部署模式**：使用 GitHub Actions 的最新部署功能
- **适合追求简洁仓库的场景**

### 配置步骤
1. 将 `deploy-direct.yml` 复制到 `.github/workflows/` 目录
2. 在仓库 Settings → Pages 中设置：
   - Source: GitHub Actions
3. 推送代码到 `main` 分支触发部署

## 两种方案的对比

| 特性 | gh-pages 分支部署 | GitHub Actions 直接部署 |
|------|------------------|------------------------|
| 是否创建新分支 | 是 | 否 |
| 构建产物可见性 | 可见（在 gh-pages 分支中） | 不可见（存储在 GitHub Pages 服务中） |
| 部署源配置 | Deploy from a branch | GitHub Actions |
| 工作流复杂度 | 中等 | 中等 |
| 适合场景 | 需要查看构建产物 | 追求简洁仓库 |
| GitHub Pages 配置 | 需设置分支 | 需选择 GitHub Actions |

## 如何选择

### 选择 gh-pages 分支部署如果：
- 你需要查看或下载构建产物
- 你习惯传统的 GitHub Pages 部署模式
- 你需要对构建产物进行版本控制

### 选择 GitHub Actions 直接部署如果：
- 你希望保持仓库简洁，不产生额外分支
- 你不需要查看构建产物
- 你想使用 GitHub 的最新部署功能

## 使用说明

### 切换部署方案
1. 删除当前 `.github/workflows/` 目录下的部署文件
2. 复制对应方案的部署文件到 `.github/workflows/` 目录
3. 更新仓库 Settings → Pages 中的部署源配置
4. 推送代码触发部署

### 查看部署状态
两种方案都可以在 GitHub Actions 面板中查看部署状态和日志：
1. 进入仓库页面
2. 点击 "Actions" 选项卡
3. 选择对应的工作流
4. 查看工作流运行记录和日志

### 访问站点
无论使用哪种方案，部署完成后，站点都可以通过以下地址访问：
`https://tianicy.github.io`