import typer
from . import laya, popxcmd, node, npm, nvm  # 按需导入模块

install_app = typer.Typer(help="安装 popx 相关依赖项", no_args_is_help=True)


@install_app.command("laya")
def laya_cmd():
    """安装 laya 工具"""
    laya.install_laya()


@install_app.command("all")
def install_all():
    """
    一键安装 nvm + node + npm（离线优先）
    """
    from . import nvm, node, npm

    typer.echo("🚀 开始一键安装所有组件（nvm → node → npm）")
    
    # 顺序安装
    try:
        nvm.install_nvm()
        node.install_node()
        npm.install_npm()
        typer.secho("🎉 全部安装完成！", fg=typer.colors.GREEN)
    except Exception as e:
        typer.secho(f"❌ 安装过程中出错: {e}", fg=typer.colors.RED)


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

# 确保 install_app 被模块导出
__all__ = ["install_app"]
