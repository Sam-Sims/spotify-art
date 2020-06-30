from PIL import Image as image


def evaluate(averages):
    print(averages)
    if averages['mode'] == 0:
        sky = "night"
    else:
        sky = "day"

    if averages['bpm'] < 90:
        forest = "sparse"
    elif 90 < averages['bpm'] < 120:
        forest = "medium"
    elif averages['bpm'] > 120:
        forest = 'dense'

    if averages['popularity'] < 40:
        balloons = "sparse"
    elif 40 < averages['bpm'] < 65:
        balloons = "medium"
    elif averages['bpm'] > 65:
        balloons = 'dense'

    evaluation = {
        "sky": sky,
        "forest": forest,
        "balloons": balloons
    }
    print(evaluation)
    return evaluation


def construct_image(evaluation):
    background_path = "./static/assets/background/" + evaluation['sky'] + "-background.png"
    background_image = image.open(background_path)
    tree_path = "./static/assets/trees/trees-" + evaluation['forest'] + "-pine.png"
    tree_image = image.open(tree_path)
    balloon_path = "./static/assets/balloons/" + evaluation['balloons'] + "-balloon.png"
    balloon_image = image.open(balloon_path)
    background_image.paste(tree_image, (0, 0), tree_image)
    background_image.paste(balloon_image, (0, 0), balloon_image)
    background_image.save('test.png', "PNG")
    return background_image


