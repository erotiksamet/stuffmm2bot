import requests
from time import sleep
import shopify
from flask import Flask, request
import asyncio
import websockets
from websockets.sync.client import connect
app = Flask(__name__)

# Set up important variables
shopify.ShopifyResource.set_site('https://43a7-88-240-180-166.ngrok-free.app/admin')
cookie = '_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_2FF63EF93918E68D45E27C32A3D07FDAD41921CE3A95545F80A4742C97430B067AB75A4058406687BC56D3DF623519E0A700F74EB671B4846D52A5231BC3E2EB4A941134E5B18128D7A595793A2BB96837A7CC9D90BCD6E1E83FBF5779E30B8AAEC2EDF99FC19149BA2B0BB829D94CD2C77CEE6FC1111A47222275864A25D052B806E52CF8109E09711F516F4B1D7C401490FE88311CE94747438890A52936F11D89446A2B44B8E48605B1A147E4C6ABF1AF306DE91D429981FCB0AC8F7194D6F17E9FE10042B6AF8FF309954822D200A834A6C08E7FAA66A9EA0A96607424408AA2CDBEDDFEC9A95A9312966A459FA42307B165E6465705B253CDA4D5370AB46FF88D077B8ADD0F8D56A76EFAF5B212F93E6672159DAD96C9503DA3C47780D83DC8177AECED0E16ED678D8544A57C4C14FB0FB7C9F02F9864C140DB20774A65417CD705704C1FE8ADD1F0CCFD02C2371CF8FFF23A589033C7701607B100C25EB677D8D01EB892D06FEB517DF5BAAA709C2DB77A30A36D711A1C615836482BA0E81E64DE'
# Don't touch above this line
# Set up Shopify credentials
shopify.ShopifyResource.set_user('a2a94ebd76cb1720dc41ed5267a542a6')
shopify.ShopifyResource.set_password('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')
shopify.ShopifyResource.set_format('json')
# Set Up Roblox credentials

# Set up the Discord webhook URL
webhook_url = 'https://discord.com/api/webhooks/1100883481136996384/fi8LQOaJv-7HxQNmvwBQQ4z6oy_AZldA4JtW410I3sSNHrcpB3SUr-sP-bwsYr1UZj_T'
# Set up the Roblox API endpoint
ROBLOX_API_ENDPOINT = 'https://users.roblox.com/v1/usernames/users'




def sendmsg(message):
    with connect("ws://localhost:3131") as websocket:
        websocket.send(message)
        print(f"Sent message to {websocket.remote_address}: {message}")


def get_user_id(username):
    request_payload = {
        "usernames": [username],
        "excludeBannedUsers": True
    }

    response_data = requests.post(ROBLOX_API_ENDPOINT, json=request_payload)

    # Check if the request succeeded
    if response_data.status_code == 200:
        user_data = response_data.json()["data"]
        if len(user_data) > 0:
            user_id = user_data[0]["id"]
            print(f"User ID for '{username}' is {user_id}")
            return user_id
        else:
            print(f"No user found with the username '{username}'")
    else:
        print(f"Error {response_data.status_code} - {response_data.text}")


