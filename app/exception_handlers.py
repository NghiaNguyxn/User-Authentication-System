from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from app import exceptions

def register_exception_handlers(app: FastAPI):
    # Unauthorized Error (401)
    @app.exception_handler(exceptions.IncorrectCredentials)
    async def auth_exception_handler(request: Request, exc: exceptions.IncorrectCredentials):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": exc.message},
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Not Found Error (404)
    @app.exception_handler(exceptions.UserNotFound)
    async def user_not_found_handler(request: Request, exc: exceptions.UserNotFound):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": exc.message},
        )
    
    # Bad request Error (400)
    @app.exception_handler(exceptions.InvalidToken)
    async def iInvalid_token_handler(request: Request, exc: exceptions.InvalidToken):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": exc.message},
        )
    
    @app.exception_handler(exceptions.PasswordSameAsOld)
    async def password_same_as_old_handler(request: Request, exc: exceptions.PasswordSameAsOld):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": exc.message},
        )
    
    @app.exception_handler(exceptions.UserAlreadyVerified)
    async def user_already_verified_handler(request: Request, exc: exceptions.UserAlreadyVerified):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": exc.message},
        )
    
    @app.exception_handler(exceptions.UserInactive)
    async def user_inactive_handler(request: Request, exc: exceptions.UserInactive):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": exc.message},
        )
    
    @app.exception_handler(exceptions.UserNotVerified)
    async def user_not_verified_handler(request: Request, exc: exceptions.UserNotVerified):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": exc.message},
        )
    
    @app.exception_handler(exceptions.UserAlreadyExists)
    async def user_already_exists_handler(request: Request, exc: exceptions.UserAlreadyExists):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": exc.message},
        )
    
    @app.exception_handler(exceptions.AppError)
    async def app_error_handler(request: Request, exc: exceptions.AppError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": exc.message},
        )
    
    # Internal Server Error (500)
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "An unexpected system error has occurred"},
        )