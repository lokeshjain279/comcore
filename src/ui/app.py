import streamlit as st
import requests

# API endpoints
BARCODE_API_URL = "http://localhost:8000/api/v1/product/lookup/"  # Endpoint for barcode lookup
IMAGE_API_URL = "http://localhost:8000/api/v1/product/describe"  # Endpoint for image upload
SHOPIFY_SYNC_API_URL = "http://localhost:8000/api/v1/shopify/sync"  # Endpoint for Shopify sync

# Initialize session state variables
if "product_data" not in st.session_state:
    st.session_state["product_data"] = {}
if "shopify_sync_message" not in st.session_state:
    st.session_state["shopify_sync_message"] = ""
if "update_trigger" not in st.session_state:
    st.session_state["update_trigger"] = False  # Trigger to control UI refreshes

# Function to toggle update trigger for UI refresh
def toggle_update_trigger():
    st.session_state["update_trigger"] = not st.session_state["update_trigger"]

# Page configuration
st.set_page_config(page_title="Product Enrichment Tool", layout="centered")
st.markdown("<style>body { background-color: #f7f7f7; }</style>", unsafe_allow_html=True)

st.title("📦 Product Enrichment Tool")
st.write("Retrieve and enrich product details by scanning a barcode or uploading an image.")

# Tabs for input options
tab1, tab2 = st.tabs(["🔍 Lookup by Barcode", "📸 Upload Image"])

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

    # Sync to Shopify Button
    if st.button("Sync to Shopify"):
        # Prepare payload for Shopify sync
        sync_payload = {
            "title": title,
            "description": description,
            "manufacturer": manufacturer,
            "category": category
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

    # Display Shopify sync result message if available
    if st.session_state["shopify_sync_message"]:
        st.write(st.session_state["shopify_sync_message"])


# Function to display product details for image-based lookup
def display_product_details_from_image():
    product_data = st.session_state["product_data"]
    st.write("### Product Details from Image")
    if not product_data:
        st.warning("No product data available.")
        return

    # Basic Information
    with st.expander("Basic Information", expanded=True):
        name = st.text_input("Name", value=product_data.get("name", ""))
        description = st.text_area("Description", value=product_data.get("description", ""))
        brand = st.text_input("Brand", value=product_data.get("brand", ""))
        model = st.text_input("Model", value=product_data.get("model", ""))
        sku = st.text_input("SKU", value=product_data.get("sku", ""))
        upc = st.text_input("UPC", value=product_data.get("upc", ""))
        asin = st.text_input("ASIN", value=product_data.get("asin", ""))
        category = st.text_input("Category", value=product_data.get("category", ""))
        subcategory = st.text_input("Subcategory", value=product_data.get("subcategory", ""))

    # Tags
    with st.expander("Tags"):
        for tag in product_data.get("tags", []):
            st.text_input("Tag", value=tag, key=tag)

    # Specifications
    specifications = product_data.get("specifications", {})
    with st.expander("Specifications"):
        st.text_input("Material", value=specifications.get("material", ""))
        st.text_input("Color", value=specifications.get("color", ""))
        st.text_input("Style", value=specifications.get("style", ""))

        # Display all features in a single text area
        features_text = "\n".join(specifications.get("features", []))  # Join features into a single string
        st.text_area("Additional Features", value=features_text)

    # Weight and Dimensions
    with st.expander("Weight and Dimensions"):
        st.text_input("Weight", value=product_data.get("weight", ""))
        dimensions = product_data.get("dimensions", {})
        if "chair" in dimensions:
            st.write("Chair Dimensions")
            st.text_input("Width", value=dimensions["chair"].get("width", ""))
            st.text_input("Depth", value=dimensions["chair"].get("depth", ""))
            st.text_input("Height", value=dimensions["chair"].get("height", ""))
        if "ottoman" in dimensions:
            st.write("Ottoman Dimensions")
            st.text_input("Width", value=dimensions["ottoman"].get("width", ""))
            st.text_input("Depth", value=dimensions["ottoman"].get("depth", ""))
            st.text_input("Height", value=dimensions["ottoman"].get("height", ""))

    # Sync to Shopify Button
    if st.button("Sync to Shopify"):
        # Prepare payload for Shopify sync
        sync_payload = {
            "title": name,
            "description": description,
            "manufacturer": brand,
            "category": category
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

    # Display Shopify sync result message if available
    if st.session_state["shopify_sync_message"]:
        st.write(st.session_state["shopify_sync_message"])

# Barcode lookup functionality
with tab1:
    st.subheader("🔍 Lookup Product by Barcode")
    barcode = st.text_input("Enter Product Barcode")
    if st.button("Fetch Product Details", key="barcode_button"):
        if barcode:
            try:
                # Call barcode API
                response = requests.get(f"{BARCODE_API_URL}{barcode}")
                if response.status_code == 200:
                    data = response.json()
                    st.session_state["product_data"] = data.get("product_data", {})
                    # st.session_state["product_data"].pop("images", None)  # Remove images if present
                    st.session_state["shopify_sync_message"] = ""
                    toggle_update_trigger()  # Trigger refresh
                else:
                    st.error("Product not found or error in fetching data.")
            except Exception as e:
                st.error(f"Error calling barcode API: {e}")
        else:
            st.warning("Please enter a valid barcode.")

# Image upload functionality
with tab2:
    st.subheader("📸 Upload Product Image")
    uploaded_file = st.file_uploader("Choose a product image", type=["jpg", "jpeg", "png"])
    if st.button("Fetch Product Details", key="image_button"):
        if uploaded_file:
            try:
                files = {"image": (uploaded_file.name, uploaded_file, "multipart/form-data")}
                response = requests.post(IMAGE_API_URL, files=files)
                print(f"Response IMAGe is {response}")
                if response.status_code == 200:
                    st.session_state["product_data"] = response.json().get("product_data", {})
                    st.session_state["product_data"].pop("images", None)  # Remove images if present
                    st.session_state["shopify_sync_message"] = ""
                    toggle_update_trigger()  # Trigger refresh
                else:
                    st.error("Error in fetching data or processing image.")
            except Exception as e:
                st.error(f"Error calling image API: {e}")
        else:
            st.warning("Please upload a valid image file.")

# Display product details based on the type of lookup
if st.session_state["product_data"]:
    if "name" in st.session_state["product_data"]:
        display_product_details_from_image()  # Display for image-based lookup
    else:
        display_product_details()  # Display for barcode-based lookup
