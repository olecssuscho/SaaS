from datetime import datetime, timedelta,timezone
from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
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
        # plane's name and id
        stmt = await db.execute(select(models.PlanDB))
        plane_name_db = stmt.scalars()
        list_of_plans_name = []
        list_of_plans_id = []
        list_of_plans_period = []
        for i in plane_name_db:
            list_of_plans_name.append(i.name)
            list_of_plans_id.append(i.id)
            list_of_plans_period.append(i.period_days)

        for i in range(len(list_of_plans_name)):
            if tenant.plane_name == list_of_plans_name[i]:
                plan_id = list_of_plans_id[i]
                end_of_period = list_of_plans_period[i]
                break

        else:
            logger.warning(f"Someone have tried to register with plane {tenant.plane_name}, but it is not exist")
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="That plane is not exist") 

        if end_of_period is not None:
            # end of pro period
            end_of_period = now + timedelta(days=end_of_period)
        
        # subscription status
        stmt = await db.execute(select(models.StatusDB).filter(models.StatusDB.name == "active"))
        status_id = stmt.scalar_one_or_none().id

        added_tenant = models.TenantDB(
            name = tenant.name, plane_id = plan_id, subscription_status = status_id, 
            current_period_end = end_of_period, created_at = now
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


