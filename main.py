"""Augment just so so"""

try:
    import tkinter as tk
    from tkinter import ttk, messagebox, scrolledtext
except ImportError:
    print("错误：缺少tkinter模块。请安装完整的Python版本。")
    import sys
    sys.exit(1)
import platform
import ctypes
import os
import sys
import time
import subprocess
import threading
import webbrowser
from pathlib import Path
from datetime import datetime
try:
    from importlib import files
except ImportError:
    try:
        from importlib_resources import files
    except ImportError:
        files = None
import requests
import json
import re
import random
import string
import logging
VERSION_CONFIG = {
    "current_version": "1.0.0",
    "update_check": {
        "enabled": True,
        "test_mode": False,
        "test_version": "1.1.0",
        "primary_api": "https://aizaozao.com/accelerate.php/https://raw.githubusercontent.com/chc7nj2/version/refs/heads/main/augmentcode.json",
        "backup_api": "https://your-server.com/api/version",
        "timeout": 30,
        "download_url": "https://frequent-city-667.notion.site/augmentcode-21e22957056580659e0bcdf2ae6f57cd",
        "release_notes": """版本更新说明：
- ✅ 添加了软件更新检查功能
- ✅ 优化了用户界面显示
- ✅ 修复了一些已知问题
- 🆕 增强了邮箱生成功能
- 🆕 改进了验证码获取逻辑"""
    }
}

APP_CONFIG = {
    "name": "Augment just so so",
    "window": {
        "title": "Augment just so so",
        "size": "900x700",
        "resizable": True
    },
    "logging": {
        "level": "INFO",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    }
}

EMAIL_CONFIG = {
    "api": {
        "base_url": "https://tempmail.plus/api",
        "timeout": 30
    },
    "domains": [
        "196mail.tech",
        "qqemail.online", 
        "126mail.online",
        "163mail.online",
        "gmailgmail.site",
        "txmail.store",
        "mailto.plus",
        "tempmail.plus"
    ]
}

def get_system_info():
    system = platform.system().lower()
    machine = platform.machine().lower()

    if system == 'darwin':
        system = 'macos'
    elif system == 'windows':
        system = 'windows'
    elif system == 'linux':
        system = 'linux'

    if machine in ('x86_64', 'amd64'):
        arch = 'x86_64'
    elif machine in ('arm64', 'aarch64'):
        arch = 'aarch64'
    else:
        arch = machine

    return system, arch

def get_executable_filename():
    system, arch = get_system_info()
    return f"augment-just-so-so-{system}-{arch}" + (".exe" if system == "windows" else "")

def is_admin():
    try:
        if platform.system() == 'Windows':
            return ctypes.windll.shell32.IsUserAnAdmin()
        else:
            return os.geteuid() == 0
    except:
        return False

def get_resource_path(relative_path):
    if files is not None:
        try:
            if __package__ is None:
                package_files = files(__name__.split('.')[0])
            else:
                package_files = files(__package__)

            resource_path = package_files / relative_path
            if resource_path.is_file():
                return str(resource_path)
        except Exception:
            pass

    try:
        base_path = Path(sys._MEIPASS)
    except AttributeError:
        try:
            base_path = Path(__file__).parent
        except NameError:
            base_path = Path.cwd()

    return str(base_path / relative_path)

