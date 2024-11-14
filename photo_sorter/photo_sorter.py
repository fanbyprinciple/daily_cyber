import os
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime
import shutil

def get_photo_date(file_path):
    """
    Extract the date a photo was taken from its EXIF metadata.
    """
    try:
        image = Image.open(file_path)
        exif_data = image._getexif()
        if exif_data:
            for tag_id, value in exif_data.items():
                tag_name = TAGS.get(tag_id, tag_id)
                if tag_name == "DateTimeOriginal":
                    return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
        return None
    except Exception as e:
        print(f"Error reading metadata for {file_path}: {e}")
        return None

def organize_photos_by_date(source_folder, destination_folder):
    """
    Organize photos into folders by the date they were taken.
    """

    print(source_folder)
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    print(os.listdir(source_folder))

    for root, _, files in os.walk(source_folder):
        print(root)
        print("elngth: " , len(files))

    for root, _, files in os.walk(source_folder):
        for file in files:
            file_path = os.path.join(root, file)
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.tiff')):
                photo_date = get_photo_date(file_path)
               
                if photo_date:
                    date_folder = photo_date.strftime("%Y-%m-%d")
                    target_folder = os.path.join(destination_folder, date_folder)
                    if not os.path.exists(target_folder):
                        os.makedirs(target_folder)
                    shutil.copy(file_path, target_folder)
                    print(f"Moved {file} to {target_folder}")
                else:
                    print(f"Date not found for {file}, skipping.")

if __name__ == "__main__":
    source_folder = "D:\\100D3200"
    destination_folder = "D:\\Nandi_hills"
    organize_photos_by_date(source_folder, destination_folder)
    print("Photo organization complete!")