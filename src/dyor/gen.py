from PIL import Image, ImageDraw, ImageFont
import io

# Load the background image from the file system
background_votes_path = "src/dyor/img/Story1-background.png"
background_votes = Image.open(background_votes_path)
output_votes_path = "src/dyor/results/Story1-custom.png"

# Load the background image from the file system
background_trends_path = "src/dyor/img/Story2-background.png"
background_trends = Image.open(background_trends_path)
output_trends_path = "src/dyor/results/Story2-custom.png"

# Define the tokens and hearts
tokens_votes = [
    (
        "Scale",
        "SCALE",
        "https://cache.tonapi.io/imgproxy/jHx0m3tMBFj9z9vLy1cooH_v8DIi_2Zi43RLxyfga3g/rs:fill:200:200:1/g:no/aXBmczovL1FtU01pWHNaWU1lZndyVFEzUDZIbkRRYUNwZWNTNEVXTHBnS0s1RVgxRzhpQTg.webp",
        111000,
    ),
    (
        "TON Drift",
        "DRIFT",
        "https://cache.tonapi.io/imgproxy/jHx0m3tMBFj9z9vLy1cooH_v8DIi_2Zi43RLxyfga3g/rs:fill:200:200:1/g:no/aXBmczovL1FtU01pWHNaWU1lZndyVFEzUDZIbkRRYUNwZWNTNEVXTHBnS0s1RVgxRzhpQTg.webp",
        183,
    ),
    (
        "Tonnel Network Token",
        "TONNEL",
        "https://cache.tonapi.io/imgproxy/jHx0m3tMBFj9z9vLy1cooH_v8DIi_2Zi43RLxyfga3g/rs:fill:200:200:1/g:no/aXBmczovL1FtU01pWHNaWU1lZndyVFEzUDZIbkRRYUNwZWNTNEVXTHBnS0s1RVgxRzhpQTg.webp",
        72,
    ),
    (
        "Find & Check",
        "FCK",
        "https://cache.tonapi.io/imgproxy/jHx0m3tMBFj9z9vLy1cooH_v8DIi_2Zi43RLxyfga3g/rs:fill:200:200:1/g:no/aXBmczovL1FtU01pWHNaWU1lZndyVFEzUDZIbkRRYUNwZWNTNEVXTHBnS0s1RVgxRzhpQTg.webp",
        33,
    ),
    (
        "Huebel Bolt",
        "BOLT",
        "https://cache.tonapi.io/imgproxy/jHx0m3tMBFj9z9vLy1cooH_v8DIi_2Zi43RLxyfga3g/rs:fill:200:200:1/g:no/aXBmczovL1FtU01pWHNaWU1lZndyVFEzUDZIbkRRYUNwZWNTNEVXTHBnS0s1RVgxRzhpQTg.webp",
        32,
    ),
]

