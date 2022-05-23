# This is a sample Python script.
import aiofiles as aiofiles
import cv2
import datetime
import PIL
import cvzone
import numpy as np
from PIL import Image
import io
from PIL import ImageDraw
from PIL import ImageFont
import os
import requests
import json
from flask_cors import CORS
from flask import Flask, request
from flask import send_file
from common.common import Common
from model.image_content import ImageContent
from model.product import Product

app = Flask(__name__, template_folder='')
CORS(app)

url = 'http://maps.googleapis.com/maps/api/directions/json'

imageText = {
    "image": "image_test.png",
    "content":
        [
            {
                "font": "FreeFont.ttf",
                "position": {
                    "x": 338,
                    "y": 689
                },
                "text": "Yo"
            },
            {
                "font": "FreeFont.ttf",
                "position": {
                    "x": 837,
                    "y": 680
                },
                "text": "Man"
            }
        ]
}

x_offset = y_offset = 50

SKIN_LIGHT = "#7A472E"
SKIN_DARK = "#CD8F6A"
SKIN_TAN = "#FACCB9"


@app.post('/')
def postRequest():
    try:
        data = json.loads(request.data)

        # strData = json.dump(data)

        # print("Hello Data " + data)

        image_content = ImageContent.fromJson(data)

        img = Image.open(image_content.image)

        # Call draw Method to add 2D graphics in an image
        I1 = ImageDraw.Draw(img)

        content = image_content.content

        # Custom font style and font size
        for i in range(0, len(content)):
            item_content = content[i]
            print("Font " + item_content.font)
            myFont = ImageFont.truetype(item_content.font, 35)

            # Add Text to an image
            I1.text((item_content.position.x, item_content.position.y), item_content.text, font=myFont,
                    fill=(0, 0, 0))

        # Display edited image
        # img.show()
        # Save the edited image
        img.save("D:\\ME\\2022\\Python\\Folder_Image\\test.png")
    except Exception as e:
        print("An Exception " + e.__class__)

        error = app.response_class(
            status=400
        )

        return error

    res = app.response_class(
        response=json.dumps({
            "name": "test.png"
        }),
        status=200,
        mimetype='application/json'
    )

    return res


rootFolder: str = "D:\\ME\\2022\\Python\\Folder_Image_Test\\"


@app.post('/test')
def createTest():
    img1 = cv2.imread(rootFolder + "girl\\girl-7-light-preview.png", cv2.IMREAD_UNCHANGED)
    img2 = cv2.imread("D:\\ME\\2022\\Python\\Folder_Image_Test\\img.jpg")
    img3 = cv2.imread(rootFolder + "girl\\girl-7-hair-27.png", cv2.IMREAD_UNCHANGED)

    imgResult = cvzone.overlayPNG(img2, img1)

    # imgResult = cvzone.overlayPNG(img1, img3, [8, -22])

    imgResult = cvzone.overlayPNG(img1, img3, [8, -22])

    final_img = Image.fromarray(imgResult)
    final_img.save("Hello123.png")

    # imgOver1 = cv2.imread("Hello123.png", cv2.IMREAD_UNCHANGED)
    #
    # imgOverRes = cvzone.overlayPNG(imgOver1, img3, [0, 0])
    #
    # final_img2 = Image.fromarray(imgOverRes)
    # final_img2.save("Hello1234.png")

    # cv2.imshow("Image", imgResult)
    # cv2.waitKey(0)

    return {}


