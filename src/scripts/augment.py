import cv2
import os
import random
import numpy as np
import sys

def adjust_brightness(image, factor):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv = np.array(hsv, dtype=np.float64)
    hsv[:,:,1] = hsv[:,:,1] * factor
    hsv[:,:,1][hsv[:,:,1] > 255] = 255
    hsv[:,:,2] = hsv[:,:,2] * factor
    hsv[:,:,2][hsv[:,:,2] > 255] = 255
    hsv = np.array(hsv, dtype=np.uint8)
    image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return image

def adjust_contrast(image, factor):
    alpha = factor
    new_image = cv2.convertScaleAbs(image, alpha=alpha, beta=0)
    return new_image

def random_flip_mirror(image):
    flip_code = -1
    if random.choice([True, False]):
        flip_code = 1 if random.choice([True, False]) else 0
        image = cv2.flip(image, flip_code)
    return image, flip_code

def random_rotate(image):
    angle = random.uniform(-30, 30)
    (h, w) = image.shape[:2]
    center = (w / 2, h / 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h))
    return rotated, angle

def add_curved_distortion(image):
    height, width = image.shape[:2]
    # Create a slight barrel distortion
    K = np.array([[width, 0, width / 2], [0, width, height / 2], [0, 0, 1]], dtype=np.float32)
    D = np.array([0.0005, 0.0005, 0, 0], dtype=np.float32)  # Small distortion coefficients for minimal effect
    map1, map2 = cv2.initUndistortRectifyMap(K, D, np.eye(3, dtype=np.float32), K, (width, height), cv2.CV_32FC1)
    distorted = cv2.remap(image, map1, map2, cv2.INTER_LINEAR)
    return distorted

def augment_image(image, augmentations_to_apply, mode):
    augmentations = []
    applied_any_augmentation = False

    if mode == 'automatic':
        if 'brightness' in augmentations_to_apply and (random.choice([True, False]) or not applied_any_augmentation):
            factor = 0.7 + random.random() * 0.4
            image = adjust_brightness(image, factor)
            augmentations.append(f"brightness_{factor:.2f}")
            applied_any_augmentation = True

        if 'contrast' in augmentations_to_apply and (random.choice([True, False]) or not applied_any_augmentation):
            factor = 0.8 + random.random() * 0.3
            image = adjust_contrast(image, factor)
            augmentations.append(f"contrast_{factor:.2f}")
            applied_any_augmentation = True

        if 'flip' in augmentations_to_apply and (random.choice([True, False]) or not applied_any_augmentation):
            image, flip_code = random_flip_mirror(image)
            if flip_code != -1:
                augmentations.append(f"flip_{flip_code}")
                applied_any_augmentation = True

        if 'rotate' in augmentations_to_apply and (random.choice([True, False]) or not applied_any_augmentation):
            image, angle = random_rotate(image)
            augmentations.append(f"rotate_{angle:.2f}")
            applied_any_augmentation = True

        if 'distortion' in augmentations_to_apply and (random.choice([True, False]) or not applied_any_augmentation):
            image = add_curved_distortion(image)
            augmentations.append("distortion")
            applied_any_augmentation = True

    elif mode == 'manual':
        if 'brightness' in augmentations_to_apply:
            factor = 0.7 + random.random() * 0.4
            image = adjust_brightness(image, factor)
            augmentations.append(f"brightness_{factor:.2f}")

        if 'contrast' in augmentations_to_apply:
            factor = 0.8 + random.random() * 0.3
            image = adjust_contrast(image, factor)
            augmentations.append(f"contrast_{factor:.2f}")

        if 'flip' in augmentations_to_apply:
            image, flip_code = random_flip_mirror(image)
            if flip_code != -1:
                augmentations.append(f"flip_{flip_code}")

        if 'rotate' in augmentations_to_apply:
            image, angle = random_rotate(image)
            augmentations.append(f"rotate_{angle:.2f}")

        if 'distortion' in augmentations_to_apply:
            image = add_curved_distortion(image)
            augmentations.append("distortion")

    return image, augmentations

def augment_images(base_path, output_path, sub_dir, augmentations_to_apply, mode):
    sub_dir_path = os.path.join(base_path, sub_dir)
    output_sub_dir_path = os.path.join(output_path, sub_dir)
    os.makedirs(output_sub_dir_path, exist_ok=True)

    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif')

    print(f"Processing directory: {sub_dir_path}")
    print(f"Saving to directory: {output_sub_dir_path}")
    
    for file_name in os.listdir(sub_dir_path):
        if file_name.lower().endswith(valid_extensions):
            file_path = os.path.join(sub_dir_path, file_name)
            image = cv2.imread(file_path)
            
            if image is not None:
                augmented_image, applied_augmentations = augment_image(image, augmentations_to_apply, mode)
                augmentation_str = '_'.join(applied_augmentations)
                output_file_name = f"{os.path.splitext(file_name)[0]}_{augmentation_str}.jpg"
                output_file_path = os.path.join(output_sub_dir_path, output_file_name)
                cv2.imwrite(output_file_path, augmented_image)
                print(f"Saved: {output_file_path}")
            else:
                print(f"Error reading image {file_path}")
        else:
            print(f"Skipping file {file_name} as it does not have a valid image extension")

if __name__ == "__main__":
    if '--help' in sys.argv:
        print("Usage: python augment.py <mode> <augmentation1> <augmentation2> ...")
        print("Modes:")
        print("  automatic - Apply augmentations randomly")
        print("  manual - Apply all specified augmentations")
        print("Available augmentations:")
        print("  brightness - Adjusts the brightness of the images.")
        print("  contrast - Adjusts the contrast of the images.")
        print("  flip - Randomly flips the images horizontally or vertically.")
        print("  rotate - Randomly rotates the images.")
        print("  distortion - Adds a slight curve to the images.")
        sys.exit(0)

    if len(sys.argv) < 3:
        print("Usage: python augment.py <mode> <augmentation1> <augmentation2> ...")
        sys.exit(1)

    mode = sys.argv[1]
    augmentations_to_apply = sys.argv[2:]
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(current_dir, '../../data/raw')
    output_path = os.path.join(current_dir, '../../data/augmentations')
    
    sub_dirs = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    
    for sub_dir in sub_dirs:
        print(f"Starting augmentation for {sub_dir}.")
        augment_images(base_path, output_path, sub_dir, augmentations_to_apply, mode)
