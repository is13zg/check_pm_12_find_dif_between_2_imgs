from PIL import Image, ImageChops
import cv2
import os


def find_image_position_opencv(large_image_path, small_image_path):
    # Загружаем изображения
    large_image = cv2.imread(large_image_path, cv2.IMREAD_COLOR)
    small_image = cv2.imread(small_image_path, cv2.IMREAD_COLOR)

    # Конвертируем изображения в оттенки серого для сопоставления шаблонов
    large_gray = cv2.cvtColor(large_image, cv2.COLOR_BGR2GRAY)
    small_gray = cv2.cvtColor(small_image, cv2.COLOR_BGR2GRAY)

    # Используем метод сопоставления шаблонов
    result = cv2.matchTemplate(large_gray, small_gray, cv2.TM_CCOEFF_NORMED)

    # Находим локацию с максимальным совпадением
    _, _, _, max_loc = cv2.minMaxLoc(result)

    return max_loc

def insert_image_with_transparency(large_image_path, small_image_path, position, output_path):
    # Загружаем изображения
    large_image = Image.open(large_image_path).convert("RGBA")
    small_image = Image.open(small_image_path).convert("RGBA")

    # Изменяем прозрачность маленького изображения
    # Создаем промежуточное изображение для установки прозрачности
    transparent_small_image = Image.new("RGBA", small_image.size)
    for x in range(small_image.width):
        for y in range(small_image.height):
            r, g, b, a = small_image.getpixel((x, y))
            transparent_small_image.putpixel((x, y), (r, g, b, int(a * 0.5)))  # Устанавливаем прозрачность 50%

    # Вставляем маленькое изображение на большое в заданной позиции
    large_image.paste(transparent_small_image, position, transparent_small_image)

    # Сохраняем результат
    large_image.save(output_path)

def list_files(directory):
    result = []
    """Выводит список всех файлов в указанной директории."""
    # Проверяем, существует ли директория
    if not os.path.exists(directory):
        print("Директория не найдена.")
        return

    # Перебираем все файлы в директории
    for root, dirs, files in os.walk(directory):
        for file in files:
            result.append(os.path.join(root, file))
    return result







# Путь к вашим изображениям
old_large_image_path = 'old_big'
new_small_image_path = 'new_small'
output_path = 'res'


old_files_ls = list_files(old_large_image_path)
print(old_files_ls)

for x in old_files_ls:
    print(x,"...")
    nf_name = x.replace(old_large_image_path, new_small_image_path)
    position = find_image_position_opencv(x, nf_name)
    insert_image_with_transparency(x, nf_name, position, x.replace(old_large_image_path, output_path))



# Найдем позицию и выведем ее
#position = find_image_position_opencv(large_image_path, small_image_path)
#print(f"Маленькое изображение должно быть вставлено в позицию: {position}")


# Вызываем функцию
#insert_image_with_transparency(large_image_path, small_image_path, position, output_path)
