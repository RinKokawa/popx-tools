import typer
import subprocess
import os
from . import runner

run_app = typer.Typer(
    help="运行 popx 相关命令，自动管理 Node.js 版本",
    no_args_is_help=True,
    epilog="示例: popx run ui  # 运行 UI 开发服务器\n       popx run build  # 构建项目"
)


@run_app.command("ui")
def run_ui():
    """
    运行 UI 开发服务器
    
    自动检查并切换到 Node.js 10.24.1 版本，执行 npm run ui 命令，
    完成后自动切换回 Node.js 22.15.0 版本。
    
    工作流程:
    1. 检查当前 Node.js 版本
    2. 如果不是 10.24.1，自动切换到 10.24.1
    3. 执行 npm run ui
    4. 自动切换回 22.15.0
    """
    runner.run_command("ui")


@run_app.command("build")
def run_build():
    """
    构建项目
    
    自动检查并切换到 Node.js 10.24.1 版本，执行 npm run build 命令，
    完成后自动切换回 Node.js 22.15.0 版本。
    
    工作流程:
    1. 检查当前 Node.js 版本
    2. 如果不是 10.24.1，自动切换到 10.24.1
    3. 执行 npm run build
    4. 自动切换回 22.15.0
    """
    runner.run_command("build")


# 确保 run_app 被模块导出
__all__ = ["run_app"] 