import requests
from tqdm import tqdm
import typer
import os
import subprocess
from importlib.resources import files
from pathlib import Path

app = typer.Typer()

@app.command("install-nvm")
def install_nvm():
    """
    在线下载并安装 nvm，失败则回退使用内置安装器。
    """
    url = "https://github.com/coreybutler/nvm-windows/releases/latest/download/nvm-setup.exe"
    temp_path = os.path.join(os.environ["TEMP"], "nvm-setup.exe")
    typer.echo("🔽 正在尝试从 GitHub 下载 nvm 安装程序...")

    try:
        with requests.get(url, stream=True, timeout=30) as r:
            r.raise_for_status()
            total = int(r.headers.get('Content-Length', 0))
            with open(temp_path, 'wb') as f, tqdm(
                total=total, unit='B', unit_scale=True, desc="📦 下载进度"
            ) as bar:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        bar.update(len(chunk))

        typer.echo("✅ 下载完成，启动安装程序...")
        typer.echo("✅ 全部执行下一步即可。")
        subprocess.Popen([temp_path], shell=True)

    except Exception as e:
        typer.echo(f"❌ 下载失败: {e}")
        typer.echo("👉 正在尝试使用内置安装包继续安装...")
        install_nvm_local()


@app.command("install-nvm-local")
def install_nvm_local():
    """
    直接使用内置 nvm 安装器安装。
    """
    try:
        resource = files("install.bin").joinpath("nvm-setup.exe")
        fallback_path = Path(os.environ["TEMP"]) / "nvm-setup-fallback.exe"

        with resource.open("rb") as src, open(fallback_path, "wb") as dst:
            dst.write(src.read())

        typer.echo("✅ 内置安装包已准备，启动安装程序...")
        typer.echo("✅ 全部执行下一步即可。")
        subprocess.Popen([str(fallback_path)], shell=True)

    except Exception as fallback_error:
        typer.echo(f"❌ 内置安装也失败了: {fallback_error}")
        typer.echo("👉 手动下载地址：https://github.com/coreybutler/nvm-windows/releases")

if __name__ == "__main__":
    app()