# Define the item categories
item_categories = {
    #exclusives
'Rainbow_K': 'Weapons',
'Rainbow_G': 'Weapons',
'Blossom_G': 'Weapons',
'Sakura_K': 'Weapons',
'AmericaGun': 'Weapons',
'BloodKnife': 'Weapons',
'Gun1': 'Weapons',
'Frostbite': 'Weapons',
'Frostsaber': 'Weapons',
'GhostKnife': 'Weapons',
'GoldenGun': 'Weapons',
'Icebeam': 'Weapons',
'IceDragon': 'Weapons',
'Iceflake': 'Weapons',
'IceShard': 'Weapons',
'Phantom2022': 'Weapons',
'Phaser': 'Weapons',
'Plasmabeam': 'Weapons',
'Plasmablade': 'Weapons',
'ShadowKnife': 'Weapons',
'Snowflake': 'Weapons',
'Spectre2022': 'Weapons',
'Knife1': 'Weapons',
"WintersEdge": 'Weapons',
    #knifes

'HallowsBalde': 'Weapons',
'Hallow': 'Weapons',
'VampiresEdge': 'Weapons',
'ZombieBat': 'Weapons',
'BattleAxe': 'Weapons',
'BattleAxe2': 'Weapons',
'Scythe': 'Weapons',
'BlueSeer': 'Weapons',
'Boneblade': 'Weapons',
'Candleflame': 'Weapons',
'Candy': 'Weapons',
'Chill': 'Weapons',
'BonebladeChroma': 'Weapons',
'CandleflameChroma': 'Weapons',
'Gingermint_KChroma': 'Weapons',
'DeathshardChroma': 'Weapons',
'ElderwoodKnifeChroma': 'Weapons',
'FangChroma': 'Weapons',
'GemstoneChroma': 'Weapons',
'GingerbladeChroma': 'Weapons',
'HeatChroma': 'Weapons',
'SawChroma': 'Weapons',
'SeerChroma': 'Weapons',
'Slasher': 'Weapons',
'TidesChroma': 'Weapons',
'Clockwork': 'Weapons',
'Gingermint_K': 'Weapons',
'Sorry': 'Weapons',
'Deathshard': 'Weapons',
'ElderwoodKnife': 'Weapons',
'ElderwoodScythe': 'Weapons',
'EternalCane': 'Weapons',
'Eternal': 'Weapons',
'Eternal2': 'Weapons',
'Eternal3': 'Weapons',
'Eternal4': 'Weapons',
'Fang': 'Weapons',
'Flames': 'Weapons',
'Gemstone': 'Weapons',
'Ghostblade': 'Weapons',
'Gingerblade': 'Weapons',
'Hallowscythe': 'Weapons',
'Handsaw': 'Weapons',
'Heartblade': 'Weapons',
'Heat': 'Weapons',
'Icebreaker': 'Weapons',
'Icewing': 'Weapons',
'Logchopper': 'Weapons',
'Nebula': 'Weapons',
'Nightblade': 'Weapons',
'AmericaSword': 'Weapons',
'OrangeSeer': 'Weapons',
'Pixel': 'Weapons',
'Prismatic': 'Weapons',
'Pumpking': 'Weapons',
'PurpleSeer': 'Weapons',
'RedSeer': 'Weapons',
'Saw': 'Weapons',
'TheSeer': 'Weapons',
'SlasherChroma': 'Weapons',
'Spider': 'Weapons',
'SwirlyAxe': 'Weapons',
'SwirlyBlade': 'Weapons',
'TidesChroma': 'Weapons',
'Virtual': 'Weapons',
'Xmas': 'Weapons',
'YellowSeer': 'Weapons',
# Guns
'Amerilaser': 'Weapons',
'Iceblaster': 'Weapons',
'ChromaDarkbringer': 'Weapons',
'LaserChroma': 'Weapons',
'ChromaLightbringer': 'Weapons',
'LugerChroma': 'Weapons',
'SharkChroma': 'Weapons',
'SwirlyGunChroma': 'Weapons',
'Darkbringer': 'Weapons',
'Disint': 'Weapons',
'ElderwoodGun': 'Weapons',
'GingerLuger': 'Weapons',
'Gingermint_G': 'Weapons',
'GreenLuger': 'Weapons',
'Hallowgun': 'Weapons',
'Harvester': 'Weapons',
'Iceblaster': 'Weapons',
'Icepiercer': 'Weapons',
'Jinglegun': 'Weapons',
'Laser': 'Weapons',
'Lightbringer': 'Weapons',
'Luger': 'Weapons',
'Lugercane': 'Weapons',
'Makeshift': 'Weapons',
'Minty': 'Weapons',
'RedLuger': 'Weapons',
'Shark': 'Weapons',
'Sugar': 'Weapons',
'SwirlyGun': 'Weapons',
  #pets
'BatChroma': 'Pets',
'BearChroma': 'Pets',
'BunnyChroma': 'Pets',
'DogChroma': 'Pets',
'FoxChroma': 'Pets',
'PigFire': 'Pets',
'PigChroma': 'Pets',
'Deathspeaker': 'Pets',
'Electro': 'Pets',
'BatFire': 'Pets',
'BearFire': 'Pets',
'BunnyFire': 'Pets',
'CatFire': 'Pets',
'DogFire': 'Pets',
'FoxFire': 'Pets',
'PigFire': 'Pets',
'Frostbird': 'Pets',
'Ghosty': 'Pets',
'<3': 'Pets',
'IcePhoenix': 'Pets',
'Icey': 'Pets',
'Phoenix': 'Pets',
'AmericanEagle': 'Pets',
'Skelly': 'Pets',
'Steambird': 'Pets',
'Traveller': 'Pets'
}

