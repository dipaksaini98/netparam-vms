import os
from django.core.exceptions import ValidationError


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    filesize = value.size
    valid_extensions = ['.jpg', '.jpeg', '.png']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension')
    else:
        if 5000 < filesize < 50:
            raise ValidationError("The max file size is 5000KB")
        else:
            return value


def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (instance.name, instance.date_visited, ext)
    return os.path.join('visitor', filename)
