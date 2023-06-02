"""
This script is used to rename files by their path and move them to home directory.
把脚本所在目录下的所有文件夹内的所有文件，重命名并移动到脚本所在目录
重命名规则为：......{文件夹名称}{分隔符}{原文件名称（包含扩展名）}
重命名之前会输出预览到{脚本名称}.{年月日时分秒}.log.txt
"""
import datetime
import os


# 获取脚本所在目录
script_path = os.path.dirname(os.path.realpath(__file__))
# os.path.dirname() 函数用于获取文件路径中的目录部分
# os.path.realpath() 函数用于获取文件的真实路径，自动判断符号链接
# __file__ 是当前文件的路径


# 自定义分隔符，留空则使用默认分隔符 "."
separator = input("enter separator: ")
if separator == "":
    separator = "."
print(f'separator is "{separator}"')


# 创建文件用于记录重命名前后的path，文件名格式为：{脚本名}.{当前时间}.log.txt
now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
# datetime.datetime.now() 方法返回当前本地时间
# strftime() 方法接收以时间元组，并返回以可读字符串表示的当地时间，格式由参数 format 决定
# print("now: ", now)
log_file_path = os.path.join(script_path, f"{os.path.basename(__file__)}.{now}.log.txt")
# os.path.join() 方法用于将多个路径组合后返回
# os.path.basename() 方法用于返回指定文件的文件名，即去掉路径，只返回文件名
# print("log_file_path: ", log_file_path)
# print("__file__: ", __file__)
log_file = open(log_file_path, "w")


# 遍历所有文件夹和文件，并输出输出预览信息到log文件
for root, dirs, files in os.walk(script_path):
    # os.walk() 方法是一个简单易用的文件、目录遍历器，可以帮助我们高效地处理文件、目录方面的事情。
    # print("root: ", root)
    # print("dirs: ", dirs)
    # print("files: ", files)

    for file_name in files:
        # relative_path = os.path.join(root, file_name)
        # 获取绝对路径，即文件在根目录的完整路径，包括文件名
        # 实际需要的是相对路径，即文件相对于脚本所在目录的路径，不包括文件名

        relative_path = os.path.relpath(root, script_path)
        # os.path.relpath() 方法用于获取相对路径
        # print("relative_path: ", relative_path)

        if relative_path == ".":
            # 防止出现相对路径为当前目录时，被重命名成“..{name}”的情况
            # 例如，与脚本所在同一目录下的文件“demo”，被重命名成“..demo”
            new_file_name = file_name
        else:
            new_file_name = f"{relative_path.replace(os.sep, separator)}{separator}{file_name}"
            # replace() 方法把字符串中的旧字符串，替换成新字符串，如果指定第三个参数max，则替换不超过 max 次
            # os.sep 是当前操作系统的路径分隔符，Windows 下为 "\"，Linux 下为 "/"
            # print("new_file_name: ", new_file_name)

        old_file_path = os.path.join(root, file_name)
        new_file_path = os.path.join(script_path, new_file_name)
        # print("old_file_path: ", old_file_path)
        # print("new_file_path: ", new_file_path)
        log_file.write(f"{old_file_path}\n{new_file_path}\n\n")

log_file.close()
# 关闭log文件，到此为止，log文件中已经记录了所有文件的重命名前后的path


# 接下来开始重命名部分
print(f"\nlog file is saved at:\n{script_path}\n")
continue_flag = input("all files will be renamed, continue? (y/n): ")


if continue_flag.lower() == "y":
    # continue_flag.lower() 方法把大写字母转换为小写字母
    for root, dirs, files in os.walk(script_path):
        for file_name in files:
            relative_path = os.path.relpath(root, script_path)
            if relative_path == ".":
                new_file_name = file_name
            else:
                new_file_name = f"{relative_path.replace(os.sep, separator)}{separator}{file_name}"
            old_file_path = os.path.join(root, file_name)
            new_file_path = os.path.join(script_path, new_file_name)

            print(f"{old_file_path}\n{new_file_path}\n\n")
            # 注意，不要运行这一行，否则会把脚本所在目录下的所有文件夹内的所有文件，重命名并移动到脚本所在目录
            # 只有当使用时，才需要取消注释
            # os.rename(old_file_path, new_file_path)
            # os.rename() 方法用于命名文件或目录，从 src 到 dst，如果 dst 是一个存在的目录，将抛出 OSError。

    print("all files are renamed")
