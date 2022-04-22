from PIL import Image
import cairo

# Turn the image into paths
def generate_paths(img, path_width):
    # Reduce to the pixel size
    img = img.convert('RGB')
    img_size = img.size
    reduced_size = (img_size[0] // path_width, img_size[1] // path_width)
    img_reduced = img.resize(reduced_size, Image.Resampling.NEAREST)

    possible_colors = [data[1] for data in img.getcolors()]

    # Iterate over pixels to generate rudimentry paths of single colours
    paths = []

    for x in range(img_reduced.size[0]):
        path_start = (x, 0)
        current_color = (255,255,0)

        # Move vertically until reaching a new colour or the end
        for y in range(img_reduced.size[1]):

            pixel_color = img_reduced.getpixel((x,y))

            assert pixel_color in possible_colors, "pixel_color set to {0}".format(pixel_color)

            if pixel_color != current_color or y == (img_reduced.size[1] - 1):
                paths.append((path_start, (x,y), current_color))
        
                current_color = pixel_color

                path_start = (x,y)
            

    return paths, reduced_size

def visualise_paths(paths, size):
    with cairo.SVGSurface("path_visualisation.svg", size[0], size[1]) as surface:
        context = cairo.Context(surface)
        
        context.set_line_width(0.75)

        for path in paths:
            start = path[0]
            end = path[1]
            color = path[2] # Color index stored in last element of the path
            context.set_source_rgba(color[0] / 255, color[1] / 255, color[2] / 255, 1)
            context.move_to(start[0], start[1])
            context.line_to(end[0], end[1])
            context.stroke()

pixel_size = 10
processed_img = Image.open('output.png')
paths, paths_size = generate_paths(processed_img, pixel_size)
visualise_paths(paths, paths_size)