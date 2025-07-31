# AugmentJSS MailTM邮箱复用功能设计方案

## 📋 项目概述

### 功能目标
为AugmentJSS临时邮箱工具添加MailTM服务的邮箱复用功能，允许用户保存和重复使用MailTM邮箱账户，提升用户体验和工具实用性。

### 核心价值
- **邮箱复用**：一次生成，多次使用，避免频繁创建新邮箱
- **状态持久化**：保存邮箱凭据，支持会话恢复
- **差异化服务**：充分利用MailTM的密码机制，提供独特功能

## 🎯 功能需求分析

### 1. 用户场景
- **场景1**：用户需要多次接收同一服务的验证码
- **场景2**：用户希望在程序重启后继续使用之前的邮箱
- **场景3**：用户有多个临时邮箱需要管理

### 2. 功能需求
#### 2.1 核心功能
- [x] 邮箱生成时同时生成密码
- [x] 邮箱和密码信息显示
- [x] 已有邮箱登录功能
- [x] 登录状态管理
- [x] 密码输入框动态启用/禁用

#### 2.2 扩展功能
- [ ] 邮箱信息本地存储
- [ ] 多邮箱账户管理
- [ ] 自动登录选项
- [ ] 邮箱使用历史

## 🎨 UI设计方案

### 1. 界面布局设计

```
┌─────────────────────────────────────────────────────┐
│ 📧 邮箱生成                                          │
├─────────────────────────────────────────────────────┤
│ 选择服务: [MailTM        ▼]                         │
│                                                     │
│ 生成的邮箱: [user@mail.tm                    ] 📋   │
│                                                     │
│ 邮箱密码:   [••••••••••••                   ] 👁   │
│             ↑ 仅MailTM服务时启用                     │
│                                                     │
│ [🔄 生成邮箱] [📋 复制邮箱] [🔑 登录邮箱] [🔧 重置]  │
└─────────────────────────────────────────────────────┘
```

### 2. 状态设计

#### 2.1 服务选择状态
```
非MailTM服务:
- 密码输入框: 禁用 + 深色背景 + 占位符"仅MailTM服务可用"
- 登录按钮: 禁用

MailTM服务:
- 密码输入框: 启用 + 正常背景 + 占位符"输入密码或生成新邮箱"
- 登录按钮: 启用
```

#### 2.2 登录状态
```
未登录状态:
- 邮箱框: 可编辑，显示占位符"输入邮箱地址或点击生成"
- 密码框: 可编辑，显示占位符"输入密码"
- 登录按钮: "🔑 登录邮箱"

已登录状态:
- 邮箱框: 只读，显示当前邮箱
- 密码框: 只读，显示密码（可切换显示/隐藏）
- 登录按钮: "🚪 退出登录"
```

### 3. 视觉设计规范

#### 3.1 颜色方案
```python
COLORS = {
    "normal_bg": "#FFFFFF",      # 正常输入框背景
    "disabled_bg": "#F5F5F5",   # 禁用输入框背景
    "readonly_bg": "#F9F9F9",   # 只读输入框背景
    "border_normal": "#CCCCCC",  # 正常边框
    "border_focus": "#007CBA",   # 焦点边框
    "border_disabled": "#E0E0E0", # 禁用边框
    "text_normal": "#333333",    # 正常文本
    "text_disabled": "#999999",  # 禁用文本
    "text_placeholder": "#AAAAAA" # 占位符文本
}
```

#### 3.2 状态指示
- **禁用状态**：深色背景 + 浅色文本 + 虚线边框
- **只读状态**：浅色背景 + 正常文本 + 实线边框
- **编辑状态**：白色背景 + 正常文本 + 蓝色焦点边框

## 🔧 技术实现方案

### 1. 数据结构设计

#### 1.1 邮箱账户类
```python
@dataclass
class MailTMAccount:
    email: str
    password: str
    token: str = None
    created_at: datetime = None
    last_used: datetime = None
    is_active: bool = False
    
    def to_dict(self) -> dict:
        """转换为字典格式"""
        pass
    
    @classmethod
    def from_dict(cls, data: dict) -> 'MailTMAccount':
        """从字典创建实例"""
        pass
```

#### 1.2 账户管理器
```python
class MailTMAccountManager:
    def __init__(self):
        self.current_account: MailTMAccount = None
        self.saved_accounts: List[MailTMAccount] = []
    
    def create_account(self) -> MailTMAccount:
        """创建新账户"""
        pass
    
    def login_account(self, email: str, password: str) -> bool:
        """登录已有账户"""
        pass
    
    def logout_current(self):
        """退出当前账户"""
        pass
    
    def save_account(self, account: MailTMAccount):
        """保存账户信息"""
        pass
    
    def load_accounts(self) -> List[MailTMAccount]:
        """加载已保存的账户"""
        pass
```

### 2. UI组件设计

#### 2.1 密码输入框组件
```python
class PasswordEntry(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent)
        self.setup_ui()
        self.is_enabled = True
        self.show_password = False
    
    def setup_ui(self):
        """设置UI组件"""
        pass
    
    def set_enabled(self, enabled: bool):
        """设置启用/禁用状态"""
        pass
    
    def set_readonly(self, readonly: bool):
        """设置只读状态"""
        pass
    
    def toggle_password_visibility(self):
        """切换密码显示/隐藏"""
        pass
```

#### 2.2 邮箱管理面板
```python
class MailTMPanel(tk.Frame):
    def __init__(self, parent, account_manager: MailTMAccountManager):
        super().__init__(parent)
        self.account_manager = account_manager
        self.setup_ui()
        self.bind_events()
    
    def setup_ui(self):
        """设置UI布局"""
        pass
    
    def on_service_changed(self, service: str):
        """服务选择变化处理"""
        pass
    
    def on_login_clicked(self):
        """登录按钮点击处理"""
        pass
    
    def update_ui_state(self):
        """更新UI状态"""
        pass
```