@app.post('/create')
async def createImageRequest():
    saveFolder = rootFolder + "saved\\"
    savedPath = rootFolder + "img_test.png"

    x, y = 0, 0

    # l_img = cv2.imread("D:\\ME\\2022\\Python\\Folder_Image_Test\\girl\\girl-7-light-preview.png")
    # s1_img = cv2.imread("D:\\ME\\2022\\Python\\Folder_Image_Test\\girl\\girl-7-clothes.png", -1)
    # s2_img = cv2.imread("D:\\ME\\2022\\Python\\Folder_Image_Test\\girl\\girl-7-hair-27.png", -1)

    jsonData = json.loads(request.data)
    data = Product.fromJson(jsonData)

    scalePercent = Common.PERCENT_SCALES[data.numbers - 1]
    print("Percent Scale " + str(scalePercent))

    for i in range(0, data.numbers):
        member = data.members[i]

        headFolder = member.gender.lower()

        # pathFolder = "D:\\ME\\2022\\Python\\Folder_Image_Test\\" + headFolder + "\\"

        # Body
        skin = ""
        if member.body == 1:
            skin = Common.LIGHT
        elif member.body == 2:
            skin = Common.DARK
        else:
            skin = Common.TAN

        # Large Image
        pathBody = rootFolder + headFolder + "\\" + headFolder + "-" + str(
            member.body) + "-" + skin + "-preview.png"

        # l_img = cv2.imread(pathBody)

        print("Path Body " + pathBody)
        imgBody = Image.open(pathBody)

        width, height = imgBody.size
        # print("Width " + str(width) + " Height " + str(height))
        # Clothes
        pathClothes = rootFolder + headFolder + "\\" + headFolder + "-" + str(
            member.body) + "-clothes.png"

        pathHair = ""
        if member.gender == Common.WOMAN:
            # Style
            indexStyleHair = Common.styles[member.hairStyle - 1]

            pathHair = rootFolder + Common.WOMAN.lower() + "\\" + Common.WOMAN.lower() + "_" + str(
                indexStyleHair + member.hairStyle) + "-preview.png"
        else:
            #  Hair
            pathHair = rootFolder + headFolder + "\\" + headFolder + "-" + str(
                member.body) + "-hair-" + str(member.hair) + ".png"
            # imgHair = Image.open(pathHair)
            # copyHair = imgHair.copy()
            # imgBody.paste(copyHair, (0, 0))

        img = np.array(
            Image.open(pathBody).convert("RGBA"))
        img_overlay_rgba = np.array(
            Image.open(pathClothes).convert("RGBA"))

        img_hair = np.array(Image.open(pathHair).convert("RGBA"))

        alpha_mask = img_overlay_rgba[:, :, 3] / 255.0

        img_result = img[:, :, :3].copy()

        img_overlay = img_overlay_rgba[:, :, :3]

        alpha_mask1 = img_hair[:, :, 3] / 255.0
        img_hair_overlay = img_hair[:, :, :3]
        overlay_image_alpha(img_result, img_overlay, x, y, alpha_mask)
        overlay_image_alpha(img_result, img_hair_overlay, 8, -22, alpha_mask1)
        # Save result
        await saveImage(img_result, "img_result.png")

        print("Hehe3")
        # img_body = np.array()
        #
        # await remove_background(Image.open("D:\\ME\\2022\\Python\\Add_Text_Image\\img_result.png"))
        # jsonData = json.loads(request.data)
        # data = Product.fromJson(jsonData)
        # pathImage = data.background
        #
        # imgBodyOverlay = cv2.imread("img_result.png", cv2.IMREAD_UNCHANGED)
        # imgMainOverlay = cv2.imread(pathImage)
        #
        # imgMain1 = Image.open(pathImage)
        #
        # width, height = imgMain1.size
        #
        # imgFinalOverlay = cvzone.overlayPNG(imgMainOverlay, imgBodyOverlay, [int(width / 2 - width / 8), int(height / 2)])
        # final_img2 = Image.fromarray(imgFinalOverlay)
        #
        # final_img2.save("img_final.png")

        img_body_saved = np.array(Image.open("img_result.png"))

        imgText = Image.open("img_result.png")

        imgText.save("img_scale.png")

        widthBody, heightBody = imgText.size

        # imgText = scaleImage(imgText, 0.3)

        I1 = ImageDraw.Draw(imgText)

        # imgBody = imgBody.resize((width, height + 100))

        myFont = ImageFont.truetype("FreeFont.ttf", 35)

        # Add Text to an image
        I1.text((0, heightBody + 20), "Alo 1234", font=myFont,
                fill=(0, 0, 0))
        #
        #         imgBody.save(saveFolder + "Hello123.png")
        imgText.save("img_result.png")

        # await remove_background(imgText)

        imgBodyResize = cv2.imread("img_result.png")

        half = cv2.resize(imgBodyResize, (0, 0), fx=0.1, fy=0.1)

        alpha_mask_body = img_body_saved[:, :, 3] / 255.0
        img_body_overlay = img_body_saved[:, :, :3]

        pathImage = data.background

        imgMain = np.array(Image.open(pathImage))
        img_result_Main = imgMain[:, :, :3].copy()

        imgBodySize = Image.open(pathImage)
        width, height = imgBodySize.size

        # Overlay Image
        overlay_image_alpha(img_result_Main, img_body_overlay, int(width / 2 - width / 8 + i * 50), int(height / 2),
                            alpha_mask_body)

        Image.fromarray(img_result_Main).save("img_result_main.png")

        imgFinalMain = Image.open("img_result_main.png")

        # Call draw Method to add 2D graphics in an image
        I1 = ImageDraw.Draw(imgFinalMain)

        widthFinalMain, heightFinalMain = imgFinalMain.size

        # imgBody = imgBody.resize((width, height + 100))

        # Add Text to an image
        I1.text((int(width / 2 - width / 8), int(height / 2) + heightBody + 20), "Hello 123", font=myFont,
                fill=(0, 0, 0))

        # imgBody.save(saveFolder + "Hello123.png")
        imgFinalMain.save("img_result_main.png")

    # try:
    #     jsonData = json.loads(request.data)
    #
    #     data = Product.fromJson(jsonData)
    #
    #     pathImage = data.background
    #     imgMain = Image.open(pathImage)
    #
    #     for i in range(0, data.numbers):
    #         # Member
    #         member = data.members[i]
    #
    #         headFolder = member.gender.lower()
    #
    #         # pathFolder = "D:\\ME\\2022\\Python\\Folder_Image_Test\\" + headFolder + "\\"
    #
    #         # Body
    #         body = ""
    #         if member.body == 1:
    #             body = Common.LIGHT
    #         elif member.body == 2:
    #             body = Common.DARK
    #         else:
    #             body = Common.TAN
    #
    #         # Large Image
    #         pathBody = "D:\\ME\\2022\\Python\\Folder_Image_Test\\" + headFolder + "\\" + headFolder + "-" + str(
    #             member.body) + "-" + body + "-preview.png"
    #
    #         l_img = cv2.imread(pathBody)
    #
    #         imgBody = Image.open(pathBody)
    #
    #         width, height = imgBody.size
    #         print("Width " + str(width) + " Height " + str(height))
    #         # Clothes
    #         pathClothes = "D:\\ME\\2022\\Python\\Folder_Image_Test\\" + headFolder + "\\" + headFolder + "-" + str(
    #             member.body) + "-clothes.png"
    #
    #         imgClothesTmp = Image.open(pathClothes)
    #         imgClothesTmp = imgClothesTmp.convert("RGBA")
    #
    #         # Small Image
    #         s_img = cv2.imread(pathClothes, -1)
    #
    #         y1, y2 = y_offset, y_offset + s_img.shape[0]
    #         x1, x2 = x_offset, x_offset + s_img.shape[1]
    #
    #         alpha_s = s_img[:, :, 3] / 255.0
    #         alpha_l = 1.0 - alpha_s
    #
    #         # for c in range(0, 3):
    #         #     l_img[y1:y2, x1:x2, c] = (alpha_s * s_img[:, :, c] + alpha_l * l_img[y1:y2, x1:x2, c])
    #
    #         datas = imgClothesTmp.getdata()
    #
    #         newData = []
    #
    #         for item in datas:
    #             if item[0] == 255 and item[1] == 255 and item[2] == 255:
    #                 newData.append((255, 255, 255, 0))
    #             else:
    #                 newData.append(item)
    #
    #         imgClothesTmp.putdata(newData)
    #
    #         imgClothesTmp.save("test.png", "PNG")
    #
    #         # imgClothes = Image.new('RGBA', (imgClothesTmp.size[0], imgClothesTmp.size[1]), (255, 255, 255, 20))
    #         copyClothes = imgClothesTmp.copy()
    #
    #         copyClothes = remove_background(copyClothes)
    #
    #         # imgBody.paste(imgClothesTmp)
    #
    #         if member.gender == Common.WOMAN:
    #             # Style
    #             indexStyleHair = Common.styles[member.hairStyle - 1]
    #
    #             pathHair = rootFolder + Common.WOMAN.lower() + "\\" + Common.WOMAN.lower() + "_" + str(
    #                 indexStyleHair + member.hairStyle) + "-preview.png"
    #
    #             print("Path Hair " + pathHair)
    #
    #         else:
    #             #  Hair
    #             pathHair = "D:\\ME\\2022\\Python\\Folder_Image_Test\\" + headFolder + "\\" + headFolder + "-" + str(
    #                 member.body) + "-hair-" + str(member.hair) + ".png"
    #             # imgHair = Image.open(pathHair)
    #             # copyHair = imgHair.copy()
    #             # imgBody.paste(copyHair, (0, 0))
    #
    #         # Font Text
    #         myFont = ImageFont.truetype("FreeFont.ttf", 35)
    #
    #         # Image
    #         # img = Image.open(image_content.image)
    #
    #         # Call draw Method to add 2D graphics in an image
    #         I1 = ImageDraw.Draw(imgBody)
    #
    #         position = member.position
    #
    #         # imgBody = imgBody.resize((width, height + 100))
    #
    #         # Add Text to an image
    #         I1.text((width / 2, height + 50), member.name, font=myFont,
    #                 fill=(255, 0, 0))
    #
    #         imgBody.save(saveFolder + "Hello123.png")
    #
    #         back_im = imgBody.copy()
    #         back_im = await remove_background(back_im)
    #         # imgMain.paste(back_im, (position.x, position.y))
    #
    #     imgMain.save(savedPath)
    #
    #     res = app.response_class(
    #         response=json.dumps({
    #             "path": savedPath
    #         }),
    #         status=200,
    #         mimetype='application/json'
    #     )
    #
    #     return res
    #
    # except Exception as e:
    #     print("An Exception " + e.__class__)
    #
    #     error = app.response_class(
    #         status=400
    #     )
    #     return error

    return {}


