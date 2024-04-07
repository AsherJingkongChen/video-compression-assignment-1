from PIL import Image
from numpy import array, moveaxis, uint8
from .utils.env import ASSETS_DIR_PATH, OUTPUTS_DIR_PATH
from ..modules.color import H273, KR_KB_BT601

image = Image.open(ASSETS_DIR_PATH / "foreman_qcif_0_rgb.bmp").convert("RGB")
image_data_as_drgb = array(image, dtype=uint8)

# Ensure that the source image is in the full range RGB color space

image_must_be_full_range = (image_data_as_drgb.max() > 219 + 16) or (
    image_data_as_drgb.min() < 16
)
assert (
    image_must_be_full_range
), "The source image is assumed to be in the full range RGB color space"

# Uses ITU-R BT.601 parameter values
# - The source image is assumed to be gamma-corrected
color = H273(rgb_gamma_corrected=True)

# De-quanitze the image
image_data_as_argb = color.set_full_range(True).dequantize_rgb(image_data_as_drgb)

# Convert the image from analog RGB to YPbPr
kr, kb = KR_KB_BT601()
image_data_as_ypbpr = color.ypbpr_from_rgb(image_data_as_argb, kr, kb)

image_data_as_ycbcr = color.set_full_range(False).quantize_ypbpr(image_data_as_ypbpr)

# Quantize the image from YPbPr to YCbCr and save it in YUV444 planar format
print(image_data_as_ycbcr.min(), image_data_as_ycbcr.max())

planar_image_data = moveaxis(image_data_as_ycbcr, -1, 0)
y_plane, cb_plane, cr_plane = planar_image_data

cb_plane = cb_plane[::2, ::2]
cr_plane = cr_plane[::2, ::2]
planar_image_data_as_bytes = y_plane.tobytes() + cb_plane.tobytes() + cr_plane.tobytes()
(OUTPUTS_DIR_PATH / "foreman_qcif_0_ycbcr.yuv").write_bytes(planar_image_data_as_bytes)

# Sub-sample the image in YPbPr color space using 4:2:0 scheme
pass

# Quantize from YPbPr to YCbCr and save the image in YUV420 planar format
pass

# Up-sample the image in YPbPr color space using 4:2:0 scheme
pass

# Convert the image from YPbPr to analog RGB
image_data_as_argb_back = color.rgb_from_ypbpr(image_data_as_ypbpr, kr, kb)

# Quantize the image from analog RGB to digital RGB and save in it BMP RGB24 format
image_data_as_drgb_back = color.set_full_range(True).quantize_rgb(
    image_data_as_argb_back
)
