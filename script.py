import os
from datetime import datetime
import time
import json
import re
import shutil


class FileSort:
    def __init__(self, target_dir):
        self.target_dir = target_dir
        self.folder_names = None
        self.flist = None
        self.list_files()
        self.create_subfolders()
        self.move_files()
        # print(self.flist)

    def list_files(self):
        flist = []
        group_key = {
            "Image Files": [
                ".jpeg",
                ".png",
                ".jpg",
                ".webp",
                ".PNG",
                ".JPG",
                ".JPEG",
                ".gif",
            ],
            "Text Files": [".txt", ".rtf", ".docx", ".pdf", ".EPUB", ".md"],
            "Audio Files": [
                ".aa",
                ".aac",
                ".alac",
                ".flac",
                ".m4a",
                ".m4b",
                ".m4p",
                ".mmf",
                ".mp3",
                ".mogg",
            ],
            "Batch Files": [".cmd", ".bat", ".batch", ".sh"],
            "Video Files": [
                ".webm",
                ".mkv",
                ".flv",
                ".avi",
                ".mov",
                ".wmv",
                ".mp4",
                ".m4p",
                ".m4v",
                ".mpg",
                ".mpg",
                ".mpeg",
            ],
            "Compressed Files": [".zip", ".rar", ".gzip", ".tar"],
            "Exe Files": [".exe"],
            "Local or Internet Shortcuts": [".lnk", ".url"],
            "Folders": ["folder"],
        }
        self.group_key = group_key

        os.chdir(self.target_dir)
        for f in os.listdir():
            fname = str(f)

            pattern = re.compile(r"\.[^\.\s]+$")
            matches = pattern.finditer(fname)
            f_extension = "folder"
            for match in matches:
                if match.group(0):
                    f_extension = str(match.group(0))

            group = f_extension
            for key, value in group_key.items():
                if f_extension in value:
                    group = str(key)

            if (
                not fname is f_extension
                or fname in group_key.keys()
                and os.path.isdir(os.path.join(self.target_dir, fname))
            ):
                flist.append(
                    {
                        "File Name:": fname,
                        "File Extension:": f_extension,
                        "Group Name:": group,
                    }
                )

        self.folder_names = set([i["Group Name:"] for i in flist])
        for f in flist:
            if (
                f["File Name:"] in self.folder_names
                and f["File Extension:"] == "folder"
            ):
                flist.remove(f)
        self.flist = flist

    def create_subfolders(self):
        for i in self.flist:
            try:
                os.mkdir(i["Group Name:"])
            except FileExistsError:
                pass
        os.chdir(self.target_dir)

    def move_files(self):
        for i in self.flist:
            if not i["File Name:"] in self.group_key.keys():
                current = os.path.join(self.target_dir, i["File Name:"])
                destination = os.path.join(self.target_dir, i["Group Name:"])
                temp = i["File Name:"]
                print(temp)
                if temp in os.listdir(destination):
                    num = 1
                    for j in os.listdir(destination):
                        if j == temp:
                            num += 1
                    name = (
                        temp.strip(i["File Extension:"])
                        + "_"
                        + str(num)
                        + i["File Extension:"]
                    )
                    try:
                        os.rename(current, name)
                    except Exception:
                        continue
                    i["File Name:"] = name
                    current = os.path.join(self.target_dir, i["File Name:"])
                try:
                    shutil.move(current, destination)
                except Exception:
                    continue

    def unsort(self):
        pass


def run():
    while True:
        print("Input Path To Sort:\n")
        i = input()
        try:
            os.chdir(i)
            if os.path.isdir(i):
                print("runing")
                FileSort(i)
                print(f"Sorting files in dir: {i}")
                break
            else:
                print("PATH MUST BE TO DIRECTORY NOT FILE TRY AGAIN")
        except FileNotFoundError:
            print("INVALID PATH TRY AGAIN: file not found")
        # except OSError:
        # print('INVALID PATH TRY AGAIN: os error')


run()
