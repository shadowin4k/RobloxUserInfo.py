import datetime
import sys
import requests

class Color:
    RED = "\033[91m"
    WHITE = "\033[97m"
    RESET = "\033[0m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    PURPLE = "\033[95m"

BEFORE = Color.BLUE + "["
AFTER = "]" + Color.RESET
INFO = Color.GREEN + "[INFO]" + Color.RESET
INFO_ADD = Color.YELLOW + "[DATA]" + Color.RESET
INPUT = Color.CYAN + "[INPUT]" + Color.RESET
WAIT = Color.PURPLE + "[WAIT]" + Color.RESET

def current_time():
    return datetime.datetime.now().strftime("%H:%M:%S")

def print_error(msg):
    print(Color.RED + "[ERROR] " + str(msg) + Color.RESET)
    input("Press Enter to exit...")
    sys.exit()

def continue_prompt():
    input(Color.CYAN + "\n[Press Enter to continue]" + Color.RESET)

def title(name):
    print(f"\n{Color.WHITE}==== {name} ====\n")

def choice_user_agent():
    return "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

try:
    title("Roblox User Info")

    headers = {"User-Agent": choice_user_agent()}
    print(f"\n{BEFORE + current_time() + AFTER} {INFO} Selected User-Agent: {Color.WHITE + headers['User-Agent']}")

    username_input = input(f"{BEFORE + current_time() + AFTER} {INPUT} Username -> {Color.RESET}")
    print(f"{BEFORE + current_time() + AFTER} {WAIT} Fetching user info...{Color.RESET}")

    user_data = requests.post(
        "https://users.roblox.com/v1/usernames/users",
        headers=headers,
        json={"usernames": [username_input], "excludeBannedUsers": True}
    ).json()
    
    if not user_data.get("data"):
        raise Exception("Username not found or is banned.")

    user_id = user_data['data'][0]['id']

    profile = requests.get(f"https://users.roblox.com/v1/users/{user_id}").json()

    friends = requests.get(f"https://friends.roblox.com/v1/users/{user_id}/friends/count").json().get("count", "N/A")
    followers = requests.get(f"https://friends.roblox.com/v1/users/{user_id}/followers/count").json().get("count", "N/A")
    followings = requests.get(f"https://friends.roblox.com/v1/users/{user_id}/followings/count").json().get("count", "N/A")

    avatar = requests.get(
        f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user_id}&size=420x420&format=Png&isCircular=false"
    ).json()
    avatar_url = avatar.get("data", [{}])[0].get("imageUrl", "Unavailable")

    presence_data = requests.post("https://presence.roblox.com/v1/presence/users", json={"userIds": [user_id]}).json()
    presence_code = presence_data.get("userPresences", [{}])[0].get("userPresenceType", -1)
    presence_status = {
        0: "Offline",
        1: "Online",
        2: "In Game",
        3: "In Studio"
    }.get(presence_code, "Unknown")

    print(f"""
    {INFO_ADD} Username         : {Color.WHITE}{profile.get('name', 'N/A')}{Color.RED}
    {INFO_ADD} ID               : {Color.WHITE}{profile.get('id', 'N/A')}{Color.RED}
    {INFO_ADD} Display Name     : {Color.WHITE}{profile.get('displayName', 'N/A')}{Color.RED}
    {INFO_ADD} Description      : {Color.WHITE}{profile.get('description', 'N/A')}{Color.RED}
    {INFO_ADD} Created          : {Color.WHITE}{profile.get('created', 'N/A')}{Color.RED}
    {INFO_ADD} Verified Badge   : {Color.WHITE}{profile.get('hasVerifiedBadge', 'N/A')}{Color.RED}
    {INFO_ADD} External Name    : {Color.WHITE}{profile.get('externalAppDisplayName', 'N/A')}{Color.RED}
    {INFO_ADD} Friends Count    : {Color.WHITE}{friends}{Color.RED}
    {INFO_ADD} Followers        : {Color.WHITE}{followers}{Color.RED}
    {INFO_ADD} Following        : {Color.WHITE}{followings}{Color.RED}
    {INFO_ADD} Presence Status  : {Color.WHITE}{presence_status}{Color.RED}
    {INFO_ADD} Banned           : {Color.WHITE}{profile.get('isBanned', 'N/A')}{Color.RED}
    {INFO_ADD} Avatar URL       : {Color.WHITE}{avatar_url}{Color.RED}
    """)

    continue_prompt()

except Exception as e:
    print_error(e)
