import io

import streamlit as st
from PIL import Image, ImageOps
import numpy as np
import cv2

# Function to apply selected filter

def apply_filter(image, filter_name, filter_params=None):
    if filter_name == 'Scaling':
        return apply_scaling_filter(image, filter_params['scale_factor'])
    elif filter_name == 'Rotation':
        return apply_rotation_filter(image, filter_params['rotation_angle'])
    elif filter_name == 'Translation':
        return apply_translation_filter(image, filter_params['x_translation'], filter_params['y_translation'])
    elif filter_name == 'Shearing':
        return apply_shearing_filter(image, filter_params['x_shear'], filter_params['y_shear'])

# Function to apply the Scaling filter
def apply_scaling_filter(image, scale_factor):
    width, height = image.size
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    scaled_image = image.resize((new_width, new_height))
    return scaled_image

# Function to apply the Rotation filter
def apply_rotation_filter(image, angle):
    return image.rotate(angle, resample=Image.BICUBIC, expand=True)

# Function to apply the Translation filter
def apply_translation_filter(image, x_translation, y_translation):
    return image.transform(image.size, Image.AFFINE, (1, 0, x_translation, 0, 1, y_translation))

# Function to apply the Shearing filter
def apply_shearing_filter(image, x_shear, y_shear):
    return image.transform(image.size, Image.AFFINE, (1, x_shear, 0, y_shear, 1, 0))

# Streamlit app
st.title('Image Transformation App')
st.sidebar.header('Settings')

# Upload an image
uploaded_image = st.file_uploader('Upload an image', type=['jpg', 'png', 'jpeg'])

if uploaded_image is not None:
    try:
        # Use PIL to open the uploaded image
        image = Image.open(uploaded_image)

        if image is not None:
            # Display the original image
            st.image(image, use_column_width=True, caption='Original Image')

            # Choose a filter
            filter_name = st.selectbox('Select a filter', ['Select','Scaling', 'Rotation', 'Translation', 'Shearing'])

            filter_params = {} 
            if filter_name == 'Scaling':
                filter_params['scale_factor'] = st.slider('Scale Factor', 0.1, 2.0, 1.0)
            elif filter_name == 'Rotation':
                filter_params['rotation_angle'] = st.slider('Rotation Angle (degrees)', -180.0, 180.0, 0.0)
            elif filter_name == 'Translation':
                filter_params['x_translation'] = st.slider('X-Translation', -100, 100, 0)
                filter_params['y_translation'] = st.slider('Y-Translation', -100, 100, 0)
            elif filter_name == 'Shearing':
                filter_params['x_shear'] = st.slider('X-Shear', -1.0, 1.0, 0.0)
                filter_params['y_shear'] = st.slider('Y-Shear', -1.0, 1.0, 0.0)

            if st.button('Apply Filter'):
                filtered_image = apply_filter(image, filter_name, filter_params)
                st.image(filtered_image, use_column_width=True, caption=f'{filter_name} Filtered Image')

                # Add a download button for the filtered image
                filtered_image_bytes = io.BytesIO()
                filtered_image.save(filtered_image_bytes, format='PNG')
                st.download_button('Download Filtered Image', filtered_image_bytes.getvalue(), 'filtered_image.png', 'image/png')

        else:
            st.warning('Invalid image format. Please upload a valid image file.')
    except Exception as e:
        st.error(f'An error occurred: {str(e)}')

