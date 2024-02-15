from PIL import Image, ImageChops
import cv2


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






# Путь к вашим изображениям
large_image_path = 'page_10_2.png'
small_image_path = 'page_10_1.png'
output_path = 'f.png'



# Найдем позицию и выведем ее
position = find_image_position_opencv(large_image_path, small_image_path)
print(f"Маленькое изображение должно быть вставлено в позицию: {position}")


# Вызываем функцию
insert_image_with_transparency(large_image_path, small_image_path, position, output_path)
