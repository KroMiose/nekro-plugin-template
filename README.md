# NekroAgent 插件模板

> 一个帮助开发者快速创建 NekroAgent 插件的模板仓库。

## 🚀 快速开始

### 1. 使用模板创建仓库

1. 点击本仓库页面上的 "Use this template" 按钮
2. 输入你的插件仓库名称，推荐命名格式：`nekro-plugin-[你的插件包名]`
3. 选择公开或私有仓库
4. 点击 "Create repository from template" 创建你的插件仓库

### 2. 克隆你的插件仓库

```bash
git clone https://github.com/你的用户名/你的插件仓库名.git
cd 你的插件仓库名
```

### 3. 安装依赖

```bash
# 安装 uv 包管理工具
curl -LsSf https://astral.sh/uv/install.sh | sh

# 根据指引安装 uv 后打开新的终端检查 uv 是否安装成功
uv --version

# 同步安装所有依赖（自动创建虚拟环境）
uv sync
```

## 📝 插件开发指南

### 插件结构

一个标准的 NekroAgent 插件需要在 `__init__.py` 中提供一个 `plugin` 实例，这是插件的核心，用于注册插件功能和配置。

```python
# 示例插件结构
plugin = NekroPlugin(
    name="你的插件名称",  # 插件显示名称
    module_name="plugin_module_name",  # 插件模块名 (在NekroAI社区需唯一)
    description="插件描述",  # 插件功能简介
    version="1.0.0",  # 插件版本
    author="你的名字",  # 作者信息
    url="https://github.com/你的用户名/你的插件仓库名",  # 插件仓库链接
)
```

### 开发功能

1. **配置插件参数**：使用 `@plugin.mount_config()` 装饰器创建可配置参数

```python
@plugin.mount_config()
class MyPluginConfig(ConfigBase):
    """插件配置说明"""

    API_KEY: str = Field(
        default="",
        title="API密钥",
        description="第三方服务的API密钥",
    )
```

2. **添加沙盒方法**：使用 `@plugin.mount_sandbox_method()` 添加 AI 可调用的函数

```python
@plugin.mount_sandbox_method(SandboxMethodType.AGENT, name="函数名称", description="函数功能描述")
async def my_function(_ctx: AgentCtx, param1: str) -> str:
    """实现插件功能的具体逻辑"""
    return f"处理结果: {param1}"
```

3. **资源清理**：使用 `@plugin.mount_cleanup_method()` 添加资源清理函数

```python
@plugin.mount_cleanup_method()
async def clean_up():
    """清理资源，如数据库连接等"""
    logger.info("资源已清理")
```

## 📦 插件发布

完成开发后，你可以：

1. 提交到 GitHub 仓库
2. 发布到 NekroAI 云社区共享给所有用户

## 🔍 更多资源

- [NekroAgent 官方文档](https://doc.nekro.ai/)
- [插件开发详细指南](https://doc.nekro.ai/docs/04_plugin_dev/intro.html)
- [社区交流群](https://qm.qq.com/q/hJlRwD17Ae)：636925153

## 📄 许可证

MIT
