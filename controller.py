from . import models


def get_tags(min_confidence, b64str):

    image_name = str(uuid.uuid4())
    print(f"image_name = {image_name}")

    # Obtenemos credenciales
    with open("credentials.json") as f:
        credentials = json.load(f)

    # Usamos imagekit.io para subir la imagen a la nube de forma pública.
    print("Usamos imagekit.io para subir la imagen a la nube de forma pública")
    imagekit = ImageKit(
        public_key = credentials.public_key,
        private_key = credentials.private_key,
        url_endpoint = credentials.url_endpoint
    )
    
    upload_info = imagekit.upload(file=b64str, file_name=image_name)
    # la url es accesible mediante `upload_info.url`
    
    # Usamos https://imagga.com/ para extraer tags a partir de la imagen subida anteriormente.
    print("Usamos https://imagga.com/ para extraer tags a partir de la imagen subida anteriormente")
    api_key = credentials.api_key
    api_secret = credentials.api_secret
    image_url = upload_info.url
    print(f"image_url = {image_url}")

    response = requests.get(f"https://api.imagga.com/v2/tags?image_url={image_url}", auth=(api_key, api_secret))

    tags = [
        {
            "tag": t["tag"]["en"],
            "confidence": t["confidence"]
        }
        for t in response.json()["result"]["tags"]
        if t["confidence"] > min_confidence
    ]
    print(tags)
    
    # Borramos la imagen subida a https://docs.imagekit.io/ usando la api delete.
    print("Borramos la imagen subida a https://docs.imagekit.io/ usando la api delete")
    delete = imagekit.delete_file(file_id=upload_info.file_id)
    
    # Almacenamos en una carpeta determinada la imagen
    print("Almacenamos en una carpeta determinada la imagen")
    path = "pictures/images/" + image_name
    text_file = open(path, "w")
    text_file.write(b64str)
    text_file.close()

    return models.pictures.get_tags(path, tags)
 


def list_images(min_date, max_date, tags):

    return models.pictures.list_images(min_date, max_date, tags)