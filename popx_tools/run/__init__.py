import typer
import subprocess
import os
from . import runner

run_app = typer.Typer(help="运行 popx 相关命令", no_args_is_help=True)


@run_app.command("ui")
def run_ui():
    """运行 UI 开发服务器"""
    runner.run_command("ui")


@run_app.command("build")
def run_build():
    """构建项目"""
    runner.run_command("build")


# 确保 run_app 被模块导出
__all__ = ["run_app"] 