def scaleImage(image, scale):
    width, height = image.size
    image = image.resize((int(width * scale), int(height * scale)), Image.ANTIALIAS)
    return image


async def saveImage(img_result, nameFile) -> None:
    # async with aiofiles.open(path, "wb") as file:
    #     await file.write(image)

    image = Image.fromarray(img_result).convert("RGBA")
    imgByteArr = io.BytesIO()

    image.save(imgByteArr, format="PNG")
    imgByteArr = imgByteArr.getvalue()

    async with aiofiles.open(nameFile, "wb") as file:
        print("Hehe1")
        await file.write(imgByteArr)
        print("Hehe2")


# def remove_background(image: PIL.Image):
#     image = np.asarray(image.convert("RGBA"))
#     idx = (image[..., :3] == np.array((0, 0, 0))).all(axis=-1)
#     image[idx, 3] = 0
#     return PIL.Image.fromarray(image)


async def remove_background(image):
    # image = image.convert("RGBA")
    # datas = image.getdata()
    # newData = []
    # for item in datas:
    #     if item[0] == 255 and item[1] == 255 and item[2] == 255:
    #         newData.append((255, 0, 0))
    # else:
    #     newData.append(item)
    #
    # imgByteArr = io.BytesIO()
    #
    # image.putdata(newData)
    # transparent_image = np.asarray(image)
    # image.save(imgByteArr, format="PNG")
    # imgByteArr = imgByteArr.getvalue()
    #
    # async with aiofiles.open("D:\\ME\\2022\\Python\\Add_Text_Image\\img_result.png", "wb") as file:
    #     await file.write(imgByteArr)

    image = np.asarray(image.convert("RGBA"))
    idx = (image[..., :3] == np.array((0, 0, 0))).all(axis=-1)
    image[idx, 3] = 0

    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format="PNG")
    imgByteArr = imgByteArr.getvalue()

    async with aiofiles.open("D:\\ME\\2022\\Python\\Add_Text_Image\\img_remove_background.png", "wb") as file:
        await file.write(imgByteArr)
    return ""


def overlay_image_alpha(img, img_overlay, x, y, alpha_mask):
    """Overlay `img_overlay` onto `img` at (x, y) and blend using `alpha_mask`.

    `alpha_mask` must have same HxW as `img_overlay` and values in range [0, 1].
    """
    # Image ranges
    y1, y2 = max(0, y), min(img.shape[0], y + img_overlay.shape[0])
    x1, x2 = max(0, x), min(img.shape[1], x + img_overlay.shape[1])

    # Overlay ranges
    y1o, y2o = max(0, -y), min(img_overlay.shape[0], img.shape[0] - y)
    x1o, x2o = max(0, -x), min(img_overlay.shape[1], img.shape[1] - x)

    # Exit if nothing to do
    if y1 >= y2 or x1 >= x2 or y1o >= y2o or x1o >= x2o:
        return

    img_crop = img[y1:y2, x1:x2]
    img_overlay_crop = img_overlay[y1o:y2o, x1o:x2o]
    alpha = alpha_mask[y1o:y2o, x1o:x2o, np.newaxis]
    alpha_inv = 1.0 - alpha
    img_crop[:] = alpha * img_overlay_crop + alpha_inv * img_crop


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)
