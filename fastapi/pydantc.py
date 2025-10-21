from datetime import datetime

from pydantic import BaseModel, Field


class User(BaseModel):
    id: int
    name: str = "John Doe"
    signup_ts: datetime | None = None
    friends: list[int] = Field(default_factory=list)


external_data = {
    "id": "123",
    "signup_ts": "2017-06-01 12:22",
    "friends": [1, "2", b"3"],
}
user = User(**external_data)
print(user)
# > User id=123 name='John Doe' signup_ts=datetime.datetime(2017, 6, 1, 12, 22) friends=[1, 2, 3]
print(user.id)
# > 123

# Add a friend in-place (simple, but bypasses Pydantic field validation for the append)
user.friends.append(4)
print("after append (in-place):", user.friends)

# Add a friend using a validated copy (works for both pydantic v1 and v2)
def add_friend_validated(u: User, new_friend) -> User:
    # normalize new_friend to int (or let Pydantic validate on copy)
    updated = u.friends + [new_friend]
    try:  # pydantic v2
        return u.model_copy(update={"friends": updated})
    except AttributeError:  # pydantic v1
        return u.copy(update={"friends": updated})

user = add_friend_validated(user, "5")
print("after validated add (new model):", user.friends)