class RedFlags():
    red_flag_id = 0
    red_flags = []

    def __init__(self, created_on, created_by, latitude, longitude, status, images, videos, description):
        self.red_flag_id = len(RedFlags.red_flags) + 1
        self.created_on = created_on
        self.created_by = created_by
        self.latitude = latitude
        self.longitude = longitude
        self.status = status
        self.images = images
        self.videos = videos
        self.description = description

    def create_red_flag(self):
        """Method to create a new red flag into list"""
        red_flag_item = dict(
            red_flag_id = self.red_flag_id,
            created_on = self.created_on,
            created_by = self.created_by,
            latitude = self.latitude,
            longitude = self.longitude,
            status = self.status,
            images = self.images,
            videos = self.videos,
            description = self.description
        ) 
        """Adding the red flag into red_flags list"""   
        self.red_flags.append(red_flag_item)
        return red_flag_item

    def get_all_red_flags(self):
        """Method to get all red flags"""
        return RedFlags.red_flags
