# 🤝 贡献指南

感谢您对 Augment Just So So 项目的关注！我们欢迎各种形式的贡献。

## 📋 贡献方式

### 🐛 报告Bug
如果您发现了bug，请通过以下方式报告：

1. **检查现有Issues**: 首先查看是否已有相同问题的报告
2. **创建新Issue**: 如果没有找到相关问题，请创建新的Issue
3. **提供详细信息**: 包含以下信息会帮助我们更快解决问题：
   - 操作系统版本
   - 程序版本
   - 复现步骤
   - 期望行为
   - 实际行为
   - 错误截图或日志

### 💡 功能建议
我们欢迎新功能的建议：

1. **创建Feature Request**: 使用GitHub Issues创建功能请求
2. **详细描述**: 说明功能的用途和预期效果
3. **讨论可行性**: 与维护者讨论实现的可行性

### 🔧 代码贡献

#### 开发环境设置
1. **Fork仓库**: 点击GitHub页面右上角的Fork按钮
2. **克隆到本地**:
   ```bash
   git clone https://github.com/your-username/AugmentJSS.git
   cd AugmentJSS
   ```
3. **创建虚拟环境**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```
4. **安装依赖**:
   ```bash
   pip install -r requirements.txt
   ```

#### 开发流程
1. **创建分支**: 为您的功能或修复创建新分支
   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/your-bug-fix
   ```

2. **编写代码**: 
   - 遵循现有的代码风格
   - 添加必要的注释
   - 确保代码可读性

3. **测试代码**:
   ```bash
   python main.py  # 测试程序是否正常运行
   ```

4. **提交更改**:
   ```bash
   git add .
   git commit -m "feat: 添加新功能描述"
   # 或
   git commit -m "fix: 修复bug描述"
   ```

5. **推送分支**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **创建Pull Request**: 在GitHub上创建PR

#### 提交信息规范
请使用以下格式的提交信息：

```
类型: 简短描述

详细描述（可选）
```

**类型包括**:
- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

**示例**:
```
feat: 添加邮箱域名自定义功能

允许用户自定义邮箱域名，提高邮箱生成的灵活性
```

## 📝 代码规范

### Python代码风格
- 遵循PEP 8规范
- 使用4个空格缩进
- 行长度不超过88字符
- 函数和类使用docstring文档

### 命名规范
- 变量和函数：`snake_case`
- 类名：`PascalCase`
- 常量：`UPPER_CASE`
- 私有成员：以`_`开头

### 注释规范
```python
def generate_email(self):
    """生成临时邮箱地址
    
    Returns:
        str: 生成的邮箱地址，失败时返回None
    """
    # 实现逻辑...
```

## 🧪 测试

### 手动测试
在提交PR前，请确保：
- [ ] 程序能正常启动
- [ ] 所有功能按预期工作
- [ ] 没有明显的UI问题
- [ ] 错误处理正常

### 测试用例
如果添加新功能，请考虑：
- 正常情况的测试
- 边界条件的测试
- 错误情况的处理

## 📚 文档贡献

### 文档类型
- README.md：项目介绍和使用说明
- INSTALL.md：安装指南
- CHANGELOG.md：更新日志
- 代码注释：函数和类的文档

### 文档规范
- 使用清晰的标题结构
- 提供具体的示例
- 保持内容的准确性和时效性

## 🔍 代码审查

### PR审查标准
- 代码质量和可读性
- 功能完整性
- 错误处理
- 文档完整性
- 与现有代码的兼容性

### 审查流程
1. 自动化检查通过
2. 维护者代码审查
3. 必要时的修改和讨论
4. 合并到主分支

## 🎯 优先级

### 高优先级
- 安全性问题修复
- 严重bug修复
- 性能优化

### 中优先级
- 新功能开发
- 用户体验改进
- 文档完善

### 低优先级
- 代码重构
- 非关键功能
- 样式调整

## 📞 联系方式

如果您有任何问题或需要帮助：

- **GitHub Issues**: 技术问题和bug报告
- **GitHub Discussions**: 功能讨论和一般问题
- **Email**: [your-email@example.com]

## 🙏 致谢

感谢所有贡献者的努力！您的贡献让这个项目变得更好。

### 贡献者列表
- [维护者姓名] - 项目创建者和主要维护者
- [贡献者1] - 功能A的贡献
- [贡献者2] - Bug修复B的贡献

---

**💡 提示**: 如果您是第一次贡献开源项目，建议先从小的改进开始，比如修复文档中的错别字或改进错误信息。
