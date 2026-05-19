from fastapi import APIRouter, HTTPException
from psycopg2.extras import RealDictCursor
from db.connection import get_connection

router = APIRouter()

@router.post("", status_code=201)
def create_doctors(
    name: str,
    specialization: str
):
    connection = get_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT COALESCE(MAX(id), 0) FROM doctors
    """)

    count = int(cursor.fetchone()["coalesce"]) + 1
    doctor_id = f"D{count:03d}"

    query = """
        INSERT INTO doctors(doctor_id, name, specialization)
        VALUES(%s, %s, %s)
        RETURNING *
    """

    cursor.execute(query, (doctor_id, name, specialization))

    doctor = cursor.fetchone()
    connection.commit()

    cursor.close()
    connection.close()

    return doctor

@router.get("")
def list_doctors():

    connection = get_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    query = """
        SELECT doctor_id, name, specialization
        FROM doctors
        WHERE is_active = TRUE
    """
    cursor.execute(query)

    doctors = cursor.fetchall()

    cursor.close()
    connection.close()

    return doctors


@router.get("/{doctor_id}")
def get_doctor(doctor_id: str):

    connection = get_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    query = """
        SELECT doctor_id, name, specialization
        FROM doctors
        WHERE doctor_id = %s
        AND is_active = TRUE
    """
    cursor.execute(query, (doctor_id,))
    
    doctor = cursor.fetchone()

    cursor.close()
    connection.close()

    if doctor is None:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )
    return doctor