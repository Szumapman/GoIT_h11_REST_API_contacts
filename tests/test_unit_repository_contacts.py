import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, date

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.repository.contacts import PostgresContactRepository
from src.database.models import Contact
from src.schemas import ContactOut, ContactIn, UserOut, UserIn


class MockedSession:
    def commit(self):
        pass

    def refresh(self, contact):
        pass


class TestPostgresContactRepository(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.users_repository = PostgresContactRepository(self.session)
        self.created_at_set = datetime.now()
        self.user = UserOut(
            id=1,
            username="testuser",
            email="test@example.com",
            password="Pass123!",
            salt="somesalt",
            created_at=self.created_at_set,
            avatar="Avatar",
        )
        self.contact = ContactOut(
            id=1,
            first_name="testname",
            last_name="lasttest",
            email="test@example.com",
            phone="+48654789654",
            birth_date=datetime(2000, 1, 1),
            user_id=1,
        )

    # get_contacts
    # async def test_get_contacts_success(self):
    #     contacts = [
    #         Contact(id=1, name="testcontact", email="test@example.com", user_id=1)
    #     ]
    #     self.session.query().filter().all.return_value = contacts
    #     actual_contacts = await self.users_repository.get_contacts(
    #         search_name="",
    #         search_email="",
    #         upcoming_birthdays=False,
    #         user=self.user,
    #     )
    #     self.assertEqual(contacts, actual_contacts)

    async def test_get_contact_success(self):
        contact = Contact(
            id=1,
            first_name="testname",
            last_name="lasttest",
            email="test@example.com",
            phone="+48654789654",
            birth_date=datetime(2000, 1, 1),
            user_id=1,
        )
        self.session.query().filter().first.return_value = contact
        actual_contact = await self.users_repository.get_contact(
            contact_id=contact.id, user=self.user
        )
        self.assertEqual(contact.id, actual_contact.id)
        self.assertEqual(contact.first_name, actual_contact.first_name)
        self.assertEqual(contact.last_name, actual_contact.last_name)
        self.assertEqual(contact.email, actual_contact.email)
        self.assertEqual(contact.phone, actual_contact.phone)
        self.assertEqual(contact.birth_date.date(), actual_contact.birth_date)

    async def test_get_contact_not_found(self):
        contact = None
        self.session.query().filter().first.return_value = contact

        with self.assertRaises(HTTPException) as context:
            await self.users_repository.get_contact(contact_id=1, user=self.user)
        self.assertEqual(context.exception.status_code, status.HTTP_404_NOT_FOUND)

    # create_contact
    async def test_create_contact_success(self):
        contact_in = ContactIn(
            first_name="testname",
            last_name="lasttest",
            email="test@example.com",
            phone="+48654789654",
            birth_date=date(2000, 1, 1),
            user_id=1,
        )
        contact = Contact(
            id=1,
            first_name="testname",
            last_name="lasttest",
            email="test@example.com",
            phone="+48654789654",
            birth_date=datetime(2000, 1, 1),
            user_id=1,
        )
        self.session.add.return_value = contact
        self.session.commit.return_value = contact
        self.session.refresh.return_value = contact

        await self.users_repository.create_contact(contact_in, self.user)

        # self.session.add.assert_called_once()
        # self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once()
        # self.assertEqual(contact_in.first_name, actual_contact.first_name)
        # self.assertEqual(contact_in.last_name, actual_contact.last_name)
        # self.assertEqual(contact_in.email, actual_contact.email)
        # self.assertEqual(contact_in.phone, actual_contact.phone)
        # self.assertEqual(contact_in.birth_date.date(), actual_contact.birth_date)


if __name__ == "__main__":
    unittest.main()
