"""empty message

Revision ID: 261b49b2568c
Revises: 2dc8b46903e2
Create Date: 2014-04-18 12:39:50.169164

"""

# revision identifiers, used by Alembic.
revision = '261b49b2568c'
down_revision = '2dc8b46903e2'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('about_page', sa.Column('bigTitleContent', sa.String(length=80), nullable=True))
    op.add_column('about_page', sa.Column('howDoesItWorkContent', sa.String(length=120), nullable=True))
    op.add_column('about_page', sa.Column('howDoesItWorkTitle', sa.String(length=80), nullable=True))
    op.add_column('about_page', sa.Column('otherQuestionContent', sa.String(length=120), nullable=True))
    op.add_column('about_page', sa.Column('otherQuestionTitle', sa.String(length=80), nullable=True))
    op.add_column('about_page', sa.Column('ourMissionContent', sa.String(length=120), nullable=True))
    op.add_column('about_page', sa.Column('ourMissionTitle', sa.String(length=80), nullable=True))
    op.drop_column('about_page', 'description')
    op.drop_column('about_page', 'title')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('about_page', sa.Column('title', sa.VARCHAR(length=80), nullable=True))
    op.add_column('about_page', sa.Column('description', sa.VARCHAR(length=120), nullable=True))
    op.drop_column('about_page', 'ourMissionTitle')
    op.drop_column('about_page', 'ourMissionContent')
    op.drop_column('about_page', 'otherQuestionTitle')
    op.drop_column('about_page', 'otherQuestionContent')
    op.drop_column('about_page', 'howDoesItWorkTitle')
    op.drop_column('about_page', 'howDoesItWorkContent')
    op.drop_column('about_page', 'bigTitleContent')
    ### end Alembic commands ###