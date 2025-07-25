import requests
import os
import json
import time
import subprocess
from urllib.parse import quote
from base64 import b64encode

CLIENT_ID = '34a02cf8f4414e29b15921876da36f9a'
CLIENT_SECRET = 'daafbccc737745039dffe53d94fc76cf'
WEBHOOK_URL = os.getenv("WEBHOOK_URL") # .env
# WEBHOOK_URL = os.environ['WEBHOOK_URL'] # replit

URLS = {
    'Android': '5cb97847cee34581afdbc445400e2f77/app/FortniteContentBuilds',
    'Android Shipping': '4fe75bbc5a674f4f9b356b5c90567da5/app/Fortnite',
    'IOS': '5cb97847cee34581afdbc445400e2f77/app/FortniteContentBuilds',
    'Windows': '4fe75bbc5a674f4f9b356b5c90567da5/app/Fortnite',
    'Windows Content': '5cb97847cee34581afdbc445400e2f77/app/FortniteContentBuilds',
    # 'Windows UEFN': '1e8bda5cfbb641b9a9aea8bd62285f73/app/Fortnite_Studio',
    'Switch': '5cb97847cee34581afdbc445400e2f77/app/FortniteContentBuilds',
    'Switch2': '5cb97847cee34581afdbc445400e2f77/app/FortniteContentBuilds',
    'PS4': '5cb97847cee34581afdbc445400e2f77/app/FortniteContentBuilds',
    'PS5': '5cb97847cee34581afdbc445400e2f77/app/FortniteContentBuilds',
    'XB1': '5cb97847cee34581afdbc445400e2f77/app/FortniteContentBuilds',
    'XSX': '5cb97847cee34581afdbc445400e2f77/app/FortniteContentBuilds',
}

PLATFORM_COLORS = {
    "Windows": 0x0078D7,
    "Windows Content": 0x0078D7,
    "UEFN": 0x0078D7,
    "Android": 0x00C853,
    "Android Apk": 0x00C853,
    "IOS": 0x999999,
    "Switch": 0xE60012,
    "Switch2": 0xE60012,
    "PS4": 0x003791,
    "PS5": 0x0A0A0A,
    "Xbox One": 0x107C10,
    "Xbox Series X/S": 0x107C10,
}

PLATFORM_ICON_URL = {
    "Windows": "https://github.com/Th3DryZ69/Discord-Webhook-Manifest-Fortnite/raw/main/.github/icon/windows.png",
    "Windows Content": "https://github.com/Th3DryZ69/Discord-Webhook-Manifest-Fortnite/raw/main/.github/icon/windows.png",
    "UEFN": "https://github.com/Th3DryZ69/Discord-Webhook-Manifest-Fortnite/raw/main/.github/icon/uefn.png",
    "Android": "https://github.com/Th3DryZ69/Discord-Webhook-Manifest-Fortnite/raw/main/.github/icon/android.png",
    "Android Apk": "https://github.com/Th3DryZ69/Discord-Webhook-Manifest-Fortnite/raw/main/.github/icon/android.png",
    "IOS": "https://github.com/Th3DryZ69/Discord-Webhook-Manifest-Fortnite/raw/main/.github/icon/ios.png",
    "Switch": "https://github.com/Th3DryZ69/Discord-Webhook-Manifest-Fortnite/raw/main/.github/icon/switch.png",
    "Switch2": "https://github.com/Th3DryZ69/Discord-Webhook-Manifest-Fortnite/raw/main/.github/icon/switch.png",
    "PS4": "https://github.com/Th3DryZ69/Discord-Webhook-Manifest-Fortnite/raw/main/.github/icon/ps4.png",
    "PS5": "https://github.com/Th3DryZ69/Discord-Webhook-Manifest-Fortnite/raw/main/.github/icon/ps5.png",
    "Xbox One": "https://github.com/Th3DryZ69/Discord-Webhook-Manifest-Fortnite/raw/main/.github/icon/xbox.png",
    "Xbox Series X/S": "https://github.com/Th3DryZ69/Discord-Webhook-Manifest-Fortnite/raw/main/.github/icon/xboxs.png",
}

