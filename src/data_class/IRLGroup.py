class IRLGroup:
    def __init__(self, post_url, author, coven_name, region, subregion=None, min_age=None, created_timestamp=None):
        self.post_url = post_url
        self.author = author
        self.coven_name = coven_name
        self.region = region
        self.subregion = subregion
        self.min_age = min_age
        self.created_timestamp = created_timestamp

    def __repr__(self):
        return (f"IRLGroup(post_url={self.post_url}, author={self.author}, coven_name={self.coven_name}, "
                f"region={self.region}, subregion={self.subregion}, min_age={self.min_age}, "
                f"created_timestamp={self.created_timestamp})")