# 📚 GitHub仓库发布指南

本指南将帮助您将AugmentJSS项目发布到GitHub仓库中。

## 🚀 快速发布流程

### 步骤1: 创建GitHub仓库

1. **登录GitHub**: 访问 [github.com](https://github.com) 并登录
2. **创建新仓库**: 点击右上角的 "+" 按钮，选择 "New repository"
3. **仓库设置**:
   - **Repository name**: `AugmentJSS`
   - **Description**: `🎯 一个功能强大的多合一工具，集成了临时邮箱生成、验证码获取和机器码重置功能`
   - **Visibility**: Public（推荐）或 Private
   - **Initialize**: 不要勾选任何初始化选项（我们已有文件）

### 步骤2: 上传项目文件

#### 方式一：使用Git命令行（推荐）

```bash
# 在项目目录中初始化Git仓库
git init

# 添加远程仓库
git remote add origin https://github.com/your-username/AugmentJSS.git

# 添加所有文件
git add .

# 提交文件
git commit -m "feat: 初始版本发布 - v1.0.0"

# 推送到GitHub
git push -u origin main
```

#### 方式二：使用GitHub Desktop

1. 下载并安装 [GitHub Desktop](https://desktop.github.com/)
2. 选择 "Add an Existing Repository from your Hard Drive"
3. 选择项目目录
4. 点击 "Publish repository"

#### 方式三：使用GitHub Web界面

1. 在GitHub仓库页面点击 "uploading an existing file"
2. 拖拽或选择项目文件上传
3. 填写提交信息并提交

### 步骤3: 创建Release

#### 自动发布（推荐）

项目已配置GitHub Actions自动发布：

```bash
# 创建并推送标签
git tag v1.0.0
git push origin v1.0.0
```

GitHub Actions将自动：
- 构建可执行文件
- 创建Release
- 上传发布文件

#### 手动发布

1. **进入Releases页面**: 在仓库主页点击右侧的 "Releases"
2. **创建新Release**: 点击 "Create a new release"
3. **设置标签**: 
   - Tag version: `v1.0.0`
   - Target: `main` branch
4. **填写信息**:
   - Release title: `AugmentJSS v1.0.0`
   - Description: 复制 `release/RELEASE_NOTES.md` 的内容
5. **上传文件**:
   - 拖拽 `release/binary/AugmentJSS-v1.0.0-windows-x64.exe`
   - 拖拽 `release/source/AugmentJSS-v1.0.0-source.zip`
   - 拖拽 `release/SHA256SUMS.txt`
6. **发布**: 点击 "Publish release"

## 📋 发布清单

### 必需文件
- [x] `README.md` - 项目介绍和使用说明
- [x] `LICENSE` - 开源许可证
- [x] `main.py` - 主程序文件
- [x] `requirements.txt` - Python依赖
- [x] `dist/AugmentJSS.exe` - 可执行文件

### 推荐文件
- [x] `INSTALL.md` - 安装指南
- [x] `CHANGELOG.md` - 更新日志
- [x] `CONTRIBUTING.md` - 贡献指南
- [x] `.gitignore` - Git忽略文件
- [x] `.github/workflows/release.yml` - 自动发布工作流

### 发布文件
- [x] 可执行文件 (50.5 MB)
- [x] 源码包 (23.1 KB)
- [x] 校验和文件
- [x] 发布说明

## 🎯 仓库优化建议

### 1. 添加仓库标签（Topics）
在仓库主页点击设置图标，添加相关标签：
- `python`
- `tkinter`
- `email-generator`
- `verification-code`
- `windows`
- `gui-application`

### 2. 设置仓库描述
在仓库设置中添加详细描述和网站链接。

### 3. 启用功能
- [x] Issues - 用于bug报告和功能请求
- [x] Wiki - 用于详细文档
- [x] Discussions - 用于社区讨论
- [x] Projects - 用于项目管理

### 4. 保护主分支
在Settings > Branches中设置分支保护规则：
- 要求pull request审查
- 要求状态检查通过
- 限制推送到主分支

## 📊 发布后的维护

### 版本管理
使用语义化版本号：
- `v1.0.0` - 主要版本
- `v1.1.0` - 次要版本（新功能）
- `v1.0.1` - 修订版本（bug修复）

### 更新流程
1. 修改代码
2. 更新 `CHANGELOG.md`
3. 提交更改
4. 创建新标签
5. 推送标签触发自动发布

### 社区管理
- 及时回复Issues
- 审查Pull Requests
- 更新文档
- 发布更新公告

## 🔧 故障排除

### 常见问题

#### 1. 推送失败
```bash
# 如果遇到推送失败，尝试强制推送（谨慎使用）
git push -f origin main
```

#### 2. 大文件问题
如果可执行文件太大，考虑使用Git LFS：
```bash
git lfs track "*.exe"
git add .gitattributes
```

#### 3. Actions失败
检查GitHub Actions日志，常见问题：
- Python版本不匹配
- 依赖安装失败
- 权限问题

### 获取帮助
- [GitHub文档](https://docs.github.com/)
- [GitHub Community](https://github.community/)
- [Git教程](https://git-scm.com/docs)

## 📞 联系支持

如果在发布过程中遇到问题：
1. 检查本指南的故障排除部分
2. 搜索GitHub社区相关问题
3. 联系项目维护者

---

**🎉 恭喜！您的项目现在已经成功发布到GitHub！**

记住定期更新项目，回应社区反馈，让您的开源项目茁壮成长！
