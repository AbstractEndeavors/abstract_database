from .imports import *
# Assuming getRequest is defined in globalImports, import it explicitly


def fetch_image(uri, max_size=(200, 200)):
    """
    Fetch an image from the given URI, verify its integrity, resize it,
    and return the processed image data as PNG bytes.
    
    The function first attempts to extract an image URL from the URI via
    get_img_url. If none is found, it falls back to using the original URI.
    """
    logging.info(f"Fetching image from URI: {uri}")
    try:
        # Attempt to extract the image URL from the provided URI.
        image_url = get_img_url(uri)
        if not image_url:
            logging.error("Image URL could not be retrieved. Falling back to the provided URI.")
            image_url = uri

        # Fetch the image content.
        content = get_image_content(image_url)
        if not content:
            logging.error("Image content could not be retrieved.")
            return None

        # Load the image from the content bytes and verify integrity.
        image_data = io.BytesIO(content)
        img = Image.open(image_data)
        img.verify()  # Verify image integrity

        # Re-open the image for processing.
        image_data.seek(0)
        img = Image.open(image_data)
        img.thumbnail(max_size)  # Resize image to fit within max_size

        # Save the processed image to a bytes buffer.
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        bio.seek(0)
        return bio.getvalue()

    except requests.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except requests.RequestException as req_err:
        logging.error(f"Request exception: {req_err}")
    except Image.UnidentifiedImageError:
        logging.error("Failed to identify the image file.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

    return None


def get_image_content(image_url):
    """
    Fetch content from the image URL and ensure it is an image.
    
    Raises:
        ValueError: If the Content-Type does not indicate an image.
    Returns:
        The raw bytes of the image.
    """
    try:
        # Perform a GET request to fetch the image data.
        response = requests.get(image_url)
        response.raise_for_status()

        # Check if the returned content is an image.
        content_type = response.headers.get('Content-Type', '')
        if not content_type.startswith('image/'):
            logging.error(f"URI does not point to an image. Content-Type: {content_type}")
            raise ValueError("Non-image content")

        return response.content

    except requests.HTTPError as http_err:
        logging.error(f"HTTP error occurred while fetching image content: {http_err}")
        raise
    except requests.RequestException as req_err:
        logging.error(f"Request exception while fetching image content: {req_err}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error in get_image_content: {e}")
        raise


def get_img_url(uri):
    """
    Extract the image URL from the given URI by fetching image variables.
    
    The function calls get_image_vars, which is expected to return a JSON-like
    dictionary with an 'image' key. If the extraction fails, returns None.
    """
    logging.info(f"Extracting image URL from URI: {uri}")
    try:
        uri_vars = get_image_vars(uri)
        # Expecting uri_vars to be a dictionary containing the image URL.
        return uri_vars.get('image')
    except Exception as e:
        logging.error(f"Error extracting image URL from URI vars: {e}")
        return None


def get_image_vars(uri):
    """
    Fetch and parse image variables from the given URI.
    
    Assumes the response is JSON and either returns a parsed dictionary or,
    if getRequest already returns JSON, passes it through.
    """
    try:
        # Call getRequest (assumed to be a wrapper around requests.get).
        response = getRequest(url=uri, data={})
        
        # If response is already a dict, assume it is the parsed JSON.
        if isinstance(response, dict):
            return response
        else:
            # Otherwise, try to parse the response as JSON.
            return response.json()
    except requests.HTTPError as http_err:
        logging.error(f"HTTP error occurred while fetching image vars: {http_err}")
        raise
    except requests.RequestException as req_err:
        logging.error(f"Request exception while fetching image vars: {req_err}")
        raise
    except ValueError as ve:
        logging.error(f"JSON decoding failed: {ve}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error in get_image_vars: {e}")
        raise


def get_image_data(image_url, max_size=(200, 200)):
    """
    Alternative function to fetch and process an image given an image URL.
    
    This function directly uses requests.get (without getRequest) to obtain
    the image, resize it, and return the image data as PNG bytes.
    """
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        image = Image.open(io.BytesIO(response.content))
        image.thumbnail(max_size)
        bio = io.BytesIO()
        image.save(bio, format="PNG")
        return bio.getvalue()
    except Exception as e:
        logging.error(f"Error in get_image_data: {e}")
        return None
