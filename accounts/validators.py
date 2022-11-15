import os
from django.core.exceptions import ValidationError

def allow_only_image_validator(value):
        ext = os.path.splitext(value.name)[1] #value=image.jpg
        print(ext)
        valid_extention = ['.jpg','.png','.jpeg']
        if not ext.lower() in valid_extention:
            raise ValidationError("Unsupported file extention. Allowed extention" + str(valid_extention))