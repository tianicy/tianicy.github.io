# GitHub Actions 工作流原理说明

## 什么是 GitHub Actions？
GitHub Actions 是 GitHub 提供的持续集成/持续部署 (CI/CD) 平台，允许您在代码仓库中自动化软件开发生命周期。

## 工作流文件结构
工作流文件是一个 YAML 文件，位于 `.github/workflows/` 目录下，包含以下主要部分：

1. **name**: 工作流的名称
2. **on**: 触发工作流的事件（如 push、pull_request 等）
3. **permissions**: 工作流所需的权限
4. **jobs**: 工作流中包含的作业
5. **steps**: 每个作业包含的步骤

## 我们的 GitHub 工作流原理

### 触发机制
当代码推送到 `main` 分支时，工作流自动触发。也可以通过 GitHub UI 手动触发。

### 执行流程
1. **检出代码**：使用 `actions/checkout@v4` 动作从 GitHub 仓库中检出代码
2. **设置 Python 环境**：使用 `actions/setup-python@v5` 动作设置 Python 3.11 环境
3. **安装依赖**：通过 `pip install -r requirements.txt` 安装所有必需的依赖
4. **构建站点**：执行 `mkdocs build` 命令生成静态网站文件
5. **部署到 GitHub Pages**：使用 `peaceiris/actions-gh-pages@v4` 动作将构建结果部署到 GitHub Pages

### 关键组件说明

#### 1. 作业 (Jobs)
- 每个作业运行在独立的虚拟环境中
- 我们的工作流只包含一个作业 `build-and-deploy`
- 运行环境为 `ubuntu-latest`

#### 2. 步骤 (Steps)
- 每个步骤可以是一个 shell 命令或一个动作
- 步骤按顺序执行
- 前一个步骤失败，后续步骤不会执行

#### 3. 动作 (Actions)
- 可重用的代码块，简化工作流配置
- 我们使用了以下动作：
  - `actions/checkout@v4`: 检出代码
  - `actions/setup-python@v5`: 设置 Python 环境
  - `peaceiris/actions-gh-pages@v4`: 部署到 GitHub Pages

#### 4. 环境变量与密钥
- 工作流使用 GitHub 内置的 `GITHUB_TOKEN` 进行认证
- 无需手动配置密钥，GitHub 自动管理

## 工作流执行结果

### 成功情况
- 工作流执行完成，显示绿色的 "Success" 状态
- 站点成功部署到 GitHub Pages
- 可以通过 `https://tianicy.github.io` 访问

### 失败情况
- 工作流执行失败，显示红色的 "Failed" 状态
- GitHub 会发送通知邮件
- 可以在 GitHub Actions 面板查看详细的错误日志

## 优势

1. **自动化**：无需手动构建和部署
2. **可追溯**：每次部署都有完整的日志记录
3. **可扩展**：可以根据需要添加更多步骤
4. **免费**：GitHub 提供一定的免费使用额度
5. **集成性**：与 GitHub 仓库深度集成