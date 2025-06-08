import typer
import sys
from typing import List, Optional
from .install import install_app
from .uninstall import uninstall_app
from .ui import ui_app

app = typer.Typer(help="Popx 环境部署 CLI 工具", no_args_is_help=True)

# 添加子命令
app.add_typer(install_app, name="install", help="安装相关依赖")
app.add_typer(uninstall_app, name="uninstall", help="卸载相关依赖") 
app.add_typer(ui_app, name="ui", help="图像处理工具")

def main():
    """主入口函数"""
    app()

if __name__ == "__main__":
    main()
