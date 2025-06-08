import subprocess
import typer
import os
from pathlib import Path
import shutil

def install_node():
    """
    使用 npmmirror 镜像安装 Node.js v10.24.1，并自动切换环境
    """
    typer.echo("🔧 正在使用国内镜像安装 Node.js v10.24.1...")

    env = os.environ.copy()
    env["NVM_NODEJS_ORG_MIRROR"] = "https://npmmirror.com/mirrors/node"

    try:
        subprocess.run("nvm install 10.24.1", check=True, shell=True, env=env)
        subprocess.run("nvm use 10.24.1", check=True, shell=True, env=env)

        # 自动添加 node 路径
        node_path = shutil.which("node")
        if node_path:
            node_dir = os.path.dirname(node_path)
            if node_dir not in env["PATH"]:
                env["PATH"] = f"{node_dir};{env['PATH']}"
            node_ver = subprocess.check_output(["node", "-v"], text=True, env=env).strip()
            npm_ver = subprocess.check_output(["npm", "-v"], text=True, env=env).strip()
            typer.echo(f"✅ Node.js 版本: {node_ver}")
            typer.echo(f"✅ npm 版本: {npm_ver}")
        else:
            raise FileNotFoundError

        typer.echo("🎉 Node.js 安装完成并已切换。")

    except subprocess.CalledProcessError:
        typer.echo("❌ Node.js 安装失败，请确认 nvm 是否已正确安装。")
        typer.echo("👉 可手动尝试：")
        typer.echo("   set NVM_NODEJS_ORG_MIRROR=https://npmmirror.com/mirrors/node")
        typer.echo("   nvm install 10.24.1")
        raise

    except FileNotFoundError:
        typer.echo("❌ 未找到 node 命令，可能 PATH 未正确更新。")
        typer.echo("🔎 请确认 `nvm use` 后 node 可用，或尝试重启终端。")
        raise
