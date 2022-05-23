import cv2
import cvzone
import numpy as np
from PIL import Image, ImageFont, ImageDraw
import json
import aiofiles as aiofiles
import io

from model.product import Product

# async def saveImage(img_result, nameFile) -> None:
#     # async with aiofiles.open(path, "wb") as file:
#     #     await file.write(image)
#
#     image = Image.fromarray(img_result).convert("RGBA")
#     imgByteArr = io.BytesIO()
#
#     image.save(imgByteArr, format="PNG")
#     imgByteArr = imgByteArr.getvalue()
#
#     async with aiofiles.open(nameFile, "wb") as file:
#         print("Hehe1")
#         await file.write(imgByteArr)
#         print("Hehe2")
#
# def overlay_image_alpha(img, img_overlay, x, y, alpha_mask):
#     """Overlay `img_overlay` onto `img` at (x, y) and blend using `alpha_mask`.
#
#     `alpha_mask` must have same HxW as `img_overlay` and values in range [0, 1].
#     """
#     # Image ranges
#     y1, y2 = max(0, y), min(img.shape[0], y + img_overlay.shape[0])
#     x1, x2 = max(0, x), min(img.shape[1], x + img_overlay.shape[1])
#
#     # Overlay ranges
#     y1o, y2o = max(0, -y), min(img_overlay.shape[0], img.shape[0] - y)
#     x1o, x2o = max(0, -x), min(img_overlay.shape[1], img.shape[1] - x)
#
#     # Exit if nothing to do
#     if y1 >= y2 or x1 >= x2 or y1o >= y2o or x1o >= x2o:
#         return
#
#     img_crop = img[y1:y2, x1:x2]
#     img_overlay_crop = img_overlay[y1o:y2o, x1o:x2o]
#     alpha = alpha_mask[y1o:y2o, x1o:x2o, np.newaxis]
#     alpha_inv = 1.0 - alpha
#     img_crop[:] = alpha * img_overlay_crop + alpha_inv * img_crop
#
# async def remove_background(image):
#     image = image.convert("RGBA")
#     datas = image.getdata()
#     newData = []
#     for item in datas:
#         if item[0] == 255 and item[1] == 255 and item[2] == 255:
#             newData.append((255, 0, 0))
#     else:
#         newData.append(item)
#
#     imgByteArr = io.BytesIO()
#
#     image.putdata(newData)
#     transparent_image = np.asarray(image)
#     image.save(imgByteArr, format="PNG")
#     imgByteArr = imgByteArr.getvalue()
#
#     async with aiofiles.open("D:\\ME\\2022\\Python\\Add_Text_Image\\img_result.png", "wb") as file:
#         await file.write(imgByteArr)
#
#     return transparent_image
#
# rootFolder: str = "D:\\ME\\2022\\Python\\Folder_Image_Test\\"
#
# saveFolder = "D:\\ME\\2022\\Python\\Folder_Image_Test\\saved\\"
#
# savedPath = "D:\\ME\\2022\\Python\\Folder_Image_Test\\img_test.png"
#
# x, y = 0, 0
#
# l_img = cv2.imread("D:\\ME\\2022\\Python\\Folder_Image_Test\\girl\\girl-7-light-preview.png")
# s1_img = cv2.imread("D:\\ME\\2022\\Python\\Folder_Image_Test\\girl\\girl-7-clothes.png", -1)
# s2_img = cv2.imread("D:\\ME\\2022\\Python\\Folder_Image_Test\\girl\\girl-7-hair-27.png", -1)
#
# img = np.array(Image.open("D:\\ME\\2022\\Python\\Folder_Image_Test\\girl\\girl-7-light-preview.png").convert("RGBA"))
# img_overlay_rgba = np.array(
#     Image.open("D:\\ME\\2022\\Python\\Folder_Image_Test\\girl\\girl-7-clothes.png").convert("RGBA"))
#
# img_hair = np.array(Image.open("D:\\ME\\2022\\Python\\Folder_Image_Test\\girl\\girl-7-hair-27.png"))
#
# alpha_mask = img_overlay_rgba[:, :, 3] / 255.0
# img_result = img[:, :, :3].copy()
# img_overlay = img_overlay_rgba[:, :, :3]
#
# alpha_mask1 = img_hair[:, :, 3] / 255.0
# img_hair_overlay = img_hair[:, :, :3]
#
# overlay_image_alpha(img_result, img_overlay, x, y, alpha_mask)
# overlay_image_alpha(img_result, img_hair_overlay, 8, -22, alpha_mask1)
# # Save result
# await saveImage(img_result, "img_result.png")
#
# print("Hehe3")
# # img_body = np.array()
# #
# await remove_background(Image.open("D:\\ME\\2022\\Python\\Add_Text_Image\\img_result.png"))
#
# img_body_saved = np.array(Image.open("D:\\ME\\2022\\Python\\Add_Text_Image\\img_result.png"))
#
# imgText = Image.open("img_result.png")
#
# widthBody, heightBody = imgText.size
#
# I1 = ImageDraw.Draw(imgText)
#
# # imgBody = imgBody.resize((width, height + 100))
#
# myFont = ImageFont.truetype("FreeFont.ttf", 35)
#
# # Add Text to an image
# I1.text((0, heightBody + 20), "Alo 1234", font=myFont,
#         fill=(0, 0, 0))
# #
# #         imgBody.save(saveFolder + "Hello123.png")
# imgText.save("img_result.png")
#
# #
# alpha_mask_body = img_body_saved[:, :, 3] / 255.0
# img_body_overlay = img_body_saved[:, :, :3]
#
# # jsonData = json.loads(request.data)
# # data = Product.fromJson(jsonData)
# # pathImage = data.background
#
# pathImage = "D:\\ME\\2022\\Python\\Folder_Image_Test\\img.jpg"
#
# imgMain = np.array(Image.open(pathImage))
# img_result_Main = imgMain[:, :, :3].copy()
#
# imgBodySize = Image.open(pathImage)
#
# width, height = imgBodySize.size
#
# # Overlay Image
# overlay_image_alpha(img_result_Main, img_body_overlay, int(width / 2 - width / 8), int(height / 2), alpha_mask_body)
# Image.fromarray(img_result_Main).save("img_result_main.png")


# imgResult = cvzone.overlayPNG(img1, img3, [8, -22])

# imgOver1 = cv2.imread("Hello123.png", cv2.IMREAD_UNCHANGED)
#
# imgOverRes = cvzone.overlayPNG(imgOver1, img3, [0, 0])
#
# final_img2 = Image.fromarray(imgOverRes)
# final_img2.save("Hello1234.png")

# cv2.imshow("Image", imgResult)
# cv2.waitKey(0)

import cv2
import numpy as np

# read foreground image
img = cv2.imread('D:\\ME\\2022\\Python\\Folder_Image_Test\\girl\\girl-7-light-preview.png', cv2.IMREAD_UNCHANGED)

# read background image
back = cv2.imread('D:\\ME\\2022\\Python\\Folder_Image_Test\\img.jpg')

# extract alpha channel from foreground image as mask and make 3 channels
alpha = img[:,:,3]
alpha = cv2.merge([alpha,alpha,alpha])

# extract bgr channels from foreground image
front = img[:,:,0:3]

# blend the two images using the alpha channel as controlling mask
result = np.where(alpha==(0,0,0), back, front)

# save result
cv2.imwrite("front_back.png", result)


