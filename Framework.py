import chompjs
import requests
import re
import random
import pokepastes_scraper as pastes
from Pokemon import Pokemon
from pokemon_formats import PokePaste
from Clanker import Cook

def formatName(pName):
    return pName.replace(":","").replace("-","").replace(" ","").replace("\u2019","").replace(".","").replace("e\u0301","e").lower().strip()

def tier(pokemon):
    content = requests.get("https://raw.githubusercontent.com/smogon/pokemon-showdown/master/data/formats-data.ts").text
    match = re.search(r'=\s*(\{.*?\});', content, re.DOTALL)
    if match:
        ts_object = match.group(1)
        data = chompjs.parse_js_object(ts_object)
        return chompjs.parse_js_object(ts_object).get(formatName(pokemon), {})
    else:
        return None

def dexSearch(pokemon):
    content = requests.get("https://raw.githubusercontent.com/smogon/pokemon-showdown/master/data/pokedex.ts").text
    match = re.search(r'=\s*(\{.*?\});', content, re.DOTALL)
    if match:
        ts_object = match.group(1)
        return chompjs.parse_js_object(ts_object).get(formatName(pokemon), {})
    else:
        return "N/A"

def moves(pokemon):
    content = requests.get("https://raw.githubusercontent.com/smogon/pokemon-showdown/master/data/learnsets.ts").text
    match = re.search(r'=\s*(\{.*?\});', content, re.DOTALL)
    if match:
        ts_object = match.group(1)
        data = chompjs.parse_js_object(ts_object)
        if dexSearch(formatName(pokemon)).get("forme", "N/A") in ["Mega", "Mega-X", "Mega-Y", "Mega-Z", "Wellspring", "Hearthflame", "Cornerstone", "Therian", "Terastal", "Stellar", "Crowned"]:
            return list(data.get(formatName(dexSearch(formatName(pokemon)).get("baseSpecies", "N/A")), {}).get('learnset', 'N/A').keys())
        elif dexSearch(formatName(pokemon)).get("baseSpecies", "N/A") == "Rotom":
            return list(data.get(formatName(dexSearch(formatName(pokemon)).get("baseSpecies", "N/A")), {}).get('learnset', 'N/A').keys()) + list(data.get(formatName(pokemon), {}).get('learnset', 'N/A').keys())
        try:
            return list(data.get(formatName(pokemon), {}).get('learnset', 'N/A').keys())
        except AttributeError:
            return list(data.get(formatName(dexSearch(formatName(pokemon)).get("changesFrom", "N/A")), {}).get('learnset', 'N/A').keys())
    else:
        return "N/A"

