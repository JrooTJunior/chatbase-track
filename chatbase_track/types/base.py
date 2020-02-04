from pydantic import BaseModel, BaseConfig


class Base(BaseModel):
    class Config(BaseConfig):
        use_enum_values = True
