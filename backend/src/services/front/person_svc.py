from sqlalchemy.orm import Session
from sqlalchemy.sql import text


def check_email_exists(email: str, db: Session):
    sql = text(
        """
        SELECT email 
        FROM person 
        WHERE email = :email
        """
    )
    
    result = db.execute(sql, {"email": email}).fetchone()
    
    return result is not None