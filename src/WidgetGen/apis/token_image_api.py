from fastapi import APIRouter, HTTPException, UploadFile, File, Response
from pydantic import AnyHttpUrl
from typing import List
from PIL import Image, ImageDraw, ImageFont
from src.WidgetGen.models.token_vote_data import TokenVoteData
from src.WidgetGen.models.token_trend_data import TokenTrendData
from io import BytesIO
import requests
from urllib.parse import urlparse

FONT_BOLD_PATH = "src/dyor/fonts/inter/static/Inter-Bold.ttf"
FONT_REGULAR_PATH = "src/dyor/fonts/inter/static/Inter-Regular.ttf"
HEART_ICON_PATH = "src/dyor/img/heart.png"
BACKGROUND_VOTES_PATH = "src/dyor/img/Story1-background.png"
BACKGROUND_TRENDS_PATH = "src/dyor/img/Story2-background.png"
WIDGET_START_X = 74
WIDGET_START_Y = 515
WIDGET_HEIGHT = 200
WIDGET_WIDTH = 932
ICON_SIZE = (120, 120)

FONT_TOKEN_NAME = ImageFont.truetype(FONT_BOLD_PATH, 51)
FONT_TOKEN_NAME_COLOR = (255, 255, 255, 255)
FONT_TOKEN_SHORT = ImageFont.truetype(FONT_REGULAR_PATH, 33)
FONT_TOKEN_SHORT_COLOR = (255, 255, 255, 102)
FONT_HEARTS_COUNT = ImageFont.truetype(FONT_BOLD_PATH, 52)


def is_url(path: AnyHttpUrl) -> bool:
    path_str = str(path)
    return path_str.startswith("http://") or path_str.startswith("https://")


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


def create_circular_icon(icon_path):
    if is_url(icon_path):
        icon = download_image(icon_path)
    else:
        icon = Image.open(icon_path).convert("RGBA")

    mask = Image.new("L", icon.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + icon.size, fill=255)

    circular_icon = Image.new("RGBA", icon.size)
    circular_icon.paste(icon, (0, 0), mask)
    return circular_icon.resize(ICON_SIZE, Image.Resampling.LANCZOS)


def draw_widget(
    draw,
    background,
    widget_x,
    widget_y,
    token_data,
    widget_type="votes",
):
    left_space = 40
    right_padding = 40
    widget_end = widget_x + WIDGET_WIDTH
    icon = create_circular_icon(token_data.icon_url)
    icon_x = widget_x + left_space
    icon_y = widget_y + (WIDGET_HEIGHT - ICON_SIZE[1]) // 2

    # Circle with icon
    background.paste(icon, (icon_x, icon_y), icon)

    # Symbol
    draw.text(
        (left_space + ICON_SIZE[0] + widget_x + left_space, widget_y + 50),
        token_data.symbol,
        font=FONT_TOKEN_NAME,
        fill=FONT_TOKEN_NAME_COLOR,
    )

    # Name
    temp_image = Image.new("RGBA", background.size, (255, 255, 255, 0))
    temp_draw = ImageDraw.Draw(temp_image)
    temp_draw.text(
        (left_space + ICON_SIZE[0] + widget_x + left_space, widget_y + 112),
        token_data.name,
        font=FONT_TOKEN_SHORT,
        fill=FONT_TOKEN_SHORT_COLOR,
    )
    background.alpha_composite(temp_image)

    if widget_type == "votes":
        # Hearts count
        hearts_count = str(token_data.votes)
        hearts_count_length = draw.textlength(hearts_count, font=FONT_HEARTS_COUNT)
        heart_icon = Image.open(HEART_ICON_PATH).convert("RGBA")
        heart_icon_size = 40
        heart_icon = heart_icon.resize(
            (heart_icon_size, heart_icon_size), Image.Resampling.LANCZOS
        )

        heart_icon_x = widget_x + WIDGET_WIDTH - heart_icon_size - right_padding
        heart_icon_y = int(widget_y + ((WIDGET_HEIGHT / 2) - (heart_icon_size // 2)))

        text_x = (
            widget_x
            + WIDGET_WIDTH
            - heart_icon_size
            - 20
            - hearts_count_length
            - right_padding
        )

        background.paste(heart_icon, (heart_icon_x, heart_icon_y), heart_icon)

        draw.text(
            (text_x, widget_y + ((WIDGET_HEIGHT / 2) - 30)),
            hearts_count,
            font=FONT_HEARTS_COUNT,
            fill=FONT_TOKEN_NAME_COLOR,
        )
    elif widget_type == "trends":
        # Price
        font_price = ImageFont.truetype(FONT_BOLD_PATH, 52)
        font_change = ImageFont.truetype(FONT_BOLD_PATH, 37)
        price_text = f"${token_data.price:,.2f}"
        price_text_length = draw.textlength(price_text, font=FONT_HEARTS_COUNT)
        price_text_x = widget_x + WIDGET_WIDTH - price_text_length - right_padding
        draw.text(
            (price_text_x, widget_y + 50),
            price_text,
            font=FONT_HEARTS_COUNT,
            fill=FONT_TOKEN_NAME_COLOR,
        )

        # Change
        change_text = f"{token_data.change:+.2f}%"
        change_text_length = draw.textlength(change_text, font=font_change)
        change_text_x = widget_x + WIDGET_WIDTH - change_text_length - right_padding
        change_color = (
            (
                117,
                255,
                117,
                255,
            )
            if token_data.change >= 0
            else (255, 117, 117, 255)
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
    background = Image.open(BACKGROUND_VOTES_PATH)
    draw = ImageDraw.Draw(background)

    widget_y = WIDGET_START_Y
    for token in tokens:
        draw_widget(
            draw, background, WIDGET_START_X, widget_y, token, widget_type="votes"
        )
        widget_y += WIDGET_HEIGHT + 32  # Переход к следующему виджету

    img_byte_arr = BytesIO()
    background.save(img_byte_arr, format="PNG")
    return Response(content=img_byte_arr.getvalue(), media_type="image/png")


@router.post("/tokens/trends/")
def create_trend_image(tokens: List[TokenTrendData]):
    background = Image.open(BACKGROUND_TRENDS_PATH)
    draw = ImageDraw.Draw(background)

    widget_y = WIDGET_START_Y
    for token in tokens:
        draw_widget(
            draw, background, WIDGET_START_X, widget_y, token, widget_type="trends"
        )
        widget_y += WIDGET_HEIGHT + 32

    img_byte_arr = BytesIO()
    background.save(img_byte_arr, format="PNG")
    return Response(content=img_byte_arr.getvalue(), media_type="image/png")
