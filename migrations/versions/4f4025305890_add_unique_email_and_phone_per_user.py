"""Add unique email and phone per user

Revision ID: 4f4025305890
Revises: 03dc5516dc59
Create Date: 2024-03-22 14:51:42.416891

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4f4025305890'
down_revision: Union[str, None] = '03dc5516dc59'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('contacts_email_key', 'contacts', type_='unique')
    op.drop_constraint('contacts_phone_key', 'contacts', type_='unique')
    op.create_unique_constraint('unique_email_user', 'contacts', ['email', 'user_id'])
    op.create_unique_constraint('unique_phone_user', 'contacts', ['phone', 'user_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('unique_phone_user', 'contacts', type_='unique')
    op.drop_constraint('unique_email_user', 'contacts', type_='unique')
    op.create_unique_constraint('contacts_phone_key', 'contacts', ['phone'])
    op.create_unique_constraint('contacts_email_key', 'contacts', ['email'])
    # ### end Alembic commands ###