### 3. 状态管理

#### 3.1 状态枚举
```python
class MailTMState(Enum):
    DISABLED = "disabled"      # 非MailTM服务
    READY = "ready"           # MailTM服务，未登录
    LOGGING_IN = "logging_in" # 登录中
    LOGGED_IN = "logged_in"   # 已登录
    ERROR = "error"           # 错误状态
```

#### 3.2 状态机
```python
class MailTMStateMachine:
    def __init__(self):
        self.current_state = MailTMState.DISABLED
        self.state_handlers = {
            MailTMState.DISABLED: self._handle_disabled,
            MailTMState.READY: self._handle_ready,
            MailTMState.LOGGING_IN: self._handle_logging_in,
            MailTMState.LOGGED_IN: self._handle_logged_in,
            MailTMState.ERROR: self._handle_error,
        }
    
    def transition_to(self, new_state: MailTMState):
        """状态转换"""
        pass
    
    def _handle_disabled(self):
        """处理禁用状态"""
        pass
    
    def _handle_ready(self):
        """处理就绪状态"""
        pass
    
    def _handle_logging_in(self):
        """处理登录中状态"""
        pass
    
    def _handle_logged_in(self):
        """处理已登录状态"""
        pass
    
    def _handle_error(self):
        """处理错误状态"""
        pass
```

## 🔄 业务流程设计

### 1. 邮箱生成流程
```
选择MailTM服务 → 点击生成邮箱 → 调用MailTM API → 
API调用成功? → 显示邮箱和密码 → 保存账户信息 → 更新UI状态为已登录
```

### 2. 邮箱登录流程
```
输入邮箱和密码 → 点击登录按钮 → 验证输入格式 → 
格式正确? → 调用MailTM登录API → 登录成功? → 保存登录状态 → 更新UI状态
```

### 3. 服务切换流程
```
用户选择服务 → 是否为MailTM? → 启用/禁用密码输入框 → 
显示/隐藏登录按钮 → 更新UI样式
```

## 🛡️ 安全设计

### 1. 数据安全
- **密码存储**：使用Base64编码（临时存储，非永久保存）
- **Token管理**：及时清理过期Token
- **内存清理**：程序退出时清理敏感信息

### 2. 输入验证
- **邮箱格式**：正则表达式验证
- **密码强度**：基础长度检查
- **特殊字符**：防止注入攻击

### 3. 错误处理
- **网络异常**：超时重试机制
- **API错误**：友好错误提示
- **状态异常**：自动状态恢复

## 📊 性能优化

### 1. UI响应性
- **异步操作**：网络请求使用线程池
- **状态缓存**：减少重复API调用
- **懒加载**：按需加载账户信息

### 2. 内存管理
- **对象池**：复用UI组件
- **垃圾回收**：及时释放无用对象
- **缓存策略**：LRU缓存机制

## 🧪 测试方案

### 1. 单元测试
- **账户管理器**：创建、登录、保存功能
- **状态机**：状态转换逻辑
- **UI组件**：启用/禁用状态

### 2. 集成测试
- **API集成**：MailTM服务调用
- **UI集成**：组件交互测试
- **状态同步**：前后端状态一致性

### 3. 用户测试
- **易用性**：新用户上手难度
- **稳定性**：长时间使用测试
- **兼容性**：不同系统环境测试

## 📈 实施计划

### Phase 1: 基础功能 (1-2周)
- [x] 密码输入框UI组件
- [x] 服务选择联动逻辑
- [x] 基础登录功能
- [x] 状态管理框架

### Phase 2: 功能完善 (1周)
- [ ] 错误处理优化
- [ ] UI状态完善
- [ ] 基础测试用例
- [ ] 用户体验优化

### Phase 3: 高级功能 (1-2周)
- [ ] 账户信息存储
- [ ] 多账户管理
- [ ] 高级安全特性
- [ ] 性能优化

### Phase 4: 测试发布 (1周)
- [ ] 完整测试覆盖
- [ ] 用户文档编写
- [ ] 版本发布准备
- [ ] 用户反馈收集

## 📝 风险评估

### 1. 技术风险
- **API变更**：MailTM服务API可能变更
- **兼容性**：不同Python版本兼容性
- **性能**：大量账户管理的性能影响

### 2. 用户体验风险
- **复杂度**：功能增加可能导致界面复杂
- **学习成本**：新功能的学习曲线
- **稳定性**：新功能可能引入Bug

### 3. 缓解措施
- **API监控**：定期检查API状态
- **向下兼容**：保持旧功能可用
- **渐进发布**：分阶段发布新功能

## 📋 验收标准

### 1. 功能验收
- [x] MailTM服务选择时密码框正常启用
- [x] 非MailTM服务时密码框正确禁用
- [x] 邮箱生成同时显示密码
- [x] 登录功能正常工作
- [x] 状态切换流畅无误

### 2. 性能验收
- [x] UI响应时间 < 100ms
- [x] API调用超时 < 10s
- [x] 内存使用增长 < 20%

### 3. 用户体验验收
- [x] 界面直观易懂
- [x] 操作流程顺畅
- [x] 错误提示友好
- [x] 帮助文档完整

---

## 📞 联系信息

**项目负责人**: AugmentJSS开发团队  
**文档版本**: v1.0  
**最后更新**: 2025-07-30  
**审核状态**: 待审核

---

*本设计方案为AugmentJSS MailTM邮箱复用功能的详细技术设计文档，包含完整的功能需求、技术实现、测试方案和实施计划。*
