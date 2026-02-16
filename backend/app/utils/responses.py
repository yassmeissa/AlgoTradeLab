"""API response utilities"""

from typing import Dict, Any, List
from datetime import datetime


class APIResponse:
    """Standard API response wrapper"""
    
    @staticmethod
    def success(data: Any, message: str = "Success", status_code: int = 200) -> Dict[str, Any]:
        """Success response"""
        return {
            "status": "success",
            "status_code": status_code,
            "message": message,
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def error(message: str, status_code: int = 400, errors: List[str] = None) -> Dict[str, Any]:
        """Error response"""
        return {
            "status": "error",
            "status_code": status_code,
            "message": message,
            "errors": errors or [],
            "timestamp": datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def paginated(data: List[Any], total: int, page: int, page_size: int) -> Dict[str, Any]:
        """Paginated response"""
        return {
            "status": "success",
            "data": data,
            "pagination": {
                "total": total,
                "page": page,
                "page_size": page_size,
                "total_pages": (total + page_size - 1) // page_size
            },
            "timestamp": datetime.utcnow().isoformat()
        }
