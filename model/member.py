from model.position import Position


class Member:
    def __init__(self, gender, body, skin, hairStyle, hair, wing, name, position):
        self.gender = gender
        self.skin = skin
        self.body = body
        self.hairStyle = hairStyle
        self.hair = hair
        self.wing = wing
        self.name = name
        self.position = Position(position["x"], position["y"])


