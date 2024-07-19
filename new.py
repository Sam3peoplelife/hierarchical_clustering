import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random

data1 = pd.read_csv('data1.csv')

#Створення вікна
window = tk.Tk()

#Назва та розмір вікна
window.title('Ціни на Нерухомість')
window.geometry("450x450")

def FindColum(city, SelectedType):
    if SelectedType != "Усі":
        matching_column = [column for column in data1 if city in column and SelectedType in column]
    else:
        matching_column = [column for column in data1 if city in column]
    return matching_column

def MainSelectionFunction():
    city = combo1.get()
    SelectedType = combo2.get()
    SelectedPlot = combo3.get()
    matching_column = FindColum(city, SelectedType)
    for i in matching_column:
        if SelectedPlot == "Звичайний графік":
            plot_histogram(i)
        elif SelectedPlot == "Графік змін цін":
            plot_price_differences(i)
        elif SelectedPlot == "Екстраполяції та Апроксимації":
            exstra_aprox(i)
        else:
            j = random.choice(data1.columns)
            linear_regression(i,j)


#Побудова гістограми звичайного росту цін
def plot_histogram(label):
    plt.figure(figsize=(12, 6))
    months = data1['Місяць']
    column_name = label
    plt.bar(months, data1[column_name], color='b', alpha=0.7)
    plt.title(label)
    plt.xlabel('Місяць')
    plt.ylabel('Ціна (грн)')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

#Рахуємо і робимо графік різниці цін
def calculate_price_differences(price_column):
    price_differences = []
    months = data1['Місяць']
    prices = data1[price_column]
    for i in range(1, len(prices)):
        price_difference = prices[i] - prices[i - 1]
        price_differences.append(price_difference)
    return months[1:], price_differences

def plot_price_differences(label):
    months, price_differences = calculate_price_differences(label)
    plt.figure(figsize=(12, 6))
    plt.plot(months, price_differences, marker='o', linestyle='-', color='b')
    plt.title(f'Різниця цін для {label}')
    plt.xlabel('Місяць')
    plt.ylabel('Різниця цін')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def exstra_aprox(label):
    x = np.arange(1, 27)
    y = data1[label].values
    # Побудова матриці X
    X = np.vstack([np.array(x) ** 2, x, np.ones(len(x))]).T
    # Обчислення коефіцієнтів a, b, c за методом найменших квадратів
    a, b, c = np.linalg.lstsq(X, y, rcond=None)[0]
    # Побудова апроксимаційної кривої
    x_vals = np.linspace(min(x), max(x), 100)
    y_approx = a * x_vals ** 2 + b * x_vals + c
    # Екстраполяція за допомогою функції апроксимації
    extrapolation_x = np.array([27, 28, 29, 30])
    extrapolation_y = a * extrapolation_x ** 2 + b * extrapolation_x + c
    # Побудова графіку
    plt.figure(figsize=(10, 8))
    plt.scatter(x, y, label='Дані')
    plt.plot(x_vals, y_approx, 'r', label='Апроксимація')
    plt.scatter(extrapolation_x, extrapolation_y, color='g', label='Екстраполяція')
    plt.xlabel('Місяць')
    plt.ylabel({label})
    plt.title('Екстраполяція та Апроксимація')
    plt.legend()
    plt.grid(True)
    coefficients_text = f'a: {a}, b: {b}, c: {c}'
    plt.text(0.5, -0.1, coefficients_text, transform=plt.gca().transAxes, fontsize=12, ha='center')
    plt.show()

def linear_regression(label,label2):
    x = data1[label].values
    y = data1[label2].values
    mean_x = np.mean(x)
    mean_y = np.mean(y)
    m = np.sum((x - mean_x) * (y - mean_y)) / np.sum((x - mean_x) ** 2)
    b = mean_y - m * mean_x
    y_pred = m * x + b

    mse = np.mean((y - y_pred) ** 2)
    plt.scatter(x, y, color='blue', label='Дані')
    plt.plot(x, y_pred, color='red', label='Лінійна Регресія')
    plt.xlabel(label)
    plt.ylabel(label2)
    plt.title('Лінійна регресія з СКВ')
    text = f"\nНахил (m): {m}\nВільний член (b): {b}\nСередня Квадратична Похибка: {mse}\n"
    plt.text(0.5, -0.3, text, transform=plt.gca().transAxes, fontsize=10, ha='center')

    plt.tight_layout()
    plt.legend()
    plt.show()

combo1 = ttk.Combobox(window, values=["Київ", "Львів", "Одеса"],width=20,font=("Helvetica", 14))
combo1.set("Оберіть місто")
combo1.pack(pady = 20)

combo2 = ttk.Combobox(window, values=["Однокімнатна, Оренда", "Двохкімнатна, Оренда", "Ціна за метр квадратний", "Усі"], width=20,font=("Helvetica", 14))
combo2.set("Для чого саме графік?")
combo2.pack(pady = 20)

plot_list = ["Звичайний графік", "Графік змін цін", "Екстраполяції та Апроксимації", "Лінійна Регресія"]
combo3 = ttk.Combobox(window, values=plot_list, width=20,font=("Helvetica", 14))
combo3.set("Який графік вас цікавить?")
combo3.pack(pady = 20)

button = tk.Button(window, text='Submit', command=MainSelectionFunction,height=2, width=20,font=("Helvetica", 14))
button.pack()

window.mainloop()