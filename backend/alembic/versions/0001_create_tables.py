from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0001_create_tables'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'site',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('domain', sa.String(), nullable=False, unique=True),
        sa.Column('created_at', sa.DateTime(), nullable=True)
    )

    op.create_table(
        'page',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('site_id', sa.Integer(), sa.ForeignKey('site.id', ondelete='CASCADE')),
        sa.Column('url', sa.Text(), nullable=False, unique=True),
        sa.Column('status_code', sa.Integer()),
        sa.Column('html_hash', sa.String(length=64)),
        sa.Column('fetched_at', sa.DateTime()),
    )

    crawl_status_enum = sa.Enum('pending', 'in_progress', 'completed', 'failed', name='crawlstatus')
    crawl_status_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        'crawl_job',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('site_id', sa.Integer(), sa.ForeignKey('site.id', ondelete='CASCADE')),
        sa.Column('status', sa.Enum('pending', 'in_progress', 'completed', 'failed', name='crawlstatus'), nullable=False),
        sa.Column('depth', sa.Integer(), default=1),
        sa.Column('started_at', sa.DateTime()),
        sa.Column('finished_at', sa.DateTime()),
    )


def downgrade() -> None:
    op.drop_table('crawl_job')
    op.drop_table('page')
    op.drop_table('site')
    sa.Enum(name='crawlstatus').drop(op.get_bind(), checkfirst=True)