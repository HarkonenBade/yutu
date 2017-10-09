import requests
import io

from PIL import Image as ImageFile, ImageFont, ImageDraw

import discord
from discord.ext import commands


# Source: https://commons.wikimedia.org/wiki/File:Heart_corazón.svg
HEART = "./data/heart.png"


class Draw:
    @commands.command(usage="{@user|url} top text | bottom text")
    async def meme(self, ctx: commands.Context, image_source: str, *args):
        """
        Create a meme from a users avatar
        """
        async with ctx.typing():
            try:
                user = await commands.MemberConverter().convert(ctx, image_source)
                tmp = io.BytesIO(requests.get(user.avatar_url_as(format="png")).content)
            except commands.BadArgument:
                try:
                    tmp = io.BytesIO(requests.get(image_source).content)
                except requests.ConnectionError:
                    await ctx.send(content="Please post either a mention or a url.")
                    return
            tmp2 = io.BytesIO()
            msg_text = await commands.clean_content().convert(ctx, " ".join(args))
            captions = msg_text.upper().split("|")
            if len(captions) == 2:
                top = captions[0].strip()
                bottom = captions[1].strip()
            else:
                top = captions[0].strip()
                bottom = "bottom text"
            (await _agen(ctx.bot.loop, top, bottom, tmp, tmp2, 1024, 1024))
            tmp2.seek(0)
            await ctx.send(file=discord.File(tmp2, filename="meme.png"))
            await ctx.message.delete()

    @commands.command()
    async def ship(self, ctx: commands.Context, first: discord.Member, second: discord.Member):
        """
        Ship two users together
        """
        with ctx.typing():
            out = io.BytesIO()
            await ctx.bot.loop.run_in_executor(None, lambda: _ship(first, second, out))
            out.seek(0)
            await ctx.send(file=discord.File(out, filename="ship.png"))


def _ship(u1: discord.Member, u2: discord.Member, out: io.BytesIO):
    av_first = ImageFile.open(io.BytesIO(requests.get(u1.avatar_url_as(format="png", size=1024)).content))
    av_first = av_first.resize((1024, 1024))
    av_second = ImageFile.open(io.BytesIO(requests.get(u2.avatar_url_as(format="png", size=1024)).content))
    av_second = av_second.resize((1024, 1024))
    heart = ImageFile.open(HEART)
    result = ImageFile.new("RGBA", (1024 * 3, 1024))
    result.paste(av_first)
    result.paste(heart, box=(1024, 0))
    result.paste(av_second, box=(2048, 0))
    result.save(out, format="png")


async def _agen(loop, *args, **kwargs):
    return await loop.run_in_executor(None, lambda: _generate(*args, **kwargs))

