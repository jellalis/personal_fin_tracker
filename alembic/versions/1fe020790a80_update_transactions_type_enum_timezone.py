"""update transactions type enum timezone

Revision ID: 1fe020790a80
Revises: 39bb309dc2b6
Create Date: 2026-06-05 00:45:33.081968

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '1fe020790a80'
down_revision: Union[str, Sequence[str], None] = '39bb309dc2b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # PostgreSQL needs the ENUM type to exist BEFORE we can use it in a column
    op.execute("CREATE TYPE transactiontype AS ENUM ('income', 'expense')")
    
    op.alter_column('transactions', 'type',
               existing_type=sa.VARCHAR(),
               type_=sa.Enum('income', 'expense', name='transactiontype'),
               postgresql_using='type::transactiontype',  # ← πώς να κάνει cast τα υπάρχοντα values
               existing_nullable=False)
    op.alter_column('transactions', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    op.alter_column('transactions', 'created_at',
               existing_type=sa.DateTime(timezone=True),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=True)
    op.alter_column('transactions', 'type',
               existing_type=sa.Enum('income', 'expense', name='transactiontype'),
               type_=sa.VARCHAR(),
               postgresql_using='type::varchar',
               existing_nullable=False)
    # Drop the ENUM type after reverting the column
    op.execute("DROP TYPE transactiontype")
    # ### end Alembic commands ###
