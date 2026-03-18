file = open("example.txt", "w")

# 2. Записываем данные
file.write("Hello\n")
file.write("This is my file\n")
file.write("Python practice\n")

# 3 закрываем файл
file.close()

file = open("example.txt", "r")

content = file.read()
print(content)

file.close()

file = open("example.txt", "a")

file.write("New line 1\n")
file.write("New line 2\n")

file.close()

file = open("example.txt", "r")
print(file.read())
file.close()

import shutil
shutil.copy("example.txt", "copy_example.txt")
shutil.copy("example.txt", "backup_example.txt")

import os

if os.path.exists("copy_example.txt"):
    os.remove("copy_example.txt")
    print("Файл удалён.")
else:
    print("Файл не найден.")