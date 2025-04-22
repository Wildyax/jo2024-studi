from django.core.files.uploadedfile import SimpleUploadedFile
import base64

def get_test_image():
    return SimpleUploadedFile(
        name='test.jpg',
        content=base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="),
        content_type='image/jpeg'
    )