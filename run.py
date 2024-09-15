from alembic import command
from alembic.config import Config
import uvicorn
from app.main import app

if __name__ == '__main__':
    # Path to your alembic.ini file
    alembic_cfg = Config("alembic.ini")

    # Running the upgrade to head
    command.upgrade(alembic_cfg, "head")

    uvicorn.run(app, host='0.0.0.0', port=8000)