# calories_gui.py — Калькулятор калорий с ОКНОМ
import tkinter as tk

# База продуктов (на 100г)
FOOD = {"курица": 165, "рис": 130, "яйцо": 155, "творог": 121, "овсянка": 68}


def add_food():
    product = entry_product.get().lower().strip()
    if product not in FOOD:
        result_label.config(text="Продукт не найден!", fg="red")
        return
    try:
        grams = float(entry_grams.get())
    except:
        result_label.config(text="Введи число!", fg="red")
        return

    cal = (FOOD[product] * grams) / 100
    total[0] += cal
    listbox.insert(tk.END, f"{product}: {cal:.1f} ккал")
    result_label.config(text=f"Итого: {total[0]:.1f} ккал", fg="green")
    entry_product.delete(0, tk.END)
    entry_grams.delete(0, tk.END)


total = [0.0]
root = tk.Tk()
root.title("Калькулятор калорий")
root.geometry("400x400")

tk.Label(root, text="Продукт:", font=("Arial", 12)).pack(pady=5)
entry_product = tk.Entry(root, width=30)
entry_product.pack()

tk.Label(root, text="Грамм:", font=("Arial", 12)).pack(pady=5)
entry_grams = tk.Entry(root, width=30)
entry_grams.pack()

tk.Button(root, text="Добавить", command=add_food, bg="green", fg="white", font=("Arial", 12)).pack(pady=10)

listbox = tk.Listbox(root, width=50, height=10)
listbox.pack(pady=10)

result_label = tk.Label(root, text="Итого: 0.0 ккал", font=("Arial", 14))
result_label.pack(pady=10)

root.mainloop()