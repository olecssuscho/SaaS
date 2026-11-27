from datetime import datetime, timedelta, timezone
from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import models
from shemas import roles
import logging
from sqlalchemy.exc import SQLAlchemyError,IntegrityError

logger = logging.getLogger(__name__)

def calc_period_end(plan: models.PlanDB, now: datetime):
    if plan.period_days is None:
        return None
    return now + timedelta(days=plan.period_days)

async def find_plan(db:AsyncSession,name:str = "Free"):
    result = await db.execute(select(models.PlanDB).where(models.PlanDB.name == name, models.PlanDB.is_active.is_(True)))
    plan_db = result.scalar_one_or_none()
    if plan_db is None:
        logger.error(f"Someone have tried to register with plan {name}, but it is not exist")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    return plan_db

async def find_status(db:AsyncSession,name:str = "active"):
    result = await db.execute(select(models.StatusDB).filter(models.StatusDB.name == name))
    status_db = result.scalar_one_or_none()
    if status_db is None:
        logger.error(f"Someone have tried to register with status {name}, but it is not exist")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    else:
        return status_db

async def register_tenant_services(tenant:models.TenantDB,user:models.UserDB,db:AsyncSession):
    try:
        stmt = await db.execute(select(models.TenantDB).filter(models.TenantDB.name == tenant.name))
        tenant_db = stmt.scalar_one_or_none()
        if tenant_db:
            logger.warning(f"Someone have tried to register with Company's name {tenant.name}, but it was used")
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Company name was used")

        now = datetime.now(timezone.utc)
        user_id = user.id
        # plan's id, period
        plan_db = await find_plan(db)
        plan_id_db = plan_db.id
 
        # subscription status
        status_ = await find_status(db)
        status_id = status_.id

        added_tenant = models.TenantDB(
            name = tenant.name, plane_id = plan_id_db, subscription_status = status_id, 
            current_period_end = None, created_at = now
        )

        db.add(added_tenant)
        await db.flush()
        tenant_id = added_tenant.id
        tenant_role = roles.TenantRole.owner

        tenant_owner = models.TenantMembershipDB(
            tenant_id = tenant_id, user_id = user_id, tenant_role = tenant_role, created_at = now
        )

        db.add(tenant_owner)
        await db.commit()
        await db.refresh(added_tenant)
        return added_tenant
    except IntegrityError as e:
        logger.exception(f"Something went wrong: {e}")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Name was used")
    except (ValueError,SQLAlchemyError) as e:
        await db.rollback()
        logger.exception(f"Something went wrong: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


