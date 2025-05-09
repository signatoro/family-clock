
from fastapi import Depends

from app.src.models.user import User
from app.src.util.auth import get_current_user
from app.src.util.user_router import UserAPIRouter


class GroupEndpoints():

    router = UserAPIRouter(prefix='/group', tags=['group'])

    def __init__(self):
        # self.controller = controller

        self.router.add_api_route('/who', self.who_am_i, methods=['Get'])
    
    async def who_am_i(self, current_user: User = Depends(get_current_user)):
        return {
            "username": current_user.username,
            "email": current_user.email,
            "phone_number": current_user.phone_number,
    }