import numpy as np
from PIL import Image, ImageEnhance
import requests
import io
import base64
import cairosvg
import os


class PNG2SVG2PNGNode :
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required" : {"image" : ("IMAGE",)}
            }
    RETURN_TYPES = ({"svg" : "STRING", "image" : "IMAGE"})
    FUNCTION = "png2svg2png"
    CATEGORY = "image"
    OUTPUT_NODE = True

    def png2svg2png(self, image, api_key):
            # 이미지를 SVG로 변환
            image = Image.open(io.BytesIO(base64.b64decode(image)))

            # 투명 배경을 흰색으로 변환
            if image.mode == 'RGBA':
                background = Image.new('RGBA', image.size, (255, 255, 255))
                image = Image.alpha_composite(background, image).convert('RGB')

            # PIL 이미지를 BMP 바이너리 데이터로 변환
            bmp_io = io.BytesIO()
            image.save(bmp_io, format='BMP')
            bmp_data = bmp_io.getvalue()

            # potrace를 사용하여 BMP를 SVG로 변환
            bmp_file_path = '/tmp/temp.bmp'
            svg_file_path = '/tmp/temp_svg.svg'

            with open(bmp_file_path, 'wb') as bmp_file:
                bmp_file.write(bmp_data)

            # BMP 파일을 SVG 파일로 변환
            cairosvg.svg2png(url=svg_file_path, write_to=svg_file_path)

            with open(svg_file_path, 'rb') as svg_file:
                svg_data = svg_file.read()

            output_image_svg = Image.open(io.BytesIO(svg_data))
            # SVG 데이터를 PNG로 변환하여 PIL 이미지로 읽기
            png_data = cairosvg.svg2png(bytestring=svg_data, background_color=None)
            output_image_png = Image.open(io.BytesIO(png_data))

            # SVG 파일 삭제
            os.remove(svg_file_path)

            print("image", image)
            return(output_image_svg, output_image_png)
    
NODE_CLASS_MAPPINGS = {"PNG2SVG2PNG" : PNG2SVG2PNGNode}