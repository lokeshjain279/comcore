import streamlit as st
import requests

# Define the base API URLs
BARCODE_API_URL = "https://comcore.onrender.com/api/v1/product/lookup/"
IMAGE_API_URL = "https://comcore.onrender.com/api/v1/product/describe/"
SHOPIFY_SYNC_API_URL = "https://comcore.onrender.com/api/v1/shopify/sync/"

# BARCODE_API_URL = "http://localhost:8000/api/v1/product/lookup/"  # Endpoint for barcode lookup
# IMAGE_API_URL = "http://localhost:8000/api/v1/product/describe"  # Endpoint for image upload
# SHOPIFY_SYNC_API_URL = "http://localhost:8000/api/v1/shopify/sync"  # Endpoint for Shopify sync

# Initialize session state variables
if "product_data" not in st.session_state:
    st.session_state["product_data"] = {}
if "shopify_sync_message" not in st.session_state:
    st.session_state["shopify_sync_message"] = ""

# Function to clear product data
def clear_product_data():
    st.session_state["product_data"] = {}
    st.session_state["shopify_sync_message"] = ""

# Tabs for different functionalities
tab = st.sidebar.radio("Select functionality", ["Lookup by Barcode", "Upload Image"])

# Clear data when switching tabs
if "active_tab" not in st.session_state:
    st.session_state["active_tab"] = tab
elif st.session_state["active_tab"] != tab:
    st.session_state["active_tab"] = tab
    clear_product_data()

# Function to display product details for image-based lookup
def display_product_details_from_image():
    product_data = st.session_state["product_data"]
    st.write("### Product Details from Image")
    if not product_data:
        st.warning("No product data available.")
        return

    # Basic Information
    with st.expander("Basic Information", expanded=True):
        st.text_input("Title", value=product_data.get("Title", ""))
        st.text_area("Description", value=product_data.get("Description", ""))
        st.text_input("Brand", value=product_data.get("Brand", ""))
        st.text_input("Model Number", value=product_data.get("Model number", ""))
        st.text_input("ASIN", value=product_data.get("ASIN", ""))
        st.text_input("Manufacturer Part Number (MPN)", value=product_data.get("Manufacturer part number (MPN)", ""))
        st.text_input("Barcode Number", value=product_data.get("Barcode number", ""))
        st.text_input("Barcode Formats", value=product_data.get("Barcode formats", ""))
        st.text_input("Category", value=product_data.get("Category", ""))
        st.text_input("Color", value=product_data.get("Color", ""))
        st.text_input("Size", value=product_data.get("Size", ""))
    
    # Material
    material_text = "\n".join(product_data.get("Material", []))
    with st.expander("Material"):
        st.text_area("Material", value=material_text)

    # Features
    features_text = "\n".join(product_data.get("Features", []))
    with st.expander("Features"):
        st.text_area("Additional Features", value=features_text)

    # Images
    if "Images" in product_data and product_data["Images"] != ["N/A"]:
        with st.expander("Images"):
            for image_url in product_data["Images"]:
                if image_url != "N/A":
                    st.image(image_url, width=150)
                else:
                    st.write("No images available")

    # Shopify Sync Button
    if st.button("Sync to Shopify"):
        sync_to_shopify(product_data)

    # Display Shopify sync result message if available
    if st.session_state["shopify_sync_message"]:
        st.write(st.session_state["shopify_sync_message"])