# Define the item name mappings
item_name_mappings = {
    #exclusives
'Rainbow_K': 'Rainbow_K',
'Rainbow_G': 'Rainbow_G',
'Blossom_G': 'Blossom_G',
'Sakura_K': 'Sakura_K',
'America': 'AmericaGun',
'Blood': 'BloodKnife',
'Cowboy': 'Gun1',
'Frostbite': 'Frostbite',
'Frostsaber': 'Frostsaber',
'Ghost': 'GhostKnife',
'Golden': 'GoldenGun',
'IceDragon': 'IceDragon',
'IceShard': 'IceShard',
'Icebeam': 'Icebeam',
'Iceflake': 'Iceflake',
'Phantom': 'Phantom2022',
'Phaser': 'Phaser',
'Plasmabeam': 'Plasmabeam',
'Plasmablade': 'Plasmablade',
'Shadow': 'ShadowKnife',
'Snowflake': 'Snowflake',
'Spectre': 'Spectre2022',
'Splitter': 'Knife1',
"Winter'sEdge": 'WintersEdge',
        #knifes
"Hallow'sBlade": 'HallowsBalde',
"Hallow'sEdge": 'Hallow',
"Vampire'sEdge": 'VampiresEdge',
'Bat': 'ZombieBat',
'BattleAxe': 'BattleAxe',
'BattleAxeII': 'BattleAxe2',
'Batwing': 'Scythe',
'BlueSeer': 'BlueSeer',
'Boneblade': 'Boneblade',
'Candleflame': 'Candleflame',
'Candy': 'Candy',
'Chill': 'Chill',
'ChromaBoneblade': 'BonebladeChroma',
'ChromaCandleflame': 'CandleflameChroma',
'ChromaCookiecane': 'Gingermint_KChroma',
'ChromaDeathshard': 'DeathshardChroma',
'ChromaElderwoodBlade': 'ElderwoodKnifeChroma',
'ChromaFang': 'FangChroma',
'ChromaGemstone': 'GemstoneChroma',
'ChromaGingerblade': 'GingerbladeChroma',
'ChromaHeat': 'HeatChroma',
'ChromaSaw': 'SawChroma',
'ChromaSeer': 'SeerChroma',
'ChromaSlasher': 'SlasherChroma',
'ChromaTides': 'TidesChroma',
'Clockwork': 'Clockwork',
'Cookiecane': 'Gingermint_K',
'Corrupt': 'Sorry',
'Deathshard': 'Deathshard',
'ElderwoodBlade': 'ElderwoodKnife',
'ElderwoodScythe': 'ElderwoodScythe',
'Eternalcane': 'EternalCane',
'EternalI': 'Eternal',
'EternalII': 'Eternal2',
'EternalIII': 'Eternal3',
'EternalIV': 'Eternal4',
'Fang': 'Fang',
'Flames': 'Flames',
'Gemstone': 'Gemstone',
'Ghostblade': 'Ghostblade',
'Gingerblade': 'Gingerblade',
'Hallowscythe': 'Hallowscythe',
'Handsaw': 'Handsaw',
'Heartblade': 'Heartblade',
'Heat': 'Heat',
'Icebreaker': 'Icebreaker',
'Icewing': 'Icewing',
'Logchopper': 'Logchopper',
'Nebula': 'Nebula',
'Nightblade': 'Nightblade',
'OldGlory': 'AmericaSword',
'OrangeSeer': 'OrangeSeer',
'Pixel': 'Pixel',
'Prismatic': 'Prismatic',
'Pumpking': 'Pumpking',
'PurpleSeer': 'PurpleSeer',
'RedSeer': 'RedSeer',
'Saw': 'Saw',
'Seer': 'TheSeer',
'Slasher': 'Slasher',
'Spider': 'Spider',
'SwirlyAxe': 'SwirlyAxe',
'SwirlyBlade': 'SwirlyBlade' ,
'Tides': 'TidesChroma',
'Virtual': 'Virtual',
'Xmas': 'Xmas',
'YellowSeer': 'YellowSeer',
# Guns
'Amerilaser': 'Amerilaser',
'Blaster': 'Iceblaster',
'ChromaDarkbringer': 'ChromaDarkbringer',
'ChromaLaser': 'LaserChroma',
'ChromaLightbringer': 'ChromaLightbringer',
'ChromaLuger': 'LugerChroma',
'ChromaShark': 'SharkChroma',
'ChromaSwirlyGun': 'SwirlyGunChroma',
'Darkbringer': 'Darkbringer',
'Disint': 'Disint',
'ElderwoodRevolver': 'ElderwoodGun',
'GingerLuger': 'GingerLuger',
'Gingermint': 'Gingermint_G',
'GreenLuger': 'GreenLuger',
'Hallowgun': 'Hallowgun',
'Harvester': 'Harvester',
'Iceblaster': 'Iceblaster',
'Icepiercer': 'Icepiercer',
'Jinglegun': 'Jinglegun',
'Laser': 'Laser',
'Lightbringer': 'Lightbringer',
'Luger': 'Luger',
'Lugercane': 'Lugercane',
'Makeshift': 'Makeshift',
'Minty': 'Minty',
'RedLuger': 'RedLuger',
'Shark': 'Shark',
'Sugar': 'Sugar',
'SwirlyGun': 'SwirlyGun',
    #pets
'ChromaFireBat': 'BatChroma',
'ChromaFireBear': 'BearChroma',
'ChromaFireBunny': 'BunnyChroma',
'ChromaFireDog': 'DogChroma',
'ChromaFireFox': 'FoxChroma',
'ChromaFirePig': 'PigChroma',
'Deathspeaker': 'Deathspeaker',
'Electro': 'Electro',
'FireBat': 'BatFire',
'FireBear': 'BearFire',
'FireBunny': 'BunnyFire',
'FireCat': 'CatFire',
'FireDog': 'DogFire',
'FireFox': 'FoxFire',
'FirePig': 'PigFire',
'Frostbird': 'Frostbird',
'Ghosty': 'Ghosty',
'HeartPet': '<3',
'IcePhoenix': 'IcePhoenix',
'Icey': 'Icey',
'Phoenix': 'Phoenix',
'Sammy': 'AmericanEagle',
'Skelly': 'Skelly',
'Steambird': 'Steambird',
'Traveller': 'Traveller'
}

