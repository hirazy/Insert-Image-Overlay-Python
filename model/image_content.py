import json

from model.content import Content
from model.position import Position


class ImageContent():
    def __init__(self, image, content):
        self.image = image
        self.content = []

        for i in range(0, len(content)):
            item_content = content[i]
            self.content.append(Content(item_content["font"],
                                        Position(item_content["position"]["x"], item_content["position"]["y"]),
                                        item_content["text"]))

    @classmethod
    def fromJson(cls, json_string):
        json_dict = json.loads(json_string)
        return cls(**json_dict)
