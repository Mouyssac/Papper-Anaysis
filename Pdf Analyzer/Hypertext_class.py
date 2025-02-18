class Hypertext_class:
    def __init__(self, uri, bbox, link_type, destination, text, target_page, page_number):
        self.uri = uri  # URL du lien
        self.bbox = bbox  # Position du lien (bounding box)
        self.link_type = link_type  # Type du lien
        self.destination = destination  # Destination du lien
        self.text = text  # Texte associé au lien
        self.target_page = target_page  # page cible du lien
        self.page_number = page_number

    def __repr__(self):
        return (f"HypertextClass(uri={self.uri}, "
                f"bbox={self.bbox}, "
                f"link_type={self.link_type}, "
                f"destination={self.destination}, "
                f"page destination={self.target_page} "
                f"text={self.text})")
        
