from fastapi import FastAPI, UploadFile, File
from PIL import Image, ImageDraw, ImageFont
import io
from starlette.responses import StreamingResponse

app = FastAPI()

@app.get("/")
def welcome():
    return "A very long journey is indeed boring, But the memories of cheese burger remains unduplicated.\n- Borgar"

@app.post("/text")
async def write_text_on_image(image: UploadFile = File(...), text: str = None):
    # Read the uploaded image
    image_data = await image.read()
    image_stream = io.BytesIO(image_data)
    img = Image.open(image_stream).convert("RGBA")

    # Define the font and size
    text_size=int(img.height/6)
    font = ImageFont.truetype("/workspaces/Meme-generator-API/Oswald-Bold.ttf", text_size)

    # Create a transparent layer for text
    text_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(text_layer)

    # Calculate the position to center the text
    text_width, text_height = draw.textsize(text, font=font)
    x = (img.width - text_width) // 2
    y = (img.height - text_height) - 20

    # Draw the text on the text layer with stroke
    stroke_width = text_size/15
    stroke_color = (0, 0, 0, 255)
    draw.text((x - stroke_width, y - stroke_width), text, font=font, fill=stroke_color)
    draw.text((x + stroke_width, y - stroke_width), text, font=font, fill=stroke_color)
    draw.text((x - stroke_width, y + stroke_width), text, font=font, fill=stroke_color)
    draw.text((x + stroke_width, y + stroke_width), text, font=font, fill=stroke_color)

    # Draw the main text on the text layer
    draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))

    # Combine the original image and the text layer
    result = Image.alpha_composite(img, text_layer)

    # Save the result to a new image
    output_stream = io.BytesIO()
    result.save(output_stream, format="PNG")
    output_stream.seek(0)

    return StreamingResponse(output_stream, media_type="image/png")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
