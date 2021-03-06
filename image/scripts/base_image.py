from builder import BuilderBase

class BaseImage(BuilderBase):
    repo = 'base_image'

    def get_description(self):
        return "Base Build Docker Image"

    def __init__(self, configs):
        self.image = configs['base_image']['image']
        self.repo = configs['base_image']['repo']
        self.branch = configs['base_image'].get('branch')

    def is_built(self):
        return self.image_is_built()

    def build(self):
        if not self.image_is_built():
            self.build_image()
