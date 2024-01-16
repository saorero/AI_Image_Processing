import cv2
import os

def split_image(input_image_path, output_folder, tile_size):
    # Read the input image
    image = cv2.imread(input_image_path)

    # Get the dimensions of the image
    height, width, _ = image.shape

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through the image and create tiles
    for i in range(0, height, tile_size):
        for j in range(0, width, tile_size):
            # Extract the tile from the image
            tile = image[i:i+tile_size, j:j+tile_size]

            # Save the tile as a PNG image
            tile_name = f"tile_{i}_{j}.png"
            tile_path = os.path.join(output_folder, tile_name)
            cv2.imwrite(tile_path, tile)

if __name__ == "__main__":
    # Set the input image path, output folder, and tile size
    input_image_path = r"C:\Users\user\Downloads\learnTensor\janPic2015.png"
    output_folder = r"C:\Users\user\Downloads\learnTensor\3000"
    tile_size = 3000  # Adjust the tile size as needed

    # Call the function to split the image
    split_image(input_image_path, output_folder, tile_size)