# PLATFORM_EMOJIS = {
#     "Windows": "<:windows:1377998819941286049>",
#     "Windows Content": "<:windows:1377998819941286049>",
#     "Android": "<:android:1377998429493657611>",
#     "Android Shipping": "<:android:1377998429493657611>",
#     "IOS": "<:ios:1377996922907791391>",
#     "Switch": "<:switch:1377998371658399974>",
#     "Switch2": "<:switch:1377998371658399974>",
#     "PS4": "<:ps4:1377998418370232370>",
#     "PS5": "<:ps5:1377998403706818691>",
#     "XB1": "<:xbox:1377998397633724526>",
#     "XSX": "<:xboxs:1378000249909542913>",
# }

ANDROID_BODY = {
    "abis": ["arm64-v8a", "armeabi-v7a", "armeabi"],
    "apiLevel": 30,
    "coreCount": 8,
    "hardwareName": "Qualcomm Technologies, Inc SDMMAGPIE",
    "hasLibHoudini": False,
    "machineId": "REDACTED",
    "manufacturer": "samsung",
    "memoryMiB": 5524,
    "model": "SM-A715F",
    "platform": "Android",
    "preInstallInfo": "ThirdPartyInstall",
    "renderingDevice": "Adreno (TM) 618",
    "renderingDriver": "OpenGL ES 3.2 V@0502.0",
    "sha1Fingerprint": "",
    "supportsArmNEON": True,
    "supportsFpRenderTargets": True,
    "textureCompressionFormats": ["ASTC", "ATC", "ETC2", "ETC1"],
    "version": "5.2.0"
}

VERSIONS_FILE = os.path.join(os.path.dirname(__file__), "latest.json")

