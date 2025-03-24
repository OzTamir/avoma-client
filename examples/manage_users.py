import asyncio
import os
from uuid import UUID

from avoma import AvomaClient
from avoma.models.users import UserCreate, UserUpdate


async def main():
    # Get API key from environment variable
    api_key = os.getenv("AVOMA_API_KEY")
    if not api_key:
        raise ValueError("AVOMA_API_KEY environment variable is required")

    # Create client
    async with AvomaClient(api_key) as client:
        # Get current user information
        current_user = await client.users.get_current()
        print(f"\nCurrent user: {current_user.first_name} {current_user.last_name}")
        print(f"Role: {current_user.role.name}")
        print("Permissions:", ", ".join(current_user.role.permissions))

        # List all users
        users = await client.users.list()
        print(f"\nFound {users.count} users:")
        for user in users.results:
            print(f"\nName: {user.first_name} {user.last_name}")
            print(f"Email: {user.email}")
            print(f"Role: {user.role.name}")
            if user.department:
                print(f"Department: {user.department}")
            if user.title:
                print(f"Title: {user.title}")
            print(f"Active: {'Yes' if user.is_active else 'No'}")

        # Create a new user
        try:
            new_user = UserCreate(
                email="new.employee@company.com",
                first_name="New",
                last_name="Employee",
                role_uuid=UUID(
                    "123e4567-e89b-12d3-a456-426614174001"
                ),  # Replace with actual role UUID
                department="Sales",
                title="Account Executive",
                timezone="America/New_York",
            )
            created_user = await client.users.create(new_user)
            print(f"\nCreated new user: {created_user.email}")
            print(f"UUID: {created_user.uuid}")
        except Exception as e:
            print(f"Error creating user: {e}")

        # Update a user
        try:
            user_uuid = UUID(
                "123e4567-e89b-12d3-a456-426614174000"
            )  # Replace with actual user UUID
            update = UserUpdate(
                department="Business Development",
                title="Senior Account Executive",
            )
            updated_user = await client.users.update(user_uuid, update)
            print(f"\nUpdated user: {updated_user.email}")
            print(f"New department: {updated_user.department}")
            print(f"New title: {updated_user.title}")
        except Exception as e:
            print(f"Error updating user: {e}")

        # Deactivate a user
        try:
            user_uuid = UUID(
                "123e4567-e89b-12d3-a456-426614174002"
            )  # Replace with actual user UUID
            deactivate = UserUpdate(is_active=False)
            deactivated_user = await client.users.update(user_uuid, deactivate)
            print(f"\nDeactivated user: {deactivated_user.email}")
        except Exception as e:
            print(f"Error deactivating user: {e}")


if __name__ == "__main__":
    asyncio.run(main())