def manualLoop(team):
    state = ""
    while True:
        print(f"\nCURRENT TEAM:\n{terminalCur(team)}") if state != "show" else None
        state = input("\nWhat to do? (add/remove/edit/show/paste/finish): ").lower()
        if state == "add":

            new = Pokemon()
            flag, cont = True, True
            while flag and cont:
                try:
                    if len(team) == 6:
                        print("Team is full.")
                        flag = False
                        break
                    inp = formatName(str(input("Pokemon Species ('help' to list available pokemon,'x' to cancel): ")))
                    if inp == "x":
                        flag = False
                        break
                    elif inp == "help":
                        print("\nAvailable Pokemon: " + ", ".join(mon for mon in NDOULegal))
                        flag = False
                        break
                    elif inp not in NDOULegal:
                        print("Pokemon is not legal in SVNatDexOU. Make sure you spelled and formatted the name correctly (e.g. " + '"Raichu-Alola"' + ')')
                    else:
                        new.sName(dexSearch(inp).get("name", "N/A"))
                        cont = False

                except ValueError:
                    print("Invalid input. Please try again.")
            cont = True
            while flag and cont:
                try:
                    inp = input("Nickname (leave blank for none, 'x' to cancel): ")
                    if inp.lower() == "x":
                        flag = False
                        break
                    if len(inp.strip()) > 18:
                        print("Nickname must be 18 characters or less.")
                    elif len(inp.strip()) > 0:
                        new.sNickname(inp.strip())
                        cont = False
                    else:
                        cont = False
                except ValueError:
                    print("Invalid input. Please try again.")
            cont = True
            while flag and cont:
                try:
                    inp = input("Nature (leave blank for docile, 'x' to cancel): ")
                    if inp.lower() == "x":
                        flag = False
                        break
                    if len(inp) > 0 and inp.lower().capitalize() not in ["Adamant", "Bashful", "Bold", "Brave", "Calm", "Careful", "Docile", "Gentle", "Hardy", "Hasty", "Impish", "Jolly", "Lax", "Lonely", "Mild", "Modest", "Naive", "Naughty", "Quiet", "Quirky", "Rash", "Relaxed", "Sassy", "Serious", "Timid"]:
                        print("Invalid nature. Please try again.")
                    elif len(inp) > 0:
                        new.sNature(inp.lower().capitalize())
                        cont = False
                    else:
                        cont = False
                except ValueError:
                    print("Invalid input. Please try again.")
            cont = True
            while flag and cont:                
                try:
                    if dexSearch(new.name).get("requiredItem", False):
                        new.sItem(dexSearch(new.name).get("requiredItem"))
                        cont = False
                    else:
                        inp = input("Item (leave blank for none, 'help' to list available items, 'x' to cancel): ")
                        if inp.lower() == "x":
                            flag = False
                            break
                        elif inp.lower() == "help":
                            print("\nAvailable Items: " + ", ".join(item for item in allItems.keys()))
                            flag = False
                            break
                        elif len(inp) > 0 and formatName(inp) not in allItems:
                            print("Item not found. Make sure you spelled and formatted the name correctly (e.g. " + '"Choice Band"' + ')')
                        elif len(inp) > 0:
                            new.sItem(allItems.get(formatName(inp)))
                            cont = False
                        else:
                            cont = False
                except ValueError:
                    print("Invalid input. Please try again.")
            cont = True
            while flag and cont:                 
                try:
                    inp = input("Level (leave blank to default to 100, 'x' to cancel): ")
                    if inp.lower() == "x":
                        flag = False
                        break
                    if len(inp) > 0 and (not inp.isdigit() or int(inp) < 1 or int(inp) > 100):
                        print("Level must be a number between 1 and 100.")
                    elif len(inp) > 0:
                        new.sLevel(int(inp))
                        cont = False
                    else:
                        cont = False
                except ValueError:
                    print("Invalid input. Please try again.")
            cont = True
            while flag and cont:
                try:
                    inp = input("EVs (HP Atk Def SpA SpD Spe, separated by spaces, leave blank to default to 6x0, 'x' to cancel): ")
                    if inp.lower() == "x":
                        flag = False
                        break
                    if len(inp) > 0:
                        evs = list(map(int, inp.split()))
                        if len(evs) != 6 or any(ev < 0 or ev > 252 for ev in evs) or sum(evs) > 510:
                            print("EVs must be 6 numbers between 0 and 252, and their sum must be at most 510.")
                        else:
                            new.sEvs(evs)
                            cont = False
                    else:
                        cont = False
                except ValueError:
                    print("Invalid input. Please try again.")
            cont = True
            while flag and cont:
                try:
                    inp = input("IVs (HP Atk Def SpA SpD Spe, separated by spaces, leave blank to default to 6x31, 'x' to cancel): ")
                    if inp.lower() == "x":
                        flag = False
                        break
                    if len(inp) > 0:
                        ivs = list(map(int, inp.split()))
                        if len(ivs) != 6 or any(iv < 0 or iv > 31 for iv in ivs):
                            print("IVs must be 6 numbers between 0 and 31.")
                        else:
                            new.sIvs(ivs)
                            cont = False
                    else:
                        cont = False
                except ValueError:
                    print("Invalid input. Please try again.")
            cont = True
            while flag and cont:
                try:
                    if dexSearch(new.name).get("forme", False) in ["Mega", "Mega-X", "Mega-Y", "Mega-Z", "Terastal", "Stellar"]: #maybe for form changes too like Zacian-h/primals?
                        inp = input(f"Ability before transforming: {', '.join(dexSearch(dexSearch(new.name).get("baseSpecies")).get('abilities', {}).values())} (will become {list(dexSearch(new.name).get('abilities', {}).values())[0]} after transforming,leave blank to skip, 'x' to cancel): ")
                        if inp.lower() == "x":
                            flag = False
                            break
                        elif inp.lower() == "":
                            cont = False
                        elif formatName(inp) not in allAbilities:
                            print("Invalid ability. Pleaset try again.")
                        elif formatName(inp) not in [formatName(ability) for ability in dexSearch(dexSearch(new.name).get("baseSpecies")).get('abilities', {}).values()]:
                            print(f"{new.name} cannot have '{inp}' as a base ability. Please try again.")
                        else:
                            new.sAbility(str([ability for ability in dexSearch(dexSearch(new.name).get("baseSpecies")).get('abilities', {}).values() if formatName(ability) == formatName(inp)][0]))
                            cont = False
                    else:
                        inp = input(f"Ability: {', '.join(dexSearch(new.name).get('abilities', {}).values())} (leave blank to skip, 'x' to cancel): ")
                        if inp.lower() == "x":
                            flag = False
                            break
                        elif inp.lower() == "":
                            cont = False
                        elif formatName(inp) not in allAbilities:
                            print("Invalid ability. Please try again.")
                        elif formatName(inp) not in [formatName(ability) for ability in dexSearch(new.name).get("abilities", {}).values()]:
                            print(f"{new.name} cannot have '{inp}' as an ability. Please try again.")
                        else:
                            new.sAbility(str([ability for ability in dexSearch(new.name).get("abilities", {}).values() if formatName(ability) == formatName(inp)][0]))
                            cont = False
                except ValueError:
                    print("Invalid input. Please try again.")
            cont = True
            while flag and cont:
                try:
                    if dexSearch(new.name).get("gender", "N/A") in ["M", "F"]:
                        new.sGender(dexSearch(new.name).get("gender"))
                        cont = False
                    elif dexSearch(new.name).get("gender", "N/A") == "N":
                        cont = False
                    else:
                        inp = input("Gender ('M' or 'F', Leave blank for no set, 'x' to cancel): ")
                        if inp.lower() == "x":
                            flag = False
                            break
                        if inp.lower() in ['m', 'f']:
                            new.sGender(inp.capitalize())
                            cont = False
                        elif inp == "":
                            cont = False
                        else:
                            print("Bad Gender. Please try again.")
                except ValueError:
                    print("Invalid input. Please try again.")
            cont = True
            while flag and cont:
                try:
                    moveList = moves(new.name)
                    inp = input(f"Enter a move for {f'{new.nickname} ({new.name})' if (new.nickname != new.name) else new.name} ('help' for available moves, 'stop' to finish early, 'x' to cancel): ")
                    if inp.lower() == "x":
                        flag = False
                        break
                    elif inp.lower() == "help":
                        print(f"\nAvailable moves for {new.name}: {', '.join(moveList)}\n")
                    elif inp.lower() == "stop":
                        cont = False
                    elif formatName(inp) not in moveList:
                        print("Move not found. Make sure you spelled and your pokemon learns the move.")
                    elif formatName(inp) in [formatName(move) for move in new.moves]:
                        print("Move already added.")
                    else:
                        new.moves.append(allMoves.get(formatName(inp)))
                    if len(new.moves) == 4:
                        cont = False
                except ValueError:
                    print("Invalid input. Please try again.")
            if flag: 
                team.append(new)
                print(f"Added {f"{new.nickname} ({new.name})" if (new.nickname != new.name) else (new.name)} to the team.")
            else:
                print("Cancelled adding Pokemon.")
        elif state == "remove":
            try:
                idx = int(input("\nslot of Pokemon to remove (1-6): ")) - 1
                if idx in range(len(team)):
                    removed = team.pop(idx)
                    print(f"\nRemoved {f"{removed.nickname} ({removed.name})" if removed.nickname != removed.name else (removed.name)} from team.")
                else:
                    print("\nInvalid index.")
            except ValueError:
                print("\nAn error occured.")
        elif state == "edit":
            print("\nHow about you remove and re-add the Pokemon with the changes you want to make you lazy bum?")
            """
            idx = int(input("\nslot of Pokemon to edit (1-6): "))-1
            if idx in range(len(team)):
                print(f"\nEditing {f"{team[idx].nickname} ({team[idx].name})" if team[idx].nickname != team[idx].name else team[idx].name}:")
            else:
                print("\nInvalid index.")
            """
        elif state == "show":
            print(f"\nCURRENT TEAM:\n{terminalCur(team)}")
        elif state == "paste":
            try:
                url = input("\nPokéPaste URL: ").strip()
                paste = requests.get(url.rstrip('/') + '/raw' if '/raw' not in url else url).text.splitlines()
                team = []
                for line in paste:
                    line = line.strip()
                    if not line:
                        continue
                    if not any(line.startswith(x) for x in ["- ", "Ability:", "Level:", "EVs:", "IVs:", "Nature", "Shiny:"]):
                        if " Nature" not in line:
                            current_p = Pokemon()
                            team.append(current_p)
                            if " @ " in line:
                                name_part, item = line.split(" @ ", 1)
                                current_p.sItem(item)
                            else:
                                name_part = line
                            if "(" in name_part and ")" in name_part:
                                p_nick = name_part[:name_part.find("(")].strip()
                                p_name = name_part[name_part.find("(")+1:name_part.find(")")].strip()
                                current_p.sName(p_name)
                                current_p.sNickname(p_nick)
                            else:
                                current_p.sName(name_part.strip())
                                current_p.sNickname(name_part.strip())
                            continue
                    if current_p:
                        if line.startswith("- "):
                            current_p.moves.append(line.replace("- ", "").strip())
                        elif line.startswith("Ability: "):
                            current_p.sAbility(line.replace("Ability: ", "").strip())
                        elif " Nature" in line:
                            current_p.sNature(line.replace(" Nature", "").strip())
                        elif line.startswith("Level: "):
                            current_p.sLevel(int(line.replace("Level: ", "")))
                        elif line.startswith("EVs: "):
                            ev_map = {"HP":0, "Atk":1, "Def":2, "SpA":3, "SpD":4, "Spe":5}
                            parts = line.replace("EVs: ", "").split(" / ")
                            for part in parts:
                                val, stat = part.split()
                                current_p.cEvs(int(val), ev_map[stat])
                        elif line.startswith("IVs: "):
                            iv_map = {"HP":0, "Atk":1, "Def":2, "SpA":3, "SpD":4, "Spe":5}
                            parts = line.replace("IVs: ", "").split(" / ")
                            for part in parts:
                                val, stat = part.split()
                                current_p.cIvs(int(val), iv_map[stat])
            except ValueError:
                print("\nInvalid URL. Are you using a pokepaste link? Format should look like 'https://pokepast.es/...'")
        elif state == "finish" or state == "fin":
            break
        else: print("\nInvalid input, try again.")
    print("\nAll the ingredients are gathered! McPokeBot is cooking up your team...")
    pokepaste(Cook.shitCook(team))

