import typer
from . import laya, popxcmd, node, npm, nvm  ,uninstall# 按需导入模块

install_app = typer.Typer(help="安装 popx 相关依赖项")


@install_app.command("laya")
def laya_cmd():
    """安装 laya 工具"""
    laya.install_laya()


@install_app.command("nvm")
def nvm_cmd():
    """安装 nvm"""
    nvm.install_nvm()


@install_app.command("install-nvm-local")
def nvm_local_cmd():
    """使用本地安装器安装 nvm"""
    nvm.install_nvm_local()




@install_app.command("node")
def node_cmd():
    """安装 Node.js"""
    node.install_node()


@install_app.command("npm")
def npm_cmd():
    """安装 npm"""
    npm.install_npm()

@install_app.command("popxcmd")
def popxcmd_cmd():
    """安装 popx 命令工具"""
    popxcmd.install_popxcmd()

install_app.add_typer(uninstall.app, name="uninstall", help="卸载所有组件")

# 确保 install_app 被模块导出
__all__ = ["install_app"]