# Function to display product details for barcode-based lookup
def display_product_details():
    product_data = st.session_state["product_data"]
    st.write("### Product Details from Barcode")
    if not product_data:
        st.warning("No product data available.")
        return

    # Basic Information
    with st.expander("Basic Information", expanded=True):
        title = st.text_input("Title", value=product_data.get("title", ""))
        description = st.text_area("Description", value=product_data.get("description", ""))
        price = st.text_input("Price", value=str(product_data.get("price", "")))
        sku = st.text_input("SKU", value=product_data.get("sku", ""))

    # Specifications
    with st.expander("Specifications"):
        manufacturer = st.text_input("Manufacturer", value=product_data.get("manufacturer", ""))
        category = st.text_input("Category", value=product_data.get("category", ""))
        model = st.text_input("Model", value=product_data.get("model", ""))
        brand = st.text_input("Brand", value=product_data.get("brand", ""))

    # Dimensions and Weight
    with st.expander("Dimensions and Weight"):
        length = st.text_input("Length", value=str(product_data.get("length", "")))
        width = st.text_input("Width", value=str(product_data.get("width", "")))
        height = st.text_input("Height", value=str(product_data.get("height", "")))
        weight = st.text_input("Weight", value=str(product_data.get("weight", "")))

    # Additional Features
    features_text = "\n".join(product_data.get("features", []))  # Join features into a single string
    with st.expander("Additional Features"):
        st.text_area("Features", value=features_text)

    # Images
    if "images" in product_data:
        with st.expander("Images"):
            for image_url in product_data["images"]:
                st.image(image_url, width=150)

    # Shopify Sync Button
    if st.button("Sync to Shopify"):
        sync_to_shopify(product_data)

    # Display Shopify sync result message if available
    if st.session_state["shopify_sync_message"]:
        st.write(st.session_state["shopify_sync_message"])

# Function to sync product data to Shopify
def sync_to_shopify(product_data):
    # Prepare payload for Shopify sync
    sync_payload = {
        "title": product_data.get("Title", product_data.get("title", "")),
        "description": product_data.get("Description", product_data.get("description", "")),
        "brand": product_data.get("Brand", product_data.get("brand", "")),
        "category": product_data.get("Category", product_data.get("category", ""))
    }

    # Call the Shopify sync FastAPI endpoint
    with st.spinner("Syncing product to Shopify..."):
        try:
            response = requests.post(SHOPIFY_SYNC_API_URL, json=sync_payload)
            if response.status_code == 200:
                st.session_state["shopify_sync_message"] = "Product synced successfully with Shopify!"
                st.session_state["shopify_sync_message"] += f"\nShopify Response: {response.json()}"
            else:
                st.session_state["shopify_sync_message"] = f"Failed to sync with Shopify: {response.status_code}"
                st.session_state["shopify_sync_message"] += f"\nError Details: {response.json().get('detail', 'No further details available')}"
        except Exception as e:
            st.session_state["shopify_sync_message"] = f"Error calling Shopify sync API: {e}"

# Barcode Lookup functionality
if tab == "Lookup by Barcode":
    st.subheader("🔍 Lookup Product by Barcode")
    barcode = st.text_input("Enter Product Barcode")
    if st.button("Fetch Product Details"):
        if barcode:
            try:
                # Call barcode API
                # response = requests.get(f"{BARCODE_API_URL}?barcode={barcode}")
                response = requests.get(f"{BARCODE_API_URL}{barcode}")
                if response.status_code == 200 and "product_data" in response.json():
                    st.session_state["product_data"] = response.json().get("product_data", {})
                    st.session_state["shopify_sync_message"] = ""
                else:
                    st.error("Product not found or error in fetching data.")
            except Exception as e:
                st.error(f"Error calling barcode API: {e}")
        else:
            st.warning("Please enter a valid barcode.")

    # Display product details if fetched
    if "product_data" in st.session_state and st.session_state["product_data"]:
        display_product_details()

# Image Upload functionality
elif tab == "Upload Image":
    st.subheader("📸 Upload Product Image")
    uploaded_file = st.file_uploader("Choose a product image", type=["jpg", "jpeg", "png"])
    if st.button("Fetch Product Details from Image"):
        if uploaded_file:
            try:
                files = {"image": uploaded_file}
                response = requests.post(IMAGE_API_URL, files=files)
                if response.status_code == 200 and "product_data" in response.json():
                    st.session_state["product_data"] = response.json().get("product_data", {})
                    st.session_state["shopify_sync_message"] = ""
                else:
                    st.error("Error in fetching data or processing image.")
            except Exception as e:
                st.error(f"Error calling image API: {e}")
        else:
            st.warning("Please upload a valid image file.")

    # Display product details if fetched
    if "product_data" in st.session_state and st.session_state["product_data"]:
        display_product_details_from_image()
