from PIL import Image as image

dict_of_values = {
    "name": "Cooler",
    "artist_name": "Gleemer",
    "popularity": 0.34
}

def combine():
    if dict_of_values["popularity"] < 0.4:
        im1 = image.open('../static/assets/night-background.png')
        im2 = image.open('../static/assets/forest/trees-medium-pine.png')
        im1.paste(im2, (0,0), im2)
        im1.save('test.png', 'PNG')

combine()