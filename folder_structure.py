import os
import shutil
from random import shuffle

# Set the paths
main_dir = "PlantVillage"
output_dir = "Structured_PlantVillageOne"
dummy_class_dir = "dummy_class"  # New directory for unlabelled images

# Create the main output directory if it does not exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Create the unlabelled directory if it does not exist
unlabelled_dir = os.path.join(output_dir, "unlabelled")
dummy_class_path = os.path.join(unlabelled_dir, dummy_class_dir)
if not os.path.exists(dummy_class_path):
    os.makedirs(dummy_class_path)

# Get all class names
classes = [d for d in os.listdir(
    main_dir) if os.path.isdir(os.path.join(main_dir, d))]

for cls in classes:
    class_dir = os.path.join(main_dir, cls)
    all_images = [f for f in os.listdir(
        class_dir) if os.path.isfile(os.path.join(class_dir, f))]
    shuffle(all_images)  # Randomize the images

    # Calculate the count for train, test, and validation
    total_images = len(all_images)
    train_count = int(total_images * 0.15)
    test_count = int(total_images * 0.10)
    validation_count = int(total_images * 0.05)

    # Split the images into train, test, and validation
    train_images = all_images[:train_count]
    test_images = all_images[train_count:train_count + test_count]
    validation_images = all_images[train_count +
                                   test_count:train_count + test_count + validation_count]

    # Define paths for train, test, and validation
    train_dir = os.path.join(output_dir, "train", cls)
    test_dir = os.path.join(output_dir, "test", cls)
    validation_dir = os.path.join(output_dir, "validation", cls)

    # Create directories if they don't exist
    if not os.path.exists(train_dir):
        os.makedirs(train_dir)
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    if not os.path.exists(validation_dir):
        os.makedirs(validation_dir)

    # Copy the labelled images to their respective directories
    for img in train_images:
        shutil.copy(os.path.join(class_dir, img), train_dir)
    for img in test_images:
        shutil.copy(os.path.join(class_dir, img), test_dir)
    for img in validation_images:
        shutil.copy(os.path.join(class_dir, img), validation_dir)

    # The rest of the images are considered unlabelled
    unlabelled_images = all_images[train_count +
                                   test_count + validation_count:]

    # Move the unlabelled images to the dummy_class directory and rename them
    for img in unlabelled_images:
        # Prepend the class name to the image filename
        new_name = f"{cls}_{img}"
        img_path = os.path.join(class_dir, img)
        shutil.move(img_path, os.path.join(dummy_class_path, new_name))

print("done")