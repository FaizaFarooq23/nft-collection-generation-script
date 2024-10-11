import os

# Create output directory if it doesn't exist
os.makedirs("output", exist_ok=True)

# Iterate through all folders in the current directory
for folder in os.listdir():
    if folder == "output":
        continue
    if os.path.isdir(folder):
        # Read all the files in the folder
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            if os.path.isdir(file_path):
                print(file_path)
                # Iterate through the contents of the subdirectory
                for file2 in os.listdir(file_path):
                    # Rename the file to the output directory
                    print(file2)
                    os.rename(os.path.join(file_path, file2), os.path.join("output", file2))
