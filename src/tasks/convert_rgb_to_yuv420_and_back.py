from PIL import Image
from numpy import array, uint8, typing
from .utils.env import ASSETS_DIR_PATH, OUTPUTS_DIR_PATH
from ..modules.color import H273, KR_KB_BT601
from ..modules.data import planar_from_packed, save_ycbcr_image
from ..modules.sample import BT2100

image = Image.open(ASSETS_DIR_PATH / "foreman_qcif_0_rgb.bmp")

# Ensure that the source image is in the full range RGB color space
image = image.convert("RGB")
image_data_as_drgb = array(image, dtype=uint8)
image_must_be_full_range = (image_data_as_drgb.max() > 219 + 16) or (
    image_data_as_drgb.min() < 16
)
assert (
    image_must_be_full_range
), "The source image is assumed to be in the full range RGB color space"

# Uses ITU-R BT.601 parameter values
# - The source image is assumed to be gamma-corrected RGB
color = H273()

# Uses ITU-R BT.2100 parameter values
sample = BT2100()

# De-quanitze the image to analog RGB
image_data_as_argb = color.set_full_range(True).dequantize_rgb(image_data_as_drgb)

# Convert the image from analog RGB to YPbPr
kr, kb = KR_KB_BT601()
image_data_as_ypbpr = color.ypbpr_from_rgb(image_data_as_argb, kr, kb)

# Quantize the image from YPbPr to YCbCr
image_data_as_ycbcr = color.set_full_range(False).quantize_ycbcr(image_data_as_ypbpr)

# Sub-sample the image in YCbCr color space using 4:2:0 scheme
image_data_as_y, image_data_as_cb, image_data_as_cr = planar_from_packed(
    image_data_as_ycbcr
)
image_data_as_y_subsampled = image_data_as_y.copy()
image_data_as_cb_subsampled = sample.subsample_420(image_data_as_cb)
image_data_as_cr_subsampled = sample.subsample_420(image_data_as_cr)

# Save the sub-sampled image in the planar YCbCr format
height, width = image_data_as_y_subsampled.shape
with open(OUTPUTS_DIR_PATH / f"foreman_qcif_0_ycbcr_4-2-0.{width}x{height}.yuv", "wb") as file:
    save_ycbcr_image(file, (image_data_as_y, image_data_as_cb, image_data_as_cr))

# Up-sample the image in YCbCr color space using 4:2:0 scheme
pass

# Convert the image from YPbPr to analog RGB
image_data_as_argb_back = color.rgb_from_ypbpr(image_data_as_ypbpr, kr, kb)

# Quantize the image from analog RGB to digital RGB
image_data_as_drgb_back = color.set_full_range(True).quantize_rgb(
    image_data_as_argb_back
)

# Save the image in the 24-bit RGB BMP format
image_back = Image.fromarray(image_data_as_drgb_back, mode="RGB")
width, height = image_back.size
image_back.save(OUTPUTS_DIR_PATH / f"foreman_qcif_0_rgb.{width}x{height}.bmp")

# Ensure that the back image has the same size as the source image
assert (
    image.size == image_back.size
), "The back image should have the same size as the source image"
