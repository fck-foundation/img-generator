from fastapi import APIRouter, HTTPException, UploadFile, File, Response
from typing import List
from PIL import Image, ImageDraw, ImageFont
from src.WidgetGen.models.token_vote_data import TokenVoteData
from src.WidgetGen.models.token_trend_data import TokenTrendData
from io import BytesIO
import requests
from urllib.parse import urlparse


def is_url(path):
    try:
        result = urlparse(path)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def download_image(url):
    response = requests.get(url)
    response.raise_for_status()
    return Image.open(BytesIO(response.content))


def process_token_icon_path(token_icon_path):
    if is_url(token_icon_path):
        token_icon = download_image(token_icon_path)
    else:
        token_icon = Image.open(token_icon_path).convert("RGBA")

    if token_icon_path.lower().endswith(".webp"):
        token_icon = token_icon.convert("RGBA")

    return token_icon


def make_icon_circular(icon):
    mask = Image.new("L", icon.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + icon.size, fill=255)

    circular_icon = Image.new("RGBA", icon.size)
    circular_icon.paste(icon, (0, 0), mask)

    return circular_icon


def draw_token_widget_votes(
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
    font_bold_path = "src/dyor/fonts/inter/static/Inter-Bold.ttf"
    font_regular_path = "src/dyor/fonts/inter/static/Inter-Regular.ttf"
    font_size = 51
    font_token_name = ImageFont.truetype(font_bold_path, 51)
    font_token_name_color = (255, 255, 255, 255)
    font_token_short = ImageFont.truetype(font_regular_path, 33)
    font_token_short_color = (255, 255, 255, 102)
    font_hearts_count = ImageFont.truetype(font_bold_path, 52)
    icon_font_size = 100
    icon_font = ImageFont.truetype(font_bold_path, icon_font_size)
    left_space = 40
    right_padding = 40

    text_length = draw.textlength(str(token_votes), font=font_hearts_count)

    heart_icon = Image.open(heart_icon_path).convert("RGBA")
    heart_icon_size = 40
    heart_icon = heart_icon.resize(
        (heart_icon_size, heart_icon_size), Image.Resampling.LANCZOS
    )

    heart_icon_x = widget_x + widget_width - heart_icon_size - right_padding
    heart_icon_y = int(widget_y + ((widget_height / 2) - (heart_icon_size // 2)))

    text_x = (
        widget_x + widget_width - heart_icon_size - 20 - text_length - right_padding
    )

    circle_size = 110
    circle_margin_left = left_space
    icon_size = (120, 120)
    circle_color = (0, 0, 0, 0)

    circle_x = widget_x + circle_margin_left
    circle_y = widget_y + (widget_height - circle_size) // 2
    draw.ellipse(
        (circle_x, circle_y, circle_x + circle_size, circle_y + circle_size),
        fill=circle_color,
        outline=None,
    )

    token_icon = process_token_icon_path(token_icon_path)

    if token_icon is not None:
        token_icon = make_icon_circular(token_icon)
        token_icon = token_icon.resize(icon_size, Image.Resampling.LANCZOS)
        icon_x = circle_x + (circle_size - icon_size[0]) // 2
        icon_y = circle_y + (circle_size - icon_size[1]) // 2
        background.paste(token_icon, (icon_x, icon_y), token_icon)

    draw.text(
        (circle_margin_left + circle_size + widget_x + left_space, widget_y + 50),
        token_short,
        font=font_token_name,
        fill=font_token_name_color,
    )

    temp_image = Image.new("RGBA", background.size, (255, 255, 255, 0))
    temp_draw = ImageDraw.Draw(temp_image)
    temp_draw.text(
        (circle_margin_left + circle_size + widget_x + left_space, widget_y + 112),
        token_name,
        font=font_token_short,
        fill=font_token_short_color,
    )
    background.alpha_composite(temp_image)
    background.paste(heart_icon, (heart_icon_x, heart_icon_y), heart_icon)

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
    right_padding = 40

    price_text = f"${token_price:,.2f}"
    change_text = f"{price_change:+.2f}%"

    change_color = (117, 255, 117, 255) if price_change >= 0 else (255, 117, 117, 255)

    price_text_length = draw.textlength(price_text, font=font_price)
    change_text_length = draw.textlength(change_text, font=font_change)

    price_text_x = widget_x + widget_width - price_text_length - right_padding
    change_text_x = widget_x + widget_width - change_text_length - right_padding

    circle_size = 110
    circle_margin_left = left_space
    icon_size = (120, 120)
    circle_color = (0, 0, 0, 0)

    circle_x = widget_x + circle_margin_left
    circle_y = widget_y + (widget_height - circle_size) // 2
    draw.ellipse(
        (circle_x, circle_y, circle_x + circle_size, circle_y + circle_size),
        fill=circle_color,
        outline=None,
    )

    token_icon = process_token_icon_path(token_icon_path)

    if token_icon is not None:
        token_icon = make_icon_circular(token_icon)
        token_icon = token_icon.resize(icon_size, Image.Resampling.LANCZOS)
        icon_x = circle_x + (circle_size - icon_size[0]) // 2
        icon_y = circle_y + (circle_size - icon_size[1]) // 2
        background.paste(token_icon, (icon_x, icon_y), token_icon)

    draw.text(
        (circle_margin_left + circle_size + widget_x + left_space, widget_y + 50),
        token_short,
        font=font_token_name,
        fill=font_token_name_color,
    )

    temp_image = Image.new("RGBA", background.size, (255, 255, 255, 0))
    temp_draw = ImageDraw.Draw(temp_image)
    temp_draw.text(
        (circle_margin_left + circle_size + widget_x + left_space, widget_y + 112),
        token_name,
        font=font_token_short,
        fill=font_token_short_color,
    )
    background.alpha_composite(temp_image)

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


router = APIRouter()


@router.post("/tokens/votes/")
def create_vote_image(tokens: List[TokenVoteData]):
    background_votes_path = "src/dyor/img/Story1-background.png"
    background_votes = Image.open(background_votes_path)

    widgets_start_x = 74
    widgets_start_y = 515
    widget_height = 200
    widget_width = 932

    widgets_start_y = 515

    for token_name, token_short, icon_url, hearts in tokens:
        draw_token_widget_votes(
            ImageDraw.Draw(background_votes),
            token_name[1],
            token_short[1],
            hearts[1],
            widgets_start_x,
            widgets_start_y,
            widget_height,
            widget_width,
            token_icon_path=str(icon_url[1]),
            background=background_votes,
        )

        widgets_start_y += widget_height + 32

    img_byte_arr = BytesIO()

    background_votes.save(
        img_byte_arr,
        format="PNG",
        save_all=True,
    )
    img_byte_arr = img_byte_arr.getvalue()
    return Response(content=img_byte_arr, media_type="image/png")


@router.post("/tokens/trends/")
def create_trend_image(tokens: List[TokenTrendData]):
    background_trends_path = "src/dyor/img/Story2-background.png"
    background_trends = Image.open(background_trends_path)

    widgets_start_x = 74
    widgets_start_y = 515
    widget_height = 200
    widget_width = 932

    widgets_start_y = 515
    for token_name, token_short, icon_url, price, change in tokens:
        draw_token_widget_trends(
            ImageDraw.Draw(background_trends),
            token_name[1],
            token_short[1],
            price[1],
            change[1],
            widgets_start_x,
            widgets_start_y,
            widget_height,
            widget_width,
            token_icon_path=str(icon_url[1]),
            background=background_trends,
        )

        widgets_start_y += widget_height + 32

    img_byte_arr = BytesIO()

    background_trends.save(
        img_byte_arr,
        format="PNG",
        save_all=True,
    )
    img_byte_arr = img_byte_arr.getvalue()
    return Response(content=img_byte_arr, media_type="image/png")
