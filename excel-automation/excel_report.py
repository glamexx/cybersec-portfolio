import pandas as pd
import matplotlib.pyplot as plt

# Тестовый бюджет
data = {
    "Дата": ["2025-11-01", "2025-11-02", "2025-11-03"],
    "Категория": ["Еда", "Транспорт", "Развлечения"],
    "Сумма": [800, 300, 500]
}
df = pd.DataFrame(data)
df.to_excel("budget.xlsx", index=False)
print("Создан budget.xlsx")

# Анализ
total = df["Сумма"].sum()
by_category = df.groupby("Категория")["Сумма"].sum()

print(f"Всего потрачено: {total} руб")
print("По категориям:")
print(by_category)

# График
by_category.plot(kind="pie", autopct="%1.1f%%", title="Расходы")
plt.savefig("budget_chart.png")
plt.show()

# Отчёт
by_category.to_frame("Сумма").to_excel("budget_report.xlsx")
print("Отчёт сохранён: budget_report.xlsx + budget_chart.png")