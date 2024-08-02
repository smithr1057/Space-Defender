from PIL import Image

# Load the image
img = Image.open("alien_bullet.png")

# Save the image with the ICC profile removed
img.save("alien_bullet_fixed.png", icc_profile=None)

print("ICC profile removed and image saved as player_bullet_fixed.png")
