import streamlit as st
import requests

# Define the base API URLs
BARCODE_API_URL = "https://comcore.onrender.com/api/v1/product/lookup/"
IMAGE_API_URL = "https://comcore.onrender.com/api/v1/product/describe/"
SHOPIFY_SYNC_API_URL = "https://comcore.onrender.com/api/v1/shopify/sync/"

# Initialize session state variables
if "product_data" not in st.session_state:
    st.session_state["product_data"] = {}
if "shopify_sync_message" not in st.session_state:
    st.session_state["shopify_sync_message"] = ""

# Function to clear product data
def clear_product_data():
    st.session_state["product_data"] = {}
    st.session_state["shopify_sync_message"] = ""

# Title and Tagline
st.markdown(
    """
    <div style="text-align: center; padding: 20px; background-color: #f0f2f6; border-radius: 10px; margin-bottom: 20px;">
        <h1 style="color: #4A4A4A;">Comcore</h1>
        <p style="font-size: 18px; color: #6D6D6D;">
            AI-powered Product Data Enrichment Tool for Retailers
        </p>
        <p style="font-size: 14px; color: #8C8C8C;">
            Empowering businesses with instant, accurate, and comprehensive product information
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar for configuration
st.sidebar.title("Settings")

# Shopify Configuration Section
st.sidebar.subheader("Shopify Configuration")
shopify_url = st.sidebar.text_input("Shopify Store URL", value="https://your-shopify-store.myshopify.com")
shopify_token = st.sidebar.text_input("Shopify Access Token", type="password")

# General Settings Section
st.sidebar.subheader("General Settings")
enable_image_preview = st.sidebar.checkbox("Enable Image Preview", value=True)
output_format = st.sidebar.selectbox("Select Output Format", ["JSON", "CSV"])

# API Key Management Section
st.sidebar.subheader("API Key Management")
barcode_lookup_api_key = st.sidebar.text_input("Barcode Lookup API Key", type="password")
google_vision_api_key = st.sidebar.text_input("Google Vision API Key", type="password")

# Appearance Settings Section
st.sidebar.subheader("Appearance Settings")
theme = st.sidebar.radio("Theme", ["Light", "Dark"], index=0)
font_size = st.sidebar.slider("Font Size", min_value=12, max_value=24, value=16)

# Help & Support Section
st.sidebar.subheader("Help & Support")
st.sidebar.markdown("[📄 Documentation](https://your-documentation-url.com)")
st.sidebar.markdown("[❓ FAQ](https://your-faq-url.com)")
st.sidebar.markdown("[💬 Contact Support](mailto:support@yourcompany.com)")

# Display the entered Shopify URL in the main section for reference
st.write(f"Current Shopify URL: {shopify_url}")

# Functionality selection
tab = st.selectbox("Choose Functionality", ["🔍 Lookup by Barcode", "📸 Upload Image"])

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
    with st.expander("🔑 Basic Information", expanded=True):
        st.text_input("🏷️ Title", value=product_data.get("Title", ""))
        st.text_area("📄 Description", value=product_data.get("Description", ""))
        st.text_input("🏢 Brand", value=product_data.get("Brand", ""))
        st.text_input("🔢 Model Number", value=product_data.get("Model number", ""))
        st.text_input("🔗 ASIN", value=product_data.get("ASIN", ""))
        st.text_input("🔧 Manufacturer Part Number (MPN)", value=product_data.get("Manufacturer part number (MPN)", ""))
        st.text_input("🔍 Barcode Number", value=product_data.get("Barcode number", ""))
        st.text_input("📊 Barcode Formats", value=product_data.get("Barcode formats", ""))
        st.text_input("📂 Category", value=product_data.get("Category", ""))
        st.text_input("🎨 Color", value=product_data.get("Color", ""))
        st.text_input("📏 Size", value=product_data.get("Size", ""))
    
    # Material
    material_text = "\n".join(product_data.get("Material", []))
    with st.expander("🧵 Material"):
        st.text_area("Material", value=material_text)

    # Features
    features_text = "\n".join(product_data.get("Features", []))
    with st.expander("💡 Additional Features"):
        st.text_area("Features", value=features_text)

    # Images
    if "Images" in product_data and product_data["Images"] != ["N/A"]:
        with st.expander("📸 Images"):
            for image_url in product_data["Images"]:
                if image_url != "N/A":
                    st.image(image_url, width=150)
                else:
                    st.write("No images available")

    # Shopify Sync Button
    if st.button("🚀 Sync to Shopify"):
        st.success("Product successfully synced to Shopify!")
        # sync_to_shopify(product_data)

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
    with st.expander("🔑 Basic Information", expanded=True):
        st.text_input("🏷️ Title", value=product_data.get("title", ""))
        st.text_area("📄 Description", value=product_data.get("description", ""))
        st.text_input("💲 Price", value=str(product_data.get("price", "")))
        st.text_input("🔢 SKU", value=product_data.get("sku", ""))

    # Specifications
    with st.expander("📋 Specifications"):
        st.text_input("🏢 Manufacturer", value=product_data.get("manufacturer", ""))
        st.text_input("📂 Category", value=product_data.get("category", ""))
        st.text_input("🔢 Model", value=product_data.get("model", ""))
        st.text_input("🏢 Brand", value=product_data.get("brand", ""))

    # Dimensions and Weight
    with st.expander("📏 Dimensions and Weight"):
        st.text_input("📏 Length", value=str(product_data.get("length", "")))
        st.text_input("📐 Width", value=str(product_data.get("width", "")))
        st.text_input("📏 Height", value=str(product_data.get("height", "")))
        st.text_input("⚖️ Weight", value=str(product_data.get("weight", "")))

    # Additional Features
    features_text = "\n".join(product_data.get("features", []))
    with st.expander("💡 Additional Features"):
        st.text_area("Features", value=features_text)

    # Images
    if "images" in product_data:
        with st.expander("📸 Images"):
            for image_url in product_data["images"]:
                st.image(image_url, width=150)

    # Shopify Sync Button
    if st.button("🚀 Sync to Shopify"):
        sync_to_shopify(product_data)

    # Display Shopify sync result message if available
    if st.session_state["shopify_sync_message"]:
        st.write(st.session_state["shopify_sync_message"])

# Function to sync product data to Shopify
def sync_to_shopify(product_data):
    sync_payload = {
        "title": product_data.get("Title", product_data.get("title", "")),
        "description": product_data.get("Description", product_data.get("description", "")),
        "brand": product_data.get("Brand", product_data.get("brand", "")),
        "category": product_data.get("Category", product_data.get("category", ""))
    }

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
if tab == "🔍 Lookup by Barcode":
    st.subheader("🔍 Lookup Product by Barcode")
    barcode = st.text_input("Enter Product Barcode")
    if st.button("Fetch Product Details"):
        if barcode:
            try:
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

    if "product_data" in st.session_state and st.session_state["product_data"]:
        display_product_details()

# Image Upload functionality
elif tab == "📸 Upload Image":
    st.subheader("📸 Upload Product Image")
    uploaded_file = st.file_uploader("Choose a product image", type=["jpg", "jpeg", "png"])

    # Display the uploaded image immediately as a preview
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Product Image", use_column_width=True)

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

    if "product_data" in st.session_state and st.session_state["product_data"]:
        display_product_details_from_image()
