import re
import json

# Читаем файл
with open("raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Убираем переносы строк внутри чисел
text = re.sub(r'(\d)\n(\d)', r'\1 \2', text)

# -------------------------
# 1. Извлечение всех цен
# -------------------------
price_pattern = r'\d[\d ]*,\d{2}'
prices = re.findall(price_pattern, text)

# очищаем цены от пробелов
prices_clean = [p.replace(" ", "") for p in prices]

# -------------------------
# 2. Извлечение товаров
# -------------------------
product_pattern = r'\d+\.\s*\n(.+)'
products = re.findall(product_pattern, text)

products = [p.strip() for p in products]

# -------------------------
# 3. Итоговая сумма
# -------------------------
total_pattern = r'ИТОГО:\s*\n?([\d ]+,\d{2})'
total_match = re.search(total_pattern, text)

total = total_match.group(1).replace(" ", "") if total_match else None

# -------------------------
# 4. Дата и время
# -------------------------
datetime_pattern = r'Время:\s*(\d{2}\.\d{2}\.\d{4})\s*(\d{2}:\d{2}:\d{2})'
datetime_match = re.search(datetime_pattern, text)

date = datetime_match.group(1) if datetime_match else None
time = datetime_match.group(2) if datetime_match else None

# -------------------------
# 5. Способ оплаты
# -------------------------
payment_pattern = r'(Банковская карта|Наличные)'
payment_match = re.search(payment_pattern, text)

payment_method = payment_match.group(1) if payment_match else None

# -------------------------
# 6. Структурированный вывод
# -------------------------
receipt_data = {
    "products": products,
    "prices": prices_clean,
    "total": total,
    "date": date,
    "time": time,
    "payment_method": payment_method
}

print(json.dumps(receipt_data, indent=4, ensure_ascii=False))