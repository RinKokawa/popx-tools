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
    if npm_path:
        try:
            subprocess.run(
                ["npm", "install", "-g", "npm@6.14.12", "--registry=https://registry.npmmirror.com"],
                check=True, shell=True
            )
            npm_ver = subprocess.check_output(["npm", "-v"], text=True).strip()
            print(f"✅ npm 已安装，当前版本: {npm_ver}")
            return
        except subprocess.CalledProcessError:
            print("⚠️ 使用 npm 安装失败，尝试使用压缩包手动安装...")
    else:
        print("⚠️ 未检测到 npm，开始手动安装流程...")

    # 下载 npm .tgz 包
    url = "https://registry.npmmirror.com/npm/-/npm-6.14.12.tgz"
    temp_dir = Path(os.environ["TEMP"])
    tgz_path = temp_dir / "npm-6.14.12.tgz"
    extract_path = temp_dir / "package"

    print("🔽 开始下载 npm 压缩包 (.tgz)...")
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
        "--registry=https://registry.npmmirror.com"
    ], check=True)

    # 添加 npm.cmd 到 PATH（如果需要）
    nvm_nodejs_dir = Path("C:/nvm4w/nodejs")
    npm_cmd = nvm_nodejs_dir / "npm.cmd"
    if npm_cmd.exists():
        os.environ["PATH"] = f"{nvm_nodejs_dir};" + os.environ["PATH"]
        print(f"✅ npm.cmd 路径已加入环境变量: {nvm_nodejs_dir}")
    else:
        print("⚠️ 未找到 npm.cmd，可能需要手动添加路径或重新安装 Node")

    # 重命名可能阻止执行的 .ps1
    npm_ps1 = nvm_nodejs_dir / "npm.ps1"
    if npm_ps1.exists():
        npm_ps1.rename(nvm_nodejs_dir / "npm.ps1.bak")
        print("✅ 已禁用 npm.ps1，避免 PowerShell 拦截")

    print("✅ npm 安装完成，请重新打开终端验证 `npm -v`")
