import typer
from . import laya, popxcmd, node, npm  ,nvm # 可以按需添加

install_app = typer.Typer(help="安装 popx 相关依赖项")

# @install_app.callback()
# def install_callback(ctx: typer.Context):
#     """显示 install 子命令帮助"""
#     typer.echo(ctx.get_help())


install_app.command()(laya.install_laya)
install_app.command()(nvm.install_nvm)
install_app.command("install-nvm-local")(nvm.install_nvm_local)
install_app.command()(popxcmd.install_popxcmd)
install_app.command()(node.install_node)
install_app.command("install-npm")(npm.install_npm)
