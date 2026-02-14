# ============================================
# 🚲 Smart Bike Demand Prediction System

# ============================================

import pandas as pd
import tkinter as tk
from tkinter import messagebox
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

# --------------------------------------------
# Load & Prepare Dataset
# --------------------------------------------

data = pd.read_csv("train.csv")

data['datetime'] = pd.to_datetime(data['datetime'])
data['hour'] = data['datetime'].dt.hour
data['day'] = data['datetime'].dt.day
data['month'] = data['datetime'].dt.month
data['weekday'] = data['datetime'].dt.weekday

# Use more features for better prediction
X = data[['hour','day','month','weekday',
          'temp','humidity','windspeed',
          'workingday','holiday','weather']]

y = data['count']

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Improved RandomForest
model = RandomForestRegressor(
    n_estimators=200,
    max_depth=20,
    random_state=42
)

model.fit(X_train, y_train)

# Check Accuracy
pred = model.predict(X_test)


# --------------------------------------------
# GUI Setup
# --------------------------------------------

root = tk.Tk()
root.title("Smart Bike Demand Prediction")
root.state("zoomed")

# Full screen background image
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

bg_image = Image.open("bike.jfif")
bg_image = bg_image.resize((screen_width, screen_height))
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Dark overlay
overlay = tk.Frame(root, bg="#000000")
overlay.place(relwidth=1, relheight=1)

# Card Frame
card = tk.Frame(root, bg="#1c1c1c", padx=40, pady=40)
card.place(relx=0.5, rely=0.5, anchor="center")

title = tk.Label(card,
                 text="🚲 SMART BIKE DEMAND PREDICTION",
                 font=("Segoe UI", 22, "bold"),
                 bg="#1c1c1c",
                 fg="#00ffcc")
title.grid(row=0, column=0, columnspan=2, pady=20)

# --------------------------------------------
# Input Fields
# --------------------------------------------

labels = ["Hour (0-23)",
          "Temperature (°C)",
          "Humidity (%)",
          "Wind Speed",
          "Working Day (0/1)",
          "Holiday (0/1)",
          "Weather (1=Clear,2=Cloudy,3=Rain)"]

entries = []

for i, text in enumerate(labels):
    lbl = tk.Label(card,
                   text=text,
                   font=("Segoe UI", 12),
                   bg="#1c1c1c",
                   fg="white")
    lbl.grid(row=i+1, column=0, padx=15, pady=10, sticky="w")

    entry = tk.Entry(card,
                     font=("Segoe UI", 12),
                     bg="#2c2c2c",
                     fg="white",
                     insertbackground="white",
                     width=25)
    entry.grid(row=i+1, column=1, padx=15, pady=10)
    entries.append(entry)

# --------------------------------------------
# Prediction Function
# --------------------------------------------

def predict():
    try:
        h = float(entries[0].get())
        t = float(entries[1].get())
        hum = float(entries[2].get())
        wind = float(entries[3].get())
        wd = int(entries[4].get())
        hol = int(entries[5].get())
        we = int(entries[6].get())

        # Default values for extra features
        day = 1
        month = 1
        weekday = 1

        input_data = pd.DataFrame([[h, day, month, weekday,
                                    t, hum, wind,
                                    wd, hol, we]],
                                  columns=['hour','day','month','weekday',
                                           'temp','humidity','windspeed',
                                           'workingday','holiday','weather'])

        prediction = model.predict(input_data)[0]

        result_label.config(
            text=f"🚲 Predicted Bike Count: {int(prediction)}",
            fg="#00ffcc"
        )

        # Graph
        plt.figure()
        plt.bar(["Predicted Demand"], [prediction])
        plt.title("Predicted Bike Demand")
        plt.ylabel("Bike Count")
        plt.show()

    except:
        messagebox.showerror("Error", "Please enter valid values!")

# --------------------------------------------
# Animated Hover Button
# --------------------------------------------

def on_enter(e):
    predict_btn['background'] = "#00ffcc"
    predict_btn['foreground'] = "black"
    predict_btn['font'] = ("Segoe UI", 15, "bold")

def on_leave(e):
    predict_btn['background'] = "#00bfa6"
    predict_btn['foreground'] = "white"
    predict_btn['font'] = ("Segoe UI", 14, "bold")

predict_btn = tk.Button(card,
                        text="🔍 Predict Demand",
                        font=("Segoe UI", 14, "bold"),
                        bg="#00bfa6",
                        fg="white",
                        padx=20,
                        pady=10,
                        bd=0,
                        command=predict)

predict_btn.grid(row=9, column=0, columnspan=2, pady=25)

predict_btn.bind("<Enter>", on_enter)
predict_btn.bind("<Leave>", on_leave)

# Result Label
result_label = tk.Label(card,
                        text="",
                        font=("Segoe UI", 18, "bold"),
                        bg="#1c1c1c")
result_label.grid(row=10, column=0, columnspan=2)

# Footer
footer = tk.Label(root,
                  text="Bike Demand Prediction System By Aaditi",
                  font=("Segoe UI", 11),
                  bg="#000000",
                  fg="white")
footer.pack(side="bottom", pady=10)

root.mainloop()
