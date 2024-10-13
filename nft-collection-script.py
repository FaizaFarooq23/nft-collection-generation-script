import os
import json
import random
from PIL import Image
from itertools import product

# Paths to folders containing the image layers
background_folder = "BG/"
body_folder = "Body/"
goggles_folder = "Goggles/"
helmet_folder = "Helmet/"

# Base IPFS URL for image links
base_image_url = "https://ipfs.arbornft.io/robusnipe/"

# Output folder for generated NFTs
output_base_folder = "robusnipe-{}/"
os.makedirs(output_base_folder.format(1), exist_ok=True)

def get_all_images_from_folder(folder_path):
    """Returns all image files from a given folder as a list of file paths and their trait values."""
    images = [f for f in os.listdir(folder_path) if f.endswith(('png', 'jpg', 'jpeg'))]
    if not images:
        raise ValueError(f"No images found in folder: {folder_path}")
    return [(os.path.join(folder_path, img), os.path.splitext(img)[0]) for img in images]

def generate_nft(nft_id, folder_id, background_image, body_image, helmet_image, goggles_image):
    """Generates a single NFT by combining specific image parts and saves both image and metadata."""
    # Open images from different layers and collect trait values
    background, background_trait = background_image
    body, body_trait = body_image
    helmet, helmet_trait = helmet_image
    goggles, goggles_trait = goggles_image

    # Open images
    background_img = Image.open(background).convert("RGBA")
    body_img = Image.open(body).convert("RGBA")
    helmet_img = Image.open(helmet).convert("RGBA")
    goggles_img = Image.open(goggles).convert("RGBA")

    # Create a blank canvas with the size of the background image
    canvas = Image.new("RGBA", background_img.size)

    # Paste layers in order
    canvas.paste(background_img, (0, 0), background_img)
    canvas.paste(body_img, (0, 0), body_img)
    canvas.paste(helmet_img, (0, 0), helmet_img)
    canvas.paste(goggles_img, (0, 0), goggles_img)

    # Convert to RGB and save as PNG
    final_image = canvas.convert("RGB")

    # Define image and metadata paths
    nft_image_filename = f"robusnipe{nft_id}.png"
    nft_image_path = os.path.join(output_base_folder.format(folder_id), "images", nft_image_filename)
    
    # Ensure directory structure for images and metadata
    os.makedirs(os.path.dirname(nft_image_path), exist_ok=True)
    
    # Save the image
    final_image.save(nft_image_path, "PNG")

    # Generate and save metadata
    metadata = {
        "name": f"Robusnipe{nft_id}",
        "description": (
            "Robusnipe nft collection is a set of 10,000 unique NFTs."
            "Each NFT is a combination of a background, body, helmet, and goggles."
        ),
        "external_url": base_image_url,
        "image": f"{base_image_url}robusnipe{nft_id}.png",
        "attributes": [
            {"trait_type": "Background", "value": background_trait},
            {"trait_type": "body", "value": body_trait},
            {"trait_type": "helmet", "value": helmet_trait},
            {"trait_type": "goggles", "value": goggles_trait},
        ],
        "properties": {
            "files": [
                {
                    "uri": f"{base_image_url}robusnipe{nft_id}.png",
                    "type": "image/png"
                }
            ],
            "category": "image",
            "creators": []
        },
        "compiler": "NFTexport.io"
    }

    # Define and save metadata
    metadata_filename = f"robusnipe{nft_id}.json"
    metadata_path = os.path.join(output_base_folder.format(folder_id), "metadata", metadata_filename)
    os.makedirs(os.path.dirname(metadata_path), exist_ok=True)
    
    with open(metadata_path, 'w') as metadata_file:
        json.dump(metadata, metadata_file, indent=4)

    # Close images to free memory
    background_img.close()
    body_img.close()
    helmet_img.close()
    goggles_img.close()

def generate_nft_collection(num_nfts):
    """Generates a collection of NFTs with unique trait combinations."""
    folder_counter = 1
    nft_counter = 1

    # Load all image options from each folder
    backgrounds = get_all_images_from_folder(background_folder)
    bodys = get_all_images_from_folder(body_folder)
    helmets = get_all_images_from_folder(helmet_folder)
    goggles = get_all_images_from_folder(goggles_folder)

    # Calculate total possible combinations
    total_combinations = len(backgrounds) * len(bodys) * len(helmets) * len(goggles)

    if num_nfts > total_combinations:
        raise ValueError(f"Requested {num_nfts} NFTs, but only {total_combinations} unique combinations available.")

    # Generate all unique trait combinations
    all_combinations = list(product(backgrounds, bodys, helmets, goggles))

    # Shuffle combinations for randomness
    random.shuffle(all_combinations)

    # Generate the requested number of NFTs
    for combo in all_combinations[:num_nfts]:
        background_image, body_image, helmet_image, goggles_image = combo
        generate_nft(nft_counter, folder_counter, background_image, body_image, helmet_image, goggles_image)
        print(f"Generated NFT {nft_counter} in folder robusnipe-{folder_counter}")
        
        # Create a new folder after every 100 NFTs
        if nft_counter % 100 == 0:
            folder_counter += 1
        
        nft_counter += 1

if __name__ == "__main__":
    num_nfts = 10000  # Set the number of NFTs to generate
    generate_nft_collection(num_nfts)
