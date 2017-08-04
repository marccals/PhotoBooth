import datetime
import os.path

class PhotoPathUtils:

    @staticmethod
    def get_photo_path():
        """Get a path + filename for a phto"""
        return "./captured/" + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".png"

    @staticmethod
    def get_composed_photo_path(captured_photo_path):
        """Get a path for a composed photo from the path of captured photo"""
        return "./composed/composed_" + PhotoPathUtils.__get_file_name(captured_photo_path)

    @staticmethod
    def __get_file_name(path):
        return os.path.basename(path)