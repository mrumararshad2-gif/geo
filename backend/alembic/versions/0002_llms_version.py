from alembic import op
import sqlalchemy as sa

revision = '0002_llms_version'
down_revision = '0001_create_tables'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'llms_version',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('site_id', sa.Integer(), sa.ForeignKey('site.id', ondelete='CASCADE')),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime()),
        sa.Column('created_by', sa.String()),
    )

def downgrade() -> None:
    op.drop_table('llms_version')