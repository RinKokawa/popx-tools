from setuptools import setup, find_packages
import os

# 读取README文件
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# 收集bin目录下的所有文件
def get_bin_files():
    bin_files = []
    bin_dir = "install/bin"
    if os.path.exists(bin_dir):
        for file in os.listdir(bin_dir):
            bin_files.append(os.path.join(bin_dir, file))
    return bin_files

setup(
    name="popx-tools",
    version="1.0.0",
    author="Rinkokawa",
    author_email="rin@rinco.cc",  # 请替换为您的邮箱
    description="Popx 环境部署 CLI 工具集",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/RinKokawa/popx-tools",  # 请替换为您的仓库地址
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "install": ["bin/*"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "typer>=0.9.0",
        "Pillow>=8.0.0",
        "rich>=10.0.0",
    ],
    entry_points={
        "console_scripts": [
            "popx=cli:main",
        ],
    },
    zip_safe=False,
) 