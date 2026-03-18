import os

os.makedirs("folder1/folder2/folder3", exist_ok=True)

print("Папки созданы.")


items = os.listdir(".")

for item in items:
    print(item)

for file in os.listdir("."):
    if file.endswith(".txt"):
        print("Найден файл:", file)

import shutil

shutil.move("example.txt", "folder1/example.txt")

print("Файл перемещён.")

shutil.copy("folder1/example.txt", "folder1/folder2/example_copy.txt")

print("Файл скопирован.")