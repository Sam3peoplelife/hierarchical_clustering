import tkinter as tk
from tkinter import messagebox
import pandas as pd
from scipy.cluster import hierarchy
from scipy.cluster.hierarchy import dendrogram
import matplotlib.pyplot as plt
import numpy as np

# Підвантажили датасет
df = pd.read_csv('vgsales.csv')

# Нормалізуємо дані
df.fillna(0, inplace=True)

def sci_func():
    if checkbox_var.get() == 1:
        try:
            number = int(number_entry.get())
        except:
            messagebox.showerror(message='Invalid inputs')
            return 1
        text1 = text_entry1.get()
        text2 = text_entry2.get()

        try:
            sample = df[[text1, text2]].sample(n=number, random_state=1)
        except:
            messagebox.showerror(message='Invalid inputs')
            return 1

        matrix = np.array(sample.values.tolist())

        Z = hierarchy.linkage(matrix, 'single')

        plt.figure(figsize=(8, 6))
        plt.title('Hierarchical Clustering Dendrogram (Scipy)')
        plt.xlabel('sample index')
        plt.ylabel('distance')
        dendrogram(Z)
        plt.show()

def link_matrix(matrix):
    clusters = {i: [i] for i in range(len(matrix))}
    print(clusters)
    min_val = {}
    while len(clusters) > 1:
        color = np.random.rand(3, )
        min_dist = np.inf
        cluster_pair = None
        for i in clusters:
            for j in clusters:
                if i < j:
                    dist = np.min([matrix[x][y] for x in clusters[i] for y in clusters[j]])
                    if dist < min_dist:
                        min_dist = dist
                        cluster_pair = (i,j)
        val_idx = (cluster_pair[0] + cluster_pair[1])/2
        min_val[val_idx] = min_dist
        if len(clusters[cluster_pair[0]]) > 1:
            yi1 = min_val[cluster_pair[0]]
        else:
            yi1 = 0
        if len(clusters[cluster_pair[1]]) > 1:
            yi2 = min_val[cluster_pair[1]]
        else:
            yi2 = 0
        plt.vlines(ymin=yi1, ymax=min_dist, x=cluster_pair[0], color=color)
        plt.vlines(ymin=yi2, ymax=min_dist, x=cluster_pair[1], color=color)
        plt.hlines(xmin=min(cluster_pair), xmax=max(cluster_pair), y=min_dist, color=color)
        if cluster_pair is not None:
            new_cluster_idx = (cluster_pair[0] + cluster_pair[1]) / 2
            clusters[new_cluster_idx] = clusters.pop(cluster_pair[0]) + clusters.pop(cluster_pair[1])
            print(clusters)
        else:
            break


def matrix_dist(mat):
    dist_mat = []
    for i in range(len(mat)):
        line = []
        for j in range(len(mat)):
            distance = ((mat[i][0] - mat[j][0])**2 + (mat[i][1] - mat[j][1])**2)**0.5
            line.append(distance)
        dist_mat.append(line)
    return dist_mat


def on_button_click():
    # Перевіряємо чи це число
    try:
        number = int(number_entry.get())
    except:
        messagebox.showerror(message='Invalid inputs')
        return 1
    text1 = text_entry1.get()
    text2 = text_entry2.get()
    # Малюємо дендрограму
    draw_dendrogram(number, text1, text2)


def draw_dendrogram(sample_size, col1, col2):
    # Перевіряємо правильність назв колонок
    try:
        sample = df[[col1, col2]].sample(n=sample_size, random_state=1)
        print(sample)
    except:
        messagebox.showerror(message='Invalid inputs')
        return 1

    matrix = sample.values.tolist()
    print(matrix)
    F = matrix_dist(matrix)
    for i in F:
        print(i)
    link_matrix(F)
    plt.show()

root = tk.Tk()
root.title("Dendrograms")
root.geometry("400x400")
number_label = tk.Label(root, text='Enter a sample size:')
number_label.pack()
number_entry = tk.Entry(root)
number_entry.pack()

text_label1 = tk.Label(root, text='Enter First Column:')
text_label1.pack()
text_entry1 = tk.Entry(root)
text_entry1.pack()

text_label2 = tk.Label(root, text='Enter Second Column:')
text_label2.pack()
text_entry2 = tk.Entry(root)
text_entry2.pack()

checkbox_var = tk.IntVar()
c = tk.Checkbutton(root, text="Compare with scipy", variable=checkbox_var, command=sci_func)
c.pack()

button = tk.Button(root, text='Submit', command=on_button_click)
button.pack()

root.mainloop()

