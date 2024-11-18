from fastapi import HTTPException, status


class AuthException:
    @staticmethod
    def bad_request(detail: str = '400. Bad request') -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

    @staticmethod
    def unauthorized(detail: str = '401. Unauthorized') -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
        )

    @staticmethod
    def forbidden(detail: str = '403. Forbidden') -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )
