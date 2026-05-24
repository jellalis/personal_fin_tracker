from pydantic import BaseModel,ConfigDict

# CategoryBase holds the common field shared across all category schemas
class CategoryBase(BaseModel):
    name:str

# CategoryCreate extends CategoryBase — currently adds nothing new
# Keeping it as a separate class is good practice: if we need to add creation-only fields later
# (e.g. an icon or color), we add them here without touching the base or response schema
class CategoryCreate(CategoryBase):
    pass

# CategoryResponse is what the API returns after creating or fetching a category
# from_attributes=True lets Pydantic read data directly from SQLAlchemy model objects (ORM → dict)
class CategoryResponse(CategoryBase):
    model_config=ConfigDict(from_attributes=True)
    id:int
    # int | None = None → user_id can be NULL in the database (for default categories)
    # The '= None' default means the field is optional in the JSON response
    user_id: int | None = None
