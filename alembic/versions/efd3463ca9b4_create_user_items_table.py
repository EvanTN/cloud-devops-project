from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = 'efd3463ca9b4'
down_revision = 'ad3625cc633d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create user_items table
    op.create_table(
        'user_items',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('item_id', sa.Integer(), sa.ForeignKey('items.id'), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('rating', sa.Integer(), nullable=True),
        sa.Column('review', sa.String(), nullable=True),
    )

    # Add new columns to items table
    op.add_column('items', sa.Column('external_id', sa.String(), nullable=True))
    op.add_column('items', sa.Column('type', sa.String(), nullable=True))
    op.add_column('items', sa.Column('poster_url', sa.String(), nullable=True))

    # Create unique index for external_id
    op.create_index('ix_items_external_id', 'items', ['external_id'], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    # Drop index first
    op.drop_index('ix_items_external_id', table_name='items')

    # Drop columns from items table
    op.drop_column('items', 'poster_url')
    op.drop_column('items', 'type')
    op.drop_column('items', 'external_id')

    # Drop user_items table
    op.drop_table('user_items')
