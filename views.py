# Description: Add your page endpoints here.


from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from lnbits.core.models import User
from lnbits.decorators import check_user_exists
from lnbits.helpers import template_renderer

repay_generic_router = APIRouter()


def repay_renderer():
    return template_renderer(["repay/templates"])


#######################################
##### ADD YOUR PAGE ENDPOINTS HERE ####
#######################################


# Backend admin page


@repay_generic_router.get("/", response_class=HTMLResponse)
async def index(req: Request, user: User = Depends(check_user_exists)):
    return repay_renderer().TemplateResponse("repay/index.html", {"request": req, "user": user.json()})


# Frontend shareable page
