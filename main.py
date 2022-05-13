# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import json

from flask_cors import CORS

from flask import Flask

from model.image_content import ImageContent

app = Flask(__name__, template_folder='')
CORS(app)

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


@app.route("/")
def hello_world():
    try:
        image_content = ImageContent.fromJson(json.dumps(imageText))

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
                    fill=(255, 0, 0))

        # Display edited image
        img.show()

        # Save the edited image
        img.save("nature1.png")
    except Exception as e:
        print("An Exception " + e.__class__)
    return "Hello, World!"


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
