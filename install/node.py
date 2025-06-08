import subprocess
import typer
import os

def install_node():
    """
    使用 npmmirror 镜像安装 Node.js v10.24.1
    """
    typer.echo("🔧 正在使用国内镜像安装 Node.js v10.24.1...")

    env = os.environ.copy()
    env["NVM_NODEJS_ORG_MIRROR"] = "https://npmmirror.com/mirrors/node"

    try:
        subprocess.run(["nvm", "install", "10.24.1"], check=True, shell=True, env=env)
        subprocess.run(["nvm", "use", "10.24.1"], check=True, shell=True)

        node_ver = subprocess.check_output(["node", "-v"], text=True).strip()
        npm_ver = subprocess.check_output(["npm", "-v"], text=True).strip()

        typer.echo(f"✅ Node.js 版本: {node_ver}")
        typer.echo(f"✅ npm 版本: {npm_ver}")
        typer.echo("🎉 Node.js 安装完成并已切换。")

    except subprocess.CalledProcessError as e:
        typer.echo("❌ Node.js 安装失败，请确认 nvm 是否已正确安装。")
        typer.echo("👉 手动运行也可以：")
        typer.echo("   set NVM_NODEJS_ORG_MIRROR=https://npmmirror.com/mirrors/node")
        typer.echo("   nvm install 10.24.1")
