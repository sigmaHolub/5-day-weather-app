import sys
import requests
from datetime import datetime
from collections import defaultdict
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from PyQt5.QtCore import Qt

class AppWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.UI()

    def UI(self):
        self.setWindowTitle("5 Day Weather Forecast")
        self.setMinimumSize(400, 500)

        self.top_label = QLabel("5 Day Weather Forecast")
        self.top_label.setAlignment(Qt.AlignCenter)

        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Enter a city")
        self.city_input.setAlignment(Qt.AlignCenter)

        self.get_weather_button = QPushButton("Get Weather")
        self.get_weather_button.clicked.connect(self.get_weather)

        self.forecast_text = QTextEdit()
        self.forecast_text.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.top_label)
        layout.addWidget(self.city_input)
        layout.addWidget(self.get_weather_button)
        layout.addWidget(self.forecast_text)
        self.setLayout(layout)

        self.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                font-size: 20px;
            }
            QLabel {
                font-size: 35px;
            }
            QPushButton {
                font-size: 15px;
                color: white;
                font-weight: bold;
                background-color: #0362fc;
                padding: 10px;
            }
            QTextEdit {
                font-size: 18px;
                padding: 10px;
                font-family: Segoe UI emoji
            }
        """)

    def get_weather(self):
        api_key = "1ea382e3611722e26fee01163e5384a2"
        city = self.city_input.text().strip()
        if not city:
            self.display_error("Please enter a city name")
            return

        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if str(data.get("cod")) == "200":
                self.display_weather(data)
            else:
                self.display_error(f"API Error: {data.get('message')}")

        except requests.exceptions.HTTPError:
            self.display_error("HTTP Error: Invalid input")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error: Check your internet")

        except requests.exceptions.Timeout:
            self.display_error("Request timed out")

        except requests.RequestException as error:
            self.display_error(f"Request error: {error}")

    def display_error(self, error_message):
        self.forecast_text.setText(f"ERROR:\n{error_message}")

    def display_weather(self, data):
        grouped = defaultdict(list)

        for entry in data["list"]:
            dt = datetime.fromtimestamp(entry["dt"])
            date_str = dt.strftime("%Y-%m-%d")
            grouped[date_str].append(entry)

        output = ""

        for i, (date, entries) in enumerate(grouped.items()):
            if i >= 5: 
                break

            forecast = entries[len(entries) // 2] if len(entries) >= 5 else entries[0]

            temp = forecast["main"]["temp"]
            weather = forecast["weather"][0]
            weather_id = weather["id"]
            description = weather["description"].capitalize()
            emoji = self.get_weather_emoji(weather_id)

            output += f"{date}\n{emoji} {description}, {temp:.1f}°C\n\n"

        self.forecast_text.setText(output.strip())

    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "🌩"
        elif 300 <= weather_id <= 321:
            return "🌦"
        elif 500 <= weather_id <= 531:
            return "🌧"
        elif 600 <= weather_id <= 622:
            return "🌨"
        elif 701 <= weather_id <= 741:
            return "🌫"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪"
        elif weather_id == 800:
            return "☀"
        elif 801 <= weather_id <= 804:
            return "☁"
        else:
            return "❓"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show()
    sys.exit(app.exec_())