tokens_trends = [
    (
        "Scale",
        "SCALE",
        "https://cache.tonapi.io/imgproxy/jHx0m3tMBFj9z9vLy1cooH_v8DIi_2Zi43RLxyfga3g/rs:fill:200:200:1/g:no/aXBmczovL1FtU01pWHNaWU1lZndyVFEzUDZIbkRRYUNwZWNTNEVXTHBnS0s1RVgxRzhpQTg.webp",
        123.45,
        +2.34,
    ),
    (
        "TON Drift",
        "DRIFT",
        "https://cache.tonapi.io/imgproxy/jHx0m3tMBFj9z9vLy1cooH_v8DIi_2Zi43RLxyfga3g/rs:fill:200:200:1/g:no/aXBmczovL1FtU01pWHNaWU1lZndyVFEzUDZIbkRRYUNwZWNTNEVXTHBnS0s1RVgxRzhpQTg.webp",
        123.45,
        -2.34,
    ),
    (
        "Tonnel Network Token",
        "TONNEL",
        "https://cache.tonapi.io/imgproxy/jHx0m3tMBFj9z9vLy1cooH_v8DIi_2Zi43RLxyfga3g/rs:fill:200:200:1/g:no/aXBmczovL1FtU01pWHNaWU1lZndyVFEzUDZIbkRRYUNwZWNTNEVXTHBnS0s1RVgxRzhpQTg.webp",
        123.45,
        +2.34,
    ),
    (
        "Find & Check",
        "FCK",
        "https://cache.tonapi.io/imgproxy/jHx0m3tMBFj9z9vLy1cooH_v8DIi_2Zi43RLxyfga3g/rs:fill:200:200:1/g:no/aXBmczovL1FtU01pWHNaWU1lZndyVFEzUDZIbkRRYUNwZWNTNEVXTHBnS0s1RVgxRzhpQTg.webp",
        123.45,
        -2.34,
    ),
    (
        "Huebel Bolt",
        "BOLT",
        "https://cache.tonapi.io/imgproxy/jHx0m3tMBFj9z9vLy1cooH_v8DIi_2Zi43RLxyfga3g/rs:fill:200:200:1/g:no/aXBmczovL1FtU01pWHNaWU1lZndyVFEzUDZIbkRRYUNwZWNTNEVXTHBnS0s1RVgxRzhpQTg.webp",
        123.45,
        +2.34,
    ),
]

# Starting positions
widgets_start_x = 74
widgets_start_y = 515
widget_height = 200
widget_width = 932
icon_y = widgets_start_y + 0

# Create a draw object
draw_votes = ImageDraw.Draw(background_votes)


