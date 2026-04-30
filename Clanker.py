import requests
import random
import chompjs
import re
from Pokemon import Pokemon

class Cook:
    @staticmethod
    def create_pokemon_from_set(name, set_data):
        p = Pokemon()
        p.sName(name)
        moves = [m[0] if isinstance(m, list) else m for m in set_data.get("moves", [])]
        p.sMoves(moves)
        ability = set_data.get("ability")
        if isinstance(ability, list): ability = ability[0]
        p.sAbility(ability if ability else chompjs.parse_js_object(re.search(r'=\s*(\{.*?\});', requests.get("https://raw.githubusercontent.com/smogon/pokemon-showdown/master/data/pokedex.ts").text, re.DOTALL).group(1)).get(name.replace(":","").replace("-","").replace(" ","").replace("\u2019","").replace(".","").replace("e\u0301","e").lower().strip(), {}).get("abilities", {}).get("0")) ##
        item = set_data.get("item")
        if isinstance(item, list): item = item[0]
        p.sItem(item if item else "")
        nature = set_data.get("nature")
        if isinstance(nature, list): nature = nature[0]
        p.sNature(nature if nature else "Docile")
        stat_order = ["hp", "atk", "def", "spa", "spd", "spe"]
        raw_evs = set_data.get("evs", {})
        if isinstance(raw_evs, list): raw_evs = raw_evs[0] if raw_evs else {}
        p.sEvs([raw_evs.get(stat, 0) for stat in stat_order])
        raw_ivs = set_data.get("ivs", {})
        p.sIvs([raw_ivs.get(stat, 31) for stat in stat_order])
        return p

    @staticmethod
    def shitCook(team, ):
        try:
            response = requests.get("https://raw.githubusercontent.com/pkmn/smogon/main/data/sets/gen9nationaldex.json")
            response.raise_for_status()
            pkmn_data = response.json()
            sampleSets = []
            for pkmn_name, sets_dict in pkmn_data.items():
                for set_name, set_content in sets_dict.items():
                    mon = Cook.create_pokemon_from_set(pkmn_name, set_content)
                    sampleSets.append(mon)
            while len(team) < 6:
                pot = random.choice(sampleSets)
                while (pot.name in [p.name for p in team]) or (pot.item[-3:] in ["e Z", "e Y", "e X", "ite"] and pot.item != "Eviolite" and any([mon.item[-3:] in ["e Z", "e Y", "e X", "ite"] and mon.item != "Eviolite" for mon in team])) or (pot.item[-2:] == " Z" and pot.item[-4:] != "te Z" and any([mon.item[-2:] == " Z" and mon.item[-5:] != "te Z" for mon in team])):
                    pot = random.choice(sampleSets)
                team.append(pot)
            print("Team cooked successfully!")
        except Exception as e:
            #print(f"Error loading database: {e}")
            print("Failed to cook.")
        return team