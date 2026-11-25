from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import models
import logging
from fastapi_pagination.ext.sqlalchemy import apaginate
from depends import get_role

logger = logging.getLogger(__name__)

async def get_tenants_services(user:models.UserDB,db:AsyncSession):
    await get_role(user,db)
    stmt = select(models.TenantDB)
    logger.info(f"Someone: {user.email} have tried to get tenants")
    return await apaginate(db,stmt)