"""
Read GPS coordinates and other meta data from image files.

Further reading:
- https://medium.com/spatial-data-science/how-to-extract-gps-coordinates-from-images-in-python-e66e542af354
- https://www.thepythoncode.com/article/extracting-image-metadata-in-python
- https://medium.com/spatial-data-science/build-a-useful-web-application-in-python-geolocating-photos-186122de1968
"""

import json
import os
import pandas as pd
from datetime import datetime
from exif import Image as exif_image
from PIL import Image as pil_image


def collect_metadata_for_image(img_path):
    with open(img_path, 'rb') as src:
        img = exif_image(src)

    if not img.has_exif:
        print('The image has no EXIF information.')
        return

    try:
        coords = f"{_dms_to_decimal(img.gps_latitude, img.gps_latitude_ref)},{_dms_to_decimal(img.gps_longitude, img.gps_longitude_ref)}"
    except AttributeError:
        coords = None

    datetime_taken = datetime.strptime(img.datetime_original, "%Y:%m:%d %H:%M:%S")
    pil_image_obj = pil_image.open(img_path)
    width = pil_image_obj.width
    height = pil_image_obj.height
    useful_data = {
        'filename': os.path.basename(src.name),
        'year': datetime_taken.year,
        'month': datetime_taken.month,
        'altitude': int(round(img.gps_altitude, 0)) if img.get("gps_altitude") is not None else None,
        'url': f"http://maps.google.com/?q={coords}" if coords is not None else "",
        'orientation': "landscape" if width > height else ("portrait" if height > width else "square"),
        'width': width,
        'height': height,
        'megabytes': round(os.path.getsize(src.name) / 1e6, 2),
        'coordinates': coords,
        'date': datetime_taken.strftime("%Y.%m.%d"),
        'time': datetime_taken.strftime("%H:%M:%S"),
        'phone': f"{img.make} {img.model}",
        'lens': img.get("lens_model"),
        'original_width': img.pixel_x_dimension,
        'original_height': img.pixel_y_dimension,
        'filepath': src.name,
    }
    # print(json.dumps(useful_data, indent=4))
    return useful_data


def collect_metadata_for_all_images(path):
    image_formats = [".jpg", ".png"]
    images = [fname for fname in os.listdir(path) if os.path.splitext(fname)[1].lower() in image_formats]
    metadata = [collect_metadata_for_image(os.path.join(path, image)) for image in images]
    # print(json.dumps(metadata, indent=4))
    return metadata


def export_metadata_to_simple_excel(metadata):
    df = pd.DataFrame(metadata)
    df.index.names = ['Number']
    df.to_excel('metadata_simple.xlsx', sheet_name="Images")


def export_metadata_to_advanced_excel(metadata):
    def _get_col_widths(df, with_index=False, gap=1):
        idx_max = max([len(str(s)) for s in df.index.values] + [len(str(df.index.name))])  # maximum length of the index column
        col_widths = [max([len(str(s)) for s in df[col].values] + [len(col)]) for col in df.columns]  # maximum lenghts of column names and values
        widths = [idx_max, *col_widths] if with_index else col_widths
        return [gap * width + 3 for width in widths]
    #========================================================================

    filename = 'metadata_advanced.xlsx'
    sheetname = 'Images'

    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    df = pd.DataFrame(metadata)
    df.to_excel(writer, sheet_name=sheetname, index=False, freeze_panes=(1,0))
    worksheet = writer.sheets[sheetname]
    (max_row, max_col) = df.shape
    worksheet.autofilter(0, 0, max_row, max_col-1)
    for i, width in enumerate(_get_col_widths(df)):
        worksheet.set_column(i, i, width)

    writer.save()


def _dms_to_decimal(coords, gps_ref):
    """Converts GPS coordinates from DMS (degrees, minutes, seconds) to DD (decimal degrees)."""
    decimal_degrees = round(coords[0] + coords[1]/60 + coords[2]/3600, 6)
    return -decimal_degrees if gps_ref in ['S','W'] else decimal_degrees


if __name__ == '__main__':
    path = os.path.dirname(os.path.abspath(__file__))
    metadata = collect_metadata_for_all_images(path)
    print(json.dumps(metadata, indent=4))
    # export_metadata_to_simple_excel(metadata)
    export_metadata_to_advanced_excel(metadata)
