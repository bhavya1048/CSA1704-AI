import cv2
import numpy as np
from skimage.feature import graycomatrix, graycoprops

def analyze_image(path):
    img = cv2.imread(path)

    if img is None:
        raise ValueError("Could not read the selected image.")

    # Resize
    img = cv2.resize(img, (500, 500))

    # RGB -> HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Simple green leaf mask
    lower_green = np.array([25, 30, 30])
    upper_green = np.array([95, 255, 255])
    leaf_mask = cv2.inRange(hsv, lower_green, upper_green)

    leaf_pixels = cv2.countNonZero(leaf_mask)

    if leaf_pixels == 0:
        raise ValueError("Leaf could not be detected. Use a clear green leaf image.")

    # Candidate lesion mask:
    # dark/brown regions inside the leaf
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    dark_mask = cv2.inRange(hsv, np.array([0, 35, 0]),
                                  np.array([179, 255, 150]))

    lesion_mask = cv2.bitwise_and(dark_mask, leaf_mask)

    # Remove small noise
    kernel = np.ones((5, 5), np.uint8)
    lesion_mask = cv2.morphologyEx(lesion_mask, cv2.MORPH_OPEN, kernel)

    lesion_pixels = cv2.countNonZero(lesion_mask)
    lesion_area = (lesion_pixels / leaf_pixels) * 100

    # Mean HSV in lesion region
    if lesion_pixels > 0:
        h_mean, s_mean, v_mean = cv2.mean(hsv, mask=lesion_mask)[:3]
    else:
        h_mean, s_mean, v_mean = 0, 0, 0

    # Contours and lesion count
    contours, _ = cv2.findContours(
        lesion_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    min_contour_area = 30
    valid = [c for c in contours if cv2.contourArea(c) >= min_contour_area]
    lesion_count = len(valid)

    # Average compactness
    compactness_values = []

    for c in valid:
        area = cv2.contourArea(c)
        perimeter = cv2.arcLength(c, True)

        if perimeter > 0:
            compactness = (4 * np.pi * area) / (perimeter ** 2)
            compactness_values.append(compactness)

    compactness = (
        float(np.mean(compactness_values))
        if compactness_values else 0.0
    )

    # GLCM contrast
    if lesion_pixels > 0:
        roi = cv2.bitwise_and(gray, gray, mask=lesion_mask)
        values = gray[lesion_mask > 0]

        if len(values) > 10:
            small = cv2.normalize(
                roi, None, 0, 7, cv2.NORM_MINMAX
            ).astype(np.uint8)

            glcm = graycomatrix(
                small,
                distances=[1],
                angles=[0],
                levels=8,
                symmetric=True,
                normed=True
            )

            contrast = float(graycoprops(glcm, "contrast")[0, 0])
            homogeneity = float(graycoprops(glcm, "homogeneity")[0, 0])
        else:
            contrast = 0.0
            homogeneity = 1.0
    else:
        contrast = 0.0
        homogeneity = 1.0

    # Convert OpenCV hue 0-179 to degrees 0-360
    mean_hue_degrees = h_mean * 2

    # Create symbolic facts
    facts = {}

    if lesion_area < 5:
        facts["lesion_area"] = "low"
    elif lesion_area < 15:
        facts["lesion_area"] = "medium"
    else:
        facts["lesion_area"] = "high"

    if lesion_pixels == 0 or lesion_area < 2:
        facts["lesion_colour"] = "none"
    elif 10 <= mean_hue_degrees <= 30:
        facts["lesion_colour"] = "brown"
    elif 30 < mean_hue_degrees <= 80:
        facts["lesion_colour"] = "yellow-green"
    else:
        facts["lesion_colour"] = "dark-green/brown"

    if lesion_count >= 10:
        facts["lesion_count"] = "high"
    elif lesion_count >= 3:
        facts["lesion_count"] = "medium"
    else:
        facts["lesion_count"] = "low"

    if compactness > 0.55:
        facts["lesion_shape"] = "compact"
    elif compactness > 0.25:
        facts["lesion_shape"] = "irregular"
    else:
        facts["lesion_shape"] = "angular"

    if contrast > 35:
        facts["texture"] = "water-soaked"
    else:
        facts["texture"] = "structured"

    # Approximate halo fact
    if facts["lesion_colour"] == "brown" and lesion_area >= 8:
        facts["halo_colour"] = "yellow"
    else:
        facts["halo_colour"] = "none"

    # Approximate edge-growth fact
    facts["edge_growth"] = "white-mould" if homogeneity < 0.25 and lesion_area > 15 else "none"

    features = {
        "Lesion Area %": round(lesion_area, 2),
        "Mean Hue (degrees)": round(mean_hue_degrees, 2),
        "Mean Saturation": round(s_mean, 2),
        "Mean Value": round(v_mean, 2),
        "Lesion Count": lesion_count,
        "Shape Compactness": round(compactness, 3),
        "GLCM Contrast": round(contrast, 3),
        "GLCM Homogeneity": round(homogeneity, 3)
    }

    return features, facts
