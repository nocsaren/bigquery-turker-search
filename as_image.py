from PIL import Image, ImageDraw, ImageFont
def create_image_with_text(text, font_size=16, output_file="output.png"):
    # background
    image = Image.new("RGB", (485, 300), "#E4D9D8")
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype("arialbd.ttf", font_size)

    text_bbox = draw.textbbox((0, 0), text, font=font)

    # position
    x = (image.width - text_bbox[2]) // 2
    y = (image.height - text_bbox[3]) // 2

    draw.text((x, y), text, font=font, fill="#8E4F49")

    image.save(output_file)

if __name__ == "__main__":
    create_image_with_text(text)

