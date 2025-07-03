 @field_validator('name')
    @classmethod
    def tranform_name(cls, value):
        return value.upper()