"""
The following licence applies to all code in this file below this point.

Copyright © 2017, Jace Browning

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to
deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""


def _generate(top, bottom, background, output, width, height):
    font_path = "./data/impact.ttf"
    """Add text to an image and save it."""
    background_image = ImageFile.open(background)
    if background_image.mode not in ('RGB', 'RGBA'):
        if background_image.format == 'JPEG':
            background_image = background_image.convert('RGB')
            background_image.format = 'JPEG'
        else:
            background_image = background_image.convert('RGBA')
            background_image.format = 'PNG'

    image = _resize(background_image, width, height)
    image.format = 'PNG'

    # Draw image
    draw = ImageDraw.Draw(image)

    max_font_size = int(image.size[1] / 5)
    min_font_size_single_line = int(image.size[1] / 12)
    max_text_len = image.size[0] - 20
    top_font_size, top = _optimize_font_size(
        font_path, top, max_font_size,
        min_font_size_single_line, max_text_len,
    )
    bottom_font_size, bottom = _optimize_font_size(
        font_path, bottom, max_font_size,
        min_font_size_single_line, max_text_len,
    )

    top_font = ImageFont.truetype(font_path, top_font_size)
    bottom_font = ImageFont.truetype(font_path, bottom_font_size)

    top_text_size = draw.multiline_textsize(top, top_font)
    bottom_text_size = draw.multiline_textsize(bottom, bottom_font)

    # Find top centered position for top text
    top_text_position_x = (image.size[0] / 2) - (top_text_size[0] / 2)
    top_text_position_y = 0
    top_text_position = (top_text_position_x, top_text_position_y)

    # Find bottom centered position for bottom text
    bottom_text_size_x = (image.size[0] / 2) - (bottom_text_size[0] / 2)
    bottom_text_size_y = image.size[1] - bottom_text_size[1] * (7 / 6)
    bottom_text_position = (bottom_text_size_x, bottom_text_size_y)

    _draw_outlined_text(draw, top_text_position,
                        top, top_font, top_font_size)
    _draw_outlined_text(draw, bottom_text_position,
                        bottom, bottom_font, bottom_font_size)

    image.save(output, format="png")


def _optimize_font_size(font, text, max_font_size, min_font_size,
                        max_text_len):
    """Calculate the optimal font size to fit text in a given size."""

    # Check size when using smallest single line font size
    fontobj = ImageFont.truetype(font, min_font_size)
    text_size = fontobj.getsize(text)

    # Calculate font size for text, split if necessary
    if text_size[0] > max_text_len:
        phrases = _split(text)
    else:
        phrases = (text,)
    font_size = max_font_size // len(phrases)
    for phrase in phrases:
        font_size = min(_maximize_font_size(font, phrase, max_text_len),
                        font_size)

    # Rebuild text with new lines
    text = '\n'.join(phrases)

    return font_size, text


def _draw_outlined_text(draw_image, text_position, text, font, font_size):
    """Draw white text with black outline on an image."""

    # Draw black text outlines
    outline_range = max(1, font_size // 25)
    for x in range(-outline_range, outline_range + 1):
        for y in range(-outline_range, outline_range + 1):
            pos = (text_position[0] + x, text_position[1] + y)
            draw_image.multiline_text(pos, text, (0, 0, 0),
                                      font=font, align='center')

    # Draw inner white text
    draw_image.multiline_text(text_position, text, (255, 255, 255),
                              font=font, align='center')


def _resize(foreground, width, height):
    """Add a blurred background to match the requested dimensions."""
    base_width, base_height = foreground.size
    ratio = width/height

    if base_width > base_height:
        paste_width = base_width
        paste_height = int(base_width*ratio)
    else:
        paste_width = int(base_height*ratio)
        paste_height = base_height
    paste_dimensions = paste_width, paste_height
    paste = ImageFile.new('RGB', paste_dimensions)
    paste.paste(foreground, ((paste_width - base_width) // 2,
                             (paste_height - base_height) // 2))

    padded_dimensions = (width, height)
    return paste.resize(padded_dimensions, ImageFile.LANCZOS)


def _maximize_font_size(font, text, max_size):
    """Find the biggest font size that will fit."""
    font_size = max_size

    fontobj = ImageFont.truetype(font, font_size)
    text_size = fontobj.getsize(text)
    while text_size[0] > max_size and font_size > 1:
        font_size = font_size - 1
        fontobj = ImageFont.truetype(font, font_size)
        text_size = fontobj.getsize(text)

    return font_size


def _split(text):
    """Split a line of text into two similarly sized pieces.

    >>> _split("Hello, world!")
    ('Hello,', 'world!')

    >>> _split("This is a phrase that can be split.")
    ('This is a phrase', 'that can be split.')

    >>> _split("This_is_a_phrase_that_can_not_be_split.")
    ('This_is_a_phrase_that_can_not_be_split.',)

    """
    result = (text,)

    if len(text) >= 3 and ' ' in text[1:-1]:  # can split this string
        space_indices = [i for i in range(len(text)) if text[i] == ' ']
        space_proximities = [abs(i - len(text) // 2) for i in space_indices]
        for i, j in zip(space_proximities, space_indices):
            if i == min(space_proximities):
                result = (text[:j], text[j + 1:])
                break

    return result
