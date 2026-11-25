from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from shemas.responses import TenantsRESPONCES
from shemas.users import UserMODELS
from depends import get_current_user, get_db
from sqlalchemy.ext.asyncio import AsyncSession
from services.admins import (get_tenants_services)

router = APIRouter(prefix="/admin",tags=["Admins"])

@router.get("/tenants", response_model=Page[TenantsRESPONCES])
async def get_tenants(user:UserMODELS = Depends(get_current_user),db:AsyncSession = Depends(get_db)):
    return await get_tenants_services(user,db)

