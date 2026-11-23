from fastapi import APIRouter, Depends
from shemas.tenants import TenantShema
from shemas.users import UserMODELS
from depends import get_current_user, get_db
from sqlalchemy.ext.asyncio import AsyncSession
from services.tenants import (register_tenant_services)

router = APIRouter(prefix="/tenant",tags=["Tenants"])

@router.post("/register")
async def register_tenant(tenant:TenantShema,user:UserMODELS = Depends(get_current_user),db:AsyncSession = Depends(get_db)):
    return await register_tenant_services(tenant,user,db)

