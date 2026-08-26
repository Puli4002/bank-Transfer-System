from PIL import Image
import io


Allowed_image_format={"JPEG","PNG","WEBP"}
max_image_size_bytes = 10 * 1024 * 1024
max_image_Dimension = 8000

class ImageValidationResult:
    ok:bool
    format:str | None
    width:int | None
    height:int |None
    error_code:str |None
    error_message:str |None
    
def validation_background_image(
        file_bytes:bytes,
        file_name:str,
) -> ImageValidationResult:
    try:
        img= Image.open(io.BytesIO(file_bytes))
    except:
        return ImageValidationResult(
            ok=False,
            error_code= "INVALID_IMAGE"
        )

    image_format= Image.format
    if image_format not in Allowed_image_format:
       return ImageValidationResult(
           ok=False,
           error_code="UNSUPPORTED_FORMAT"
        )
    file_size= len(file_bytes)
    if file_size > max_image_size_bytes:
        return ImageValidationResult(
            ok=False,
            error_code="FILE_TOO_LARGE"
        )
    width= Image.width
    height= Image.height
    if width>max_image_Dimension or height>max_image_Dimension:
        return ImageValidationResult(
            ok=False,
            format=image_format,
            width=width,
            height=height,
            error_code="IMAGE_DIMENSIONS_TOO_LARGE"
        )
    return ImageValidationResult(
        ok=True,
        format=image_format,
        width=width,
        height=height,
        error_code=None
    )
    
    


