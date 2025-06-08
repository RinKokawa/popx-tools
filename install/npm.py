import subprocess
import typer
import shutil
import os
import tarfile
import requests
from tqdm import tqdm
from pathlib import Path

def install_npm():
    """
    使用 npmmirror 安装 npm@6.14.12，如果失败则自动下载 .tgz 包并解压。
    """
    typer.echo("🔧 尝试使用国内镜像安装 npm@6.14.12...")

    npm_path = shutil.which("npm")
    if npm_path is not None:
        try:
            subprocess.run(
                ["npm", "install", "-g", "npm@6.14.12", "--registry=https://registry.npmmirror.com"],
                check=True, shell=True
            )
            npm_ver = subprocess.check_output(["npm", "-v"], text=True).strip()
            typer.echo(f"✅ npm 安装完成，当前版本: {npm_ver}")
            return
        except subprocess.CalledProcessError:
            typer.echo("⚠️ npm 安装失败，尝试使用压缩包安装...")

    else:
        typer.echo("⚠️ 未检测到 npm，尝试使用压缩包手动安装...")

    # fallback: 下载 .tgz 包
    url = "https://registry.npmmirror.com/npm/-/npm-6.14.12.tgz"
    temp_dir = Path(os.environ["TEMP"])
    tgz_path = temp_dir / "npm-6.14.12.tgz"
    extract_path = temp_dir / "npm-extracted"

    try:
        typer.echo("🔽 开始下载 npm 压缩包 (.tgz)...")
        with requests.get(url, stream=True, timeout=30) as r:
            r.raise_for_status()
            total = int(r.headers.get("Content-Length", 0))
            with open(tgz_path, "wb") as f, tqdm(
                total=total, unit='B', unit_scale=True, desc="📦 下载进度"
            ) as bar:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        bar.update(len(chunk))

        typer.echo("📂 下载完成，正在解压缩...")
        with tarfile.open(tgz_path, "r:gz") as tar:
            tar.extractall(path=extract_path)

        typer.echo("✅ 解压完成，npm 代码位于:")
        typer.echo(f"   {extract_path / 'package'}")

        typer.echo("👉 你可以执行以下命令手动安装:")
        typer.echo(f"   node {extract_path / 'package' / 'bin' / 'npm-cli.js'} install -g")

    except Exception as e:
        typer.echo(f"❌ 下载或解压失败: {e}")
        typer.echo("👉 手动下载地址：https://registry.npmmirror.com/npm/-/npm-6.14.12.tgz")
