from datetime import datetime, timezone
from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import models
from shemas import roles
import logging
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

async def register_tenant_services(tenant:models.TenantDB,user:models.UserDB,db:AsyncSession):
    try:
        stmt = await db.execute(select(models.TenantDB).filter(models.TenantDB.name == tenant.name))
        tenant_db = stmt.scalar_one_or_none()
        if tenant_db:
            logger.warning(f"Someone have tried to register with Company's name {tenant.name}, but it was used")
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Company name was used")

        now = datetime.now(timezone.utc)
        user_id = user.id
        # plan's name, id, period
        stmt = await db.execute(select(models.PlanDB).filter(models.PlanDB.name == "Free"))
        plan_db = stmt.scalar_one_or_none()
        plan_name_db = plan_db.name
        plan_id_db = plan_db.id
        plan_period_db = plan_db.period_days

        if plan_db is None:
            logger.warning(f"Someone have tried to register with plane {plan_name_db}, but it is not exist")
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="That plane is not exist") 
        
        # subscription status
        stmt = await db.execute(select(models.StatusDB).filter(models.StatusDB.name == "active"))
        status_id = stmt.scalar_one_or_none().id

        added_tenant = models.TenantDB(
            name = tenant.name, plane_id = plan_id_db, subscription_status = status_id, 
            current_period_end = plan_period_db, created_at = now
        )

        db.add(added_tenant)
        await db.commit()
        await db.refresh(added_tenant)
        tenant_id = added_tenant.id
        tenant_role = roles.TenantRole.owner

        tenant_owner = models.TenantMembershipDB(
            tenant_id = tenant_id, user_id = user_id, tenant_role = tenant_role, created_at = now
        )

        db.add(tenant_owner)
        await db.commit()
        await db.refresh(added_tenant)
        return added_tenant
    except (ValueError,SQLAlchemyError) as e:
        db.rollback()
        logger.exception(f"Something went wrong: {e}")
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail=f"Content: {e}")