def pokepaste(team):
    teamStr = """"""
    teamStr += "\n\n".join(pokemon.format() for pokemon in team)
    teamStr.strip()
    teamStr += "\n\n\n\n"
    print(f"Team successfully exported to: {PokePaste.createPokePaste(teamStr, title="Order Up!", author=f"McPokeClanker + {random.choice(pokeChefs)}", format="gen9nationaldex")}")

def terminalCur(team):
    teamStr = """"""
    teamStr += "\n\n".join(pokemon.format() for pokemon in team)
    teamStr.strip()
    return teamStr

pokeChefs = ["InvinIsAClown", "GgEzNoobBozo", "Dank0702", "TheMilkCan", "I_Be_Me", "Old Labsire","Blacephalon", "Oshawott", "Snom", "Spinda", "Gourgeist Ramsay", "Rattatatouille", "Binging with Bayleef", "Nickilicky DiGiovanni", "Uncle Roggenrola"]
allMoves = {m[0]: m[1] for m in re.findall(r'^\t"?(\w+)"?:\s*\{[\s\S]*?name:\s*["\'](.*?)["\']', requests.get("https://raw.githubusercontent.com/smogon/pokemon-showdown/master/data/moves.ts").text, re.MULTILINE)}
allAbilities = re.findall(r'^\t([a-z0-9]+): \{', requests.get("https://raw.githubusercontent.com/smogon/pokemon-showdown/master/data/abilities.ts").text, re.MULTILINE)
allItems = {m[0]: m[1] for m in re.findall(r'^\t"?(\w+)"?:\s*\{[\s\S]*?name:\s*["\'](.*?)["\']', requests.get("https://raw.githubusercontent.com/smogon/pokemon-showdown/master/data/items.ts").text, re.MULTILINE)}

