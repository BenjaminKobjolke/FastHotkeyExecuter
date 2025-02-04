import os
import mimetypes

magic_available = True
# pip install python-magic-bin
try:
    # Attempt to import the module
    import magic

except ImportError:
    # Magic is not available
    print("Magic not available")
    magic_available = False

import requests


class FileUtils:
    mime = None
    base_path = None

    @staticmethod
    def set_base_path(base_path):
        FileUtils.base_path = base_path

    @staticmethod
    def downloads_path():
        target_path = FileUtils.base_dir() + "downloads/"
        return os.path.normpath(target_path) + "/"

    @staticmethod
    def data_path():
        target_path = FileUtils.base_dir() + "data/"
        return os.path.normpath(target_path) + "/"
    @staticmethod
    def tools_path(path=""):
        target_path = FileUtils.base_dir() + "tools/" + path
        return os.path.normpath(target_path)

    @staticmethod
    def chrome_extension_path(path):
        target_path = FileUtils.base_dir() + path
        return os.path.normpath(target_path)

    @staticmethod
    def tmp_path():
        target_path = FileUtils.base_dir() + "tmp/"
        return os.path.normpath(target_path) + "/"

    @staticmethod
    def base_dir():
        return FileUtils.base_path

    @staticmethod
    def file_exists(file_path):
        if os.path.exists(file_path):
            return True
        else:
            return False

    @staticmethod
    def get_mime_type(file_path):
        mime_type = mimetypes.guess_type(file_path)[0]
        if mime_type is None:
            if FileUtils.mime is None:
                FileUtils.mime = magic.Magic(mime=True)
            if magic_available:
                mime_type = FileUtils.mime.from_file(file_path)
            else:
                print("magic mime is not available")

        return mime_type

    @staticmethod
    def is_image(mime_type):
        if mime_type.startswith('image/'):
            return True
        else:
            return False

    @staticmethod
    def is_audio_or_video(mime_type):
        if mime_type.startswith('audio/'):
            return True
        elif mime_type.startswith('video/'):
            return True
        else:
            return False

    @staticmethod
    def download_file(url, file_path):
        try:
            response = requests.get(url, stream=True, timeout=30)
        except requests.exceptions.RequestException as e:
            print("Unable to download file. Exception: " + str(e))
            return False

        if response.status_code == 200:
            print("Saving file...")
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
            return True
        else:
            print("Could not download file from url " + url)


        return False
