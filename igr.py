import time
import random
import pytz
from datetime import datetime, timedelta
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ClientError
import openai

# Configuration
OPENAI_API_KEY = "your_openai_key"
INSTA_USERNAME = "your_username"
INSTA_PASSWORD = "your_password"
TARGET_ACCOUNT = "target_account"
MOROCCO_TZ = pytz.timezone('Africa/Casablanca')

# Human-like behavior settings
ACTIVE_HOURS = (9, 21)  # 9 AM - 9 PM Morocco time
HUMAN_TYPING_DELAY = (1, 3)  # Seconds to simulate typing
ACTION_VARIABILITY = {  # Random action probabilities
    'scroll': 0.3,
    'like': 0.2,
    'profile_view': 0.1
}

# Initialize clients
cl = Client()
openai.api_key = OPENAI_API_KEY

def generate_friendly_message():
    """Generate unique message using OpenAI with Moroccan cultural context"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "system",
                "content": "Generate a friendly Instagram DM in Moroccan dialect or French. "
                           "Suggest following @kibrille.ma casually. Keep it under 200 characters. "
                           "Use emojis. Avoid spammy language."
            }]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI Error: {e}")
        return random.choice([
            "Salut! Check @kibrille.ma pour des contenus géniaux 😍",
            "Hey! @kibrille.ma a des posts super cool, jette un œil! 👀",
            "Coucou! Tu as vu le compte @kibrille.ma? Vraiment intéressant! 👍"
        ])

def human_delay(action_type='message'):
    """Simulate human-like delays with variability"""
    base_delay = random.uniform(*HUMAN_TYPING_DELAY) if action_type == 'message' else 0
    variability = random.choice([
        random.uniform(0.5, 2),
        random.uniform(2, 5),
        0 if random.random() < 0.2 else 1  # 20% chance of no extra delay
    ])
    time.sleep(base_delay + variability)

def in_active_hours():
    """Check if current time is within Morocco active hours"""
    now = datetime.now(MOROCCO_TZ)
    return ACTIVE_HOURS[0] <= now.hour < ACTIVE_HOURS[1]

def simulate_human_activity():
    """Random social media actions pattern"""
    if random.random() < ACTION_VARIABILITY['scroll']:
        human_delay('scroll')
    if random.random() < ACTION_VARIABILITY['like']:
        human_delay('like')
    if random.random() < ACTION_VARIABILITY['profile_view']:
        human_delay('profile_view')

def instagram_bot():
    # Time zone check
    if not in_active_hours():
        print("Not in Morocco active hours (9AM-9PM). Aborting.")
        return

    # Login with human-like pattern
    try:
        human_delay('login')
        cl.login(INSTA_USERNAME, INSTA_PASSWORD)
        print("Login successful!")
    except LoginRequired as e:
        print(f"Login failed: {e}")
        return

    # Follow target account with human pattern
    try:
        simulate_human_activity()
        user_id = cl.user_id_from_username(TARGET_ACCOUNT)
        cl.user_follow(user_id)
        print(f"Followed {TARGET_ACCOUNT} successfully!")
        human_delay('follow')
    except ClientError as e:
        print(f"Error following account: {e}")
        return

    # Get followers with randomization
    try:
        followers = list(cl.user_followers(cl.user_id).values()
        random.shuffle(followers)
        print(f"Found {len(followers)} followers")
        human_delay('load_followers')
    except ClientError as e:
        print(f"Error getting followers: {e}")
        return

    # Messaging loop
    max_messages = random.randint(30, 95)
    sent = 0
    
    for follower in followers:
        if sent >= max_messages or not in_active_hours():
            break

        try:
            # Generate unique message
            message = generate_friendly_message()
            
            # Human-like sending pattern
            simulate_human_activity()
            cl.direct_send(text=message, user_ids=[follower.pk])
            
            sent += 1
            print(f"Sent message {sent}/{max_messages} to {follower.username}")
            print(f"Message: {message}")
            
            # Variable delay with safety limits
            delay = random.randint(45, 180) + random.random()*30
            time.sleep(delay)
            
            # Periodic long break
            if sent % 15 == 0:
                time.sleep(random.randint(300, 600))  # 5-10 minute break
                
        except Exception as e:
            print(f"Error: {str(e)[:100]}")

    print(f"Completed! Sent {sent} messages today.")

if __name__ == "__main__":
    instagram_bot()
