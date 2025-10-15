from PIL import Image
import exifread


def extract_exif(file_path):
    with open(file_path, "rb") as f:
        tags = exifread.process_file(f, details=False)
    data = {}
    for tag in tags.keys():
        data[tag] = str(tags[tag])
    return data


def gps_from_exif(exif_data):
    try:
        lat_ref = exif_data.get("GPS GPSLatitudeRef")
        lon_ref = exif_data.get("GPS GPSLongitudeRef")
        lat = exif_data.get("GPS GPSLatitude")
        lon = exif_data.get("GPS GPSLongitude")

        def conv(value):
            parts = [float(x.num) / float(x.den) for x in value.values]
            return parts[0] + parts[1]/60 + parts[2]/3600

        if lat and lon:
            lat_val = conv(lat)
            lon_val = conv(lon)
            if lat_ref != "N":
                lat_val = -lat_val
            if lon_ref != "E":
                lon_val = -lon_val
            return {"latitude": lat_val, "longitude": lon_val}
    except Exception:
        pass
    return None
