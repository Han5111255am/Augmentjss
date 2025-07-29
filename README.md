# 🎯 Augment Just So So

一个功能强大的多合一工具，集成了临时邮箱生成、验证码获取和机器码重置功能。

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%2064bit-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)

## ✨ 功能特性

### 📧 临时邮箱生成
- **真实邮箱地址**: 生成可用的临时邮箱地址
- **多域名支持**: 支持多个邮箱域名服务
- **一键复制**: 快速复制邮箱地址到剪贴板

### 📬 验证码获取
- **实时获取**: 自动获取发送到临时邮箱的验证码
- **智能识别**: 支持多种验证码格式识别
- **快速复制**: 一键复制验证码

### 🔧 机器码重置
- **硬件标识符修改**: 重置系统硬件标识符
- **管理员权限**: 安全的管理员权限执行
- **用户友好**: 详细的操作指导和状态提示

## 📥 下载安装

### 方式一：直接下载可执行文件（推荐）

1. 前往 [Releases](../../releases) 页面
2. 下载最新版本的 `AugmentJSS.exe`
3. 双击运行即可使用

### 方式二：从源码运行

```bash
# 克隆仓库
git clone https://github.com/Han5111255am/Augmentjss.git
cd Augmentjss

# 安装依赖
pip install -r requirements.txt

# 运行程序
python main.py
```

## 🖥️ 系统要求

- **操作系统**: Windows 10/11 (64位)
- **内存**: 至少 512MB 可用内存
- **磁盘空间**: 至少 100MB 可用空间
- **权限**: 机器码重置功能需要管理员权限

## 🚀 使用指南

### 1. 生成临时邮箱
1. 点击 **"🔄 生成邮箱"** 按钮
2. 等待邮箱生成完成
3. 点击 **"📋 复制邮箱"** 复制到剪贴板
4. 在需要的地方使用该邮箱地址

### 2. 获取验证码
1. 确保已生成临时邮箱
2. 在目标网站使用该邮箱接收验证码
3. 点击 **"📬 获取验证码"** 按钮
4. 等待验证码获取完成
5. 点击 **"📋 复制验证码"** 使用验证码

### 3. 重置机器码
⚠️ **重要提醒**: 此功能会修改系统硬件标识符，请谨慎使用！

1. **以管理员身份运行程序**
2. 点击 **"🔧 重置机器码"** 按钮
3. 仔细阅读警告信息并确认
4. 在弹出的程序窗口中完成操作
5. 建议操作完成后重启系统

## ⚠️ 重要说明

### 安全提醒
- **机器码重置功能**具有系统级影响，请在充分了解后果的情况下使用
- 建议在使用前**备份重要数据**
- 某些软件的授权可能会受到影响

### 使用限制
- 临时邮箱服务依赖第三方API，可用性可能受网络环境影响
- 机器码重置功能仅支持Windows系统
- 程序需要稳定的网络连接

## 🔧 技术栈

- **开发语言**: Python 3.10+
- **GUI框架**: Tkinter
- **网络请求**: Requests
- **系统调用**: Windows API (ctypes)

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- 感谢所有临时邮箱API服务提供商
- 感谢Python和Tkinter社区
- 感谢所有测试用户的反馈

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 🐛 Issues: [GitHub Issues](../../issues)
- 💬 Discussions: [GitHub Discussions](../../discussions)
- 📧 GitHub: [@Han5111255am](https://github.com/Han5111255am)

---

**⭐ 如果这个项目对您有帮助，请给个Star支持一下！**
