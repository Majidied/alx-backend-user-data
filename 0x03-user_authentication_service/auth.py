#!/usr/bin/env python3
from bcrypt import hashpw, gensalt


def _hash_password(password: str) -> str:
    """Hash a password"""
    return hashpw(password.encode('utf-8'), gensalt())