# Define the bundle items
bundle_items = {
    'AllChromaPetSet': {
        'ChromaFireBat': 1,
        'ChromaFireBear': 1,
        'ChromaFireBunny': 1,
        'ChromaFireDog': 1,
        'ChromaFireFox': 1,
        'ChromaFirePig': 1,
        'Deathspeaker': 1
    },
    'SakuraSet': {
        'Sakura_K': 1,
        'Blossom_G': 1
    },

    'RainbowSet': {
        'Rainbow_K': 1,
        'Rainbow_G': 1
    },
    'AllGodlyPetSet': {
        'Electro': 1,
        'FireBat': 1,
        'FireBear': 1,
        'FireBunny': 1,
        'FireCat': 1,
        'FireDog': 1,
        'FireFox': 1,
        'FirePig': 1,
        'Frostbird': 1,
        'Ghosty': 1,
        'HeartPet': 1,
        'IcePhoenix': 1,
        'Icey': 1,
        'Phoenix': 1,
        'Sammy': 1,
        'Skelly': 1,
        'Steambird': 1,
        'Traveller': 1

    },
    'AmericanSet': {
        'Amerilaser': 1,
        'AmericaSword': 1
    },
    'EternalSet': {
        'Eternal': 1,
        'Eternal2': 1,
        'Eternal3': 1,
        'Eternal4': 1
    },
    'AncientSet': {
        'Batwing': 1,
        'Icewing': 1,
        'ElderwoodScythe': 1,
        'Hallowscythe': 1,
        'Logchopper': 1
    },
    'BatSet': {
        'Bat': 1,
        'Makeshift': 1
    },
    'BattleAxeSet': {
        'BattleAxeII': 1,
        'BattleAxe': 1

    },
    'BringerSet': {
        'Darkbringer': 1,
        'Lightbringer': 1
    },
    'CandySet': {
        'Candy': 1,
        'Sugar': 1
    },
    'CaneSet': {
        'Eternalcane': 1,
        'Lugercane': 1
    },
    'ChristmasSet': {
        'Xmas': 1,
        'Jinglegun': 1
    },
    'ChromaBringerSet': {
        'ChromaDarkbringer': 1,
        'ChromaLightbringer': 1
    },
    'CookieSet': {
        'Cookiecane': 1,
        'Gingermint': 1
    },
    'CorruptSet': {
        'Corrupt': 1,
        'Luger': 1
    },
    'ElderwoodSet': {
        'ElderwoodScythe': 1,
        'ElderwoodRevolver': 1
    },
    'ElementalSet': {
        'Tides': 1,
        'Flames': 1
    },
    'Eternal Set': {
        'EternalI': 1,
        'EternalII': 1,
        'EternalIII': 1,
        'EternalIV': 1
    },
    'FrostSet': {
        'Frostbite': 1,
        'Frostsaber': 1
    },
    'FullSwirlySet': {
        'SwirlyGun': 1,
        'SwirlyBlade': 1,
        'Swirly Axe': 1
    },
    'GemstoneSet': {
        'Gemstone': 1,
        'Lightbringer': 1
    },
    'GingerSet': {
        'GingerLuger': 1,
        'Gingerblade': 1
    },
    'HallowSet': {
        'Hallowgun': 1,
        'Hallowscythe': 1
    },
    'HalloweenSet': {
        "Hallow'sEdge": 1,
          "Hallow'sBlade": 1,
       'Boneblade': 1,
         'Pumpking': 1,
'Spider': 1,
'Ghostblade': 1,
'BattleAxe': 1,
'BattleAxeII': 1
},
'IceSet': {
    'Icebreaker': 1,
    'Iceblaster': 1
},
'IceflakeSet': {
    'Icebeam': 1,
    'Iceflake': 1
},
'SlasherSet': {
    'Slasher': 1,
    'Laser': 1
},
'LogchopperSet': {
    'Logchopper': 1,
    'Minty': 1
},
'LugerSet': {
    'Luger': 1,
    'Green Luger': 1,
    'Red Luger': 1,
    'Ginger Luger': 1,
    'Lugercane': 1
},
'PhantomSet': {
    'Phantom': 1,
    'Spectre': 1
},
'PlasmaSet': {
    'Plasmabeam': 1,
    'Plasmablade': 1
},
'SawSet': {
    'Saw': 1,
    'Handsaw': 1
},
'SeerSet': {
    'Blue Seer': 1,
    'Orange Seer': 1,
    'Purple Seer': 1,
    'Red Seer': 1,
    'Seer': 1,
    'Yellow Seer': 1
},
'SharkSet': {
    'Shark': 1,
    'Slasher': 1
},
'SwirlySet': {
    'SwirlyGun': 1,
    'SwirlyAxe': 1
},
'VampireSet': {
    "Vampire'sEdge": 1,
'Darkbringer': 1
},
'VintageSet': {
    'America': 1,
    'Blood': 1,
    'Cowboy': 1,
    'Ghost': 1,
    'Golden': 1,
    'Laser': 1,
    'Phaser': 1,
    'Disint': 1,
    'Shadow': 1,
    'Splitter': 1
},
'VirtualSet': {
    'Virtual': 1,
    'Blaster': 1
},
'WinterSet': {
    'Frostbite': 1,
    'Frostsaber': 1,
    "Winter'sEdge": 1,
                 'IceDragon': 1,
    'IceShard': 1,
    'Snowflake': 1
}
}