NDOULegal = ['bulbasaur', 'ivysaur', 'venusaur', 'venusaurmega', 'charmander', 'charmeleon', 'charizard', 'charizardmegax', 'charizardmegay', 'squirtle', 'wartortle', 'blastoise', 'caterpie', 'metapod', 'butterfree', 'weedle', 'kakuna', 'beedrill', 'beedrillmega', 'pidgey', 'pidgeotto', 'pidgeot', 'pidgeotmega', 'rattata', 'rattataalola', 'raticate', 'raticatealola', 'spearow', 'fearow', 'ekans', 'arbok', 'pichu', 'pikachu', 'pikachuoriginal', 'pikachuhoenn', 'pikachusinnoh', 'pikachuunova', 'pikachukalos', 'pikachualola', 'pikachupartner', 'pikachuworld', 'raichu', 'raichualola', 'sandshrew', 'sandshrewalola', 'sandslash', 'sandslashalola', 'nidoranf', 'nidorina', 'nidoqueen', 'nidoranm', 'nidorino', 'nidoking', 'cleffa', 'clefairy', 'clefable', 'vulpix', 'vulpixalola', 'ninetales', 'ninetalesalola', 'igglybuff', 'jigglypuff', 'wigglytuff', 'zubat', 'golbat', 'crobat', 'oddish', 'gloom', 'vileplume', 'bellossom', 'paras', 'parasect', 'venonat', 'venomoth', 'diglett', 'diglettalola', 'dugtrio', 'dugtrioalola', 'meowth', 'meowthalola', 'meowthgalar', 'persian', 'persianalola', 'perrserker', 'psyduck', 'golduck', 'mankey', 'primeape', 'growlithe', 'growlithehisui', 'arcanine', 'arcaninehisui', 'poliwag', 'poliwhirl', 'poliwrath', 'politoed', 'abra', 'kadabra', 'alakazam', 'machop', 'machoke', 'machamp', 'bellsprout', 'weepinbell', 'victreebel', 'tentacool', 'tentacruel', 'geodude', 'geodudealola', 'graveler', 'graveleralola', 'golem', 'golemalola', 'ponyta', 'ponytagalar', 'rapidash', 'rapidashgalar', 'slowpoke', 'slowpokegalar', 'slowbro', 'slowbromega', 'slowbrogalar', 'slowking', 'slowkinggalar', 'magnemite', 'magneton', 'magnezone', 'farfetchd', 'farfetchdgalar', 'sirfetchd', 'doduo', 'dodrio', 'seel', 'dewgong', 'grimer', 'grimeralola', 'muk', 'mukalola', 'shellder', 'cloyster', 'gastly', 'haunter', 'gengar', 'onix', 'steelix', 'steelixmega', 'drowzee', 'hypno', 'krabby', 'kingler', 'voltorb', 'voltorbhisui', 'electrode', 'electrodehisui', 'exeggcute', 'exeggutor', 'exeggutoralola', 'cubone', 'marowak', 'marowakalola', 'tyrogue', 'hitmonlee', 'hitmonchan', 'hitmontop', 'lickitung', 'lickilicky', 'koffing', 'weezing', 'weezinggalar', 'rhyhorn', 'rhydon', 'rhyperior', 'happiny', 'chansey', 'blissey', 'tangela', 'tangrowth', 'kangaskhan', 'horsea', 'seadra', 'kingdra', 'goldeen', 'seaking', 'staryu', 'starmie', 'mimejr', 'mrmime', 'mrmimegalar', 'mrrime', 'scyther', 'scizor', 'scizormega', 'kleavor', 'smoochum', 'jynx', 'elekid', 'electabuzz', 'electivire', 'magby', 'magmar', 'magmortar', 'pinsir', 'pinsirmega', 'tauros', 'taurospaldeacombat', 'taurospaldeablaze', 'taurospaldeaaqua', 'magikarp', 'gyarados', 'gyaradosmega', 'lapras', 'ditto', 'eevee', 'vaporeon', 'jolteon', 'flareon', 'espeon', 'umbreon', 'leafeon', 'glaceon', 'sylveon', 'porygon', 'porygon2', 'porygonz', 'omanyte', 'omastar', 'kabuto', 'kabutops', 'aerodactyl', 'aerodactylmega', 'munchlax', 'snorlax', 'articuno', 'articunogalar', 'zapdos', 'zapdosgalar', 'moltres', 'moltresgalar', 'dratini', 'dragonair', 'dragonite', 'mew', 'chikorita', 'bayleef', 'meganium', 'cyndaquil', 'quilava', 'typhlosion', 'typhlosionhisui', 'totodile', 'croconaw', 'feraligatr', 'sentret', 'furret', 'hoothoot', 'noctowl', 'ledyba', 'ledian', 'spinarak', 'ariados', 'chinchou', 'lanturn', 'togepi', 'togetic', 'togekiss', 'natu', 'xatu', 'mareep', 'flaaffy', 'ampharos', 'ampharosmega', 'azurill', 'marill', 'azumarill', 'bonsly', 'sudowoodo', 'hoppip', 'skiploom', 'jumpluff', 'aipom', 'ambipom', 'sunkern', 'sunflora', 'yanma', 'yanmega', 'wooper', 'wooperpaldea', 'quagsire', 'murkrow', 'honchkrow', 'misdreavus', 'mismagius', 'unown', 'wynaut', 'wobbuffet', 'girafarig', 'farigiraf', 'pineco', 'forretress', 'dunsparce', 'dudunsparce', 'gligar', 'gliscor', 'snubbull', 'granbull', 'qwilfish', 'qwilfishhisui', 'overqwil', 'shuckle', 'heracross', 'heracrossmega', 'sneasel', 'sneaselhisui', 'weavile', 'teddiursa', 'ursaring', 'ursaluna', 'slugma', 'magcargo', 'swinub', 'piloswine', 'mamoswine', 'corsola', 'corsolagalar', 'cursola', 'remoraid', 'octillery', 'delibird', 'mantyke', 'mantine', 'skarmory', 'houndour', 'houndoom', 'houndoommega', 'phanpy', 'donphan', 'stantler', 'wyrdeer', 'smeargle', 'miltank', 'raikou', 'entei', 'suicune', 'larvitar', 'pupitar', 'tyranitar', 'tyranitarmega', 'celebi', 'treecko', 'grovyle', 'sceptile', 'sceptilemega', 'torchic', 'combusken', 'blaziken', 'mudkip', 'marshtomp', 'swampert', 'swampertmega', 'poochyena', 'mightyena', 'zigzagoon', 'zigzagoongalar', 'linoone', 'linoonegalar', 'obstagoon', 'wurmple', 'silcoon', 'beautifly', 'cascoon', 'dustox', 'lotad', 'lombre', 'ludicolo', 'seedot', 'nuzleaf', 'shiftry', 'taillow', 'swellow', 'wingull', 'pelipper', 'ralts', 'kirlia', 'gardevoir', 'gardevoirmega', 'gallade', 'gallademega', 'surskit', 'masquerain', 'shroomish', 'breloom', 'slakoth', 'vigoroth', 'slaking', 'nincada', 'ninjask', 'shedinja', 'whismur', 'loudred', 'exploud', 'makuhita', 'hariyama', 'nosepass', 'probopass', 'skitty', 'delcatty', 'sableye', 'sableyemega', 'mawile', 'mawilemega', 'aron', 'lairon', 'aggron', 'aggronmega', 'meditite', 'medicham', 'medichammega', 'electrike', 'manectric', 'manectricmega', 'plusle', 'minun', 'volbeat', 'illumise', 'budew', 'roselia', 'roserade', 'gulpin', 'swalot', 'carvanha', 'sharpedo', 'sharpedomega', 'wailmer', 'wailord', 'numel', 'camerupt', 'cameruptmega', 'torkoal', 'spoink', 'grumpig', 'spinda', 'trapinch', 'vibrava', 'flygon', 'cacnea', 'cacturne', 'swablu', 'altaria', 'altariamega', 'zangoose', 'seviper', 'lunatone', 'solrock', 'barboach', 'whiscash', 'corphish', 'crawdaunt', 'baltoy', 'claydol', 'lileep', 'cradily', 'anorith', 'armaldo', 'feebas', 'milotic', 'castform', 'kecleon', 'shuppet', 'banette', 'banettemega', 'duskull', 'dusclops', 'dusknoir', 'tropius', 'chingling', 'chimecho', 'absol', 'absolmega', 'snorunt', 'glalie', 'glaliemega', 'froslass', 'spheal', 'sealeo', 'walrein', 'clamperl', 'huntail', 'gorebyss', 'relicanth', 'luvdisc', 'bagon', 'shelgon', 'salamence', 'beldum', 'metang', 'metagross', 'regirock', 'regice', 'registeel', 'latias', 'latiasmega', 'latios', 'latiosmega', 'jirachi', 'deoxysdefense', 'turtwig', 'grotle', 'torterra', 'chimchar', 'monferno', 'infernape', 'piplup', 'prinplup', 'empoleon', 'starly', 'staravia', 'staraptor', 'bidoof', 'bibarel', 'kricketot', 'kricketune', 'shinx', 'luxio', 'luxray', 'cranidos', 'rampardos', 'shieldon', 'bastiodon', 'burmy', 'wormadam', 'wormadamsandy', 'wormadamtrash', 'mothim', 'combee', 'vespiquen', 'pachirisu', 'buizel', 'floatzel', 'cherubi', 'cherrim', 'shellos', 'gastrodon', 'drifloon', 'drifblim', 'buneary', 'lopunny', 'lopunnymega', 'glameow', 'purugly', 'stunky', 'skuntank', 'bronzor', 'bronzong', 'chatot', 'spiritomb', 'gible', 'gabite', 'garchomp', 'garchompmega', 'riolu', 'lucario', 'hippopotas', 'hippowdon', 'skorupi', 'drapion', 'croagunk', 'toxicroak', 'carnivine', 'finneon', 'lumineon', 'snover', 'abomasnow', 'abomasnowmega', 'rotom', 'rotomheat', 'rotomwash', 'rotomfrost', 'rotomfan', 'rotommow', 'uxie', 'mesprit', 'azelf', 'heatran', 'regigigas', 'cresselia', 'phione', 'manaphy', 'shaymin', 'victini', 'snivy', 'servine', 'serperior', 'tepig', 'pignite', 'emboar', 'oshawott', 'dewott', 'samurott', 'samurotthisui', 'patrat', 'watchog', 'lillipup', 'herdier', 'stoutland', 'purrloin', 'liepard', 'pansage', 'simisage', 'pansear', 'simisear', 'panpour', 'simipour', 'munna', 'musharna', 'pidove', 'tranquill', 'unfezant', 'blitzle', 'zebstrika', 'roggenrola', 'boldore', 'gigalith', 'woobat', 'swoobat', 'drilbur', 'excadrill', 'audino', 'audinomega', 'timburr', 'gurdurr', 'conkeldurr', 'tympole', 'palpitoad', 'seismitoad', 'throh', 'sawk', 'sewaddle', 'swadloon', 'leavanny', 'venipede', 'whirlipede', 'scolipede', 'cottonee', 'whimsicott', 'petilil', 'lilligant', 'lilliganthisui', 'basculin', 'basculegion', 'basculegionf', 'sandile', 'krokorok', 'krookodile', 'darumaka', 'darumakagalar', 'darmanitan', 'maractus', 'dwebble', 'crustle', 'scraggy', 'scrafty', 'sigilyph', 'yamask', 'yamaskgalar', 'cofagrigus', 'runerigus', 'tirtouga', 'carracosta', 'archen', 'archeops', 'trubbish', 'garbodor', 'zorua', 'zoruahisui', 'zoroark', 'zoroarkhisui', 'minccino', 'cinccino', 'gothita', 'gothorita', 'gothitelle', 'solosis', 'duosion', 'reuniclus', 'ducklett', 'swanna', 'vanillite', 'vanillish', 'vanilluxe', 'deerling', 'sawsbuck', 'emolga', 'karrablast', 'escavalier', 'foongus', 'amoonguss', 'frillish', 'jellicent', 'alomomola', 'joltik', 'galvantula', 'ferroseed', 'ferrothorn', 'klink', 'klang', 'klinklang', 'tynamo', 'eelektrik', 'eelektross', 'elgyem', 'beheeyem', 'litwick', 'lampent', 'chandelure', 'axew', 'fraxure', 'haxorus', 'cubchoo', 'beartic', 'cryogonal', 'shelmet', 'accelgor', 'stunfisk', 'stunfiskgalar', 'mienfoo', 'mienshao', 'druddigon', 'golett', 'golurk', 'pawniard', 'bisharp', 'bouffalant', 'rufflet', 'braviary', 'braviaryhisui', 'vullaby', 'mandibuzz', 'heatmor', 'durant', 'deino', 'zweilous', 'hydreigon', 'larvesta', 'volcarona', 'cobalion', 'terrakion', 'virizion', 'tornadus', 'tornadustherian', 'thundurus', 'thundurustherian', 'landorustherian', 'kyurem', 'keldeo', 'meloetta', 'chespin', 'quilladin', 'chesnaught', 'fennekin', 'braixen', 'delphox', 'froakie', 'frogadier', 'greninja', 'bunnelby', 'diggersby', 'fletchling', 'fletchinder', 'talonflame', 'scatterbug', 'spewpa', 'vivillon', 'litleo', 'pyroar', 'flabebe', 'floette', 'florges', 'skiddo', 'gogoat', 'pancham', 'pangoro', 'furfrou', 'espurr', 'meowstic', 'honedge', 'doublade', 'aegislash', 'spritzee', 'aromatisse', 'swirlix', 'slurpuff', 'inkay', 'malamar', 'binacle', 'barbaracle', 'skrelp', 'dragalge', 'clauncher', 'clawitzer', 'helioptile', 'heliolisk', 'tyrunt', 'tyrantrum', 'amaura', 'aurorus', 'hawlucha', 'dedenne', 'carbink', 'goomy', 'sliggoo', 'sliggoohisui', 'goodra', 'goodrahisui', 'klefki', 'phantump', 'trevenant', 'pumpkaboo', 'gourgeist', 'bergmite', 'avalugg', 'avalugghisui', 'noibat', 'noivern', 'zygarde10', 'diancie', 'dianciemega', 'hoopa', 'hoopaunbound', 'volcanion', 'rowlet', 'dartrix', 'decidueye', 'decidueyehisui', 'litten', 'torracat', 'incineroar', 'popplio', 'brionne', 'primarina', 'pikipek', 'trumbeak', 'toucannon', 'yungoos', 'gumshoos', 'grubbin', 'charjabug', 'vikavolt', 'crabrawler', 'crabominable', 'oricorio', 'oricoriopompom', 'oricoriopau', 'oricoriosensu', 'cutiefly', 'ribombee', 'rockruff', 'rockruffdusk', 'lycanroc', 'lycanrocmidnight', 'lycanrocdusk', 'wishiwashi', 'mareanie', 'toxapex', 'mudbray', 'mudsdale', 'dewpider', 'araquanid', 'fomantis', 'lurantis', 'morelull', 'shiinotic', 'salandit', 'salazzle', 'stufful', 'bewear', 'bounsweet', 'steenee', 'tsareena', 'comfey', 'oranguru', 'passimian', 'wimpod', 'golisopod', 'sandygast', 'palossand', 'pyukumuku', 'typenull', 'silvally', 'silvallybug', 'silvallydark', 'silvallydragon', 'silvallyelectric', 'silvallyfairy', 'silvallyfighting', 'silvallyfire', 'silvallyflying', 'silvallyghost', 'silvallygrass', 'silvallyground', 'silvallyice', 'silvallypoison', 'silvallypsychic', 'silvallyrock', 'silvallysteel', 'silvallywater', 'minior', 'komala', 'turtonator', 'togedemaru', 'mimikyu', 'bruxish', 'drampa', 'dhelmise', 'jangmoo', 'hakamoo', 'kommoo', 'tapukoko', 'tapulele', 'tapubulu', 'tapufini', 'cosmog', 'cosmoem', 'nihilego', 'buzzwole', 'xurkitree', 'celesteela', 'kartana', 'guzzlord', 'necrozma', 'poipole', 'stakataka', 'blacephalon', 'zeraora', 'meltan', 'melmetal', 'grookey', 'thwackey', 'rillaboom', 'scorbunny', 'raboot', 'cinderace', 'sobble', 'drizzile', 'inteleon', 'skwovet', 'greedent', 'rookidee', 'corvisquire', 'corviknight', 'blipbug', 'dottler', 'orbeetle', 'nickit', 'thievul', 'gossifleur', 'eldegoss', 'wooloo', 'dubwool', 'chewtle', 'drednaw', 'yamper', 'boltund', 'rolycoly', 'carkol', 'coalossal', 'applin', 'flapple', 'appletun', 'dipplin', 'silicobra', 'sandaconda', 'cramorant', 'arrokuda', 'barraskewda', 'toxel', 'toxtricity', 'sizzlipede', 'centiskorch', 'clobbopus', 'grapploct', 'sinistea', 'polteageist', 'hatenna', 'hattrem', 'hatterene', 'impidimp', 'morgrem', 'grimmsnarl', 'milcery', 'alcremie', 'falinks', 'pincurchin', 'snom', 'frosmoth', 'stonjourner', 'eiscue', 'indeedee', 'indeedeef', 'morpeko', 'cufant', 'copperajah', 'dracozolt', 'arctozolt', 'arctovish', 'duraludon', 'dreepy', 'drakloak', 'zamazenta', 'kubfu', 'urshifurapidstrike', 'zarude', 'regieleki', 'regidrago', 'glastrier', 'calyrex', 'enamorus', 'enamorustherian', 'sprigatito', 'floragato', 'meowscarada', 'fuecoco', 'crocalor', 'skeledirge', 'quaxly', 'quaxwell', 'quaquaval', 'lechonk', 'oinkologne', 'oinkolognef', 'tarountula', 'spidops', 'nymble', 'lokix', 'rellor', 'rabsca', 'greavard', 'houndstone', 'flittle', 'wiglett', 'wugtrio', 'dondozo', 'veluza', 'finizen', 'smoliv', 'dolliv', 'arboliva', 'capsakid', 'scovillain', 'tadbulb', 'bellibolt', 'varoom', 'revavroom', 'orthworm', 'tandemaus', 'maushold', 'cetoddle', 'cetitan', 'frigibax', 'arctibax', 'tatsugiri', 'cyclizar', 'pawmi', 'pawmo', 'pawmot', 'wattrel', 'kilowattrel', 'bombirdier', 'squawkabilly', 'flamigo', 'klawf', 'nacli', 'naclstack', 'garganacl', 'glimmet', 'glimmora', 'shroodle', 'grafaiai', 'fidough', 'dachsbun', 'maschiff', 'mabosstiff', 'bramblin', 'brambleghast', 'gimmighoul', 'gimmighoulroaming', 'gholdengo', 'greattusk', 'brutebonnet', 'sandyshocks', 'screamtail', 'slitherwing', 'irontreads', 'ironmoth', 'ironhands', 'ironjugulis', 'ironthorns', 'ironvaliant', 'tinglu', 'wochien', 'tinkatink', 'tinkatuff', 'tinkaton', 'charcadet', 'armarouge', 'ceruledge', 'toedscool', 'toedscruel', 'kingambit', 'clodsire', 'ironleaves', 'poltchageist', 'sinistcha', 'okidogi', 'munkidori', 'fezandipiti', 'ogerpon', 'ogerponwellspring', 'ogerponcornerstone', 'archaludon', 'hydrapple', 'ragingbolt', 'ironboulder', 'ironcrown', 'terapagos', 'pecharunt'] + ['terapagosterastal']

