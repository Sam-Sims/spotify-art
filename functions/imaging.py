from PIL import Image as image

def construct_image(evaluation):
    background_path = "./static/assets/background/" + evaluation['sky'] + "-background.png"
    background_image = image.open(background_path)
    tree_path = "./static/assets/trees/trees-" + evaluation['forest'] + "-pine.png"
    tree_image = image.open(tree_path)
    balloon_path = "./static/assets/balloons/" + evaluation['balloons'] + "-balloon.png"
    balloon_image = image.open(balloon_path)
    mountain_path = "./static/assets/mountain/fuji-" + evaluation['mountain'] + ".png"
    mountain_image = image.open(mountain_path)
    background_image.paste(tree_image, (0, 0), tree_image)
    background_image.paste(balloon_image, (0, 0), balloon_image)
    background_image.paste(mountain_image, (0, 0), mountain_image)
    background_image.save('test.png', "PNG")
    return background_image


