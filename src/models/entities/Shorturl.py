class Shorturl():

    def __init__(self, id, original_url=None, short_url=None) -> None:
        self.id = id
        self.original_url = original_url
        self.short_url = short_url

    def to_JSON(self):
        return {
            'id': self.id,
            'original_url': self.original_url,
            'short_url': self.short_url
        }