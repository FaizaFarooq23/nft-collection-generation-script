import os
import json
import random
from PIL import Image
from itertools import product

# Paths to folders containing the image layers
background_folder = "BG/"
exhaust_folder = "Exhaust/"
guns_folder = "Guns/"
trunk_folder = "Trunk/"
wings_folder = "Wings/"

# Base IPFS URL for image links
base_image_url = "https://ipfs.arbornft.io/fight4hope/"

# Output folder for generated NFTs
output_base_folder = "fight4hope-{}/"
os.makedirs(output_base_folder.format(1), exist_ok=True)

def get_all_images_from_folder(folder_path):
    """Returns all image files from a given folder as a list of file paths and their trait values."""
    images = [f for f in os.listdir(folder_path) if f.endswith(('png', 'jpg', 'jpeg'))]
    if not images:
        raise ValueError(f"No images found in folder: {folder_path}")
    return [(os.path.join(folder_path, img), os.path.splitext(img)[0]) for img in images]

def generate_nft(nft_id, folder_id, background_image, wings_image, exhaust_image, trunk_image, guns_image):
    """Generates a single NFT by combining specific image parts and saves both image and metadata."""
    # Open images from different layers and collect trait values
    background, background_trait = background_image
    wings, wings_trait = wings_image
    exhaust, exhaust_trait = exhaust_image
    trunk, trunk_trait = trunk_image
    guns, guns_trait = guns_image

    # Open images
    background_img = Image.open(background).convert("RGBA")
    wings_img = Image.open(wings).convert("RGBA")
    exhaust_img = Image.open(exhaust).convert("RGBA")
    trunk_img = Image.open(trunk).convert("RGBA")
    guns_img = Image.open(guns).convert("RGBA")

    # Create a blank canvas with the size of the background image
    canvas = Image.new("RGBA", background_img.size)

    # Paste layers in order
    canvas.paste(background_img, (0, 0), background_img)
    canvas.paste(exhaust_img, (0, 0), exhaust_img)
    canvas.paste(trunk_img, (0, 0), trunk_img)
    canvas.paste(wings_img, (0, 0), wings_img)
    canvas.paste(guns_img, (0, 0), guns_img)

    # Convert to RGB and save as PNG
    final_image = canvas.convert("RGB")

    # Define image and metadata paths
    nft_image_filename = f"f4h{nft_id}.png"
    nft_image_path = os.path.join(output_base_folder.format(folder_id), "images", nft_image_filename)
    
    # Ensure directory structure for images and metadata
    os.makedirs(os.path.dirname(nft_image_path), exist_ok=True)
    
    # Save the image
    final_image.save(nft_image_path, "PNG")

    # Generate and save metadata
    metadata = {
        "name": f"F4H{nft_id}",
        "description": (
            "The Fight4Hope NFT collection consists of 10,000 unique spaceships, designed to offer players "
            "exclusive access to key gameplay features in the Fight4Hope universe. Each spaceship represents "
            "a crucial part of the game, allowing users to embark on space missions, engage in combat, and explore "
            "new galaxies. These NFTs are the key to unlocking higher levels of gameplay and rare in-game rewards."
        ),
        "external_url": base_image_url,
        "image": f"{base_image_url}f4h{nft_id}.png",
        "attributes": [
            {"trait_type": "Background", "value": background_trait},
            {"trait_type": "Wings", "value": wings_trait},
            {"trait_type": "Exhaust", "value": exhaust_trait},
            {"trait_type": "Trunk", "value": trunk_trait},
            {"trait_type": "Guns", "value": guns_trait},
        ],
        "properties": {
            "files": [
                {
                    "uri": f"{base_image_url}f4h{nft_id}.png",
                    "type": "image/png"
                }
            ],
            "category": "image",
            "creators": []
        },
        "compiler": "NFTexport.io"
    }

    # Define and save metadata
    metadata_filename = f"f4h{nft_id}.json"
    metadata_path = os.path.join(output_base_folder.format(folder_id), "metadata", metadata_filename)
    os.makedirs(os.path.dirname(metadata_path), exist_ok=True)
    
    with open(metadata_path, 'w') as metadata_file:
        json.dump(metadata, metadata_file, indent=4)

    # Close images to free memory
    background_img.close()
    wings_img.close()
    exhaust_img.close()
    trunk_img.close()
    guns_img.close()

def generate_nft_collection(num_nfts):
    """Generates a collection of NFTs with unique trait combinations."""
    folder_counter = 1
    nft_counter = 1

    # Load all image options from each folder
    backgrounds = get_all_images_from_folder(background_folder)
    wings = get_all_images_from_folder(wings_folder)
    exhausts = get_all_images_from_folder(exhaust_folder)
    trunks = get_all_images_from_folder(trunk_folder)
    guns = get_all_images_from_folder(guns_folder)

    # Generate all possible combinations of traits
    all_combinations = list(product(backgrounds, wings, exhausts, trunks, guns))

    # Shuffle the combinations to add randomness
    random.shuffle(all_combinations)

    # Ensure that we are not generating more NFTs than possible unique combinations
    if num_nfts > len(all_combinations):
        raise ValueError(f"Requested {num_nfts} NFTs, but only {len(all_combinations)} unique combinations are available.")

    # Generate NFTs from the shuffled combinations
    for combo in all_combinations[:num_nfts]:
        background, wings, exhaust, trunk, guns = combo
        generate_nft(nft_counter, folder_counter, background, wings, exhaust, trunk, guns)
        print(f"Generated NFT {nft_counter} in folder fight4hope-{folder_counter}")
        
        # Create a new folder after every 100 NFTs
        if nft_counter % 100 == 0:
            folder_counter += 1
        
        nft_counter += 1

if __name__ == "__main__":
    num_nfts = 10000  # Set the number of NFTs to generate
    generate_nft_collection(num_nfts)