@app.route('/webhook/shopify', methods=['POST'])
def shopify_webhook():
    # Get the JSON data from the Shopify webhook
    data = request.get_json()

    # Extract the data that you need from the JSON data
    note = data.get('note')
    username = data['customer']['email'] if not note else note.split(':')[0].strip()

    # Extract the username from the note_attributes section
    note_attributes = data.get('note_attributes', [])
    for attribute in note_attributes:
        if attribute['name'] == 'username':
            username = attribute['value']
            break

    items = {}
    for item in data['line_items']:
        item_name = item['title'].replace(' ', '')
        quantity = item['quantity']
        if item_name in bundle_items:
            for bundle_item_name, bundle_item_quantity in bundle_items[item_name].items():
                bundle_item_name = bundle_item_name.replace(' ', '')
                items[bundle_item_name] = items.get(bundle_item_name, 0) + bundle_item_quantity * quantity
        else:
            items[item_name] = items.get(item_name, 0) + quantity
    robloxUser = username
    robloxUser_id = get_user_id(robloxUser)
    s = requests.session()

    s.cookies['.ROBLOSECURITY'] = cookie

    csrf = s.post('https://auth.roblox.com/v2/logout', cookies={'.ROBLOSECURITY': str(cookie)}).headers[
        'x-csrf-token']

    s.headers = headers = {
        'authority': 'friends.roblox.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9,tr;q=0.8',
        'content-type': 'application/json;charset=utf-8',
        'origin': 'https://www.roblox.com',
        'referer': 'https://www.roblox.com/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'x-csrf-token': csrf,
    }

    try:
        r = s.post(f"https://friends.roblox.com/v1/users/{robloxUser_id}/request-friendship")
        r.raise_for_status()  # Raise an error if the request was not successful
        print(f"Friend request sent to {robloxUser}")

    except requests.exceptions.RequestException as e:
        print(f"Unable to send friend request to {robloxUser}: {e}")

    # Prepare payload for Discord webhook

    message = f"{robloxUser_id}\n\n"
    for item_name, quantity in items.items():
        discord_item_name = item_name_mappings.get(item_name, item_name)
        category = item_categories.get(discord_item_name, '')
        message += f"{discord_item_name}:{quantity}:{category}\n"
    payload = {
        'username': robloxUser,
        'content': message
    }

    # Send payload to Discord webhook
    print(message)
    sendmsg(message)

    requests.post(webhook_url, json=payload)
    sleep(1)
    return {'message': 'success'}


if __name__ == '__main__':
    app.run()
