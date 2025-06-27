import requests
import os
import json
import time
from base64 import b64encode
from dotenv import load_dotenv
import webbrowser

load_dotenv()

LAUNCHER_CLIENT_ID = '34a02cf8f4414e29b15921876da36f9a'
LAUNCHER_CLIENT_SECRET = 'daafbccc737745039dffe53d94fc76cf'
ANDROID_CLIENT_ID = '3f69e56c7649492c8cc29f1af08a8a12'
ANDROID_CLIENT_SECRET = 'b51ee9cb12234f50a69efa67ef53812e'
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")
DEVICE_ID = os.getenv("DEVICE_ID")
SECRET_ID = os.getenv("SECRET_ID")
VERSIONS_FILE = os.path.join(os.path.dirname(__file__), "latest.json")

URLS = {
    'Android': '5cb97847cee34581afdbc445400e2f77/app/FortniteContentBuilds',
    'Android Shipping': '4fe75bbc5a674f4f9b356b5c90567da5/app/Fortnite',
    'IOS': '5cb97847cee34581afdbc445400e2f77/app/FortniteContentBuilds',
    'Windows': '4fe75bbc5a674f4f9b356b5c90567da5/app/Fortnite',
    'Windows Content': '5cb97847cee34581afdbc445400e2f77/app/FortniteContentBuilds',
    'Windows UEFN': '1e8bda5cfbb641b9a9aea8bd62285f73/app/Fortnite_Studio',
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
    "Windows UEFN": 0x0078D7,
    "Android": 0x00C853,
    "Android Shipping": 0x00C853,
    "IOS": 0x999999,
    "Switch": 0xE60012,
    "Switch2": 0xE60012,
    "PS4": 0x003791,
    "PS5": 0x0A0A0A,
    "XB1": 0x107C10,
    "XSX": 0x107C10,
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

def getAccesToken(accoutId, deviceId, secret):
    try:
        auth = b64encode(f"{ANDROID_CLIENT_ID}:{ANDROID_CLIENT_SECRET}".encode()).decode()
        resp = requests.post(
            "https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/token",
            data={
                "grant_type": "device_auth",
                "account_id": accoutId,
                "device_id": deviceId,
                "secret": secret,
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

def getExchangeToken(token):
    try:
        resp = requests.get(
            "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/exchange?consumingClientId=34a02cf8f4414e29b15921876da36f9a",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/x-www-form-urlencoded"
            }
        )
        resp.raise_for_status()
        return resp.json()['code']
    except requests.RequestException as e:
        print(f"Error token: {e}")
        return None

def getLauncherToken(code):
    try:
        auth = b64encode(f"{LAUNCHER_CLIENT_ID}:{LAUNCHER_CLIENT_SECRET}".encode()).decode()
        resp = requests.post(
            "https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/token",
            data={
                "grant_type": "exchange_code",
                "exchange_code": code
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

def send_discord_embed(platform, version, manifest_id, manifest_hash):
    color = PLATFORM_COLORS.get(platform, 0xFFFFFF)

    if platform == "Windows UEFN":
        platform = "UEFN"
    elif platform == "XSX":
        platform = "Xbox Series X/S"
    elif platform == "XB1":
        platform = "Xbox One"
    elif platform == "Android Shipping":
        platform = "Android Apk"

    embed = {
        "author": {
            "name": f"{platform} Fortnite Update",
            "icon_url": PLATFORM_ICON_URL.get(platform, "")
        },
        "color": color,
        "fields": [
            {"name": "Build Version", "value": version, "inline": False},
            {"name": "Manifest ID", "value": manifest_id, "inline": False},
            {"name": "File Hash", "value": manifest_hash, "inline": False}
        ]
    }

    try:
        requests.post(WEBHOOK_URL, json={"embeds": [embed]}).raise_for_status()
    except Exception as e:
        print(f"Erreur envoi embed : {e}")

def watch_manifests():
    token = getAccesToken(ACCOUNT_ID, DEVICE_ID, SECRET_ID)
    tokenExchange = getExchangeToken(token)
    tokenLauncher = getLauncherToken(tokenExchange)

    known_versions = load_known_versions()
    platforms = list(URLS.keys())

    while True:
        for platform in platforms:
            data = get_manifest(platform, tokenLauncher)

            if data == "REFRESH_TOKEN":
                token = getAccesToken(ACCOUNT_ID, DEVICE_ID, SECRET_ID)
                tokenExchange = getExchangeToken(token)
                tokenLauncher = getLauncherToken(tokenExchange)
                data = get_manifest(platform, tokenLauncher)
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
            manifest_id = path.split("/")[-1].replace(".manifest", "")
            manifest_hash = elem.get('hash')

            if known_versions.get(platform) != version:
                known_versions[platform] = version
                save_known_versions(known_versions)
                send_discord_embed(platform, version, manifest_id, manifest_hash)

        time.sleep(300)

if __name__ == "__main__":
    watch_manifests()