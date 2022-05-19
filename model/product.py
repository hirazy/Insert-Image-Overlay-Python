from model.member import Member


class Product:
    def __init__(self, background, numbers, members):
        self.background = background
        self.numbers = numbers

        self.members = []

        for i in range(0, len(members)):
            member = members[i]
            if member["gender"].lower() == "woman":
                self.members.append(Member(
                    gender=member["gender"],
                    body=member["body"],
                    skin=member["skin"],
                    hair=member["hair"],
                    hairStyle=member["hairStyle"],
                    wing=member["wing"],
                    name=member["name"],
                    position=member["position"]
                ))
            else:
                self.members.append(Member(
                    gender=member["gender"],
                    body=member["body"],
                    hairStyle=None,
                    hair=member["hair"],
                    skin=member["skin"],
                    wing=member["wing"],
                    name=member["name"],
                    position=member["position"]
                ))

    @classmethod
    def fromJson(cls, json_string):
        return cls(**json_string)
