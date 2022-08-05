from pathlib import Path
from typing import Dict, List, Tuple

# ось цей словник можливо отримувати із зовнішнього середовища
# і при цьому не доведеться змінювати код програми)
REGISTER_EXTENSIONS = {
    ".JPEG": "images",
    ".JPG": "images",
    ".PNG": "images",
    ".SVG": "images",
    ".GIF": "images",
    ".MP3": "audio",
    ".OGG": "audio",
    ".WAV": "audio",
    ".AMR": "audio",
    ".MP4": "video",
    ".AVI": "video",
    ".MOV": "video",
    ".MKV": "video",
    ".DOC": "document",
    ".DOCX": "document",
    ".TXT": "document",
    ".PDF": "document",
    ".XLSX": "document",
    ".XLS": "document",
    ".CSV": "document",
    ".PPTX": "document",
    ".ZIP": "archives",
    ".GZ": "archives",
    ".TAR": "archives",
    ".RAR": "archives",
    ".ARJ": "archives",
    ".APP": "programs",
    ".PY": "programs",
    ".HTML": "programs",
    "": "other",
}


def sorter(folder) -> Dict[Tuple[str, str], List[Path]]:
    file_list = sorted(folder.glob("**/*"))
    result = {}
    for file in [files for files in file_list if files.is_file()]:
        ext = file.suffix.upper()
        file_type = REGISTER_EXTENSIONS.get(ext, "other")
        if result.get((ext, file_type)):
            result[(ext, file_type)].append(file)
        else:
            result[(ext, file_type)] = [file]
    return result


def get_bad_folders(folder: Path) -> List[Path]:
    folder_list = [
        folder
        for folder in folder.glob("*")
        if folder.is_dir() and folder.name not in set(REGISTER_EXTENSIONS.values())
    ]

    bad_folders_list = [list(folder.glob("**/*")) for folder in folder_list]
    for lst in bad_folders_list:
        if lst:
            folder_list.extend(lst)

    return folder_list


def remove_folders(folders: List[Path]):
    positiv_result = []
    negativ_result = []
    for folder in folders[::-1]:
        try:
            folder.rmdir()
            positiv_result.append(folder.name)
        except OSError:
            negativ_result.append(folder.name)
    return positiv_result, negativ_result


def file_parser(*args):
    star = "*" * 60
    try:
        folder_for_scan = Path(args[0])
        sorted_file_dict = sorter(folder_for_scan.resolve())
    except FileNotFoundError:
        return (
            f"Not able to find '{args[0]}' folder. Please enter a correct folder name."
        )
    except IndexError:
        return "Please enter a folder name."
    except IsADirectoryError:
        return "Unknown file "
    for file_types, files in sorted_file_dict.items():
        for file in files:
            if not (folder_for_scan / file_types[1]).exists():
                (folder_for_scan / file_types[1]).mkdir()
            if not (folder_for_scan / file_types[1] / file_types[0]).exists():
                (folder_for_scan / file_types[1] / file_types[0]).mkdir()
            file.replace(folder_for_scan / file_types[1] / file_types[0] / file.name)

    old_folder_list = get_bad_folders(folder_for_scan)
    positive, negative = remove_folders(old_folder_list)
    str_positive = "\n".join(positive)
    str_negative = "\n".join(negative)
    return (
        f"{star}"
        "\n"
        f"Files in {args[0]} sorted succesffully"
        "\n"
        f"{star}"
        "\n"
        f"folders that are deleted: {str_positive}"
        "\n"
        f"folders that are not deleted:{str_negative}"
    )


if __name__ == "__main__":
    print(file_parser(Path(r"d:\testfolder")))
