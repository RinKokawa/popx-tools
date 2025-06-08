import requests
from tqdm import tqdm
import typer
import os
import subprocess

def install_nvm():
    url = "https://github.com/coreybutler/nvm-windows/releases/latest/download/nvm-setup.exe"
    local_path = os.path.join(os.environ["TEMP"], "nvm-setup.exe")
    typer.echo("🔽 开始下载 nvm 安装程序...")

    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            total = int(r.headers.get('Content-Length', 0))
            with open(local_path, 'wb') as f, tqdm(
                total=total, unit='B', unit_scale=True, desc="📦 下载进度"
            ) as bar:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        bar.update(len(chunk))

        typer.echo("✅ 下载完成，启动安装程序...")
        subprocess.Popen([local_path], shell=True)

    except Exception as e:
        typer.echo(f"❌ 下载失败: {e}")
        typer.echo("👉 手动访问：https://github.com/coreybutler/nvm-windows/releases")
