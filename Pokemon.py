class Pokemon:
    def __init__(self):
        self.name = ""
        self.nickname = ""
        self.moves = []
        self.nature = "Docile"
        self.level = 100
        self.item = "No Item"
        self.evs = [0, 0, 0, 0, 0, 0]
        self.ivs = [31, 31, 31, 31, 31, 31]
        self.ability = "No Ability"
        self.gender = ""
    def sName(self, n):
        self.name = n
        self.nickname = n
    def sNickname(self, n):
        self.nickname = n
    def sMoves(self, m):
        self.moves = m
    def sNature(self, n):
        self.nature = n
    def sLevel(self, l):
        self.level = l
    def sItem(self, i):
        self.item = i
    def sEvs(self, e):
        self.evs = e
    def sIvs(self, i):
        self.ivs = i
    def sAbility(self, a):
        self.ability = a
    def sGender(self, g):
        self.gender = g

    def cEvs(self, ev, i):
        self.evs[i] = ev
    def cIvs(self, iv, i):
        self.ivs[i] = iv

    def format(self):
        return f"""{(f"{self.nickname} ({self.name})") if (self.nickname != self.name) else self.name} {(f"({self.gender}) ") if self.gender != "" else ""}{(f"@ {self.item}") if self.item != "No Item" else ("")}{f"\nLevel: {self.level}" if self.level != 100 else ""}
Ability: {self.ability}{"\nEVs:" if any(self.evs[i] > 0 for i in range(6)) else ""} {" / ".join(f"{val} {name}" for val, name in zip(self.evs, ["HP", "Atk", "Def", "SpA", "SpD", "Spe"]) if val > 0)}{"\nIVs:" if any(self.ivs[i] != 31 for i in range(6)) else ""} {" / ".join(f"{val} {name}" for val, name in zip(self.ivs, ["HP", "Atk", "Def", "SpA", "SpD", "Spe"]) if val != 31)}
{self.nature} Nature
{("- " if self.moves else "") + "\n- ".join(self.moves)}""".strip()