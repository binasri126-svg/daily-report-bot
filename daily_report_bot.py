
from datetime import datetime
from pathlib import Path
import time

import pyautogui
import pyperclip

# Safety settings
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 1

# Project folder
PROJECT_FOLDER = Path(__file__).resolve().parent

CITY = "Chennai"
WEATHER_WEBSITE = f"https://wttr.in/{CITY}?format=3"


def get_weather():
    print("Opening Chrome...")

    # Open Chrome
    pyautogui.hotkey("win", "r")
    time.sleep(1)
    pyperclip.copy("chrome")
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("enter")
    time.sleep(5)

    # Open weather website
    pyautogui.hotkey("ctrl", "l")
    pyperclip.copy(WEATHER_WEBSITE)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("enter")
    time.sleep(8)

    # Copy weather information
    pyautogui.hotkey("ctrl", "a")
    pyautogui.hotkey("ctrl", "c")
    time.sleep(2)

    weather_text = pyperclip.paste().strip()

    if not weather_text:
        raise RuntimeError("Weather information not found.")

    weather = next(
        (line.strip() for line in weather_text.splitlines() if line.strip()),
        ""
    )

    print("Weather:", weather)
    return weather


def create_report(weather):
    now = datetime.now()

    date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    date = now.strftime("%Y-%m-%d")

    excel_file = PROJECT_FOLDER / f"daily_report_{date}.xlsx"
    screenshot_file = PROJECT_FOLDER / f"daily_report_screenshot_{date}.png"

    # Remove previous files with today's date
    if excel_file.exists():
        excel_file.unlink()

    if screenshot_file.exists():
        screenshot_file.unlink()

    print("Opening Excel...")

    # Open Excel
    pyautogui.hotkey("win", "r")
    time.sleep(1)
    pyperclip.copy("excel")
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("enter")
    time.sleep(10)

    # Create a new workbook
    pyautogui.hotkey("ctrl", "n")
    time.sleep(4)

    # Enter report details
    comment = "Weather update for daily planning."

    report_data = (
        "Date & Time\tFetched Information\tComment\n"
        f"{date_time}\t{weather}\t{comment}"
    )

    pyautogui.moveTo(55, 150, duration=0.4)
    pyautogui.click()

    pyperclip.copy(report_data)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(3)

    # Save Excel file
    print("Saving Excel report...")

    pyautogui.press("f12")
    time.sleep(3)

    pyperclip.copy(str(excel_file))
    pyautogui.hotkey("ctrl", "a")
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("enter")
    time.sleep(5)

    pyautogui.press("enter")
    time.sleep(2)

    # Take screenshot
    pyautogui.screenshot().save(str(screenshot_file))

    print("Report completed!")
    print("Excel file:", excel_file)
    print("Screenshot:", screenshot_file)


def main():
    print("Daily Report Bot Started")
    time.sleep(3)

    try:
        weather = get_weather()
        create_report(weather)

    except Exception as error:
        print("Error:", error)


if __name__ == "__main__":
    main()