"""
NDOULegal = []
for a in list(chompjs.parse_js_object(re.search(r'=\s*(\{.*?\});', requests.get("https://raw.githubusercontent.com/smogon/pokemon-showdown/master/data/formats-data.ts").text, re.DOTALL).group(1)).keys()):
    if tier(a).get("natDexTier", "N/A") not in ["AG", "Uber", "N/A"]:
        NDOULegal.append(formatName(a))
    elif (tier(a).get("natDexTier", "N/A") == "N/A") and (tier(a).get("tier", "N/A") in ["LC", "NFE", "ZU", "ZUBL","PU", "PUBL", "NU", "NUBL", "RU", "RUBl", "UU", "UUBL", "OU"]):
        NDOULegal.append(formatName(a))
takes too long so manual set
"""

print("""No autovalidation for teams yet, so validate yourself before adding to your team.
On that note, it tries to guide you torwards valid sets, but it is still possible to create
invalid teams (eg. species clause is not enabled for building purposes.)
The bot autofills the rest once you finish your manual part (make sure it's legal)""")
manualLoop([])
"""
    t = Pokemon()
    t.sName("Blacephalon"))
    t.sNickname("Employee OTM")
    t.sMoves(["Calm Mind", "Substitute", "Flamethrower", "Shadow Ball"])
    t.sNature("Timid")
    t.sItem("Ghostium Z")
    t.sEvs([0, 0, 0, 252, 4, 252])
    t.sIvs([31, 0, 31, 31, 31, 31])
    t.sAbility("Beast Boost")
    t2 = Pokemon()
    t2.sName("Blacephalon")
    t2.sNickname("WOAT")
    t2.sMoves(["Mind Blown", "Rock Blast", "Flame Charge", "Astonish"])
    t2.sNature("Naive")
    t2.sItem("Life Orb")
    t2.sEvs([0, 196, 0, 56, 4, 252])
    t2.sIvs([31, 31, 31, 0, 31, 0])
    t2.sAbility("Beast Boost")
    print(t.format())
    print(t2.format())
    pokepaste([t, t2])
    """
"""
except Exception as e:
    print(f"ERROR: {e}")
"""