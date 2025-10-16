import os
import requests
import random
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import datetime

#-----CONFIG----

# --- Use GitHub Secrets for safety ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
#---MY THOUGHTS ----

thoughts = [
    "Endings be damned — build, learn, iterate, repeat.",
    "In the planning room it is democracy. In the workspace it is dictatorship... speak now or forever hold peace until the next version.",
    "I want to be the best — not just in Malawi, not just in Africa, but in the world.",
    "won’t slow down. I will push hard and improve relentlessly. You can either catch up or cease to exist.",
    "It only takes 10 minutes to learn something new. Start — the momentum will carry you",
    "Fine-tune what exists instead of building from scratch. Build on giants",
    "Discuss ideas freely, then execute ruthlessly. Speak now, or forever hold peace until the next version.",
    "Build in public, share ideas, attract attention. Visibility is power.",
    "People lie to beg, but I choose to see the truth: need is real. Help where you can.",
    "Originality is dangerous and often unnecessary. Smart is building on what works",
    "Consistency and discipline beat motivation",
    "Every challenge is a chance to raise the bar, for myself and for others.",
    "Post, observe, strike. Presence is bait, engagement is the target, hesitation is the enemy.",
    "Build, share, repeat. Consistent attention is magnetic. Strike while they’re curious—don’t wait for permission",
    "Every library, every tool someone shared is a gift. Stand on it, don’t rebuild it.",
    "Value > originality. Solve problems, remix, improve, repeat.",
    "Open-source isn’t copy, it’s fuel. Use it to sprint further than others.",
    "Don’t mourn similar ideas — see them as a launchpad, not a threat.",
    "Build on giants — free what exists, tweak what matters, add what’s only yours."
]

# --- IMAGE CREATION FUNCTION ---

selected_thoughts = random.sample(thoughts, 2)

def create_thought_image(text):

    #create base Image
    img = Image.new('RGB', (800, 400), color=(25,25,25))
    draw = ImageDraw.Draw(img)

    #Load a nice readable font
    try:
        font = ImageFont.truetype("arial.ttf", 28)
    except:
        font = ImageFont.truetype("DejaVuSans.ttf", 28)


    #wrap text manually
    lines = []
    words = text.split(' ')
    line = ''

    for word in words:
        if draw.textlength(line + word, font=font) < 700:
            line += word + ' '
        else:
            lines.append(line)
            line = word + ' '
    lines.append(line)

    #calculating text height
    y_text = (400 - (len(lines) * 35)) // 2
    for line in lines:
        text_width = draw.textlength(line, font=font)
        x_text = (800 - text_width) // 2
        draw.text((x_text, y_text), line, font = font, fill=(255,255,255))
        y_text += 35

    # Save image to memory
    bio = BytesIO()
    img.save(bio, format = 'PNG')
    bio.seek(0)
    return bio

#--- SEND FUNCTION---

def send_thought():
    thought = random.choice(thoughts)
    img_data = create_thought_image(thought)
    files = {'photo': img_data}
    data = {'chat_id':CHAT_ID}

    try:
        resp = requests.post(BASE_URL + '/sendPhoto', data = data, files = files, timeout =10)
        resp.raise_for_status()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{now} ✅ Sent thought: {thought}]")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error sending thought: {e}")

# ---MAIN RUN ---
if __name__ == "__main__":
    send_thought()