def load_known_versions():
    if os.path.isfile(VERSIONS_FILE):
        try:
            with open(VERSIONS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_known_versions(known_versions):
    try:
        with open(VERSIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(known_versions, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(e)

def get_access_token():
    try:
        auth = b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
        resp = requests.post(
            "https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/token",
            data={
                "grant_type": "client_credentials",
                "token_token": "eg1",
                "scope": "launcher:download:live:* READ"
            },
            headers={
                "Authorization": f"Basic {auth}",
                "Content-Type": "application/x-www-form-urlencoded"
            }
        )
        resp.raise_for_status()
        return resp.json()['access_token']
    except requests.RequestException as e:
        print(f"Error token: {e}")
        return None

def get_manifest(logical_platform, token):
    platform = (
        "Android" if logical_platform.startswith("Android") else
        "Windows" if logical_platform.startswith("Windows") else
        logical_platform
    )
    url = (
        f"https://launcher-public-service-prod06.ol.epicgames.com/"
        f"launcher/api/public/assets/v2/platform/{platform}/namespace/"
        f"fn/catalogItem/{URLS[logical_platform]}/label/Live"
    )
    headers = {"Authorization": f"Bearer {token}"}
    try:
        if logical_platform == "Android Shipping":
            headers["Content-Type"] = "application/json"
            resp = requests.post(url, headers=headers, json=ANDROID_BODY)
        else:
            resp = requests.get(url, headers=headers)

        if resp.status_code == 401:
            return "REFRESH_TOKEN"
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        print(f"Error for {logical_platform}: {e}")
        return None

def download_and_push_manifest(manifest_url, platform, manifest_id, version):
    if platform == "Android":
        folder = "manifests/Mobiles/Android"
    elif platform == "Android Shipping":
        folder = "manifests/Mobiles/Android/Shipping"
    elif platform == "IOS":
        folder = "manifests/Mobiles/IOS"
    elif platform == "Windows":
        folder = "manifests/PC/Windows"
    elif platform == "Windows Content":
        folder = "manifests/PC/Windows/Content"
    elif platform == "Windows UEFN":
        folder = "manifests/PC/UEFN"
    elif platform == "Switch":
        folder = "manifests/Consoles/Switch"
    elif platform == "Switch2":
        folder = "manifests/Consoles/Switch2"
    elif platform == "PS4":
        folder = "manifests/Consoles/PS4"
    elif platform == "PS5":
        folder = "manifests/Consoles/PS5"
    elif platform == "XSX":
        folder = "manifests/Consoles/XBoxSeriesX"
    elif platform == "XB1":
        folder = "manifests/Consoles/XBoxOne"
    else:
        print(f"Unsupported platform for manifest download: {platform}")
    os.makedirs(folder, exist_ok=True)
    filename = f"{version}.manifest"
    filepath = os.path.join(folder, filename)

    response = requests.get(manifest_url)
    if response.status_code == 200:
        if not os.path.exists(filepath):
            with open(filepath, 'wb') as f:
                f.write(response.content)
            subprocess.run(["git", "add", filepath])
            subprocess.run(["git", "commit", "-m", f"Add {platform} manifest for version {version} ({manifest_id})"])
            subprocess.run(["git", "push"])
        else:
            print(f"The file '{filepath}' already exists. No downloads have been performed.")

        github_path = f"{folder}/{filename}"
        github_url = f"https://github.com/Th3DryZ69/Discord-Webhook-Manifest-Fortnite/raw/main/{quote(github_path)}"

        return github_url
    else:
        print(f"Error downloading manifest: {response.status_code}")
        return manifest_url

def send_discord_embed(platform, version, manifest_url, manifest_id, manifest_hash):
    color = PLATFORM_COLORS.get(platform, 0xFFFFFF)
    # emoji = PLATFORM_EMOJIS.get(platform, "📦")

    github_url = download_and_push_manifest(manifest_url, platform, manifest_id, version)
    manifest_value = f"[{manifest_id}]({github_url})"
    # manifest_value = f"[{manifest_id}]({manifest_url})"

    if platform == "Windows UEFN":
        platform = "UEFN"
    elif platform == "XSX":
        platform = "Xbox Series X/S"
    elif platform == "XB1":
        platform = "Xbox One"
    elif platform == "Android Shipping":
        platform = "Android Apk"

    embed = {
        # "title": f"{emoji} {platform} Fortnite Update",
        "author": {"name": f"{platform} Fortnite Update", "icon_url": PLATFORM_ICON_URL.get(platform, "")},
        "color": color,
        "fields": [
            {"name": "Build Version", "value": version, "inline": True},
            {"name": f"Manifest ID", "value": manifest_value, "inline": False},
            {"name": f"File Hash", "value": manifest_hash, "inline": False}
        ]
    }

    payload = {"embeds": [embed]}
    try:
        requests.post(WEBHOOK_URL, json=payload).raise_for_status()
    except Exception as e:
        print(e)

def watch_manifests():
    token = get_access_token()
    if not token:
        return

    known_versions = load_known_versions()
    platforms = list(URLS.keys())

    while True:
        for platform in platforms:
            data = get_manifest(platform, token)

            if data == "REFRESH_TOKEN":
                token = get_access_token()
                data = get_manifest(platform, token)
                if not data or data == "REFRESH_TOKEN":
                    continue

            if not data:
                continue

            elem = data.get('elements', [{}])[0]
            version = elem.get('buildVersion', 'unknown_version')
            manifests = elem.get('manifests', [])
            if not manifests:
                continue

            m = manifests[1] if len(manifests) > 1 else manifests[0]
            path = m.get('uri')
            q = m.get('queryParams', [{}])[0]
            manifest_url = f"{path}?{q.get('name')}={q.get('value')}"
            manifest_id = path.split("/")[-1].replace(".manifest", "")
            manifest_hash = elem.get('hash')

            if known_versions.get(platform) != version:
                known_versions[platform] = version
                save_known_versions(known_versions)
                send_discord_embed(platform, version, manifest_url, manifest_id, manifest_hash)

        time.sleep(150) # > 2.5 minutes

if __name__ == "__main__":
    watch_manifests()
