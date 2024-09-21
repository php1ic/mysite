import os
import shutil

import gencontent


def copy_fn(source, destination):
    if os.path.exists(destination):
        print(f"The destination directory <{destination}> already exists, deleting")
        shutil.rmtree(destination)

    def verbose_copy(src, dst):
        print(f"Copying {src} -> {dst}")
        shutil.copy2(src, dst)

    shutil.copytree(source, destination, copy_function=verbose_copy)


def main():
    copy_fn("static", "public")

    print("Generating Page")
    gencontent.generate_page("./content/index.md", "./template.html", "./public/index.html")


if __name__ == "__main__":
    main()