# Define a function to draw text with shadow
def draw_token_widget_votes(
    # Draw the token name and heart count
    draw,
    token_name="None Project",
    token_short="NONE",
    token_votes=0,
    widget_x=100,
    widget_y=100,
    widget_height=200,
    widget_width=932,
    token_icon_path=None,
    background=None,
):
    widget_end = widget_x + widget_width
    heart_icon_path = "src/dyor/img/heart.png"
    # Load a font
    font_path = "src/dyor/fonts/inter/static/Inter-Bold.ttf"
    font_size = 51
    font_token_name = ImageFont.truetype(font_path, 51)
    font_token_name_color = (255, 255, 255, 255)
    font_token_short = ImageFont.truetype(font_path, 33)
    font_token_short_color = (255, 255, 255, 102)
    font_hearts_count = ImageFont.truetype(font_path, 52)
    icon_font_size = 100
    icon_font = ImageFont.truetype(font_path, icon_font_size)
    left_space = 40
    # Расстояние справа, которое мы хотим оставить пустым
    right_padding = 40
    # Получаем ширину текста с количеством голосов
    text_length = draw.textlength(str(token_votes), font=font_hearts_count)

    # Загрузка иконки сердца
    heart_icon = Image.open(heart_icon_path).convert("RGBA")
    heart_icon_size = 40  # или любой другой размер, который вам нужен
    heart_icon = heart_icon.resize(
        (heart_icon_size, heart_icon_size), Image.Resampling.LANCZOS
    )

    # Рассчитайте координаты для размещения иконки
    # heart_icon_x = int(text_x - heart_icon_size - 20)  # 5 пикселей отступ от текста
    heart_icon_x = widget_x + widget_width - heart_icon_size - right_padding
    heart_icon_y = int(widget_y + ((widget_height / 2) - (heart_icon_size // 2)))

    # Рассчитываем X координату так, чтобы текст был выровнен по правому краю
    # text_x = widget_x + widget_width - text_length - right_padding
    text_x = (
        widget_x + widget_width - heart_icon_size - 20 - text_length - right_padding
    )

    # Дополнительные настройки
    circle_size = 110  # Размер круга
    circle_margin_left = left_space  # Отступ круга от левого края виджета
    icon_size = (120, 120)  # Размер иконки внутри круга
    circle_color = (0, 0, 0, 0)  # Цвет круга

    # Рисуем круг
    circle_x = widget_x + circle_margin_left
    circle_y = widget_y + (widget_height - circle_size) // 2
    draw.ellipse(
        (circle_x, circle_y, circle_x + circle_size, circle_y + circle_size),
        fill=circle_color,
        outline=None,
    )

    # Проверяем, является ли формат иконки WEBP
    if token_icon_path and token_icon_path.lower().endswith(".webp"):
        # Конвертируем WEBP в PNG
        token_icon = Image.open(token_icon_path).convert("RGBA")
        png_token_icon_path = token_icon_path.rstrip(".webp") + ".png"
        token_icon.save(png_token_icon_path, "PNG")
        token_icon_path = png_token_icon_path  # Обновляем путь к иконке

    # Загружаем иконку токена
    if token_icon_path:
        token_icon = Image.open(token_icon_path).convert("RGBA")
        # Изменяем размер иконки
        token_icon = token_icon.resize(icon_size, Image.ANTIALIAS)
        # Вставляем иконку в круг
        icon_x = circle_x + (circle_size - icon_size[0]) // 2
        icon_y = circle_y + (circle_size - icon_size[1]) // 2
        background.paste(token_icon, (icon_x, icon_y), token_icon)

    print(f"Drawing widget for {token_name}: X - {widget_x}, Y - {widget_y}")
    draw.text(
        (circle_margin_left + circle_size + widget_x + left_space, widget_y + 50),
        token_short,
        font=font_token_name,
        fill=font_token_name_color,
    )
    draw.text(
        (circle_margin_left + circle_size + widget_x + left_space, widget_y + 112),
        token_name,
        font=font_token_short,
        fill=font_token_short_color,
    )

    # Вставьте иконку на изображение
    background.paste(heart_icon, (heart_icon_x, heart_icon_y), heart_icon)

    # Рисуем количество голосов, выровненное по правому краю
    draw.text(
        (text_x, widget_y + ((widget_height / 2) - 30)),
        str(token_votes),
        font=font_hearts_count,
        fill=font_token_name_color,
    )


def draw_token_widget_trends(
    draw,
    token_name="None Project",
    token_short="NONE",
    token_price=0.0,
    price_change=0.0,
    widget_x=100,
    widget_y=100,
    widget_height=200,
    widget_width=932,
    token_icon_path=None,
    background=None,
):
    widget_end = widget_x + widget_width
    heart_icon_path = "src/dyor/img/heart.png"
    # Load a font
    font_path = "src/dyor/fonts/inter/static/Inter-Bold.ttf"
    font_size = 51
    font_token_name = ImageFont.truetype(font_path, 51)
    font_token_name_color = (255, 255, 255, 255)
    font_token_short = ImageFont.truetype(font_path, 33)
    font_token_short_color = (255, 255, 255, 102)
    font_price = ImageFont.truetype(font_path, 52)
    font_change = ImageFont.truetype(font_path, 37)
    icon_font_size = 100
    icon_font = ImageFont.truetype(font_path, icon_font_size)
    left_space = 40
    # Расстояние справа, которое мы хотим оставить пустым
    right_padding = 40
    # Получаем ширину текста с количеством голосов
    # text_length = draw.textlength(str(token_votes), font=font_hearts_count)
    # Рассчитываем X координату так, чтобы текст был выровнен по правому краю
    # text_x = widget_x + widget_width - text_length - right_padding

    # Задаем формат отображения цены и изменения процента
    price_text = f"${token_price:,.2f}"  # Форматирование цены с двумя знаками после запятой и разделителями тысяч
    change_text = f"{price_change:+.2f}%"  # Форматирование изменения процента с знаком и двумя знаками после запятой

    # Выбираем цвет для текста изменения процента в зависимости от его значения
    change_color = (117, 255, 117, 255) if price_change >= 0 else (255, 117, 117, 255)

    # Получаем ширину текста с ценой
    price_text_length = draw.textlength(price_text, font=font_price)
    change_text_length = draw.textlength(change_text, font=font_change)

    # Рассчитываем X координаты так, чтобы текст был выровнен по правому краю
    price_text_x = widget_x + widget_width - price_text_length - right_padding
    change_text_x = widget_x + widget_width - change_text_length - right_padding

    # Дополнительные настройки
    circle_size = 110  # Размер круга
    circle_margin_left = left_space  # Отступ круга от левого края виджета
    icon_size = (120, 120)  # Размер иконки внутри круга
    circle_color = (0, 0, 0, 0)  # Цвет круга

    # Рисуем круг
    circle_x = widget_x + circle_margin_left
    circle_y = widget_y + (widget_height - circle_size) // 2
    draw.ellipse(
        (circle_x, circle_y, circle_x + circle_size, circle_y + circle_size),
        fill=circle_color,
        outline=None,
    )

    # Проверяем, является ли формат иконки WEBP
    if token_icon_path and token_icon_path.lower().endswith(".webp"):
        # Конвертируем WEBP в PNG
        token_icon = Image.open(token_icon_path).convert("RGBA")
        png_token_icon_path = token_icon_path.rstrip(".webp") + ".png"
        token_icon.save(png_token_icon_path, "PNG")
        token_icon_path = png_token_icon_path  # Обновляем путь к иконке

    # Загружаем иконку токена
    if token_icon_path:
        token_icon = Image.open(token_icon_path).convert("RGBA")
        # Изменяем размер иконки
        token_icon = token_icon.resize(icon_size, Image.ANTIALIAS)
        # Вставляем иконку в круг
        icon_x = circle_x + (circle_size - icon_size[0]) // 2
        icon_y = circle_y + (circle_size - icon_size[1]) // 2
        background.paste(token_icon, (icon_x, icon_y), token_icon)

    print(f"Drawing widget for {token_name}: X - {widget_x}, Y - {widget_y}")
    draw.text(
        (circle_margin_left + circle_size + widget_x + left_space, widget_y + 50),
        token_short,
        font=font_token_name,
        fill=font_token_name_color,
    )
    draw.text(
        (circle_margin_left + circle_size + widget_x + left_space, widget_y + 112),
        token_name,
        font=font_token_short,
        fill=font_token_short_color,
    )

    # Рисуем цену и изменение процента
    draw.text(
        (price_text_x, widget_y + 50),
        price_text,
        font=font_price,
        fill=font_token_name_color,
    )
    draw.text(
        (change_text_x, widget_y + 110),
        change_text,
        font=font_change,
        fill=change_color,
    )


# Loop through each token and draw the icons, names, and heart counts
for token_name, token_short, hearts in tokens_votes:
    draw_token_widget_votes(
        ImageDraw.Draw(background_votes),
        token_name,
        token_short,
        hearts,
        widgets_start_x,
        widgets_start_y,
        widget_height,
        widget_width,
        token_icon_path="src/dyor/icons/scale.webp",
        background=background_votes,
    )

    # Move down to the next line
    widgets_start_y += widget_height + 32

widgets_start_y = 515
# Цикл отрисовки виджетов для каждого токена
for token_name, token_short, token_price, price_change in tokens_trends:
    draw_token_widget_trends(
        ImageDraw.Draw(background_trends),
        token_name,
        token_short,
        token_price,
        price_change,
        widgets_start_x,
        widgets_start_y,
        widget_height,
        widget_width,
        token_icon_path="src/dyor/icons/scale.webp",
        background=background_trends,
    )

    # Перемещение вниз для следующего виджета
    widgets_start_y += widget_height + 32

# Save the resulting images
background_votes.save(output_votes_path)
background_trends.save(output_trends_path)

# Return the path to the saved image
print(f"Saved image to {output_votes_path}")
print(f"Saved image to {output_trends_path}")
