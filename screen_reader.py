import cv2
import numpy as np
import pyautogui
import pytesseract
from PIL import Image
from pynput import mouse

# Line exclusive to Windows, remove if not running on Windows
pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR/tesseract.exe'

# Function to capture a screenshot of a specified area
def capture_screenshot(top_left, bottom_right):
    screenshot = pyautogui.screenshot(region=(top_left[0], top_left[1], bottom_right[0] - top_left[0], bottom_right[1] - top_left[1]))
    return screenshot

# Function to perform OCR on the captured screenshot
def ocr_image(screenshot):
    # Convert the screenshot to a NumPy array
    screenshot_np = np.array(screenshot)

    # Convert the screenshot to grayscale
    grayscale_image = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2GRAY)

    # Invert the colors (create a negative image)
    inverted_image = cv2.bitwise_not(grayscale_image)

    # Save the inverted image as a temporary image file
    cv2.imwrite("inverted_screenshot.png", inverted_image)

    # Read text from the inverted image using Tesseract OCR
    text = pytesseract.image_to_string(Image.open("inverted_screenshot.png"))

    return text

top_left = None
bottom_right = None

# Callback function to handle mouse clicks
def on_click(x, y, button, pressed):
    global top_left, bottom_right
    if pressed:
        if top_left is None:
            top_left = (x, y)
            print("Top-left corner set to:", top_left)
            return False
        elif bottom_right is None:
            bottom_right = (x, y)
            print("Bottom-right corner set to:", bottom_right)
            return False



def get_text():
  """
  Prompts the user to select the bounding box for the text, then returns the text.
  """
  # Listen for mouse clicks
  global top_left, bottom_right
  print("Please click on the top-left corner of the screen area to capture.")
  with mouse.Listener(on_click=on_click) as listener:
      listener.join()

  print("Please click on the bottom-right corner of the screen area to capture.")
  with mouse.Listener(on_click=on_click) as listener:
      listener.join()

  try:
      screenshot = capture_screenshot(top_left, bottom_right)
      top_left = None
      bottom_right = None
      text = ocr_image(screenshot)

      print("\nText in the specified area:")
      print(text)
      return text
  except Exception as e:
      print("An error occurred:", str(e))