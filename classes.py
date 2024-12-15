# sudo apt-get install -y build-essential python3-dev python3-pillow python3-numpy
# git clone https://github.com/hzeller/rpi-rgb-led-matrix.git
# cd rpi-rgb-led-matrix
# sudo make install-python




import requests
from datetime import datetime, timezone
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw, ImageFont

# Define the base URL and parameters
BASE_URL = "https://api.momence.com/api/v1/Events"
PARAMS = {
    "hostId": 40143,  # Your Host ID
    "token": "77fc18f720"  # Your API token
}

# LED Matrix setup
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
matrix = RGBMatrix(options=options)

# Fetch the events
response = requests.get(BASE_URL, params=PARAMS)

# Check if the request was successful
if response.status_code == 200:
    events_data = response.json()  # Parse the JSON response

    # Get the current time as an offset-aware datetime in UTC
    now = datetime.now(timezone.utc)

    # Create an image to draw on
    font = ImageFont.truetype("arial.ttf", 10)  # Update font path if needed
    image = Image.new("RGB", (64, 32))  # Canvas for the matrix
    draw = ImageDraw.Draw(image)

    y = 0  # Start drawing at the top of the screen

    # Loop through the events
    for event in events_data:
        title = event.get("title", "Untitled Event")
        teacher = event.get("teacher", "Unknown Teacher")
        date_time_str = event.get("dateTime", None)
        capacity = event.get("capacity", "No capacity info")
        tickets_sold = event.get("ticketsSold", "No tickets sold info")

        if date_time_str:
            # Parse the dateTime string into a timezone-aware datetime object
            event_date_time = datetime.fromisoformat(date_time_str.replace("Z", "+00:00"))

            # Only show events in the future
            if event_date_time > now:
                # Format the date and time for better readability
                formatted_date_time = event_date_time.strftime("%a, %b %d %I:%M %p")

                # Add event information to the image
                draw.text((0, y), f"{title}", fill=(255, 255, 255), font=font)
                y += 10
                draw.text((0, y), f"{formatted_date_time} | {tickets_sold}/{capacity}", fill=(0, 255, 0), font=font)
                y += 10
                draw.text((0, y), f"Teacher: {teacher}", fill=(0, 0, 255), font=font)
                y += 10

                # If there are no more lines of space, break
                if y > 32 - 10:
                    break

    # Display the image on the LED matrix
    matrix.SetImage(image)
else:
    print(f"Error {response.status_code}: {response.text}")
