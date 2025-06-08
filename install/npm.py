import os
import subprocess
import shutil
import requests
import tarfile
from tqdm import tqdm
from pathlib import Path

def install_npm():
    """
    使用 npmmirror 安装 npm@6.14.12，如果未检测到 npm，则自动下载 .tgz 包手动安装。
    """
    npm_path = shutil.which("npm")
    npm_mirror = "https://npmmirror.com/mirrors/npm/"
    if npm_path:
        try:
            subprocess.run(
                ["npm", "install", "-g", "npm@6.14.12", f"--registry={npm_mirror}"],
                check=True, shell=True
            )
            npm_ver = subprocess.check_output(["npm", "-v"], text=True).strip()
            print(f"✅ npm 已安装，当前版本: {npm_ver}")
            return
        except subprocess.CalledProcessError:
            print("⚠️ 使用 npm 安装失败，尝试使用压缩包手动安装...")
    else:
        print("⚠️ 未检测到 npm，开始手动安装流程...")

    url = f"{npm_mirror}/-/npm-6.14.12.tgz"
    temp_dir = Path(os.environ["TEMP"])
    tgz_path = temp_dir / "npm-6.14.12.tgz"
    extract_path = temp_dir / "package"

    print("🔽 正在下载 npm 压缩包 (.tgz)...")
    with requests.get(url, stream=True, timeout=30) as r:
        r.raise_for_status()
        total = int(r.headers.get("Content-Length", 0))
        with open(tgz_path, "wb") as f, tqdm(total=total, unit='B', unit_scale=True, desc="📦 下载进度") as bar:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    bar.update(len(chunk))

    print("📂 下载完成，正在解压缩...")
    with tarfile.open(tgz_path, "r:gz") as tar:
        tar.extractall(path=temp_dir)

    cli_path = extract_path / "bin" / "npm-cli.js"

    print(f"🚀 使用 npm-cli.js 执行安装命令...")
    subprocess.run([
        "node", str(cli_path), "install", "-g", "npm@6.14.12",
        f"--registry={npm_mirror}"
    ], check=True)

    # 确认路径并更新 PATH
    possible_dirs = [
        Path("C:/nvm4w/nodejs"),
        Path("C:/Users/admin/AppData/Local/nvm/nodejs")
    ]

    for dir_path in possible_dirs:
        if (dir_path / "npm.cmd").exists():
            os.environ["PATH"] = f"{dir_path};" + os.environ["PATH"]
            print(f"✅ 已添加 npm 路径到 PATH: {dir_path}")

            ps1_file = dir_path / "npm.ps1"
            if ps1_file.exists():
                ps1_file.rename(ps1_file.with_suffix(".ps1.bak"))
                print("✅ 已禁用 npm.ps1，避免 PowerShell 拦截")
            break
    else:
        print("⚠️ 未找到 npm.cmd，可能需要手动添加路径或重新安装 Node")

    print("✅ npm 安装完成，请重新打开终端验证 `npm -v`")
