from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Optional

# ── Constants ─────────────────────────────────────────────────────────────────
SECRET_KEY = "hms_secret_key_must_be_32_chars!"
ALGORITHM  = "HS256"

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# ✏️ Write hash_password
def hash_password(plain: str) -> str:
    """Hash a plain text password using bcrypt."""
    # Your code here
    return pwd_context.hash(plain)


# ✏️ Write verify_password
def verify_password(plain: str, hashed: str) -> bool:
    """Verify a plain text password against a bcrypt hash."""
    # Your code here
    return pwd_context.verify(plain, hashed)


# ✏️ Write create_access_token
def create_access_token(data: dict, expires_minutes: int = 60) -> str:
    """Create a signed JWT access token with exp and iat claims."""
    # Your code here
    encode = data.copy()
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=expires_minutes)

    encode.update({
        "iat": now,
        "exp": expire
    })

    token = jwt.encode(
        encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

# ✏️ Write decode_token
def decode_token(token: str) -> Optional[dict]:
    """Decode and verify a JWT. Returns payload dict or None if invalid/expired."""
    # Your code here
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
        
    except JWTError:
        return None


# ✏️ Write get_token_role
def get_token_role(token: str) -> Optional[str]:
    """Return the 'role' field from a valid token, or None if invalid."""
    # Your code here
    payload = decode_token(token)

    if payload is None:
        return None

    return payload.get("role")