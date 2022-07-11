import pandas as pd


train_play_tennis = pd.DataFrame(
    [
        ["Sunny", "Hot", "High", "Weak", "No"],
        ["Sunny", "Hot", "High", "Strong", "No"],
        ["Overcast", "Hot", "High", "Weak", "Yes"],
        ["Rain", "Mild", "High", "Weak", "Yes"],
        ["Rain", "Cool", "Normal", "Weak", "Yes"],
        ["Rain", "Cool", "Normal", "Strong", "No"],
        ["Overcast", "Cool", "Normal", "Strong", "Yes"],
        ["Sunny", "Mild", "High", "Weak", "No"],
        ["Sunny", "Cool", "Normal", "Weak", "Yes"],
        ["Rain", "Mild", "Normal", "Weak", "Yes"],
        ["Sunny", "Mild", "Normal", "Strong", "Yes"],
        ["Overcast", "Mild", "High", "Strong", "Yes"],
        ["Overcast", "Hot", "Normal", "Weak", "Yes"],
        ["Rain", "Mild", "High", "Strong", "No"],
    ],
    columns=["Outlook", "Temperature", "Humidity", "Wind", "Play Tennis"],
)

test_play_tennis = pd.DataFrame(
    [
        ["Rain", "Mild", "Normal", "Strong", "No"],
        ["Rain", "Cool", "High", "Strong", "No"],
        ["Overcast", "Mild", "Normal", "Strong", "Yes"],
        ["Overcast", "Mild", "Normal", "Weak", "Yes"],
        ["Sunny", "Hot", "Normal", "Strong", "No"],
    ],
    columns=["Outlook", "Temperature", "Humidity", "Wind", "Play Tennis"],
)