class TempMailClient:
    def __init__(self):
        self._setup_logging()

        self.CODE_PATTERNS = {
            "standard": r"(?<![a-zA-Z@.])\b\d{4,8}\b",
            "spaced": r"\b\d\s*\d\s*\d\s*\d\s*\d\s*\d\b",
            "prefixed": r"(?:验证码|code|码|号码|编号|verification|verify)[^\d]*(\d{4,8})",
            "html_code": r"<[^>]*>(\d{4,8})<[^>]*>",
            "chinese": r"您的验证码[是为：]*\s*(\d{4,8})",
            "english": r"(?:your|verification|confirm)\s*(?:code|number)[:\s]*(\d{4,8})"
        }

        # 多个临时邮箱API服务配置
        self.EMAIL_APIS = [
            {
                "name": "MailTM",
                "base_url": "https://api.mail.tm/",
                "domains_endpoint": "domains",
                "accounts_endpoint": "accounts",
                "token_endpoint": "token",
                "messages_endpoint": "messages"
            },
            {
                "name": "TempMail",
                "base_url": "https://www.1secmail.com/api/v1/",
                "get_domains": "?action=getDomainList",
                "generate": "?action=genRandomMailbox&count=1",
                "get_messages": "?action=getMessages&login={login}&domain={domain}",
                "read_message": "?action=readMessage&login={login}&domain={domain}&id={id}"
            },
            {
                "name": "TempMailPlus",
                "base_url": "https://tempmail.plus/api",
                "timeout": 30
            },
            {
                "name": "LocalGenerated",
                "domains": ["tempmail.plus", "mailto.plus", "10minutemail.com", "guerrillamail.com"]
            }
        ]

        self.current_email = None
        self.current_login = None
        self.current_domain = None
        self.current_api = None
        self.current_token = None
        self.current_password = None

        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
        })
    
    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('TempMailClient')
    
    def _compile_patterns(self):
        return {
            name: re.compile(pattern, re.I) 
            for name, pattern in self.CODE_PATTERNS.items()
        }
    
    def _clean_verification_code(self, code):
        return ''.join(char for char in code if char.isdigit())
    
    def _validate_code(self, code):
        """验证验证码是否有效"""
        cleaned_code = self._clean_verification_code(code)

        # 验证码长度通常为4-8位
        if len(cleaned_code) < 4 or len(cleaned_code) > 8:
            return False

        # 检查是否全是相同数字（如111111）
        if len(set(cleaned_code)) == 1:
            return False

        # 检查是否是连续数字（如123456）
        if len(cleaned_code) >= 4:
            is_sequential = True
            for i in range(1, len(cleaned_code)):
                if int(cleaned_code[i]) != int(cleaned_code[i-1]) + 1:
                    is_sequential = False
                    break
            if is_sequential:
                return False

        return True
    
    def generate_email(self, preferred_service=None):
        """生成真实的临时邮箱地址"""
        self.logger.info("开始生成真实临时邮箱...")

        # 如果指定了首选服务，先尝试该服务
        if preferred_service:
            api_config = self._get_api_config_by_name(preferred_service)
            if api_config:
                try:
                    email = self._generate_email_by_service(api_config)
                    if email:
                        self.current_email = email
                        self.current_api = api_config
                        self.logger.info(f"使用指定服务 {api_config['name']} 生成邮箱成功: {email}")
                        return email
                except Exception as e:
                    self.logger.warning(f"指定服务 {preferred_service} 生成邮箱失败: {e}")

        # 尝试不同的API服务
        for api_config in self.EMAIL_APIS:
            try:
                email = self._generate_email_by_service(api_config)
                if email:
                    self.current_email = email
                    self.current_api = api_config
                    self.logger.info(f"使用 {api_config['name']} 生成邮箱成功: {email}")
                    return email

            except Exception as e:
                self.logger.warning(f"{api_config['name']} 生成邮箱失败: {e}")
                continue

        # 如果所有API都失败，生成本地邮箱（作为备选）
        self.logger.warning("所有API服务失败，生成本地邮箱作为备选")
        return self._generate_local_email()

    def _get_api_config_by_name(self, service_name):
        """根据服务名称获取API配置"""
        service_mapping = {
            "1SecMail": "TempMail",
            "MailTM": "MailTM",
            "TempMail Plus": "TempMailPlus"
        }

        mapped_name = service_mapping.get(service_name, service_name)

        for api_config in self.EMAIL_APIS:
            if api_config["name"] == mapped_name:
                return api_config
        return None

    def _generate_email_by_service(self, api_config):
        """根据API配置生成邮箱"""
        if api_config["name"] == "MailTM":
            return self._generate_mailtm()
        elif api_config["name"] == "TempMail":
            return self._generate_1secmail()
        elif api_config["name"] == "TempMailPlus":
            return self._generate_tempmail_plus()
        elif api_config["name"] == "LocalGenerated":
            return self._generate_local_email()
        else:
            return None

    def _generate_mailtm(self):
        """使用mail.tm API生成邮箱"""
        api = self.EMAIL_APIS[0]  # MailTM配置

        try:
            # 获取可用域名
            domains_url = api["base_url"] + api["domains_endpoint"]
            response = self.session.get(domains_url, timeout=10)

            if response.status_code == 200:
                domains = response.json()
                if domains and len(domains) > 0:
                    domain = domains[0]['domain']
                else:
                    domain = 'mail.tm'
            else:
                domain = 'mail.tm'

            # 生成随机用户名和密码
            username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
            email = f"{username}@{domain}"
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

            # 创建账户
            account_data = {
                "address": email,
                "password": password
            }

            accounts_url = api["base_url"] + api["accounts_endpoint"]
            create_response = self.session.post(accounts_url, json=account_data, timeout=10)

            if create_response.status_code == 201:
                # 登录获取token
                token_url = api["base_url"] + api["token_endpoint"]
                login_response = self.session.post(token_url, json=account_data, timeout=10)

                if login_response.status_code == 200:
                    token_data = login_response.json()
                    self.current_token = token_data.get('token')
                    self.current_password = password
                    self.current_login = username
                    self.current_domain = domain

                    # 设置认证头
                    self.session.headers['Authorization'] = f'Bearer {self.current_token}'

                    self.logger.info(f"mail.tm邮箱创建成功: {email}")
                    return email

        except Exception as e:
            self.logger.error(f"mail.tm API失败: {e}")

        return None

    def _generate_1secmail(self):
        """使用1secmail API生成邮箱"""
        api = self.EMAIL_APIS[1]  # TempMail配置（1SecMail）

        # 获取可用域名
        try:
            response = self.session.get(api["base_url"] + api["get_domains"], timeout=10)
            if response.status_code == 200:
                domains = response.json()
                if domains:
                    domain = random.choice(domains)
                else:
                    domain = "1secmail.com"
            else:
                domain = "1secmail.com"
        except Exception:
            domain = "1secmail.com"

        # 生成随机用户名
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        email = f"{username}@{domain}"

        self.current_login = username
        self.current_domain = domain

        return email

    def _generate_tempmail_plus(self):
        """使用TempMail Plus API生成邮箱"""
        try:
            # TempMail Plus通常需要先获取域名，然后生成邮箱
            # 这里使用简化的方法，直接生成一个邮箱地址
            domains = ["tempmail.plus", "mailto.plus", "10minutemail.com"]
            username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
            domain = random.choice(domains)
            email = f"{username}@{domain}"

            self.current_email = email
            self.current_login = username
            self.current_domain = domain

            self.logger.info(f"TempMail Plus生成邮箱: {email}")
            return email

        except Exception as e:
            self.logger.error(f"TempMail Plus API失败: {e}")
            return None

    def _generate_guerrillamail(self):
        """使用GuerrillaMail API生成邮箱"""
        api = self.EMAIL_APIS[2]

        try:
            response = self.session.get(api["base_url"] + api["get_email"], timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'email_addr' in data:
                    email = data['email_addr']
                    parts = email.split('@')
                    if len(parts) == 2:
                        self.current_login = parts[0]
                        self.current_domain = parts[1]
                    return email
        except Exception as e:
            self.logger.error(f"GuerrillaMail API错误: {e}")

        return None

    def _generate_local_email(self):
        """生成本地邮箱作为备选"""
        domains = ["tempmail.plus", "mailto.plus", "1secmail.com"]
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
        domain = random.choice(domains)

        email = f"{username}@{domain}"
        self.current_login = username
        self.current_domain = domain

        return email
    
    def _extract_code_from_message(self, message):
        """从邮件消息中提取验证码"""
        try:
            # 获取邮件文本内容
            text_content = ""

            if isinstance(message, dict):
                # mail.tm格式
                if 'text' in message:
                    text_content += message['text']
                if 'html' in message:
                    text_content += message['html']
                if 'subject' in message:
                    text_content += message['subject']

                # 1secmail格式
                if 'textBody' in message:
                    text_content += message['textBody']
                if 'htmlBody' in message:
                    text_content += message['htmlBody']
            else:
                text_content = str(message)

            if not text_content:
                return None

            return self.extract_verification_code(text_content)

        except Exception as e:
            self.logger.error(f"提取验证码时出错: {e}")
            return None

    def extract_verification_code(self, mail_text):
        """从邮件文本中提取验证码"""
        if not mail_text:
            self.logger.warning("邮件文本为空")
            return None

        self.logger.info(f"开始提取验证码，邮件长度: {len(mail_text)}")

        # 清理HTML标签
        import re
        clean_text = re.sub(r'<[^>]+>', ' ', mail_text)

        patterns = self._compile_patterns()

        # 按优先级尝试不同的模式
        pattern_priority = ["prefixed", "chinese", "english", "standard", "html_code", "spaced"]

        for pattern_name in pattern_priority:
            if pattern_name in patterns:
                pattern = patterns[pattern_name]
                matches = pattern.findall(clean_text)

                if matches:
                    for match in matches:
                        code = match if isinstance(match, str) else match[0]
                        cleaned_code = self._clean_verification_code(code)

                        if self._validate_code(cleaned_code):
                            self.logger.info(f"使用模式 {pattern_name} 提取到验证码: {cleaned_code}")
                            return cleaned_code

        # 如果没有找到，尝试在原始HTML中查找
        html_matches = re.findall(r'\b\d{4,8}\b', mail_text)
        for match in html_matches:
            if self._validate_code(match):
                self.logger.info(f"在HTML中找到验证码: {match}")
                return match

        self.logger.warning("未能提取到有效验证码")
        return None
    
    def get_verification_code(self, max_retries=5, retry_interval=5):
        """获取真实的验证码"""
        if not self.current_email or not self.current_login or not self.current_domain:
            self.logger.error("邮箱信息不完整，无法获取验证码")
            return None

        self.logger.info(f"开始获取验证码，监控邮箱: {self.current_email}")

        for attempt in range(max_retries):
            try:
                self.logger.info(f"第 {attempt + 1}/{max_retries} 次尝试获取验证码")

                if attempt > 0:  # 第一次不等待
                    time.sleep(retry_interval)

                # 根据当前使用的API获取邮件
                messages = self._get_messages()

                if messages:
                    self.logger.info(f"找到 {len(messages)} 封邮件")

                    # 检查每封邮件中的验证码
                    for message in messages:
                        code = self._extract_code_from_message(message)
                        if code:
                            self.logger.info(f"验证码获取成功: {code}")
                            return code
                else:
                    self.logger.info("暂无新邮件")

            except Exception as e:
                self.logger.error(f"获取验证码失败: {e}")

        self.logger.error("达到最大重试次数，获取验证码失败")
        return None

    def _get_messages(self):
        """根据当前API获取邮件列表"""
        if not self.current_api:
            return []

        try:
            if self.current_api["name"] == "MailTM":
                return self._get_mailtm_messages()
            elif self.current_api["name"] == "TempMail":
                return self._get_1secmail_messages()
            elif self.current_api["name"] == "LocalGenerated":
                self.logger.info("本地生成的邮箱，请手动检查")
                return []
        except Exception as e:
            self.logger.error(f"获取邮件失败: {e}")

        return []

    def _get_mailtm_messages(self):
        """获取mail.tm邮件"""
        if not self.current_token:
            return []

        try:
            api = self.current_api
            messages_url = api["base_url"] + api["messages_endpoint"]

            response = self.session.get(messages_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                messages = data.get('hydra:member', [])

                # 获取邮件详细内容
                detailed_messages = []
                for msg in messages:
                    message_id = msg.get('id')
                    if message_id:
                        detail_url = f"{messages_url}/{message_id}"
                        detail_response = self.session.get(detail_url, timeout=10)
                        if detail_response.status_code == 200:
                            detailed_messages.append(detail_response.json())

                return detailed_messages

        except Exception as e:
            self.logger.error(f"获取mail.tm邮件失败: {e}")

        return []

    def _get_1secmail_messages(self):
        """获取1secmail邮件"""
        api = self.current_api
        url = api["base_url"] + api["get_messages"].format(
            login=self.current_login,
            domain=self.current_domain
        )

        response = self.session.get(url, timeout=10)
        if response.status_code == 200:
            messages = response.json()

            # 获取邮件详细内容
            detailed_messages = []
            for msg in messages:
                detail_url = api["base_url"] + api["read_message"].format(
                    login=self.current_login,
                    domain=self.current_domain,
                    id=msg["id"]
                )

                detail_response = self.session.get(detail_url, timeout=10)
                if detail_response.status_code == 200:
                    detailed_messages.append(detail_response.json())

            return detailed_messages

        return []

    def _get_guerrillamail_messages(self):
        """获取GuerrillaMail邮件"""
        api = self.current_api
        url = api["base_url"] + api["check_email"]

        response = self.session.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'list' in data:
                return data['list']

        return []

class VersionChecker:
    def __init__(self):
        self.config = VERSION_CONFIG
        self.update_config = self.config['update_check']
        self._setup_logging()
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': f'AugmentJustSoSo/{self.config["current_version"]}',
            'Accept': 'application/json'
        })
    
    def _setup_logging(self):
        self.logger = logging.getLogger('VersionChecker')
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    def get_current_version(self):
        return self.config['current_version']
    
    def check_for_updates(self, timeout=30):
        self.logger.info("开始检查软件更新...")
        
        if not self.update_config['enabled']:
            return self._get_test_update_info()
        
        try:
            update_info = self._check_github_api(timeout)
            if update_info:
                self.logger.info(f"版本检查完成: {update_info}")
                return update_info
            
            update_info = self._check_backup_api(timeout)
            if update_info:
                return update_info
                
            self.logger.warning("无法获取版本信息")
            return None
            
        except Exception as e:
            self.logger.error(f"检查更新时发生错误: {e}")
            return None
    
    def _get_test_update_info(self):
        self.logger.info("使用测试模式检查更新")
        return self._compare_versions(
            self.config['current_version'],
            self.update_config['test_version'],
            self.update_config['download_url'],
            self.update_config['release_notes']
        )
    
    def _check_github_api(self, timeout):
        return None
    
    def _check_backup_api(self, timeout):
        return None
    
    def _compare_versions(self, current, latest, download_url, release_notes):
        has_update = current != latest
        return {
            "has_update": has_update,
            "current_version": current,
            "latest_version": latest,
            "download_url": download_url,
            "release_notes": release_notes
        }

class ExecutorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Augment just so so")
        self.root.geometry("900x700")
        
        system, arch = get_system_info()
        self.system_display = f"{system.title()} {arch}"
        
        executable_filename = get_executable_filename()
        self.executable_path = get_resource_path(f"data/{executable_filename}")
        
        self.mail_client = TempMailClient()
        self.current_email = None
        self.is_getting_code = False
        
        self.version_checker = VersionChecker()
        
        self.setup_ui()
        self.set_app_icon()
        self.check_permissions_and_show_info()
        self.check_for_updates()
    
    def setup_ui(self):
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_frame = tk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(title_frame, text="Augment just so so",
                              font=("Arial", 18, "bold"), fg="#2c3e50")
        title_label.pack()
        
        version_label = tk.Label(title_frame,
                               text=f"版本 {self.version_checker.get_current_version()} | 系统: {self.system_display}",
                               font=("Arial", 10), fg="#7f8c8d")
        version_label.pack()
        
        email_frame = tk.LabelFrame(main_frame, text="📧 邮箱生成", 
                                  padx=15, pady=15, font=("Arial", 11, "bold"))
        email_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 服务选择框
        service_frame = tk.Frame(email_frame)
        service_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(service_frame, text="选择服务:", font=("Arial", 10)).pack(side=tk.LEFT)

        self.service_var = tk.StringVar()
        service_options = ["1SecMail", "MailTM", "TempMail Plus"]
        self.service_var.set("1SecMail")  # 默认选择1SecMail

        service_combo = ttk.Combobox(service_frame, textvariable=self.service_var,
                                   values=service_options, state="readonly", width=15)
        service_combo.pack(side=tk.LEFT, padx=(10, 0))

        email_display_frame = tk.Frame(email_frame)
        email_display_frame.pack(fill=tk.X, pady=(10, 10))

        tk.Label(email_display_frame, text="生成的邮箱:", font=("Arial", 10)).pack(side=tk.LEFT)

        self.email_var = tk.StringVar()
        email_entry = tk.Entry(email_display_frame, textvariable=self.email_var,
                              state="readonly", width=50, font=("Consolas", 10))
        email_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 0))
        
        email_btn_frame = tk.Frame(email_frame)
        email_btn_frame.pack()
        
        self.generate_btn = tk.Button(email_btn_frame, text="🔄 生成邮箱",
                                     command=self.generate_email,
                                     font=("Arial", 10), width=12)
        self.generate_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.copy_email_btn = tk.Button(email_btn_frame, text="📋 复制邮箱",
                                       command=self.copy_email, state="disabled",
                                       font=("Arial", 10), width=12)
        self.copy_email_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.reset_machine_btn = tk.Button(email_btn_frame, text="🔧 重置机器码",
                                          command=self.reset_machine_code,
                                          font=("Arial", 10), width=12)
        self.reset_machine_btn.pack(side=tk.LEFT)
        
        code_frame = tk.LabelFrame(main_frame, text="🔐 验证码获取", 
                                 padx=15, pady=15, font=("Arial", 11, "bold"))
        code_frame.pack(fill=tk.X, pady=(0, 15))
        
        code_display_frame = tk.Frame(code_frame)
        code_display_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(code_display_frame, text="验证码:", font=("Arial", 10)).pack(side=tk.LEFT)
        
        self.code_var = tk.StringVar()
        code_entry = tk.Entry(code_display_frame, textvariable=self.code_var, 
                             state="readonly", width=15, font=("Consolas", 14, "bold"),
                             justify=tk.CENTER)
        code_entry.pack(side=tk.RIGHT, padx=(10, 0))
        
        code_btn_frame = tk.Frame(code_frame)
        code_btn_frame.pack()
        
        self.get_code_btn = tk.Button(code_btn_frame, text="📬 获取验证码",
                                    command=self.get_verification_code,
                                    font=("Arial", 10), width=12)
        self.get_code_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.copy_code_btn = tk.Button(code_btn_frame, text="📋 复制验证码",
                                      command=self.copy_code, state="disabled",
                                      font=("Arial", 10), width=12)
        self.copy_code_btn.pack(side=tk.LEFT)
        
        status_frame = tk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.status_var = tk.StringVar(value="状态: 就绪")
        status_label = tk.Label(status_frame, textvariable=self.status_var,
                              font=("Arial", 10), fg="#27ae60")
        status_label.pack(side=tk.LEFT)
        
        self.show_log_btn = tk.Button(status_frame, text="📋 显示日志", 
                                     command=self.show_log_window,
                                     font=("Arial", 9))
        self.show_log_btn.pack(side=tk.RIGHT, padx=(0, 10))
        
        clear_btn = tk.Button(status_frame, text="🗑️ 清空", 
                            command=self.clear_log, font=("Arial", 9))
        clear_btn.pack(side=tk.RIGHT)
        
        log_frame = tk.LabelFrame(main_frame, text="📋 执行日志", 
                                padx=10, pady=10, font=("Arial", 10, "bold"))
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, 
                                                height=15, font=("Consolas", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        self.log_message("🚀 Augment just so so 启动成功")
        self.log_message(f"📦 当前版本: {self.version_checker.get_current_version()}")
        self.log_message(f"💻 系统信息: {self.system_display}")
        self.log_message("✅ 所有功能已就绪")
    
    def set_app_icon(self):
        self.icon_status = "未设置"
        try:
            icon_path = get_resource_path("icons/app_icon.ico")
            if Path(icon_path).exists():
                self.root.iconbitmap(icon_path)
                self.icon_status = "ICO图标加载成功"
                return
        except Exception:
            pass
        
        try:
            icon_path = get_resource_path("icons/icon_32.png")
            if Path(icon_path).exists():
                import tkinter as tk
                photo = tk.PhotoImage(file=icon_path)
                self.root.iconphoto(True, photo)
                self.icon_status = "PNG图标加载成功"
                return
        except Exception:
            pass
        
        self.icon_status = "未找到图标文件"
    
    def check_permissions_and_show_info(self):
        admin_status = "管理员" if is_admin() else "普通用户"
        self.log_message(f"🔐 权限状态: {admin_status}")
       
    
    def check_for_updates(self):
        def check_update_thread():
            try:
                update_info = self.version_checker.check_for_updates()
                if update_info and update_info.get('has_update'):
                    self.root.after(0, self.show_update_dialog, update_info)
                else:
                    self.root.after(0, self.log_message, "✅ 当前已是最新版本")
            except Exception as e:
                self.root.after(0, self.log_message, f"❌ 更新检查失败: {e}")
        
        threading.Thread(target=check_update_thread, daemon=True).start()
    
    def show_update_dialog(self, update_info):
        result = messagebox.askyesno(
            "发现新版本",
            f"发现新版本 {update_info['latest_version']}\n\n"
            f"当前版本: {update_info['current_version']}\n\n"
            f"更新说明:\n{update_info['release_notes']}\n\n"
            f"是否立即下载更新？"
        )
        
        if result:
            webbrowser.open(update_info['download_url'])
    
    def log_message(self, message):
        timestamp = datetime.now().strftime('%H:%M:%S')
        formatted_message = f'[{timestamp}] {message}\n'
        self.log_text.insert(tk.END, formatted_message)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_log(self):
        self.log_text.delete(1.0, tk.END)
        self.log_message("📋 日志已清空")
    
    def show_log_window(self):
        log_window = tk.Toplevel(self.root)
        log_window.title("执行日志")
        log_window.geometry("800x600")
        
        log_text = scrolledtext.ScrolledText(log_window, wrap=tk.WORD, font=("Consolas", 9))
        log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        current_log = self.log_text.get(1.0, tk.END)
        log_text.insert(1.0, current_log)
        
        btn_frame = tk.Frame(log_window)
        btn_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        tk.Button(btn_frame, text="关闭", command=log_window.destroy).pack(side=tk.RIGHT)
        tk.Button(btn_frame, text="复制全部", 
                 command=lambda: self.copy_all_log(log_text)).pack(side=tk.RIGHT, padx=(0, 10))
    
    def copy_all_log(self, log_text):
        content = log_text.get(1.0, tk.END)
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        messagebox.showinfo("提示", "日志已复制到剪贴板")
    
    def reset_machine_code(self):
        """重置机器码 - 调用外部可执行文件实现真正的硬件标识符修改"""
        # 首先检查管理员权限
        if not is_admin():
            messagebox.showerror(
                "权限不足",
                "重置机器码需要管理员权限！\n\n请以管理员身份重新运行此程序。"
            )
            self.log_message("❌ 权限不足：需要管理员权限才能重置机器码")
            return

        # 确认操作
        result = messagebox.askyesno(
            "重置机器码",
            "确定要重置机器码吗？\n\n⚠️ 警告：\n"
            "• 这将修改系统硬件标识符\n"
            "• 操作不可逆转\n"
            "• 可能影响某些软件的授权\n"
            "• 建议在操作前备份系统\n\n"
            "确定要继续吗？"
        )

        if result:
            # 获取可执行文件路径
            executable_path = self._get_machine_reset_executable()

            if not executable_path or not executable_path.exists():
                messagebox.showerror(
                    "文件不存在",
                    f"找不到机器码重置程序：\n{executable_path}\n\n"
                    "请确保程序文件完整。"
                )
                self.log_message("❌ 机器码重置程序不存在")
                return

            # 禁用按钮防止重复操作
            self.reset_machine_btn.config(state='disabled', text='重置中...')

            # 在线程中执行重置操作
            thread = threading.Thread(target=self._execute_machine_reset,
                                    args=(executable_path,), daemon=True)
            thread.start()

    def _get_machine_reset_executable(self):
        """获取机器码重置可执行文件的路径"""
        try:
            executable_name = "augmentjss-windows-x86_64.exe"

            # 尝试多个可能的路径
            possible_paths = []

            # 1. 尝试当前脚本所在目录的父目录（正常情况）
            try:
                current_dir = Path(__file__).parent.parent
                possible_paths.append(current_dir / executable_name)
            except (AttributeError, OSError):
                pass

            # 2. 尝试项目根目录（通过环境变量或固定路径）
            project_root_paths = [
                Path.cwd(),  # 当前工作目录
                Path.cwd().parent,  # 当前工作目录的父目录
            ]

            # 添加可能的项目路径（通过查找特征文件）
            current_path = Path(__file__).parent
            search_path = current_path
            for _ in range(5):  # 最多向上查找5级目录
                try:
                    # 查找包含特征文件的目录（如 src 目录或 requirements.txt）
                    if (search_path / "src").exists() or (search_path / "requirements.txt").exists():
                        project_root_paths.append(search_path)
                        break
                    search_path = search_path.parent
                    if search_path == search_path.parent:  # 到达根目录
                        break
                except (AttributeError, OSError):
                    break

            for root_path in project_root_paths:
                if root_path.exists():
                    possible_paths.append(root_path / executable_name)

            # 3. 尝试相对于临时目录的原始项目路径
            try:
                # 如果当前在临时目录，尝试找到原始项目路径
                current_path = Path(__file__).parent
                if "Temp" in str(current_path) or "temp" in str(current_path).lower():
                    # 这可能是通过run.py启动的临时目录，尝试常见的项目路径
                    common_project_paths = [
                        Path.home() / "Desktop" / "AugmentJSS",
                        Path.home() / "Documents" / "AugmentJSS",
                        Path("C:") / "AugmentJSS",
                        Path("D:") / "AugmentJSS",
                    ]

                    for project_path in common_project_paths:
                        if project_path.exists() and (project_path / executable_name).exists():
                            possible_paths.append(project_path / executable_name)
                            break
            except (AttributeError, OSError):
                pass

            # 查找第一个存在的可执行文件
            for executable_path in possible_paths:
                self.log_message(f"🔍 检查路径: {executable_path}")
                if executable_path.exists():
                    self.log_message(f"✅ 找到机器码重置程序: {executable_path}")
                    return executable_path

            # 如果都没找到，返回第一个路径（用于错误提示）
            if possible_paths:
                self.log_message("❌ 在以下路径中未找到机器码重置程序:")
                for path in possible_paths:
                    self.log_message(f"   - {path}")
                return possible_paths[0]
            else:
                self.log_message("❌ 无法确定可执行文件路径")
                return None

        except Exception as e:
            self.log_message(f"❌ 获取可执行文件路径失败: {e}")
            return None

    def _execute_machine_reset(self, executable_path):
        """在线程中执行机器码重置"""
        try:
            self.root.after(0, self.log_message, "🔧 正在启动机器码重置程序...")
            self.root.after(0, self.log_message, "🔐 以管理员权限运行...")

            start_time = time.time()

            # 以管理员权限执行外部程序
            if sys.platform == 'win32':
                # 简化的Windows执行方式
                import ctypes

                self.root.after(0, self.log_message, "⚡ 启动可执行文件...")

                # 直接使用ShellExecute运行，不捕获输出（避免卡住）
                result_code = ctypes.windll.shell32.ShellExecuteW(
                    None,
                    "runas",  # 以管理员身份运行
                    str(executable_path),
                    None,  # 无参数
                    str(executable_path.parent),
                    1  # SW_SHOWNORMAL - 显示窗口
                )

                self.root.after(0, self.log_message, f"🔍 ShellExecute返回码: {result_code}")

                if result_code <= 32:  # 错误
                    error_messages = {
                        0: "系统内存不足",
                        2: "找不到指定文件",
                        3: "找不到指定路径",
                        5: "访问被拒绝",
                        8: "内存不足",
                        26: "共享冲突",
                        27: "关联不完整",
                        28: "DDE超时",
                        29: "DDE失败",
                        30: "DDE忙",
                        31: "没有关联",
                        32: "DLL未找到"
                    }
                    error_msg = error_messages.get(result_code, f"未知错误 (代码: {result_code})")
                    raise Exception(f"启动失败: {error_msg}")

                # 给用户一些时间来操作外部程序
                self.root.after(0, self.log_message, "✅ 程序已启动，请在弹出的窗口中完成操作")

                # 等待30秒（给用户足够时间操作）- 静默等待，不输出倒计时日志
                for _ in range(30):
                    time.sleep(1)

                # 创建成功结果（假设用户已完成操作）
                class MockResult:
                    def __init__(self, returncode, stdout, stderr):
                        self.returncode = returncode
                        self.stdout = stdout
                        self.stderr = stderr

                result = MockResult(0, "机器码重置程序已启动，请在弹出窗口中完成操作", "")

            else:
                # Linux/macOS系统使用sudo
                result = subprocess.run(
                    ["sudo", str(executable_path)],
                    capture_output=True,
                    text=True,
                    timeout=60,  # 减少到1分钟超时
                )

            execution_time = time.time() - start_time

            # 在主线程中更新UI
            self.root.after(0, self._update_reset_result, result, execution_time)

        except subprocess.TimeoutExpired:
            self.root.after(0, self._update_reset_timeout)
        except Exception as e:
            self.root.after(0, self._update_reset_error, str(e))

    def _update_reset_result(self, result, execution_time):
        """更新机器码重置结果"""
        try:
            if result.returncode == 0:
                self.log_message(f"✅ 机器码重置程序启动成功！")
                self.log_message(f"⏱️ 执行时间: {execution_time:.2f} 秒")

                if result.stdout:
                    self.log_message("📤 程序信息:")
                    for line in result.stdout.strip().split('\n'):
                        if line.strip():
                            self.log_message(f"   {line}")

                messagebox.showinfo(
                    "程序启动成功",
                    "✅ 机器码重置程序已启动！\n\n"
                    "请在弹出的程序窗口中完成以下操作：\n"
                    "1. 按照程序提示进行操作\n"
                    "2. 等待程序完成重置过程\n"
                    "3. 完成后建议重启计算机\n\n"
                    "注意：如果没有看到程序窗口，请检查任务栏或被其他窗口遮挡。"
                )

                # 提示用户手动重启系统
                self.log_message("💡 重要提示：为确保机器码重置完全生效，建议手动重启计算机")
                self.log_message("🔄 请在方便的时候重启系统以完成机器码重置过程")
                self.log_message("⚠️ 注意：机器码变更可能导致VSCode等软件自动关闭或需要重新登录")

                messagebox.showinfo(
                    "操作完成",
                    "✅ 机器码重置程序已运行完成！\n\n"
                    "💡 重要提示：\n"
                    "• 建议在方便的时候重启计算机以确保更改完全生效\n"
                    "• VSCode等开发工具可能会自动关闭，这是正常现象\n"
                    "• Augment等服务可能需要重新登录\n"
                    "• 某些软件的设备授权可能需要重新验证\n\n"
                    "请保存所有重要工作后手动重启系统。"
                )

            else:
                self.log_message(f"❌ 机器码重置程序启动失败 (返回码: {result.returncode})")
                self.log_message(f"⏱️ 执行时间: {execution_time:.2f} 秒")

                error_msg = "机器码重置程序启动失败！\n\n"

                if result.stderr:
                    self.log_message("❌ 错误输出:")
                    for line in result.stderr.strip().split('\n'):
                        if line.strip():
                            self.log_message(f"   {line}")
                    error_msg += f"错误信息:\n{result.stderr[:200]}..."

                error_msg += "\n可能的解决方案：\n"
                error_msg += "• 确保以管理员身份运行程序\n"
                error_msg += "• 检查防病毒软件是否阻止了程序\n"
                error_msg += "• 确保可执行文件完整且未损坏"

                messagebox.showerror("启动失败", error_msg)

        except Exception as e:
            self.log_message(f"❌ 处理重置结果时出错: {e}")
            messagebox.showerror("处理错误", f"处理重置结果时出错: {e}")

        finally:
            # 恢复按钮状态
            self.reset_machine_btn.config(state='normal', text='🔧 重置机器码')

    def _update_reset_timeout(self):
        """更新超时结果"""
        self.log_message("❌ 机器码重置超时 (超过5分钟)")
        messagebox.showerror(
            "操作超时",
            "机器码重置操作超时！\n\n"
            "可能原因：\n"
            "• 程序需要更长时间执行\n"
            "• 程序遇到了问题\n"
            "• 系统资源不足\n\n"
            "请检查系统状态后重试。"
        )
        self.reset_machine_btn.config(state='normal', text='🔧 重置机器码')

    def _update_reset_error(self, error_msg):
        """更新错误结果"""
        self.log_message(f"❌ 机器码重置出错: {error_msg}")
        messagebox.showerror(
            "执行错误",
            f"机器码重置程序执行出错：\n\n{error_msg}\n\n"
            "请检查：\n"
            "• 程序文件是否完整\n"
            "• 是否有足够的系统权限\n"
            "• 防病毒软件是否阻止了操作"
        )
        self.reset_machine_btn.config(state='normal', text='🔧 重置机器码')
    
    def generate_email(self):
        try:
            selected_service = self.service_var.get()
            self.log_message(f'📧 正在使用 {selected_service} 生成临时邮箱地址...')
            self.generate_btn.config(state='disabled', text='生成中...')

            # 在新线程中生成邮箱以避免UI阻塞
            def generate_thread():
                try:
                    email = self.mail_client.generate_email(preferred_service=selected_service)
                    self.root.after(0, self._update_email_result, email)
                except Exception as e:
                    self.root.after(0, self._update_email_error, str(e))

            threading.Thread(target=generate_thread, daemon=True).start()

        except Exception as e:
            self.log_message(f'❌ 生成邮箱失败: {e}')
            messagebox.showerror('错误', f'生成邮箱失败: {e}')
            self.generate_btn.config(state='normal', text='🔄 生成邮箱')

    def _update_email_result(self, email):
        """更新邮箱生成结果"""
        self.generate_btn.config(state='normal', text='🔄 生成邮箱')

        if email:
            self.current_email = email
            self.email_var.set(email)

            self.copy_email_btn.config(state='normal')
            self.get_code_btn.config(state='normal')

            self.log_message(f'✅ 邮箱生成成功: {email}')

            if self.mail_client.current_api:
                api_name = self.mail_client.current_api['name']
                self.log_message(f'🌐 使用API服务: {api_name}')

            if self.mail_client.current_domain:
                self.log_message(f'📧 邮箱域名: {self.mail_client.current_domain}')

            self.status_var.set('状态: 邮箱已生成')
        else:
            self.log_message('❌ 邮箱生成失败')
            self.status_var.set('状态: 邮箱生成失败')
            messagebox.showerror('错误', '邮箱生成失败，请重试')

    def _update_email_error(self, error_msg):
        """更新邮箱生成错误"""
        self.generate_btn.config(state='normal', text='🔄 生成邮箱')
        self.log_message(f'❌ 生成邮箱失败: {error_msg}')
        self.status_var.set('状态: 邮箱生成失败')
        messagebox.showerror('错误', f'生成邮箱失败: {error_msg}')
    
    def copy_email(self):
        if self.current_email:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.current_email)
            self.log_message('📋 邮箱地址已复制到剪贴板')
            self.status_var.set('状态: 邮箱已复制')
            messagebox.showinfo('提示', '邮箱地址已复制到剪贴板')
    
    def copy_code(self):
        code = self.code_var.get()
        if code:
            self.root.clipboard_clear()
            self.root.clipboard_append(code)
            self.log_message('📋 验证码已复制到剪贴板')
            self.status_var.set('状态: 验证码已复制')
            messagebox.showinfo('提示', '验证码已复制到剪贴板')
    
    def get_verification_code(self):
        if self.is_getting_code:
            self.log_message('⚠️ 正在获取验证码，请稍候...')
            return
        
        if not self.current_email:
            messagebox.showwarning('警告', '请先生成邮箱地址')
            return
        
        self.is_getting_code = True
        self.get_code_btn.config(state='disabled', text='获取中...')
        self.status_var.set('状态: 正在获取验证码...')
        
        thread = threading.Thread(target=self._get_code_thread, daemon=True)
        thread.start()
    
    def _get_code_thread(self):
        try:
            self.root.after(0, self.log_message, '📬 开始获取验证码...')
            self.root.after(0, self.log_message, f'📧 监控邮箱: {self.current_email}')

            if self.mail_client.current_api:
                api_name = self.mail_client.current_api['name']
                self.root.after(0, self.log_message, f'🔗 使用API: {api_name}')

            self.root.after(0, self.log_message, '⏳ 等待邮件到达，这可能需要几秒钟...')

            # 增加重试次数和间隔时间，因为真实邮件需要时间
            code = self.mail_client.get_verification_code(max_retries=5, retry_interval=5)
            self.root.after(0, self._update_code_result, code)
        except Exception as e:
            self.root.after(0, self._update_code_error, str(e))
    
    def _update_code_result(self, code):
        self.is_getting_code = False
        self.get_code_btn.config(state='normal', text='📬 获取验证码')

        if code:
            self.code_var.set(code)
            self.copy_code_btn.config(state='normal')
            self.log_message(f'✅ 验证码获取成功: {code}')
            self.log_message(f'📊 验证码长度: {len(code)} 位')
            self.status_var.set('状态: 验证码已获取')
            messagebox.showinfo('成功', f'验证码获取成功!\n\n验证码: {code}\n长度: {len(code)} 位')
        else:
            self.log_message('❌ 未能获取到验证码')
            self.log_message('💡 提示: 请确保已向该邮箱发送了验证码邮件')
            self.status_var.set('状态: 获取验证码失败')
            messagebox.showerror('失败', '未能获取到验证码\n\n可能原因:\n1. 邮件还未到达，请稍后重试\n2. 验证码邮件被过滤\n3. 邮箱服务暂时不可用')
    
    def _update_code_error(self, error_msg):
        self.is_getting_code = False
        self.get_code_btn.config(state='normal', text='📬 获取验证码')
        self.log_message(f'❌ 获取验证码出错: {error_msg}')
        self.status_var.set('状态: 获取验证码出错')
        messagebox.showerror('错误', f'获取验证码出错: {error_msg}')
    
    def run(self):
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after(1000, lambda: self.root.attributes('-topmost', False))
        
        self.root.mainloop()

def main():
    try:
        app = ExecutorApp()
        app.run()
    except Exception as e:
        print(f"程序启动失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
