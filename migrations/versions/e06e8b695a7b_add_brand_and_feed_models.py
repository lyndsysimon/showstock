"""Add Brand and Feed models

Revision ID: e06e8b695a7b
Revises: 
Create Date: 2025-04-13 00:41:58.112896

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e06e8b695a7b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create enum type for feed_type
    feed_type_enum = sa.Enum('pellet', 'pulverized', name='feedtype')
    feed_type_enum.create(op.get_bind(), checkfirst=True)
    
    # Create brands table
    op.create_table(
        'brands',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    
    # Create feeds table
    op.create_table(
        'feeds',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('brand_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('density', sa.Float(), nullable=True),
        sa.Column('feed_type', feed_type_enum, nullable=False),
        sa.Column('weight', sa.Float(), nullable=True),
        sa.Column('cost', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(['brand_id'], ['brands.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop tables in reverse order
    op.drop_table('feeds')
    op.drop_table('brands')
    
    # Drop enum type
    feed_type_enum = sa.Enum('pellet', 'pulverized', name='feedtype')
    feed_type_enum.drop(op.get_bind(), checkfirst=True)
