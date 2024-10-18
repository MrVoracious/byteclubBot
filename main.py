import discord
import firebase_admin
from firebase_admin import credentials, db
from discord.ext import commands

# Initialize Firebase
cred = credentials.Certificate("damn.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://byte-club-provisionary-members-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# Set up the bot
intents = discord.Intents.default()
intents.members = True  # This is needed to get information about members in the server
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_member_join(member):
    ref = db.reference('members')
    all_members = ref.get() 

    # Get the member's Discord ID as a string
    discord_id_str = str(member.name)
    UNVERIFIED_ROLE_NAME = 'unverified'

    print(f"Checking Firebase for Discord ID: {discord_id_str}")  # Debug print

    # Attempt to fetch the member from Firebase
    try:
        # Query the database for the member's discordID
        snapshot = ref.order_by_child('discordID').equal_to(discord_id_str).get()

        unverified_role = discord.utils.get(member.guild.roles, name=UNVERIFIED_ROLE_NAME)

        # Check if the snapshot is empty
        if snapshot:
            try:
                await member.remove_roles(unverified_role)
                print(f"Removed role from {member.name} ({member.id}) - In Firebase.")
            except discord.Forbidden:
                print(f"Failed to remove role from {member.name} ({member.id}). Insufficient permissions.")
        else:
            print(f"{member.name} ({member.id}) - Not in Firebase.")

    except Exception as e:
        print(f"An error occurred while querying Firebase: {e}")

# Run the bot
bot.run('MTI5NjkxMzY0OTIwNTY0MTMwNw.GSJmPD.p8vyGHxZTSw621P3BOQSEQBPE7Eog4swKMBoGs')  # Replace with your actual bot token
