#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: file_util.py
@author: Lyndon
@time: 2024/10/31 14:33
@env: Python @desc:
@ref: @blog:
"""
import os
import shutil

from errors.Errors import FileOperationError


class FileUtil:
    @staticmethod
    def create_directory(directory_path):
        try:
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)
        except Exception as e:
            raise FileOperationError(f"创建目录时出错：{e}")

    @staticmethod
    def delete_directory(directory_path):
        try:
            if os.path.exists(directory_path):
                shutil.rmtree(directory_path)
            else:
                raise FileOperationError(f"目录 {directory_path} 不存在！")
        except Exception as e:
            raise FileOperationError(f"删除目录时出错：{e}")

    @staticmethod
    def list_files(directory_path):
        try:
            if os.path.exists(directory_path):
                return os.listdir(directory_path)
            else:
                return []
        except Exception as e:
            raise FileOperationError(f"列出文件时出错：{e}")

    @staticmethod
    def copy_file(source_path, destination_path):
        try:
            shutil.copy2(source_path, destination_path)
        except Exception as e:
            raise FileOperationError(f"复制文件时出错：{e}")

    @staticmethod
    def move_file(source_path, destination_path):
        try:
            shutil.move(source_path, destination_path)
        except Exception as e:
            raise FileOperationError(f"移动文件时出错：{e}")

    @staticmethod
    def delete_file(file_path):
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
            else:
                raise FileOperationError(f"文件 {file_path} 不存在！")
        except Exception as e:
            raise FileOperationError(f"删除文件时出错：{e}")