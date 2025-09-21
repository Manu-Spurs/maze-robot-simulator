#!/usr/bin/env python3
"""
Maze Robot Simulator Installation Script
迷宫机器人模拟器安装脚本
"""

import subprocess
import sys
import os

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 7):
        print("错误: 需要Python 3.7或更高版本")
        print(f"当前版本: {sys.version}")
        return False
    print(f"✓ Python版本检查通过: {sys.version}")
    return True

def install_requirements():
    """安装依赖包"""
    try:
        print("正在安装依赖包...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ 依赖包安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ 依赖包安装失败: {e}")
        return False

def check_pygame():
    """检查Pygame是否正确安装"""
    try:
        import pygame
        print(f"✓ Pygame版本: {pygame.version.ver}")
        return True
    except ImportError:
        print("✗ Pygame未正确安装")
        return False

def main():
    """主安装流程"""
    print("=" * 50)
    print("迷宫机器人模拟器 - 安装程序")
    print("Maze Robot Simulator - Installation")
    print("=" * 50)
    
    # 检查Python版本
    if not check_python_version():
        return False
    
    # 安装依赖
    if not install_requirements():
        return False
    
    # 检查Pygame
    if not check_pygame():
        return False
    
    print("\n" + "=" * 50)
    print("✓ 安装完成！")
    print("✓ Installation Complete!")
    print("=" * 50)
    print("\n运行程序:")
    print("python Maze_Simulation_v1.py")
    print("\nRun the program:")
    print("python Maze_Simulation_v1.py")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
