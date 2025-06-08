import subprocess
import typer
import os

def install_node():
    """
    使用 npmmirror 镜像安装 Node.js v10.24.1，并自动切换环境
    """
    typer.echo("🔧 正在使用国内镜像安装 Node.js v10.24.1...")

    # 获取当前环境变量，并设置 NVM 镜像地址
    env = os.environ.copy()
    env["NVM_NODEJS_ORG_MIRROR"] = "https://npmmirror.com/mirrors/node"

    try:
        # 安装并切换 Node 版本
        subprocess.run("nvm install 10.24.1", check=True, shell=True, env=env)
        subprocess.run("nvm use 10.24.1", check=True, shell=True, env=env)

        # 获取 node 路径所在目录
        node_path = subprocess.check_output("where node", shell=True, text=True, env=env).strip()
        node_dir = os.path.dirname(node_path.splitlines()[0])
        env["PATH"] = f"{node_dir};{env['PATH']}"

        # 获取版本信息
        node_ver = subprocess.check_output(["node", "-v"], text=True, env=env).strip()
        npm_ver = subprocess.check_output(["npm", "-v"], text=True, env=env).strip()

        # 成功提示
        typer.echo(f"✅ Node.js 版本: {node_ver}")
        typer.echo(f"✅ npm 版本: {npm_ver}")
        typer.echo("🎉 Node.js 安装完成并已切换。")

    except subprocess.CalledProcessError:
        typer.echo("❌ Node.js 安装失败，请确认 nvm 是否已正确安装。")
        typer.echo("👉 手动运行也可以：")
        typer.echo("   set NVM_NODEJS_ORG_MIRROR=https://npmmirror.com/mirrors/node")
        typer.echo("   nvm install 10.24.1")
        raise
    except FileNotFoundError:
        typer.echo("❌ 未找到 node 命令，可能 PATH 未正确更新。")
        typer.echo("🔎 请确认 `nvm use` 后 node 可用，或尝试重启终端。")
        raise
